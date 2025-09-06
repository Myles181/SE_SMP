from django.urls import path
from . import views

urlpatterns = [
    path('', views.result_list, name='result_list'),
    path('manage/', views.manage_results, name='manage_results'),
    path('add/', views.add_result, name='add_result'),
]
