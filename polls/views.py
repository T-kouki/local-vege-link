from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from .models import Product
from .forms import EatSignupForm, FarmSignupForm
def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")

def menu(request):
    return render(request, 'registration/menu.html')
def cart(request):
    return render(request,'registration/cart.html') 
def signup_view(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')  
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})
def menu_view(request):
    query = request.GET.get('q')  # フォームからの検索キーワードを取得
    products = Product.objects.all()

    if query:
        products = products.filter(name__icontains=query)  # 部分一致検索

    context = {
        'products': products,
        'query': query,
    }
    return render(request, 'registration/menu.html', context)
def signup_eat(request):
    if request.method == 'POST':
        form = EatSignupForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')  # 登録後ログイン画面へ
    else:
        form = EatSignupForm()
    return render(request, 'registration/signup_eat.html', {'form': form})


def signup_farm(request):
    if request.method == 'POST':
        form = FarmSignupForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = FarmSignupForm()
    return render(request, 'registration/signup_farm.html', {'form': form})
def signup_menu_view(request):
    return render(request, 'registration/signup_menu.html')