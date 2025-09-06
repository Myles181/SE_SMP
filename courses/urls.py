from django.urls import path
from . import views

urlpatterns = [
    path('', views.course_list, name='course_list'),
    path('<int:course_id>/', views.course_detail, name='course_detail'),
    path('manage/', views.manage_courses, name='manage_courses'),
    path('add/', views.add_course, name='add_course'),
    path('edit/<int:course_id>/', views.edit_course, name='edit_course'),
]
