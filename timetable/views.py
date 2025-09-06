from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Timetable
from .forms import TimetableForm

@login_required
def timetable_view(request):
    if request.user.user_type == 'student':
        try:
            student = request.user.student
            # Get courses the student is enrolled in
            from courses.models import CourseEnrollment
            enrolled_courses = CourseEnrollment.objects.filter(
                student=student, is_active=True
            ).values_list('course', flat=True)
            
            timetable_entries = Timetable.objects.filter(
                course__in=enrolled_courses, is_active=True
            ).order_by('day_of_week', 'start_time')
        except:
            timetable_entries = []
    else:
        timetable_entries = Timetable.objects.filter(is_active=True).order_by('day_of_week', 'start_time')
    
    return render(request, 'timetable/timetable.html', {'timetable_entries': timetable_entries})

@login_required
def manage_timetable(request):
    if request.user.user_type != 'admin':
        messages.error(request, 'Access denied.')
        return redirect('dashboard')
    
    timetable_entries = Timetable.objects.all().order_by('day_of_week', 'start_time')
    return render(request, 'timetable/manage_timetable.html', {'timetable_entries': timetable_entries})

@login_required
def add_timetable_entry(request):
    if request.user.user_type != 'admin':
        messages.error(request, 'Access denied.')
        return redirect('dashboard')
    
    if request.method == 'POST':
        form = TimetableForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Timetable entry added successfully!')
            return redirect('manage_timetable')
    else:
        form = TimetableForm()
    
    return render(request, 'timetable/add_timetable_entry.html', {'form': form})
