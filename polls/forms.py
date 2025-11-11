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

    def save(self, commit=True):
        user = super().save(commit=False)
        user.username = self.cleaned_data['email']  # ログインをメールで行う場合
        user.role = 'farm'  # ✅ 農家ロールを設定
        if commit:
            user.save()
        return user
class ProductUploadForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'
class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
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
        fields = ['name', 'price', 'image']

    def clean_price(self):
        price = self.cleaned_data['price']
        # 入力から「円」を削除
        if price.endswith("円"):
            price = price.replace("円", "")
        try:
            return int(price)  # 数値に変換
        except ValueError:
            raise forms.ValidationError("価格は数字で入力してください")