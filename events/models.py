from django.db import models
from accounts.models import User

class Event(models.Model):
    EVENT_TYPES = (
        ('academic', 'Academic'),
        ('sports', 'Sports'),
        ('cultural', 'Cultural'),
        ('workshop', 'Workshop'),
        ('seminar', 'Seminar'),
        ('other', 'Other'),
    )
    
    title = models.CharField(max_length=200)
    description = models.TextField()
    event_type = models.CharField(max_length=20, choices=EVENT_TYPES)
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    location = models.CharField(max_length=200)
    organizer = models.ForeignKey(User, on_delete=models.CASCADE)
    max_participants = models.IntegerField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.title} - {self.date}"

class EventRegistration(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    registration_date = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('event', 'user')
    
    def __str__(self):
        return f"{self.user} registered for {self.event}"
