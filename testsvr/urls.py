"""testsvr URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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
from django.urls import path
from django.conf.urls import url, include

from django.conf import settings
from django.conf.urls.static import static

admin.AdminSite.site_header = '三语信息技术有限公司'
admin.AdminSite.site_url = None
admin.AdminSite.index_title = '首页'

urlpatterns = [
                  path('admin/', admin.site.urls),
                  url(r'^estore/', include('estore.urls')),
                  url('^', include('django.contrib.auth.urls'))
              ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) \
              + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

#@todo 后台管理 增加自动权限控制

#@todo 实现一键式增加新用户、新店铺、创建新组等等。

#@todo 上传图片不成功，返回之后，图片不显示。