from django.db import models
from accounts.models import User

class DashboardStats(models.Model):
    total_students = models.IntegerField(default=0)
    total_staff = models.IntegerField(default=0)
    total_courses = models.IntegerField(default=0)
    total_events = models.IntegerField(default=0)
    last_updated = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name_plural = "Dashboard Statistics"
    
    def __str__(self):
        return f"Stats updated on {self.last_updated}"
