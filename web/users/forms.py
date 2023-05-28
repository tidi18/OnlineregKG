from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django import forms
from django.contrib.auth.models import User
from .models import Profile
from captcha.fields import CaptchaField


class UserRegisterForm(UserCreationForm):
    username = forms.CharField(label="Имя пользователя", widget=forms.TextInput(attrs={"classs": "form-input"}))
    email = forms.EmailField(label="Email", widget=forms.EmailInput(attrs={"classs": "form-input"}))
    first_name = forms.CharField(label="Имя", widget=forms.TextInput(attrs={"classs": "form-input"}))
    last_name = forms.CharField(label="Фамилия", widget=forms.TextInput(attrs={"classs": "form-input"}))
    date_of_birth = forms.DateField(label="Дата рождения", widget=forms.DateInput(attrs={"type": "date"}))
    password1 = forms.CharField(label="Пароль", widget=forms.PasswordInput(attrs={"classs": "form-input"}))
    password2 = forms.CharField(label="Подтверждение пароля", widget=forms.PasswordInput(attrs={"classs": "form-input"}))
    captcha = CaptchaField()

    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ('email', 'first_name', 'last_name', 'date_of_birth', 'password1', 'password2', 'captcha')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        if commit:
            user.save()
        profile = Profile(user=user, date_of_birth=self.cleaned_data['date_of_birth'])
        profile.save()
        return user

    def clean_email(self):
        email = self.cleaned_data.get('email')
        username = self.cleaned_data.get('username')
        if email and User.objects.filter(email=email).exclude(username=username).exists():
            raise forms.ValidationError('Такой email уже используется в системе')
        return email

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields['username'].widget.attrs.update({"placeholder": 'Придумайте свой логин'})
            self.fields['email'].widget.attrs.update({"placeholder": 'Введите свой email'})
            self.fields['first_name'].widget.attrs.update({"placeholder": 'Ваше имя'})
            self.fields["last_name"].widget.attrs.update({"placeholder": 'Ваша фамилия'})
            self.fields["date_of_birth"].widget.attrs.update({"placeholder": 'Дата рождения'})
            self.fields['password1'].widget.attrs.update({"placeholder": 'Придумайте свой пароль'})
            self.fields['password2'].widget.attrs.update({"placeholder": 'Повторите придуманный пароль'})
            self.fields['captcha'].widget.attrs.update({"placeholder": 'Напишите текст с картинки'})
            self.fields[field].widget.attrs.update({"class": "form-control", "autocomplete": "off"})


class UserLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields['username'].widget.attrs['placeholder'] = 'Логин пользователя'
            self.fields['password'].widget.attrs['placeholder'] = 'Пароль пользователя'
            self.fields['username'].label = 'Логин'
            self.fields[field].widget.attrs.update({
                'class': 'form-control',
                'autocomplete': 'off'
            })





