from django.urls import path
from . import views

urlpatterns = [
    path('', views.timetable_view, name='timetable'),
    path('manage/', views.manage_timetable, name='manage_timetable'),
    path('add/', views.add_timetable_entry, name='add_timetable_entry'),
]
