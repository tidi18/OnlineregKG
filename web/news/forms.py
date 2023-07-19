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
            # Проверяем размер изображения (в байтах). Ограничение: 15 МБ
            max_size = 15 * 1024 * 1024  # 15 МБ
            if photo.size > max_size:
                raise forms.ValidationError('Пожалуйста, загрузите изображение размером до 15 МБ.')

            # Проверяем расширение изображения
            allowed_extensions = ['.jpeg', '.jpg', '.png', '.gif', '.bmp', '.tiff', '.svg']
            file_extension = photo.name.lower().split('.')[-1]
            if file_extension not in allowed_extensions:
                raise forms.ValidationError('Пожалуйста, загрузите изображение с расширением JPEG, JPG, PNG, GIF, BMP, TIFF или SVG.')

            # Проверяем дополнительно изображение с помощью библиотеки PIL
            try:
                with Image.open(photo.file) as img:
                    # Вы можете добавить здесь дополнительные проверки, например, размеры изображения или его разрешение
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
