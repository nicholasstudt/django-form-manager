
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

class RandForm(forms.Form):
    pass

def form(request, slug=None): 
    
    item = get_object_or_404(Form, slug=slug, active=True)

    elements = Element.objects.filter(form=item)

    # Walk through elements, build Form to use for validation.

    form = RandForm()
    form.fields['test'] = forms.CharField()
    form.fields['My penis'] = forms.CharField()


    if request.method == 'POST': 
        pass
    else:
        pass

    return render_to_response("form_manager/form.html", 
                              {'form': form, 'item': item, 
                               'elements': elements },
                              context_instance=template.RequestContext(request))
