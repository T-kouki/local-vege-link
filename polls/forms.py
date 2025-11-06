# polls/forms.py
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

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
        model = User
        fields = ('username', 'farm_name', 'email', 'password1', 'password2')
