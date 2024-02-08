from django.forms import ModelForm
from .models import Contact_item, Opt_item



class ContactForm(ModelForm):
    class Meta:
        model = Contact_item
        fields = ["phone"]
    def __init__(self, *args, **kwargs):
        super(ContactForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'input'})
            field.widget.attrs.setdefault('placeholder', field.label)
            field.widget.attrs.setdefault('label', field.label)




class OptForm(ModelForm):
    class Meta:
        model = Opt_item
        fields = ["otp"]
    def __init__(self, *args, **kwargs):
        super(OptForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'input'})
            field.widget.attrs.setdefault('placeholder', field.label)
            field.widget.attrs.setdefault('label', field.label)


  