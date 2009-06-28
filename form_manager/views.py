
from django import forms
from django import http, template
from django.shortcuts import get_object_or_404, redirect, render_to_response
from django.views.generic import list_detail

from form_manager.models import Form, Element

def index(request, page=0, **kwargs):
    return list_detail.object_list(
        request,
        page = page,
        paginate_by = 1000,
        queryset = Form.objects.active(),
        **kwargs
    )
index.__doc__ = list_detail.object_list.__doc__

def make_form(elements):
    
    # Stuff all of the form fileds in here.
    fields = {} 

    for e in elements:

        args = { 'label': e.label }

        # Raw elements are not part of the form.
        #if e.type == 'raw':
        #    continue 

        # These items are handled in outside of the form.
        if e.type in ['raw', 'image', 'reset', 'submit']:
            continue

        if e.type in ['hidden', 'text', 'textarea']:
            
            if e.type == 'textarea': 
                args['widget'] = forms.Textarea
            elif e.type == 'hidden':
                args['widget'] = forms.HiddenInput

            if e.require == 'none':
                fields[e.slug] = forms.CharField(required=False, **args)

            if e.require == 'date':
                fields[e.slug] = forms.DateField(**args)

            if e.require == 'email':
                fields[e.slug] = forms.EmailField(**args)

            if e.require == 'number':
                fields[e.slug] = forms.DecimalField(**args)

            if e.require == 'text':
                fields[e.slug] = forms.CharField(**args)

            if e.require == 'time':
                fields[e.slug] = forms.TimeField(**args)

            if e.require == 'url':
                fields[e.slug] = forms.URLField(**args)

        if e.type == 'password':
            args['widget'] = forms.PasswordInpurt

            if e.require == 'none':
                args['required'] = False
            else:
                args['required'] = True
            
            fields[e.slug] = forms.CharField(**args)

        if e.type == 'checkbox':
            if e.require == 'none':
                args['required'] = False
            else:
                args['required'] = True
              
            fields[e.slug] = forms.BooleanField(**args)
           
        if e.type == 'file':
            if e.require == 'none':
                args['required'] = False
            else:
                args['required'] = True
              
            fields[e.slug] = forms.FileField(**args)

        if e.type in ['radio', 'select']:

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
                        
            fields[e.slug] = forms.ChoiceField(**args)

#        'raw',  
#        'text', 'textarea', 'hidden',
#        'password', -- Requirements are boolean
#        'checkbox', -- Requirements are boolean
#        'file', -- Requirements are boolean
#        'radio',
#        'select',

#        'image', _('image')),  # Use <button>
#        'reset', _('reset')), # Use <button>
#        'submit', _('submit')), # Use <button>

    return type('ContactForm', (forms.BaseForm,), { 'base_fields': fields })


def form(request, slug=None): 
   
    item = get_object_or_404(Form, slug=slug, active=True)

    elements = Element.objects.filter(form=item)

    # Walk through elements, build Form to use for validation.
    form = make_form(elements, )()
    #form = f()

    # request.POST, request.FILES

    if request.method == 'POST': 
        pass
    else:
        pass

    return render_to_response('form_manager/form.html', 
                              {'form': form, 'item': item, 
                               'elements': elements },
                              context_instance=template.RequestContext(request))
