from django.contrib import admin

from form_manager.models import Form
from form_manager.models import Element

class ElementInline(admin.StackedInline):
    model = Element
    fieldsets = [
                (None, {'fields': ['page','order','label','type',],
                'description':'Extra awesome', }),
                ('Detail', {'fields': ['slug','require','value']}),
    ]

    prepopulated_fields = {'slug': ('label',)}

class FormAdmin(admin.ModelAdmin):

    fieldsets = [
        ('General', 
            {'fields':
                ['name','owner', 'abstract', 'active', 'start_date',
                 'stop_date','redirect']}),
        ('Advanced', 
            {'fields':['slug','store','send'], 'classes': ['collapse'] }),
    ]

    list_display = ('name','owner')
    prepopulated_fields = {'slug': ('name',)}

    inlines = [ ElementInline, ]


admin.site.register(Form, FormAdmin)
