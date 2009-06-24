from django.contrib import admin

from form_manager.models import Form
from form_manager.models import Element

class ElementInline(admin.StackedInline):
    model = Element
    fieldsets = [
                 (None, {'fields': ['page','order','label','type',]}),
                 ('Detail', {'fields': ['slug','require','value']}),
                ]

    prepopulated_fields = {'slug': ('label',)}

class FormAdmin(admin.ModelAdmin):

    fieldsets = [
        ('General', 
            {'fields':
                ['name','slug','owner', 'abstract', 'active',
                 'redirect','store','send']}),
    ]

    list_display = ('name','owner','active')
    prepopulated_fields = {'slug': ('name',)}
    save_on_top = True
    inlines = [ ElementInline, ]

admin.site.register(Form, FormAdmin)
