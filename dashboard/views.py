from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.utils import timezone
from accounts.models import User, Student, Staff
from courses.models import Course
from events.models import Event
from announcements.models import Announcement
from results.models import Result

def landing_view(request):
    """Landing page for non-authenticated users"""
    if request.user.is_authenticated:
        return redirect('dashboard')
    return render(request, 'landing.html')

@login_required
def dashboard_view(request):
    user = request.user
    context = {
        'user': user,
    }
    
    if user.user_type == 'admin':
        # Admin dashboard with statistics
        context.update({
            'total_students': Student.objects.count(),
            'total_staff': Staff.objects.count(),
            'total_courses': Course.objects.count(),
            'total_events': Event.objects.count(),
            'recent_announcements': Announcement.objects.order_by('-created_at')[:5],
            'recent_events': Event.objects.order_by('-created_at')[:5],
        })
        return render(request, 'dashboard/admin_dashboard.html', context)
    
    elif user.user_type == 'student':
        # Student dashboard
        try:
            student = user.student
            context.update({
                'student': student,
                'recent_announcements': Announcement.objects.order_by('-created_at')[:5],
                'upcoming_events': Event.objects.filter(date__gte=timezone.now().date()).order_by('date')[:5],
                'recent_results': Result.objects.filter(student=student).order_by('-created_at')[:5],
            })
        except:
            pass
        return render(request, 'dashboard/student_dashboard.html', context)
    
    else:
        # Staff or guest dashboard
        context.update({
            'recent_announcements': Announcement.objects.order_by('-created_at')[:5],
            'upcoming_events': Event.objects.order_by('date')[:5],
        })
        return render(request, 'dashboard/general_dashboard.html', context)
