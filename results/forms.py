from django import forms
from .models import Result
from accounts.models import Student
from courses.models import Course
from datetime import date

class ResultForm(forms.ModelForm):
    date_recorded = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        initial=date.today,
        help_text="Date when the result was recorded"
    )
    
    class Meta:
        model = Result
        fields = ['student', 'course', 'semester', 'year', 'marks_obtained', 'total_marks', 'grade', 'gpa']
        widgets = {
            'semester': forms.Select(choices=[
                ('Fall', 'Fall'),
                ('Spring', 'Spring'),
                ('Summer', 'Summer'),
            ]),
            'year': forms.NumberInput(attrs={'min': 2020, 'max': 2030, 'value': date.today().year}),
            'marks_obtained': forms.NumberInput(attrs={'step': '0.01', 'min': '0'}),
            'total_marks': forms.NumberInput(attrs={'step': '0.01', 'min': '0'}),
            'gpa': forms.NumberInput(attrs={'step': '0.01', 'min': '0', 'max': '4.0'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Populate dropdowns with actual data
        self.fields['student'].queryset = Student.objects.select_related('user').all()
        self.fields['student'].empty_label = "Select a Student"
        
        self.fields['course'].queryset = Course.objects.all()
        self.fields['course'].empty_label = "Select a Course"
        
        # Add CSS classes for styling
        for field_name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})
