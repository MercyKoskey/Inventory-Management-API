from django.urls import path
from . import views

urlpatterns = [
    path("/", views.home_redirect, name="home"),
    path("signup/", views.signup, name="signup"),
    path("login/", views.login, name="login"),
    path("items/", views.items, name="items"),
    path("reports/", views.reports, name="reports"),
]
