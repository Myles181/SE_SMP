from django import forms
from .models import Announcement

class AnnouncementForm(forms.ModelForm):
    class Meta:
        model = Announcement
        fields = ['title', 'content', 'priority']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 6}),
        }
