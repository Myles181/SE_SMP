from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from .models import User, Student, Staff
from .forms import UserRegistrationForm, ProfileUpdateForm, StaffCreationForm, StaffEditForm

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('dashboard')
                else:
                    form.add_error(None, 'Your account has been deactivated. Please contact the administrator.')
            else:
                form.add_error(None, 'Invalid username or password. Please check your credentials and try again.')
        # Form validation errors will be displayed automatically
    else:
        form = AuthenticationForm()
    return render(request, 'accounts/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def profile_view(request):
    return render(request, 'accounts/profile.html', {'user': request.user})

@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('profile')
    else:
        form = ProfileUpdateForm(instance=request.user)
    return render(request, 'accounts/edit_profile.html', {'form': form})

def register_view(request):
    if request.method == 'POST':
        # print("I got here")
        form = UserRegistrationForm(request.POST)
        print(form)
        if form.is_valid():
            user = form.save()
            messages.success(request, 'Registration successful! Please login.')
            return redirect('login')
    else:
        form = UserRegistrationForm()
    return render(request, 'accounts/register.html', {'form': form})

@login_required
def add_staff(request):
    if request.user.user_type != 'admin':
        messages.error(request, 'Access denied. Admin privileges required.')
        return redirect('dashboard')
    
    if request.method == 'POST':
        form = StaffCreationForm(request.POST)
        if form.is_valid():
            try:
                staff = form.save()
                messages.success(request, f'Staff member {staff.user.get_full_name()} created successfully!')
                return redirect('user_list')
            except Exception as e:
                messages.error(request, f'Error creating staff member: {str(e)}')
    else:
        form = StaffCreationForm()
    
    return render(request, 'accounts/add_staff.html', {'form': form})

@login_required
def instructor_list(request):
    if request.user.user_type != 'admin':
        messages.error(request, 'Access denied. Admin privileges required.')
        return redirect('dashboard')
    
    staff_members = Staff.objects.select_related('user', 'department').all()
    context = {
        'staff_members': staff_members,
        'total_staff': staff_members.count(),
        'active_staff': staff_members.filter(user__is_active=True).count(),
        'inactive_staff': staff_members.filter(user__is_active=False).count(),
    }
    return render(request, 'accounts/instructor_list.html', context)

@login_required
def edit_instructor(request, staff_id):
    if request.user.user_type != 'admin':
        messages.error(request, 'Access denied. Admin privileges required.')
        return redirect('dashboard')
    
    staff = get_object_or_404(Staff, id=staff_id)
    
    if request.method == 'POST':
        form = StaffEditForm(request.POST, instance=staff)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, f'Instructor {staff.user.get_full_name()} updated successfully!')
                return redirect('instructor_list')
            except Exception as e:
                messages.error(request, f'Error updating instructor: {str(e)}')
    else:
        form = StaffEditForm(instance=staff)
    
    return render(request, 'accounts/edit_instructor.html', {'form': form, 'staff': staff})

@login_required
def toggle_instructor_status(request, staff_id):
    if request.user.user_type != 'admin':
        messages.error(request, 'Access denied. Admin privileges required.')
        return redirect('dashboard')
    
    staff = get_object_or_404(Staff, id=staff_id)
    
    if request.method == 'POST':
        staff.user.is_active = not staff.user.is_active
        staff.user.save()
        
        status = "activated" if staff.user.is_active else "deactivated"
        messages.success(request, f'Instructor {staff.user.get_full_name()} has been {status}.')
    
    return redirect('instructor_list')

@login_required
def delete_instructor(request, staff_id):
    if request.user.user_type != 'admin':
        messages.error(request, 'Access denied. Admin privileges required.')
        return redirect('dashboard')
    
    staff = get_object_or_404(Staff, id=staff_id)
    
    if request.method == 'POST':
        instructor_name = staff.user.get_full_name()
        staff.user.delete()  # This will cascade delete the staff record
        messages.success(request, f'Instructor {instructor_name} has been deleted.')
        return redirect('instructor_list')
    
    return render(request, 'accounts/delete_instructor.html', {'staff': staff})
