# polls/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("menu/", views.menu, name="menu"),
    path("cart/", views.cart, name="cart"),
    path("signup/", views.signup_view, name="signup"),
    path("login/", views.login_view, name="login"),
    path('logout/', views.logout_view, name='logout'),
    path("signup_menu/", views.signup_menu_view, name="signup_menu"),
    path("signup/eat/", views.signup_eat, name="signup_eat"),
    path("signup/farm/", views.signup_farm, name="signup_farm"),
    path("farm_menu/", views.farm_menu_view, name="farm_menu"),
    path("eat_menu/", views.eat_menu_view, name="eat_menu"),
    path("product_upload/", views.farm_product_upload, name="product_upload"),
    path("edit_profile/", views.profile_edit, name="edit_profile"),
   
]
