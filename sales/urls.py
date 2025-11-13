from django.urls import path
from . import views

urlpatterns = [
    path('home/', views.sales_home, name='sales_home'),
    path('report/', views.sales_report, name='sales_report'),
]