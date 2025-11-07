from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms

class loginForm(forms.Form):
    username = forms.CharField(max_length=150, label='Username')
    password = forms.CharField(widget=forms.PasswordInput, label='Password')


# 飲食店向けフォーム
class EatSignupForm(UserCreationForm):
    email = forms.EmailField(required=True, label="メールアドレス")
    restaurant_name = forms.CharField(max_length=100, label="店舗名")

    class Meta:
        model = User
        fields = ('username', 'restaurant_name', 'email', 'password1', 'password2')

# 農家向けフォーム
class FarmSignupForm(UserCreationForm):
    email = forms.EmailField(required=True, label="メールアドレス")
    farm_name = forms.CharField(max_length=100, label="農園名")

    class Meta:
        familyname = forms.CharField(max_length=50, label="姓")
        lastname = forms.CharField(max_length=50, label="名")
        username = forms.CharField(max_length=150, label="表示される名前")
        address = forms.CharField(max_length=255, label="住所")
        phone_number = forms.CharField(max_length=20, label="電話番号")
        email = forms.EmailField(required=True, label="メールアドレス")
        image = forms.ImageField(required=False, label="販売実績が確認できる書類")
    class ImageUploadForm(forms.Form):
        username = forms.CharField(max_length=150)
        password = forms.CharField(widget=forms.PasswordInput)
        image = forms.ImageField(required=False)
