from django.contrib import admin

from form_manager.models import Form
from form_manager.models import Element

class ElementAdmin(admin.ModelAdmin):
    list_filter = ('form','type')

class ElementInline(admin.StackedInline):
    model = Element

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
admin.site.register(Element, ElementAdmin)
