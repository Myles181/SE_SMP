from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, Staff, Student, Faculty, Department

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    username = forms.CharField(max_length=150, required=True)
    user_type = forms.ChoiceField(choices=User.USER_TYPES, required=True)
    
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'user_type', 'password1', 'password2')
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.user_type = self.cleaned_data['user_type']
        user.username = self.cleaned_data['username']
        if commit:
            user.save()
        return user

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'phone', 'address', 'profile_picture', 'date_of_birth']
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
            'address': forms.Textarea(attrs={'rows': 3}),
        }

class StaffCreationForm(forms.ModelForm):
    # User fields
    username = forms.CharField(max_length=150, required=True)
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    email = forms.EmailField(required=True)
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput)
    
    # Staff-specific fields
    staff_id = forms.CharField(max_length=20, required=True, help_text="Unique staff identifier")
    department = forms.ModelChoiceField(queryset=Department.objects.all(), required=True)
    position = forms.CharField(max_length=100, required=True, help_text="e.g., Lecturer, Professor, Assistant")
    hire_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), required=True)
    
    class Meta:
        model = Staff
        fields = ['staff_id', 'department', 'position', 'hire_date']
    
    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2
    
    def save(self, commit=True):
        # Create the User first
        user = User.objects.create_user(
            username=self.cleaned_data['username'],
            email=self.cleaned_data['email'],
            password=self.cleaned_data['password1'],
            first_name=self.cleaned_data['first_name'],
            last_name=self.cleaned_data['last_name'],
            user_type='staff'
        )
        
        # Create the Staff profile
        staff = super().save(commit=False)
        staff.user = user
        if commit:
            staff.save()
        return staff

class StaffEditForm(forms.ModelForm):
    # User fields
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    email = forms.EmailField(required=True)
    
    # Staff-specific fields
    staff_id = forms.CharField(max_length=20, required=True, help_text="Unique staff identifier")
    department = forms.ModelChoiceField(queryset=Department.objects.all(), required=True)
    position = forms.CharField(max_length=100, required=True, help_text="e.g., Lecturer, Professor, Assistant")
    hire_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), required=True)
    
    class Meta:
        model = Staff
        fields = ['staff_id', 'department', 'position', 'hire_date']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.user:
            self.fields['first_name'].initial = self.instance.user.first_name
            self.fields['last_name'].initial = self.instance.user.last_name
            self.fields['email'].initial = self.instance.user.email
    
    def save(self, commit=True):
        staff = super().save(commit=False)
        
        # Update the associated User
        if staff.user:
            staff.user.first_name = self.cleaned_data['first_name']
            staff.user.last_name = self.cleaned_data['last_name']
            staff.user.email = self.cleaned_data['email']
            if commit:
                staff.user.save()
        
        if commit:
            staff.save()
        return staff
