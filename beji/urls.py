# beji/urls.py

from django.contrib import admin
from django.urls import include, path
from polls import views  # polls.views を使用する
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # 🔹 トップページを未ログインメニュー画面に設定
    path("", views.menu_view, name="menu"),

    path("polls/", include("polls.urls")),
    path("admin/", admin.site.urls),
    path("menu/", views.menu_view, name="menu"), 
    path("polls/", include(("polls.urls", "polls"), namespace="polls")),
    
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)