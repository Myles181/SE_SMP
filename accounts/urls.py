from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register_view, name='register'),
    path('profile/', views.profile_view, name='profile'),
    path('edit-profile/', views.edit_profile, name='edit_profile'),
    path('add-staff/', views.add_staff, name='add_staff'),
    path('instructors/', views.instructor_list, name='instructor_list'),
    path('instructors/edit/<int:staff_id>/', views.edit_instructor, name='edit_instructor'),
    path('instructors/toggle/<int:staff_id>/', views.toggle_instructor_status, name='toggle_instructor_status'),
    path('instructors/delete/<int:staff_id>/', views.delete_instructor, name='delete_instructor'),
]
