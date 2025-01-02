"""
URL configuration for ticketsales project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from app.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", index, name="index"),
    path("route_info/", route_info, name="route_info"),
    path("ticket_buy/", ticket_buy, name="ticket_buy"),
    path("about/", about, name="about"),
    path("accounts/register_done", RegisterDoneView.as_view(), name="register_done"),
    path("accounts/register", RegisterUserView.as_view(), name="register"),
    path("accounts/login", AppLoginView.as_view(), name="login"),
    path("accounts/logout", AppLogoutView.as_view(), name="logout"),
    path("accounts/profile", profile, name="profile"),
]
