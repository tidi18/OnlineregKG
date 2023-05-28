from captcha.fields import CaptchaField
from django import forms
from .models import Contact


class ContactsForm(forms.ModelForm):
    name = forms.CharField(label='Имя', widget=forms.TextInput(attrs={"classs": "form-input"}))
    email = forms.EmailField(label='Email', widget=forms.EmailInput(attrs={"classs": "form-input"}))
    subject = forms.CharField(label='Тема', widget=forms.TextInput(attrs={"classs": "form-input"}))
    message = forms.CharField(label='Сообщение', widget=forms.Textarea(attrs={"class": "form-input"}))
    captcha = CaptchaField()

    class Meta:
        model = Contact
        fields = ['name', 'email', 'subject',  'message', 'captcha']

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields['name'].widget.attrs['placeholder'] = 'Имя'
            self.fields['email'].widget.attrs['placeholder'] = 'Введите свой email'
            self.fields['subject'].widget.attrs['placeholder'] = 'Тема'
            self.fields['message'].widget.attrs['placeholder'] = 'Сообщение'
            self.fields['captcha'].widget.attrs.update({"placeholder": 'Напишите текст с картинки'})
            self.fields[field].widget.attrs.update({"class": "form-control", "autocomplete": "off"})
