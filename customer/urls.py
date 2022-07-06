from django.urls import path

from . import views

urlpatterns = [
    path('create_user/', views.create_user, name='create_user'),
    path('get_all_users/', views.get_customers_info, name='get_all_users'),
]