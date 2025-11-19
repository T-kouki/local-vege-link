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
from .forms import ProductEditForm ,JudgeResubmitForm
from django.utils import timezone
from .models import FarmerRating
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, redirect
from .models import Product, CustomUser, Inquiry,FarmJudge
from django.db.models import Avg
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.decorators import user_passes_test, login_required

#11/18 14:05 今だけ入れる
from .models import FarmJudge

def admin_required(view_func):
    return login_required(
        user_passes_test(lambda u: u.is_authenticated and u.role == 'admin')(view_func)
    )


def sales_manage(request):
    # ログイン中の農家の売上データを取得
    sales = Sale.objects.filter(farmer=request.user).order_by('-date')

    context = {
        'sales': sales
    }
    return render(request, 'farm/sales_manage.html', context)

def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")

def menu(request):
    return render(request, 'no_login/menu.html')
@login_required
def cart(request):
    # ログインユーザーのカート商品を取得
    cart_items = Item.objects.filter(user=request.user)
    total = sum(item.product.price * item.quantity for item in cart_items)  # 合計金額

    # ユーザーのロールに応じて異なるテンプレートを選択
    if request.user.role == 'eat':
        template_name = 'eat/eatcart.html'  # eat ロールなら eat_cart テンプレート
    else:
        template_name = 'no_login/cart.html'  # その他のロールなら no_login/cart テンプレート

    # コンテキストを渡してレンダリング
    context = {
        'cart_items': cart_items,
        'total': total,
    }

    return render(request, template_name, context)

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
            user = form.save(commit=False)
            user.role = 'farm'
            form.save()
            FarmJudge.objects.create(user=user, document=user.image)
            messages.success(request, "登録申請が完了しました。管理者の審査をお待ちください。")
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
            user = authenticate(request, username=user_obj.username, password=password)

        if user is not None:

            # ★農家の場合：judge を1件だけ取得
            if user.role == 'farm':

                judge = user.judge.first()  # ← これが重要！！！

                if judge is None:
                    messages.error(request, "農家申請が未完了です。まず申請してください。")
                    return render(request, 'no_login/login.html')

                # --- 状態チェック ---
                if judge.status == 'pending':
                    messages.info(request, "現在審査中です。承認をお待ちください。")
                    return render(request, 'no_login/login.html')

                elif judge.status == 'rejected':
                    messages.error(request, "審査に不合格です。お問い合わせください。")
                    return render(request, 'no_login/login.html')

                elif judge.status == 'resubmit':
                    messages.warning(request, "書類の再提出が必要です。メールに記載のリンクから再提出してください。")
                    return render(request, 'no_login/login.html')

                elif judge.status == 'approved':
                    login(request, user)
                    return redirect('farm_menu')

            # ★購入者 OK
            if user.role == 'eat':
                login(request, user)
                return redirect('eat_menu')

            # ★管理者 OK
            if user.role == 'admin':
                login(request, user)
                return redirect('admin_menu')

            login(request, user)
            return redirect('menu')

        else:
            messages.error(request, "メールアドレスまたはパスワードが誤りです。")
            return render(request, 'no_login/login.html')

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

def admin_menu_view(request):
    # ここに表示したいコンテキストを追加できます
    products = Product.objects.all()
    context = {'products': products}
    return render(request, 'admin/admin_menu.html', context)

@login_required
def profile_edit(request):
    user = request.user

    if request.method == 'POST':
        form = ProfileEditForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            return redirect('farm_menu')
    else:
        form = ProfileEditForm(instance=user)
    
    return render(request, 'farm/profile_edit.html', {'form': form})

@require_POST
def logout_view(request):
    logout(request)
    return redirect('menu')

def eat_contact_view(request):
    
    if request.method == 'POST':
        form = InquiryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'お問い合わせありがとうございます。')
            return redirect('eat_contact')
    else:
        form = InquiryForm()
    return render(request, 'eat/eat_contact.html', {'form': form})

def farm_contact_view(request):
    if request.method == 'POST':
        form = InquiryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'お問い合わせありがとうございます（農家用）。')
            # リダイレクトせずにテンプレートを返す
            return render(request, 'farm/farm_contact.html', {'form': form})
    else:
        form = InquiryForm()
    return render(request, 'farm/farm_contact.html', {'form': form})



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


def remove_from_cart(request, item_id):
    
    item = get_object_or_404(Item, id=item_id)
    item.delete()
    return redirect('cart')  # カートページに戻す
@login_required
def checkout(request):
    cart_items = Item.objects.filter(user=request.user)

    if not cart_items.exists():
        return redirect('cart')

    purchased_items = []

    for item in cart_items:
        sale = Sale.objects.create(
            product=item.product,
            quantity=item.quantity,
            total_price=item.product.price * item.quantity,
            farmer=item.product.user,  # 出品者
            buyer=request.user  # 購入者を設定
        )
        purchased_items.append(sale)

    # カートアイテムを削除
    cart_items.delete()

    return render(request, 'eat/checkout_complete.html', {
        'purchased_items': purchased_items
    })


