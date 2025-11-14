# views.py

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
from django.contrib.auth import logout
from django.views.decorators.http import require_POST
from django.contrib import messages
from .forms import InquiryForm
from .models import Item
from django.contrib.auth import update_session_auth_hash
from django.shortcuts import get_object_or_404
from django.db.models import Sum
from .models import Sale
from django.http import JsonResponse
from .forms import productEditForm 


def sales_manage(request):
    farmer_orders = Sale.objects.filter(farmer=request.user)
    total_sales = farmer_orders.aggregate(Sum('total_price'))['total_price__sum'] or 0
    return render(request, 'farm/sales_manage.html', {
        'orders': farmer_orders,
        'total_sales': total_sales
    })

def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")
 
def menu(request):
    return render(request, 'no_login/menu.html')
def cart(request):

    cart_items = Item.objects.filter(user=request.user)  # ログインユーザーのカート商品
    total = sum(item.product.price * item.quantity for item in cart_items)  # 合計金額

    context = {
        'cart_items': cart_items,
        'total': total,
    }
    return render(request, 'eat/eatcart.html', context)
def logout_confirm_view(request):
    # ロールに応じてテンプレートを切り替え
    user = request.user
    if user.role == 'farm':
        template_name = 'farm/logout_farm.html'
    elif user.role == 'eat':
        template_name = 'eat/logout_eat.html'
    return render(request, template_name)
 

 
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
        form = FarmSignupForm(request.POST, request.FILES) 
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
        email = request.POST.get("username")
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
            messages.error(request, "メールアドレスまたはパスワードが誤りです。")
            return redirect('login')  # ★ リダイレクトすることでF5連打でもフォーム再送信されない
 
    return render(request, 'no_login/login.html')
 
def farm_menu_view(request):
    # ここに表示したいコンテキストを追加できます
    products = Product.objects.all()
    context = {'products': products}
    return render(request, 'farm/farm_menu.html', context)

@login_required
def farm_product_upload(request):
    if request.method == 'POST':
        form = ProductUploadForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.user = request.user  # 出品者を紐づける
            product.save()
            messages.success(request, "商品を出品しました！")
            return redirect('farm_menu')
    else:
        form = ProductUploadForm()
    return render(request, 'farm/product_upload.html', {'form': form})


def eat_menu_view(request):
    # ここに表示したいコンテキストを追加できます
    products = Product.objects.all()
    context = {'products': products}
    return render(request, 'eat/eat_menu.html', context)
 
 
   
@login_required
def profile_edit(request):
    user = request.user
    if request.method == 'POST':
        form = ProfileEditForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, user)
            return redirect('farm_menu')  # 編集後にリダイレクトするページ
    else:
        form = ProfileEditForm(instance=user)
 
    return render(request, 'farm/profile_edit.html', {'form': form})
# polls/views.py
 
@require_POST
def logout_view(request):
    logout(request)
    return redirect('menu')
def contact_view(request):
    if request.method == 'POST':
        form = InquiryForm(request.POST)
        if form.is_valid():
            form.save()  # DBに保存
            messages.success(request, 'お問い合わせを受け付けました。ありがとうございます！')
            return redirect('polls:contact')
    else:
        form = InquiryForm()
 
    return render(request, 'eat/contact.html', {'form': form})
 
def search_view(request):
    query = request.GET.get('q')  # フォームの入力値を取得
    items = Product.objects.all()    # 全アイテムを取得

    if query:
        items = items.filter(name__icontains=query)  # 部分一致検索

    context = {
        'items': items,
        'query': query,
    }
    if request.user.is_authenticated:
        search_name = 'eat/eat_search.html'
    else:
        search_name = 'no_login/search.html'

    return render(request, search_name, context)

 
def contact_view(request):
    if request.method == 'POST':
        form = InquiryForm(request.POST)
        if form.is_valid():
            form.save()  # DBに保存
            messages.success(request, 'お問い合わせを受け付けました。ありがとうございます！')
            return redirect('polls:contact')
    else:
        form = InquiryForm()
 
    return render(request, 'eat/contact.html', {'form': form})
def product_list_view(request):
    # Productテーブルの全レコードを取得
    products = Product.objects.all()
   
    context = {
        'products': products,
    }
    return render(request, 'eat/product.html', context)


@login_required
def product_history_view(request):
    products = Product.objects.filter(user=request.user).order_by('-created_at')
    context = {'products': products}
    return render(request, 'farm/product_history.html', context)

def product_detail(request, pk):
    item = get_object_or_404(Product, pk=pk)
    
    context = {
        'item': item,
    }
    if request.user.is_authenticated:
        detail_name = 'eat/eat_detail.html'
    else:
        detail_name = 'no_login/product_detail.html'
    return render(request,detail_name, context)
@login_required

@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    # 既存アイテム取得 or 新規作成
    item = Item.objects.filter(user=request.user, product=product).first()
    if item:
        item.quantity += 1
        item.save()
    else:
        item = Item.objects.create(user=request.user, product=product, quantity=1)

    # AJAXかどうか判定（Django 5 対応）
    is_ajax = request.headers.get('x-requested-with') == 'XMLHttpRequest'

    if is_ajax:
        cart_items = Item.objects.filter(user=request.user)
        cart_data = [
            {
                'id': i.id,
                'product_name': i.product.name,
                'quantity': i.quantity,
                'price': i.product.price,
            } for i in cart_items
        ]
        return JsonResponse({'success': True, 'cart': cart_data, 'message': f"「{product.name}」をカートに追加しました！"})

    messages.success(request, f"「{product.name}」をカートに追加しました！")
    return redirect(request.META.get('HTTP_REFERER', '/'))





@login_required
def product_manage_view(request):
    products = Product.objects.filter(user=request.user).order_by('-created_at')
    context = {'products': products}
    return render(request, 'farm/product_manage.html', context)

@login_required
def product_edit_view(request, pk):
    product = get_object_or_404(Product, pk=pk, user=request.user)

    if request.method == 'POST':
        form = ProductEditForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, "商品を更新しました！")
            return redirect('product_manage')
    else:
        form = ProductEditForm(instance=product)

    return render(request, 'farm/product_edit.html', {'form': form, 'product': product})

@login_required
def product_delete_view(request, pk):
    product = get_object_or_404(Product, pk=pk, user=request.user)

    if request.method == "POST":
        
        product_name = product.name
        product.delete()
        return render(request, 'farm/product_delete_done.html', {'product_name': product_name})
    
    return render(request, 'farm/product_delete.html', {'product': product})
def remove_from_cart(request, item_id):
    
    item = get_object_or_404(Item, id=item_id)
    item.delete()
    return redirect('cart')  # カートページに戻す