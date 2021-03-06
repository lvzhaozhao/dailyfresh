"""dailyfresh URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from df_goods.views import index

urlpatterns = [
    path('', index, name='index'),
    path('admin/', admin.site.urls),
    path("user/", include("df_user.urls", namespace="user")),
    path("goods/", include("df_goods.urls", namespace="goods")),
    path("cart/", include("df_cart.urls", namespace="cart")),
    path("order/", include("df_order.urls", namespace="order")),
    path("search/", include("haystack.urls")),
    path('ckeditor', include('ckeditor_uploader.urls'))
]

if settings.DEBUG:
    # 在debug模式下把media_url开始的路径都访问到media_root的路径下
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
