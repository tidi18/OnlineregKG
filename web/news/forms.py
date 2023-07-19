import os
from django import forms
from captcha.fields import CaptchaField
from .models import News
from PIL import Image


class NewsForm(forms.ModelForm):
    header = forms.CharField(label='Заголовок', widget=forms.TextInput(attrs={"class": "form-input"}))
    announcement = forms.CharField(label='Краткий анонс:', widget=forms.Textarea())
    photo = forms.ImageField(label='Фото:')
    text = forms.CharField(label='Текст', widget=forms.Textarea())
    captcha = CaptchaField()

    class Meta:
        model = News
        fields = ['header', 'announcement', 'photo', 'text', 'captcha']

    def clean_photo(self):
        photo = self.cleaned_data.get('photo')
        if photo:
            # Check the image size (in bytes). Limit: 15 MB
            max_size = 15 * 1024 * 1024  # 15 MB
            if photo.size > max_size:
                raise forms.ValidationError('Пожалуйста, загрузите изображение размером до 15 МБ.')

            # Check the image extension
            allowed_extensions = ['.jpeg', '.jpg', '.png', '.gif', '.bmp', '.tiff', '.svg']
            file_extension = os.path.splitext(photo.name)[1].lower()
            if file_extension not in allowed_extensions:
                raise forms.ValidationError(
                    'Пожалуйста, загрузите изображение с расширением JPEG, JPG, PNG, GIF, BMP, TIFF или SVG.')

            # Additionally, check the image using the PIL library
            try:
                with Image.open(photo.file) as img:
                    # You can add additional checks here, such as image dimensions or resolution
                    pass
            except:
                raise forms.ValidationError('Пожалуйста, загрузите действительное изображение.')

        return photo

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields['header'].widget.attrs['placeholder'] = 'Заголовок'
            self.fields['announcement'].widget.attrs['placeholder'] = 'Анонс'
            self.fields['photo'].widget.attrs['placeholder'] = 'Фото'
            self.fields['text'].widget.attrs['placeholder'] = 'Введите ваш текст'
            self.fields['captcha'].widget.attrs.update({"placeholder": 'Напишите текст с картинки'})
            self.fields[field].widget.attrs.update({"class": "form-control", "autocomplete": "off"})
