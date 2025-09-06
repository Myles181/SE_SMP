from django import forms
from .models import Timetable
from courses.models import Course

class TimetableForm(forms.ModelForm):
    class Meta:
        model = Timetable
        fields = ['course', 'day_of_week', 'start_time', 'end_time', 'room', 'semester', 'year']
        widgets = {
            'start_time': forms.TimeInput(attrs={'type': 'time'}),
            'end_time': forms.TimeInput(attrs={'type': 'time'}),
            'semester': forms.Select(choices=[
                ('Fall', 'Fall'),
                ('Spring', 'Spring'),
                ('Summer', 'Summer'),
            ]),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['course'].queryset = Course.objects.filter(is_active=True)
