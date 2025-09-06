from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from .models import Course, CourseEnrollment
from .forms import CourseForm

@login_required
def course_list(request):
    courses = Course.objects.filter(is_active=True).order_by('name')
    paginator = Paginator(courses, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'courses/course_list.html', {'page_obj': page_obj})

@login_required
def course_detail(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    enrollments = CourseEnrollment.objects.filter(course=course, is_active=True)
    
    context = {
        'course': course,
        'enrollments': enrollments,
        'is_enrolled': False
    }
    
    if request.user.user_type == 'student':
        try:
            student = request.user.student
            context['is_enrolled'] = CourseEnrollment.objects.filter(
                student=student, course=course, is_active=True
            ).exists()
        except:
            pass
    
    return render(request, 'courses/course_detail.html', context)

@login_required
def manage_courses(request):
    if request.user.user_type != 'admin':
        messages.error(request, 'Access denied.')
        return redirect('dashboard')
    
    courses = Course.objects.all().order_by('-created_at')
    return render(request, 'courses/manage_courses.html', {'courses': courses})

@login_required
def add_course(request):
    if request.user.user_type != 'admin':
        messages.error(request, 'Access denied.')
        return redirect('dashboard')
    
    if request.method == 'POST':
        form = CourseForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Course added successfully!')
            return redirect('manage_courses')
    else:
        form = CourseForm()
    
    return render(request, 'courses/add_course.html', {'form': form})

@login_required
def edit_course(request, course_id):
    if request.user.user_type != 'admin':
        messages.error(request, 'Access denied.')
        return redirect('dashboard')
    
    course = get_object_or_404(Course, id=course_id)
    
    if request.method == 'POST':
        form = CourseForm(request.POST, instance=course)
        if form.is_valid():
            form.save()
            messages.success(request, 'Course updated successfully!')
            return redirect('manage_courses')
    else:
        form = CourseForm(instance=course)
    
    return render(request, 'courses/edit_course.html', {'form': form, 'course': course})
