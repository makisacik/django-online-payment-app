"""
URL configuration for webapps2024 project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from register import views as auth_views
from payapp import views as payapp_views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", auth_views.login_user),
    path("register/", auth_views.register_user, name="register"),
    path('register_admin/', auth_views.register_admin, name='register_admin'),
    path("login/", auth_views.login_user, name="login"),
    path("home/", payapp_views.home, name="home"),
    path("admin-home/", payapp_views.admin_home, name="admin_home"),
    path("logout/", auth_views.logout_user, name="logout"),
    path('transfer_money/', payapp_views.transfer_money, name='transfer_money'),
    path('request_money/', payapp_views.request_money, name='request_money'),
    path('cancel_money_request/<int:request_id>/', payapp_views.cancel_money_request, name='cancel_money_request'),
    path('accept_money_request/<int:request_id>/', payapp_views.accept_money_request, name='accept_money_request'),
    path('', include('currency_conversion.urls')),
]
