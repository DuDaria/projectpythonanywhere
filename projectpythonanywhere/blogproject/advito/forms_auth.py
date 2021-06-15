from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UsernameField
from django.contrib.auth.models import User
from .models import Profile

class LoginForm(AuthenticationForm):
    username = UsernameField(
        label="Пользователь",
        widget=forms.TextInput(attrs={
            'autofocus': True,
            'placeholder': 'Username',
            'class': 'form-control'
    }))

    password = forms.CharField(
        label="Пароль", 
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Пароль',
            'class': 'form-control'
        }))

    error_messages = {
        'invalid_login': 'Введен неправильный логин или пароль'
    }


class SignUpForm(UserCreationForm):
    password1 = forms.CharField(
        label="Пароль",
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Пароль',
            'class': 'form-control'
        })
    )

    password2 = forms.CharField(
        label="Подтверждение пароля",
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Подтвердите пароль',
            'class': 'form-control'
        })
    )

    class Meta:
        model = User
        fields = ('email', 'username')
        widgets = { 
            'username': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Username'
            }),
            'email': forms.EmailInput(attrs={
                'autofocus': True,
                'class': 'form-control',
                'placeholder': 'Email',
            }),
        }

    # Проверка емайла на уникальность
    def clean_email(self):
        email = self.cleaned_data.get('email')
        username = self.cleaned_data.get('username')
        if email and User.objects.filter(email=email).exclude(username=username).exists():
            raise forms.ValidationError('Еmail должен быть уникальным!')
        return email
        

class UpdateProfileForm(forms.ModelForm):
    max_size_img = 3

    birth_date = forms.DateField(
        label="Дата рождения", 
        input_formats=['%d-%m-%Y'],
        widget = forms.DateInput(format=('%d-%m-%Y'), attrs={
            'class': 'form-contol',
            'placeholder': 'Дата рождения в формате dd-mm-yyyy',
        })
    )

    class Meta:
        model = Profile

        fields = ['avatar', 'birth_date', 'phone', 'town', 'about']

        labels = {
            'avatar': 'Фото профиля', 
            'birth_date': 'День рождения',
            'phone': 'Телефон', 
            'town': 'Город', 
            'about': 'О себе', 
        }

        widjets = {
            'about': forms.Textarea(attrs={
                'class': 'form-control', 
                'placeholder': 'Обо мне',
            }),
            'phone': forms.CharField(), 
            
            'town': forms.Textarea(), 
            
            'avatar': forms.ClearableFileInput(attrs={
                'class': 'form__file', 
                'type': 'file',
            }),
        }
    
    def clean_avatar(self):
        image = self.cleaned_data.get('avatar', False)
        if image:
            if image.size > self.max_size_img*1024*1024:
                raise forms.ValidationError(f'Файл должен быть не больше {self.max_size_img} мб.')
            return image

        else:
            raise forms.ValidationError("Не удалось прочитать файл")

