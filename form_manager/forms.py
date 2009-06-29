from django.forms import Field
from form_manager.widgets import Raw, Button

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
