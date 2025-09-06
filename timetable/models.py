from django.db import models
from accounts.models import Faculty, Staff
from courses.models import Course

class Timetable(models.Model):
    DAYS_OF_WEEK = (
        ('monday', 'Monday'),
        ('tuesday', 'Tuesday'),
        ('wednesday', 'Wednesday'),
        ('thursday', 'Thursday'),
        ('friday', 'Friday'),
        ('saturday', 'Saturday'),
        ('sunday', 'Sunday'),
    )
    
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    day_of_week = models.CharField(max_length=10, choices=DAYS_OF_WEEK)
    start_time = models.TimeField()
    end_time = models.TimeField()
    room = models.CharField(max_length=50)
    semester = models.CharField(max_length=20)
    year = models.IntegerField()
    is_active = models.BooleanField(default=True)
    
    class Meta:
        unique_together = ('course', 'day_of_week', 'start_time', 'semester', 'year')
    
    def __str__(self):
        return f"{self.course} - {self.get_day_of_week_display()} {self.start_time}-{self.end_time}"
