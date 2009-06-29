from django.forms import Widget
from django.utils.safestring import mark_safe
from django.utils.html import escape, conditional_escape
from django.utils.encoding import StrAndUnicode, force_unicode
from django.forms.util import flatatt

class Raw(Widget):
    def render(self, name, value, attrs=None):
        final_attrs = self.build_attrs(attrs, name=name)
        return mark_safe(u'%s' % ( final_attrs['display'] ))

class Button(Widget):
    def __init__(self, attrs=None):
        # The 'rows' and 'cols' attributes are required for HTML correctness.
        self.attrs = {'type': 'submit'}
        if attrs:
            self.attrs.update(attrs)

    def render(self, name, value, attrs=None):
        if value is None: value = ''
        final_attrs = self.build_attrs(attrs, name=name)
        display = final_attrs['display']
        del final_attrs['display']

        # This may need to be input rather than button.
        return mark_safe(u'<button %s>%s</button>' % (
                flatatt(final_attrs),
                conditional_escape(force_unicode(display))))


