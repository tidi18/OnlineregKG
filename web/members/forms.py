import ast
from datetime import datetime
from django import forms
from captcha.fields import CaptchaField
from .models import Member
from competitions.models import Competition


class MemberForm(forms.ModelForm):
    competition = forms.ModelChoiceField(queryset=Competition.objects.all(), label='Название соревнования', widget=forms.Select(attrs={'class': 'form-control'}))
    name = forms.CharField(label='Имя', widget=forms.TextInput(attrs={'class': 'form-input'}))
    last_name = forms.CharField(label='Фамилия', widget=forms.TextInput(attrs={'class': 'form-input'}))
    gender = forms.ChoiceField(label='Пол', choices=Member.gender_list, widget=forms.Select(attrs={'class': 'form-input'}))
    date_of_birth = forms.DateField(label='Дата рождения', widget=forms.DateInput(attrs={'type': 'date'}))
    discharge = forms.ChoiceField(label='Разряд', choices=Member.discharge_list)
    team = forms.CharField(label='Команда', widget=forms.TextInput(attrs={'class': 'form-input'}))
    captcha = CaptchaField()

    class Meta:
        model = Member
        fields = ['competition', 'name', 'last_name', 'gender', 'date_of_birth', 'discharge', 'team', 'captcha']

    def clean(self):
        cleaned_data = super().clean()
        date_of_birth = cleaned_data.get('date_of_birth')
        competition_data = cleaned_data.get('competition')

        try:
            if date_of_birth:
                competition = Competition.objects.get(id=competition_data.id)
                competition_age_groups = competition.age_groups_of_participants
                current_year = datetime.now().year
                birth_year = date_of_birth.year
                calculated_age = current_year - birth_year

                age_groups_list = []
                age_groups_list.append(competition_age_groups)
                data_list = ast.literal_eval(age_groups_list[0])

                age_groups = []
                for sublist in data_list:
                    sublist = ast.literal_eval(sublist)
                    age_groups.extend(sublist)
                age_groups = list(map(str, age_groups))

                if 'A' not in age_groups or 'B' not in age_groups or 'C' not in age_groups or 'D' not in age_groups:
                    if str(calculated_age) not in age_groups:
                        raise forms.ValidationError("Вы не подходите ни к одной возрастной группе для данного соревнования.")
                else:
                    cleaned_data['abcd_group'] = cleaned_data.get('abcd_group')

        except Competition.DoesNotExist:
            raise forms.ValidationError("Соревнование не найдено.")

        return cleaned_data

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        competition_age_groups = self.get_competition_age_groups()

        if self.should_display_abcd_group(competition_age_groups):
            self.fields['abcd_group'] = forms.ChoiceField(
                label='Выберите группу ABCD',
                choices=[('A', 'A'), ('B', 'B'), ('C', 'C'), ('D', 'D')],
                widget=forms.Select(attrs={'class': 'form-input'})
            )

        for field in self.fields:
            self.fields[field].widget.attrs.update({"class": "form-control", "autocomplete": "off"})
            self.fields['name'].widget.attrs['placeholder'] = 'Ваше имя'
            self.fields['last_name'].widget.attrs['placeholder'] = 'Ваша фамилия'
            self.fields['gender'].widget.attrs['placeholder'] = 'Укажите свой пол'
            self.fields['date_of_birth'].widget.attrs['placeholder'] = ''
            self.fields['discharge'].widget.attrs['placeholder'] = ''
            self.fields['team'].widget.attrs['placeholder'] = 'Название вашей команды'
            self.fields['captcha'].widget.attrs.update({"placeholder": 'Напишите текст с картинки'})

            if 'abcd_group' in self.fields:
                self.fields['abcd_group'].widget.attrs.update({"class": "form-control"})
                self.fields['abcd_group'].widget.attrs['placeholder'] = 'Выберите группу ABCD'
                self.fields['abcd_group'].required = False

    def get_competition_age_groups(self):
        competition_data = self.data.get('competition')
        try:
            competition = Competition.objects.get(id=competition_data)
            competition_age_groups = competition.age_groups_of_participants
            age_groups_list = []
            age_groups_list.append(competition_age_groups)
            data_list = ast.literal_eval(age_groups_list[0])
            age_groups = []

            for sublist in data_list:
                sublist = ast.literal_eval(sublist)
                age_groups.extend(sublist)

            age_groups = list(map(str, age_groups))

            return age_groups

        except Competition.DoesNotExist:
            return []

    def should_display_abcd_group(self, age_groups):
        return 'A' in age_groups or 'B' in age_groups or 'C' in age_groups or 'D' in age_groups
