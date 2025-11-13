from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser
from .models import Product
from .models import Inquiry

class loginForm(forms.Form):
    username = forms.CharField(max_length=150, label='Username')
    password = forms.CharField(widget=forms.PasswordInput, label='Password')


# 飲食店向けフォーム
class EatSignupForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = [
            'familyname', 'lastname', 'nickname',
            'address', 'phone_number', 'email',
            'password1', 'password2'
        ]
        labels = {
            'familyname': '姓',
            'lastname': '名',
            'nickname': '表示される名前',
            'address': '住所',
            'phone_number': '電話番号',
            'email': 'メールアドレス',
        }
    def save(self, commit=True):
        user = super().save(commit=False)
        user.username = self.cleaned_data['email']
        user.role = 'eat'  # ✅ 飲食店ロールを設定
        if commit:
            user.save()
            return user

# 農家向けフォーム
class FarmSignupForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = [
            'familyname', 'lastname', 'nickname',
            'address', 'phone_number', 'email',
            'password1', 'password2', 'image'
        ]
        labels = {
            'familyname': '姓',
            'lastname': '名',
            'nickname': '表示される名前',
            'address': '住所',
            'phone_number': '電話番号',
            'email': 'メールアドレス',
            'image': '販売実績が確認できる書類',
        }

    def save(self, commit=True):
        user = super().save(commit=False)
        user.username = self.cleaned_data['email']  # ログインをメールで行う場合
        user.role = 'farm'  # ✅ 農家ロールを設定
        if commit:
            user.save()
        return user

class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['nickname', 'email', 'address', 'phone_number']
        labels = {
            'nickname': '表示される名前',
            'address': '住所',
            'phone_number': '電話番号',
            'email': 'メールアドレス',
        }
        widgets = {
            'nickname': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'address': forms.TextInput(attrs={'class': 'form-control'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control'}),
        }

class InquiryForm(forms.ModelForm):
    class Meta:
        model = Inquiry
        fields = ['name', 'email', 'message']
        widgets = {
            'message': forms.Textarea(attrs={'rows': 5}),
        }

class ProductUploadForm(forms.ModelForm):
    price = forms.CharField(label="価格", max_length=20)

    class Meta:
        model = Product
        fields = ['name', 'price', 'description', 'image']
        labels = {
            'name':'名前',
            'price':'価格',
            'description':'説明欄',
            'image':'商品画像',
        }

    def clean_price(self):
        price = self.cleaned_data['price'].replace("円", "").strip()
        try:
            return int(price)
        except ValueError:
            raise forms.ValidationError("価格は数字で入力してください。")
