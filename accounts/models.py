from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    USER_TYPES = (
        ('admin', 'Admin'),
        ('student', 'Student'),
        ('staff', 'Staff'),
        ('guest', 'Guest'),
    )
    
    user_type = models.CharField(max_length=10, choices=USER_TYPES, default='student')
    phone = models.CharField(max_length=15, blank=True)
    address = models.TextField(blank=True)
    profile_picture = models.ImageField(upload_to='profiles/', blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    
    def __str__(self):
        return f"{self.username} ({self.get_user_type_display()})"

class Department(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=10, unique=True)
    description = models.TextField(blank=True)
    head_of_department = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name

class Faculty(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=10, unique=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    description = models.TextField(blank=True)
    
    class Meta:
        verbose_name_plural = "Faculties"
    
    def __str__(self):
        return self.name

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    student_id = models.CharField(max_length=20, unique=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, null=True, blank=True)
    year_of_study = models.IntegerField()
    enrollment_date = models.DateField()
    
    def __str__(self):
        return f"{self.student_id} - {self.user.get_full_name()}"

class Staff(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    staff_id = models.CharField(max_length=20, unique=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    position = models.CharField(max_length=100)
    hire_date = models.DateField()
    
    class Meta:
        verbose_name_plural = "Staff"
    
    def __str__(self):
        return f"{self.staff_id} - {self.user.get_full_name()}"
