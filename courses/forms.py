from django import forms
from .models import Course
from accounts.models import Department, Staff, User

class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['name', 'code', 'description', 'credits', 'department', 'instructor', 'semester', 'year']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            'semester': forms.Select(choices=[
                ('Fall', 'Fall'),
                ('Spring', 'Spring'),
                ('Summer', 'Summer'),
            ]),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Get instructors from Staff members
        self.fields['instructor'].queryset = Staff.objects.select_related('user').all()
        self.fields['instructor'].empty_label = "Select an Instructor"
        
        # Get departments from database
        self.fields['department'].queryset = Department.objects.all()
        self.fields['department'].empty_label = "Select a Department"
        
        # Add CSS classes for better styling
        for field_name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})
