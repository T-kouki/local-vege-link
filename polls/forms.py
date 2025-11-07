from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser

class loginForm(forms.Form):
    username = forms.CharField(max_length=150, label='Username')
    password = forms.CharField(widget=forms.PasswordInput, label='Password')


# 飲食店向けフォーム
class EatSignupForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = [
            'familyname', 'lastname', 'farm_name',
            'address', 'phone_number', 'email',
            'password1', 'password2'
        ]
        labels = {
            'familyname': '姓',
            'lastname': '名',
            'farm_name': '表示される名前',
            'address': '住所',
            'phone_number': '電話番号',
            'email': 'メールアドレス',
        }

# 農家向けフォーム
class FarmSignupForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = [
            'familyname', 'lastname', 'farm_name',
            'address', 'phone_number', 'email',
            'password1', 'password2', 'image'
        ]
        labels = {
            'familyname': '姓',
            'lastname': '名',
            'farm_name': '表示される名前',
            'address': '住所',
            'phone_number': '電話番号',
            'email': 'メールアドレス',
            'image': '販売実績が確認できる書類',
        }