@admin_required
def admin_product_manage_view(request):
    products = Product.objects.all().order_by('-created_at')
    context = {
        'products': products,
    }
    return render(request, 'admin/product_manage.html', context)



@login_required
def farm_product_manage_view(request):
    products = Product.objects.filter(user=request.user).order_by('-created_at')
    context = {'products': products}
    return render(request, 'farm/product_manage.html', context) 

@admin_required
def user_manage_view(request):
    users = CustomUser.objects.all().order_by('id')
    context = {
        'users': users,
    }
    return render(request, 'admin/user_manage.html', context)

@admin_required
def contact_list_view(request):
    inquiries = Inquiry.objects.all().order_by('-created_at')
    context = {
        'inquiries': inquiries,
    }
    return render(request, 'admin/contact_list.html', context)

@login_required
def rate_farmer(request, pk):
    farmer = get_object_or_404(CustomUser, pk=pk, role='farm')

    if request.method == "POST":
        score = request.POST.get("score")

        if score is None:
            messages.error(request, "星を選択してください。")
            return redirect('farm_detail', pk=farmer.id)

        score = int(score)
        if 1 <= score <= 5:
            FarmerRating.objects.update_or_create(
                user=request.user,
                farmer=farmer,
                defaults={'score': score}
            )
            messages.success(request, "評価を送信しました。")
        else:
            messages.error(request, "評価は1〜5で選択してください。")

    return redirect('farm_detail', pk=farmer.id)

@login_required
def buyer_list_view(request):
    # ログイン中ユーザーの購入履歴のみ取得
    sales = Sale.objects.filter(buyer=request.user).order_by('-date')

    return render(request, 'eat/buyer_list.html', {'sales': sales})


@login_required
@admin_required
def user_list_view(request):
    judges = FarmJudge.objects.filter(status__in=['pending', 'resubmit'])
    return render(request, 'admin/user_list.html', {'judges': judges})

def judge_resubmit(request, token):
    judge = get_object_or_404(FarmJudge, resubmit_token=token)

    if request.method == "POST":
        form = JudgeResubmitForm(request.POST, request.FILES, instance=judge)
        if form.is_valid():
            judge = form.save(commit=False)
            judge.status = 'pending'
            judge.save()
            messages.success(request, "再提出が完了しました。管理者の再審査をお待ちください。")
            return redirect('menu') 
    else:
        form = JudgeResubmitForm(instance=judge)

    return render(request, 'no_login/resubmit.html', {
        'form': form,
        'judge': judge
    })

def admin_judge_action(request, pk, action):
    judge = get_object_or_404(FarmJudge, pk=pk)

    if action == 'approve':
        judge.status = 'approved'
        judge.save()
    elif action == 'reject':
        
        judge.status = 'rejected'
        judge.save()
    elif action == 'resubmit':
        judge.status = 'resubmit'
        judge.save()

        #以下メール
        subject = "再提出のお願い"
        message = f"{judge.user.nickname}さん\n\n書類に修正が必要です。以下のリンクから再提出してください。\n\n"
        message += f"http://127.0.0.1:8000/polls/judge/resubmit/{judge.resubmit_token}/"
        from_email = settings.DEFAULT_FROM_EMAIL
        recipient_list = [judge.user.email]
        send_mail(subject, message, from_email, recipient_list)
        
    return redirect('user_list')

def sales_manage(request):
    # ログイン中の農家の売上データを取得
    sales = Sale.objects.filter(farmer=request.user).order_by('-date')
    context = {
        'sales': sales
    }
    return render(request, 'farm/sales_manage.html', context)



def farm_detail(request, pk):
    # `pk` で指定された農家（CustomUser）を取得
    farmer = get_object_or_404(CustomUser, pk=pk, role='farm')
    
    # その農家が出品した商品を取得
    farmer_items = Product.objects.filter(user=farmer).order_by('-id')

    # 農家の評価（仮に `FarmerRating` モデルがある場合）
    avg_rating = FarmerRating.objects.filter(farmer=farmer).aggregate(average=Avg('score'))['average']

    context = {
        'farmer': farmer,
        'farmer_items': farmer_items,
        'avg_rating': avg_rating or 0,  # 評価がない場合は 0 を表示
    }

    return render(request, 'eat/farm_detail.html', context)

@admin_required
def user_delete_view(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)

    if request.method == "POST":
        user.delete()
        return redirect('user_manage')

    return render(request, "admin/user_delete.html", {"user": user})

@login_required
def product_delete_view(request, pk):
    product = get_object_or_404(Product, pk=pk)

    if request.method == "POST":
        product.delete()
        return redirect('farm_product_manage')

    return render(request, 'farm/product_delete.html', {'product': product})


@admin_required
def admin_product_delete_view(request, pk):
    product = get_object_or_404(Product, pk=pk)

    if request.method == "POST":
        product.delete()
        return redirect('admin_product_manage')
    
    return render(request, 'admin/product_delete.html', {'product': product})

@admin_required
def admin_contact_detail_view(request, pk):
    inquiry = get_object_or_404(Inquiry, pk=pk)
    return render(request, 'admin/contact_detail.html', {'inquiry': inquiry})
