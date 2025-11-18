# polls/urls.py

from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path("", views.index, name="index"),
    path("menu/", views.menu, name="menu"),
    path("cart/", views.cart, name="cart"),
    path("login/", views.login_view, name="login"),
    path('logout_confirm/', views.logout_confirm_view, name='logout_confirm'),
    path('logout/', views.logout_view, name='logout'),
    path("signup_menu/", views.signup_menu_view, name="signup_menu"),
    path("signup/eat/", views.signup_eat, name="signup_eat"),
    path("signup/farm/", views.signup_farm, name="signup_farm"),
    path("farm_menu/", views.farm_menu_view, name="farm_menu"),
    path("eat_menu/", views.eat_menu_view, name="eat_menu"),
    path("admin_menu/", views.admin_menu_view, name="admin_menu"),
    path("product_upload/", views.farm_product_upload, name="product_upload"),
    path("edit_profile/", views.profile_edit, name="edit_profile"),
    path('contact', views.contact_view, name='contact'),
    path("contact_view/", views.admincontact_view, name="contact_view"),
    path('search/', views.search_view, name='search'),
    path("products/", views.product_list_view, name="product_list"),
    path("product_history/", views.product_history_view, name="product_history"),
    path('product/<int:pk>/', views.product_detail, name='product_detail'),
    path('add_cart/add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path("farm/product_manage/", views.farm_product_manage_view, name="farm_product_manage"),
    path("admin/product_manage/", views.admin_product_manage_view, name="admin_product_manage"),
    path('product/<int:pk>/edit/', views.product_edit_view, name='product_edit'),
    path('product/<int:pk>/delete/', views.product_delete_view, name='product_delete'),
    path('sales_manage/', views.sales_manage, name='sales_manage'),
    path('product_edit/', views.product_edit_view, name='product_edit'),
    #path('sales_report/', views.sales_report, name='sales_report'),
    path('cart/remove/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('farm/<int:pk>/', views.farm_detail, name='farm_detail'),
    path('buyer_list/', views.buyer_list_view, name='buyer_list'),
    path("user_list/", views.user_list_view, name="user_list"),
    path("user_manage/", views.user_manage_view, name="user_manage"),
    path('farm/<int:pk>/rate/', views.rate_farmer, name='rate_farmer'),
    path("judge/resubmit/<uuid:token>/", views.judge_resubmit, name="judge_resubmit"),
    path("admin/judge_action/<int:pk>/<str:action>/", views.admin_judge_action, name="admin_judge_action"),
    

]   
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
