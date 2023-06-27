import ast
from datetime import datetime
from captcha.fields import CaptchaField
from django import forms
from .models import Member
from competitions.models import Competition


class MemberForm(forms.ModelForm):
    competition = forms.Select(attrs={'class': 'form-control'})
    name = forms.CharField(label='Имя:', widget=forms.TextInput(attrs={'class': 'form-input'}))
    last_name = forms.CharField(label='Фамилия:', widget=forms.TextInput(attrs={'class': 'form-input'}))
    gender = forms.CharField(label='Пол', widget=forms.Select(choices=Member.gender_list, attrs={'class': 'form-input'}))
    date_of_birth = forms.DateField(label='Дата рождения:', widget=forms.DateInput(attrs={'type': 'date'}))
    discharge = forms.CharField(label='Разряд:', widget=forms.Select(choices=Member.discharge_list))
    team = forms.CharField(label='Команда:', widget=forms.TextInput(attrs={'class': 'form-input'}))
    captcha = CaptchaField()

    class Meta:
        model = Member
        fields = ['competition', 'name', 'last_name', 'gender', 'date_of_birth',  'discharge', 'team', 'captcha']

    def clean(self):
        cleaned_data = super().clean()
        date_of_birth = cleaned_data.get('date_of_birth')
        competition_data = cleaned_data.get('competition')

        try:
            competition = Competition.objects.get(id=competition_data.id)
            competition_age_groups = competition.age_groups_of_participants
            current_year = datetime.now().year
            birth_year = date_of_birth.year
            calculated_age = current_year - birth_year
            tt = competition_age_groups
            age_groups1 = []
            age_groups1.append(tt)
            data_list = ast.literal_eval(age_groups1[0])
            age_groups = []
            for sublist in data_list:
                sublist = ast.literal_eval(sublist)
                age_groups.extend(sublist)

            # Преобразование элементов списка в целочисленные значения
            age_groups = list(map(str, age_groups))
            if 'A' not in str(age_groups) or 'B' not in str(age_groups) or 'C' not in str(age_groups) or 'D' not in str(age_groups):
                if str(calculated_age) not in age_groups:
                    raise forms.ValidationError(f"{age_groups}Вы не подходите ни к одной возрастной группе для данного соревнования.")

        except Competition.DoesNotExist:
            raise forms.ValidationError("Соревнование не найдено.")

        return cleaned_data

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields['name'].widget.attrs['placeholder'] = 'Ваше имя'
            self.fields['last_name'].widget.attrs['placeholder'] = 'Ваша фамилия'
            self.fields['gender'].widget.attrs['placeholder'] = 'Укажите свой пол'
            self.fields['date_of_birth'].widget.attrs['placeholder'] = ''
            self.fields['discharge'].widget.attrs['placeholder'] = ''
            self.fields['team'].widget.attrs['placeholder'] = 'Название вашей команды'
            self.fields['captcha'].widget.attrs.update({"placeholder": 'Напишите текст с картинки'})
            self.fields[field].widget.attrs.update({"class": "form-control", "autocomplete": "off"})
