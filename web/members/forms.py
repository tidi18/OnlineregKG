from captcha.fields import CaptchaField
from django import forms
from .models import Member


class MemberForm(forms.ModelForm):
    competition = forms.Select(attrs={'class': 'form-control'})
    name = forms.CharField(label='Имя:', widget=forms.TextInput(attrs={'class': 'form-input'}))
    last_name = forms.CharField(label='Фамилия:', widget=forms.TextInput(attrs={'class': 'form-input'}))
    date_of_birth = forms.DateField(label='Дата рождения:', widget=forms.DateInput(attrs={'type': 'date'}))
    discharge = forms.CharField(label='Разряд:', widget=forms.Select(choices=Member.discharge_list))
    team = forms.CharField(label='Команда:', widget=forms.TextInput(attrs={'class': 'form-input'}))
    captcha = CaptchaField()
    class Meta:
        model = Member
        fields = ['competition', 'name', 'last_name', 'date_of_birth',  'discharge', 'team', 'captcha']

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields['competition'].widget.attrs['placeholder'] = ''
            self.fields['name'].widget.attrs['placeholder'] = 'Ваше имя'
            self.fields['last_name'].widget.attrs['placeholder'] = 'Ваша фамилия'
            self.fields['date_of_birth'].widget.attrs['placeholder'] = ''
            self.fields['discharge'].widget.attrs['placeholder'] = ''
            self.fields['team'].widget.attrs['placeholder'] = 'Название вашей команды'
            self.fields['captcha'].widget.attrs.update({"placeholder": 'Напишите текст с картинки'})
            self.fields[field].widget.attrs.update({"class": "form-control", "autocomplete": "off"})


