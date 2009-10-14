import codecs
import os

from django.conf import settings
from django.core import exceptions

from django import forms
from django import http, template
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404, redirect, render_to_response
from django.views.generic import list_detail
from django.template import loader, Context

from form_manager.models import Form, Element
from form_manager.forms import RawField, ButtonField, HoneypotField

def _make_form(elements, *args, **kwargs):

    # Must use this to get ordering to work right, can't do the hot type
    # thing because BaseForm looses ordering for some reason.
    class _Form(forms.Form):
        pass

    # Stuff all of the form fileds in here.
    form = _Form(*args, **kwargs)

    for e in elements:
        args = { 'label': e.label }

        # These items are handled in outside of the form.
        if e.type == 'raw':
            args['label'] = ''
            args['display'] = e.value
            args['required'] = False

            if e.require != 'none': 
                args['required'] = True

            form.fields[e.slug] = RawField(**args) 

        elif e.type == 'honeypot':
            args['label'] = ''
            args['required'] = False 
            
            form.fields[e.slug] = HoneypotField(**args)

        elif e.type in ['image', 'reset', 'submit']:
            args['label'] = ''
            args['display'] = e.value
            args['type'] = e.type
            args['required'] = False

            if e.require != 'none': 
                args['required'] = True

            form.fields[e.slug] = ButtonField(**args)

        elif e.type in ['hidden', 'text', 'textarea']:
            
            if e.type == 'textarea': 
                args['widget'] = forms.Textarea
            elif e.type == 'hidden':
                args['widget'] = forms.HiddenInput

            if e.require == 'none':
                form.fields[e.slug] = forms.CharField(required=False, **args)

            if e.require == 'date':
                form.fields[e.slug] = forms.DateField(**args)

            if e.require == 'email':
                form.fields[e.slug] = forms.EmailField(**args)

            if e.require == 'number':
                form.fields[e.slug] = forms.DecimalField(**args)

            if e.require == 'text':
                form.fields[e.slug] = forms.CharField(**args)

            if e.require == 'time':
                form.fields[e.slug] = forms.TimeField(**args)

            if e.require == 'url':
                form.fields[e.slug] = forms.URLField(**args)

        elif e.type in ['radio', 'select']:

            if e.type == 'radio':
                args['widget'] = forms.RadioSelect

            try: 
                choices = eval(e.value)
            except SyntaxError:
                choices = None

            if choices:
                args['choices'] = choices
 
            if e.require == 'none':
                args['required'] = False
            else:
                args['required'] = True
                        
            form.fields[e.slug] = forms.ChoiceField(**args)

        elif e.type == 'checkbox':
            if e.require == 'none':
                args['required'] = False
            else:
                args['required'] = True
              
            form.fields[e.slug] = forms.BooleanField(**args)
           
        elif e.type == 'file':
            if e.require == 'none':
                args['required'] = False
            else:
                args['required'] = True
              
            form.fields[e.slug] = forms.FileField(**args)

        elif e.type == 'password':
            args['widget'] = forms.PasswordInpurt

            if e.require == 'none':
                args['required'] = False
            else:
                args['required'] = True
            
            form.fields[e.slug] = forms.CharField(**args)
    
    return form

def index(request, page=0, **kwargs):
    return list_detail.object_list(
        request,
        page = page,
        paginate_by = 1000,
        queryset = Form.objects.active(),
        **kwargs
    )
index.__doc__ = list_detail.object_list.__doc__

def form(request, slug=None): 
 
    try:
        dir = settings.FORM_MANAGER_UPLOAD_DIR
    except:
        raise exceptions.ImproperlyConfigured, "FORM_MANAGER_UPLOAD_DIR variable must be defined in settings.py"
  
    item = get_object_or_404(Form, slug=slug, active=True)

    elements = Element.objects.filter(form=item)
    
    if request.method == 'POST': 
        form = _make_form(elements, request.POST, request.FILES)

        if form.is_valid():
            files = []

            # Save files to right directory.
            if request.FILES:
                path = os.path.join(dir, item.slug)

                if not os.path.isdir(path):
                    os.mkdir(path)
               
                for file in request.FILES: 
                    count = 1
                    name = form.cleaned_data[file].name
                      
                    while os.access(os.path.join(path, name), os.R_OK):
                        count += 1
                        name = "%s-%s" % (count, form.cleaned_data[file].name)
                    
                    form.cleaned_data[file].name = name
                        
                    dest = open(os.path.join(path, name), 'wb+') 

                    for chunk in form.cleaned_data[file].chunks():
                        dest.write(chunk)
                    dest.close()

                    files.append(name)

            if item.store > 0:
              
                path = os.path.join(dir, "%s.csv" % item.slug)

                t = loader.get_template('form_manager/store/csv.html')

                if os.access(path, os.R_OK):
                    c = Context({'form': form, 'header': False}) 
                else:
                    c = Context({'form': form, 'header': True}) 

                file = codecs.open(path, encoding='utf-8', mode='a') 
                file.write(t.render(c))
                file.close()
                
            if item.send > 0:
                body = loader.render_to_string('form_manager/send/email.html',
                                               {'form': form, 'item': item,
                                                'files': files})

                send_mail("[%s] Response" % item.name, body, 
                          settings.SERVER_EMAIL, [item.owner])

            if item.redirect:
                return redirect(item.redirect)
            
            return redirect('/')
    else:
        form = _make_form(elements, )

    return render_to_response('form_manager/form.html', 
                              {'form': form, 'item': item},
                              context_instance=template.RequestContext(request))
