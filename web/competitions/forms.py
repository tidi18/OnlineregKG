from PIL import Image
from captcha.fields import CaptchaField
from django.utils import timezone
from .models import Competition
from .models import Comment
from django import forms
from django.core.validators import RegexValidator
import os


class CompetitionsForm(forms.ModelForm):
    phone_regex = RegexValidator(
        regex=r'\+996\d{9}$',
        message='Номер телефона должен быть в формате: "+996XXXXXXXXX"'
    )
    telegram_regex = RegexValidator(
        regex=r'^@[A-Za-z0-9]{5,}$',
        message='Invalid username Telegram'
    )

    state = forms.CharField(label='Государство проведения:', widget=forms.Select(choices=Competition.hostState_list, attrs={'class': 'form-control'}))
    region = forms.CharField(label='Регион:', widget=forms.Select(choices=Competition.region_list, attrs={'class': 'form-control'}))
    date = forms.DateField(label='Дата проведения:', widget=forms.DateInput(attrs={"type": "date", 'class': 'form-control'}))
    organizer_name = forms.CharField(label='Имя организатора:', widget=forms.TextInput(attrs={'class': 'form-control'}))
    organizer_last_name = forms.CharField(label='Фамилия организатора:', widget=forms.TextInput(attrs={'class': 'form-control'}))
    organizer_email = forms.EmailField(label='Email организатора:', widget=forms.EmailInput(attrs={'class': 'form-control'}))
    organizer_phone = forms.CharField(label='Номер телефона организатора:', validators=[phone_regex], required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    organizer_telegram = forms.CharField(label='Telegram организатора:', validators=[telegram_regex], required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    organizer_whatsapp = forms.CharField(label='WhatsApp организатора:', validators=[phone_regex], required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    competition_name = forms.CharField(label='Наименование:', widget=forms.TextInput(attrs={'class': 'form-control'}))
    location = forms.CharField(label='Место проведения:', widget=forms.TextInput(attrs={'class': 'form-control'}))
    age_groups_of_participants = forms.MultipleChoiceField(
        label='Возрастные группы участников:',
        choices=Competition.age_groups_of_participants_list,
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'checkbox-control'})
    )
    illustration = forms.ImageField(label='Иллюстрация:', widget=forms.FileInput(attrs={'class': 'form-control'}))
    announcement = forms.CharField(label='Краткий анонс:', widget=forms.Textarea(attrs={'class': 'form-control', "rows": 5, "cols": 40}))
    captcha = CaptchaField()

    class Meta:
        model = Competition
        fields = [
            'state',
            'region',
            'date',
            'organizer_name',
            'organizer_last_name',
            'organizer_email',
            'organizer_phone',
            'organizer_telegram',
            'organizer_whatsapp',
            'competition_name',
            'location',
            'age_groups_of_participants',
            'illustration',
            'announcement',
            'captcha'
        ]

    def clean(self):
        cleaned_data = super().clean()
        phone = cleaned_data.get('organizer_phone')
        telegram = cleaned_data.get('organizer_telegram')
        whatsapp = cleaned_data.get('organizer_whatsapp')
        if not phone and not telegram and not whatsapp:
            self.add_error('organizer_phone', 'Необходимо заполнить хотя бы одно из полей')

    def clean_date(self):
        date = self.cleaned_data.get('date')
        if date and date < timezone.now().date():
            raise forms.ValidationError('Пожалуйста, выберите будущую дату.')

        return date

    def clean_illustration(self):
        illustration = self.cleaned_data.get('illustration')
        if illustration:
            # Check the image size (in bytes). Limit: 15 MB
            max_size = 15 * 1024 * 1024  # 15 MB
            if illustration.size > max_size:
                raise forms.ValidationError('Пожалуйста, загрузите изображение размером до 15 МБ.')

            # Check the image extension
            allowed_extensions = ['.jpeg', '.jpg', '.png', '.gif', '.bmp', '.tiff', '.svg']
            file_extension =  os.path.splitext(illustration.name)[1].lower()
            if file_extension not in allowed_extensions:
                raise forms.ValidationError(
                    'Пожалуйста, загрузите изображение с расширением JPEG, JPG, PNG, GIF, BMP, TIFF или SVG.')

            # Additionally, check the image using the PIL library
            try:
                with Image.open(illustration.file) as img:
                    # You can add additional checks here, such as image dimensions or resolution
                    pass
            except:
                raise forms.ValidationError('Пожалуйста, загрузите действительное изображение.')

        return illustration


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields:
            self.fields['state'].widget.attrs['placeholder'] = 'Выберите государство'
            self.fields['region'].widget.attrs['placeholder'] = 'Выберите регион'
            self.fields['date'].widget.attrs['placeholder'] = 'Дата проведения'
            self.fields['organizer_name'].widget.attrs['placeholder'] = 'Ваше имя'
            self.fields['organizer_last_name'].widget.attrs['placeholder'] = 'Ваша фамилия'
            self.fields['organizer_email'].widget.attrs['placeholder'] = 'Введите свой email'
            self.fields['organizer_phone'].widget.attrs['placeholder'] = 'Введите свой номер телефона'
            self.fields['organizer_telegram'].widget.attrs['placeholder'] = 'Введите свой Telegram'
            self.fields['organizer_whatsapp'].widget.attrs['placeholder'] = 'Введите свой номер WhatsApp'
            self.fields['competition_name'].widget.attrs['placeholder'] = 'Наименование'
            self.fields['location'].widget.attrs['placeholder'] = 'Место проведения'
            self.fields['age_groups_of_participants'].widget.attrs['placeholder'] = 'Выберите возрастную группу'
            self.fields['illustration'].widget.attrs['placeholder'] = 'Иллюстрация'
            self.fields['announcement'].widget.attrs['placeholder'] = ''
            self.fields['captcha'].widget.attrs.update({"placeholder": 'Напишите текст с картинки'})

            if field == 'age_groups_of_participants':
                self.fields[field].widget.attrs.update({"class": "checkbox-control"})
            else:
                self.fields[field].widget.attrs.update({"class": "form-control"})


class CommentForm(forms.ModelForm):
    text = forms.CharField(label=False, widget=forms.Textarea(attrs={'class': 'form-input', 'type': 'text', 'id': 'comment', 'rows': '5'}))

    class Meta:
        model = Comment
        fields = ['text']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields['text'].widget.attrs['placeholder'] = 'Введите ваш комментарий'
            self.fields[field].widget.attrs.update({"class": "form-control", "autocomplete": "off"})


