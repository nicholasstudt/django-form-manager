
from django import forms
from django import http, template
from django.shortcuts import get_object_or_404, redirect, render_to_response
from django.views.generic import list_detail

from form_manager.models import Form, Element
from form_manager.forms import RawField, ButtonField

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
   
    item = get_object_or_404(Form, slug=slug, active=True)

    elements = Element.objects.filter(form=item)
    
    if request.method == 'POST': 
        form = _make_form(elements, request.POST, request.FILES)

        if form.is_valid():

            if item.store > 0:
                pass

            if item.send > 0:
                pass

            if item.redirect:
                return redirect(item.redirect)
            
            # ?
            
    else:
        form = _make_form(elements, )

    return render_to_response('form_manager/form.html', 
                              {'form': form, 'item': item},
                              context_instance=template.RequestContext(request))
