from captcha.fields import CaptchaField
from django import forms
from .models import Competition
from django.core.validators import RegexValidator
from .models import Comment


class CompetitionsForm(forms.ModelForm):
    phone_regex = RegexValidator(
        regex=r'\+996\d{9}$',
        message='Номер телефона должен быть в формате: "+996XXXXXXXXX'
    )
    telegram_regex = RegexValidator(
        regex=r'^@[A-Za-z0-9]{5,}$',
        message='invalid username Telegram'

    )
    state = forms.CharField(label='Государство проведения:', widget=forms.Select(choices=Competition.hostState_list))
    region = forms.CharField(label='Регион:', widget=forms.Select(choices=Competition.region_list))
    date = forms.DateField(label='Дата проведения:', widget=forms.DateInput(attrs={"type": "date"}))
    organizer_name = forms.CharField(label='Имя организатора:', widget=forms.TextInput(attrs={'class': 'form-input'}))
    organizer_last_name = forms.CharField(label='Фамилия организатора:', widget=forms.TextInput(attrs={'class': 'form-input'}))
    organizer_email = forms.EmailField(label='Email организатора:', widget=forms.EmailInput(attrs={'class': 'form-input'}))
    organizer_phone = forms.CharField(label='Номер телефона организатора:', validators=[phone_regex])
    organizer_telegram = forms.CharField(label='Telegram организатора:', validators=[telegram_regex])
    organizer_whatsapp = forms.CharField(label='WhatsApp организатора:', validators=[phone_regex])
    competition_name = forms.CharField(label='Наименование:', widget=forms.TextInput(attrs={'class': 'form-input'}))
    location = forms.CharField(label='Место проведения:', widget=forms.TextInput(attrs={'class': 'form-input'}))
    age_groups_of_participants = forms.CharField(label='Возрастные группы участников:', widget=forms.Select(choices=Competition.age_groups_of_participants_list))
    illustration = forms.ImageField(label='Иллюстрация:')
    announcement = forms.CharField(label='Краткий анонс:', widget=forms.Textarea())
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
            self.fields[field].widget.attrs.update({"class": "form-control", "autocomplete": "off"})


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


