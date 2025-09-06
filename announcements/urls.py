from django.urls import path
from . import views

urlpatterns = [
    path('', views.announcement_list, name='announcement_list'),
    path('<int:announcement_id>/', views.announcement_detail, name='announcement_detail'),
    path('manage/', views.manage_announcements, name='manage_announcements'),
    path('add/', views.add_announcement, name='add_announcement'),
]
