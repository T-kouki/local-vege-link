# polls/views.py

from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from .models import Product
from .forms import EatSignupForm, FarmSignupForm
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate, login, get_user_model
from .forms import ProductUploadForm
from .forms import ProfileEditForm
from django.contrib.auth.decorators import login_required



def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")

def menu(request):
    return render(request, 'no_login/menu.html')

def cart(request):
    return render(request,'no_login/cart.html') 

def signup_view(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')  
    else:
        form = UserCreationForm()
    return render(request, 'no_login/signup.html', {'form': form})

def logout_view(request):
    from django.contrib.auth import logout
    logout(request)
    return redirect('index')

def menu_view(request):
    query = request.GET.get('q')  # フォームからの検索キーワードを取得
    products = Product.objects.all()

    if query:
        products = products.filter(name__icontains=query)  # 部分一致検索

    context = {
        'products': products,
        'query': query,
    }
    return render(request, 'no_login/menu.html', context)
def signup_eat(request):
    if request.method == 'POST':
        form = EatSignupForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')  # 登録後ログイン画面へ
    else:
        form = EatSignupForm()
    return render(request, 'no_login/signup_eat.html', {'form': form})


def signup_farm(request):
    if request.method == 'POST':
        form = FarmSignupForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = FarmSignupForm()
    return render(request, 'no_login/signup_farm.html', {'form': form})
def signup_menu_view(request):
    return render(request, 'no_login/signup_menu.html')

def login_view(request):
    if request.method == "POST":
        email = request.POST.get("username")  # ← HTMLフォームのname属性
        password = request.POST.get("password")

        User = get_user_model()

        try:
            user_obj = User.objects.get(email=email)
        except User.DoesNotExist:
            user_obj = None

        user = None
        if user_obj:
            # authenticate()はusernameを使うので、CustomUser.usernameを渡す
            user = authenticate(request, username=user_obj.username, password=password)

        if user is not None:
            login(request, user)

            if user.role == 'farm':
                return redirect('farm_menu')
            elif user.role == 'eat':
                return redirect('eat_menu')
            else:
                return redirect('menu')

        else:
            return render(request, 'no_login/login.html', {'error': 'メールアドレスまたはパスワードが違います。'})

    return render(request, 'no_login/login.html')

def farm_menu_view(request):
    # ここに表示したいコンテキストを追加できます
    products = Product.objects.all()
    context = {'products': products}
    return render(request, 'registration/farm_menu.html', context)
def farm_product_upload(request):
    if request.method == 'POST':
        form = ProductUploadForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('farm_menu')  # 登録後はメニュー画面にリダイレクト
    else:
        form = ProductUploadForm()
    return render(request, 'registration/product_upload.html', {'form': form})
    

    
@login_required
def profile_edit(request):
    user = request.user
    if request.method == 'POST':
        form = ProfileEditForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('farm_menu')  # 編集後にリダイレクトするページ
    else:
        form = ProfileEditForm(instance=user)

    return render(request, 'registration/profile_edit.html', {'form': form})
# polls/views.py
