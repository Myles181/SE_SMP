from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from .models import Event, EventRegistration
from .forms import EventForm

@login_required
def event_list(request):
    events = Event.objects.filter(is_active=True, date__gte=timezone.now().date()).order_by('date')
    return render(request, 'events/event_list.html', {'events': events})

@login_required
def event_detail(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    is_registered = EventRegistration.objects.filter(event=event, user=request.user).exists()
    
    context = {
        'event': event,
        'is_registered': is_registered,
        'registrations_count': EventRegistration.objects.filter(event=event).count()
    }
    
    return render(request, 'events/event_detail.html', context)

@login_required
def manage_events(request):
    if request.user.user_type != 'admin':
        messages.error(request, 'Access denied.')
        return redirect('dashboard')
    
    events = Event.objects.all().order_by('-created_at')
    return render(request, 'events/manage_events.html', {'events': events})

@login_required
def add_event(request):
    if request.user.user_type != 'admin':
        messages.error(request, 'Access denied.')
        return redirect('dashboard')
    
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            event = form.save(commit=False)
            event.organizer = request.user
            event.save()
            messages.success(request, 'Event added successfully!')
            return redirect('manage_events')
    else:
        form = EventForm()
    
    return render(request, 'events/add_event.html', {'form': form})
