from django import forms
from captcha.fields import CaptchaField
from .models import News


class NewsForm(forms.ModelForm):
    header = forms.CharField(label='Заоловок', widget=forms.TextInput(attrs={"classs": "form-input"}))
    announcement = forms.CharField(label='Краткий анонс:', widget=forms.Textarea())
    photo = forms.ImageField(label='Фото:')
    text = forms.CharField(label='Текст', widget=forms.Textarea())
    captcha = CaptchaField()

    class Meta:
        model = News
        fields = ['header', 'announcement', 'photo', 'text', 'captcha']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields['header'].widget.attrs['placeholder'] = 'Заголовок'
            self.fields['announcement'].widget.attrs['placeholder'] = 'Анонс'
            self.fields['photo'].widget.attrs['placeholder'] = 'Фото'
            self.fields['text'].widget.attrs['placeholder'] = 'Введите ваш текст'
            self.fields['captcha'].widget.attrs.update({"placeholder": 'Напишите текст с картинки'})
            self.fields[field].widget.attrs.update({"class": "form-control", "autocomplete": "off"})

