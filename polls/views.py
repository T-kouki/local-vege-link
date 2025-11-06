from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from .models import Product
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
    return render(request, 'registration/menu.html', context)