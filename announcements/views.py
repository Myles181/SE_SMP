from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Announcement
from .forms import AnnouncementForm

@login_required
def announcement_list(request):
    announcements = Announcement.objects.filter(is_active=True)
    return render(request, 'announcements/announcement_list.html', {'announcements': announcements})

@login_required
def announcement_detail(request, announcement_id):
    announcement = get_object_or_404(Announcement, id=announcement_id)
    return render(request, 'announcements/announcement_detail.html', {'announcement': announcement})

@login_required
def manage_announcements(request):
    if request.user.user_type != 'admin':
        messages.error(request, 'Access denied.')
        return redirect('dashboard')
    
    announcements = Announcement.objects.all()
    return render(request, 'announcements/manage_announcements.html', {'announcements': announcements})

@login_required
def add_announcement(request):
    if request.user.user_type != 'admin':
        messages.error(request, 'Access denied.')
        return redirect('dashboard')
    
    if request.method == 'POST':
        form = AnnouncementForm(request.POST)
        if form.is_valid():
            announcement = form.save(commit=False)
            announcement.author = request.user
            announcement.save()
            messages.success(request, 'Announcement added successfully!')
            return redirect('manage_announcements')
    else:
        form = AnnouncementForm()
    
    return render(request, 'announcements/add_announcement.html', {'form': form})
