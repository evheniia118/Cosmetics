from django.urls import path, include
from . import views

app_name = 'cosmetics'

urlpatterns = [
    # Головна сторінка
    path('', views.product_list, name='home'),

    # Продукти
    path('product/<int:id>/', views.product_detail, name='product_detail'),
    path('add/', views.product_create, name='product_create'),
    path('edit/<int:id>/', views.product_update, name='product_edit'),
    path('delete/<int:id>/', views.product_delete, name='product_delete'),

    # Аутентифікація
    path('register/', views.register, name='register'),
    path('logout/', views.logout_view, name='custom_logout'),

    # Django auth (login, password change і т.д.)
    path('accounts/', include('django.contrib.auth.urls')),
]

# Перемикання мов
urlpatterns += [
    path('i18n/', include('django.conf.urls.i18n')),
]