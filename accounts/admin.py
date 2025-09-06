from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Department, Faculty, Student, Staff

class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'user_type', 'is_staff')
    list_filter = ('user_type', 'is_staff', 'is_superuser', 'is_active')
    fieldsets = UserAdmin.fieldsets + (
        ('Additional Info', {'fields': ('user_type', 'phone', 'address', 'profile_picture', 'date_of_birth')}),
    )

@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'head_of_department', 'created_at')
    search_fields = ('name', 'code')

@admin.register(Faculty)
class FacultyAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'department')
    list_filter = ('department',)
    search_fields = ('name', 'code')

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('student_id', 'user', 'department', 'year_of_study', 'enrollment_date')
    list_filter = ('department', 'year_of_study')
    search_fields = ('student_id', 'user__username', 'user__first_name', 'user__last_name')

@admin.register(Staff)
class StaffAdmin(admin.ModelAdmin):
    list_display = ('staff_id', 'user', 'department', 'position', 'hire_date')
    list_filter = ('department', 'position')
    search_fields = ('staff_id', 'user__username', 'user__first_name', 'user__last_name')

admin.site.register(User, CustomUserAdmin)
