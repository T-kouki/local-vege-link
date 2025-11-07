# beji/urls.py

from django.contrib import admin
from django.urls import include, path
from polls import views  # polls.views を使用する

urlpatterns = [
    # 🔹 トップページを未ログインメニュー画面に設定
    path("", views.menu_view, name="menu"),

    path("polls/", include("polls.urls")),
    path("admin/", admin.site.urls),
    path("accounts/", include("django.contrib.auth.urls")),
    path("menu/", views.menu_view, name="menu"), 
]
