from django.urls import path

from . import views

urlpatterns = [
    path('create_plan/', views.create_plan, name='create_plan'),
    path('get_all_plans/', views.get_plans, name='get_all_plans'),
    path('create_promotion/', views.create_promotion, name='create_promotion'),
    path('promo_for_id/', views.promotions_for_plan, name='promo_for_id'),
    path('create_customer_goal/', views.create_customer_goal, name='create_customer_goal'),
    path('get_customer_goal/', views.get_customer_goal, name='get_customer_goal'),
]