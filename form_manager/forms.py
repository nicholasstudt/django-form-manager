from django.forms import Field
from form_manager.widgets import Raw, Button

EMPTY_VALUES = (None, '',)

class RawField(Field):
    widget = Raw    

    def __init__(self, display=None, *args, **kwargs):
        self.display = display
        super(RawField, self).__init__(*args, **kwargs)

    def widget_attrs(self, widget):
        return {'display': self.display}

class ButtonField(Field):
    """ To handle submit / reset / button stuffs """
    widget = Button

    def __init__(self, display=None, type='submit', *args, **kwargs):
        self.display, self.button_type = display, type
        super(ButtonField, self).__init__(*args, **kwargs)

    def widget_attrs(self, widget):
        return {'display': self.display, 'type': self.button_type }


class HoneypotField(Field):
    """
    Creates a hidden text input field, that when validated, if the
    field has a different value in it than when initialized, the form
    is invalid.  This is used to stop simple SPAM bots.
    """

    widget = HoneypotWidget

    def clean(self, value):

        # If the value is empty or changed from the initial
        # invalidate the field.
        if (self.initial in EMPTY_VALUES and value \
            in EMPTY_VALUES) or value == self.initial:
            return value

        raise ValidationError('Honeypot field changed in value.')
