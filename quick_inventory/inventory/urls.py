from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('products/', views.product_list, name='product_list'),
    path('products/add/', views.add_product, name='add_product'),
    path('products/<int:product_id>/edit/', views.edit_product, name='edit_product'),
    path('transactions/', views.transaction_list, name='transaction_list'),
    path('profile/', views.profile, name='profile'),  # маршрут для профиля
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('daily-sales/', views.daily_sales, name='daily_sales'),
    path('close-day/', views.close_day, name='close_day'),
]
