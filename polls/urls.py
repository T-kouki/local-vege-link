from django.urls import path

from . import views


urlpatterns = [
    path("", views.index, name="index"),
    path('menu/', views.menu, name='menu'),
    path('cart/', views.cart, name='cart'),
    path('signup/', views.signup_view, name='signup'),
    path('menu/', views.menu_view, name='menu'),
]