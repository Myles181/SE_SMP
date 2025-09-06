from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Result
from .forms import ResultForm

@login_required
def result_list(request):
    if request.user.user_type == 'student':
        try:
            student = request.user.student
            results = Result.objects.filter(student=student).order_by('-created_at')
        except:
            results = []
    else:
        results = Result.objects.all().order_by('-created_at')
    
    return render(request, 'results/result_list.html', {'results': results})

@login_required
def manage_results(request):
    if request.user.user_type != 'admin':
        messages.error(request, 'Access denied.')
        return redirect('dashboard')
    
    results = Result.objects.all().order_by('-created_at')
    return render(request, 'results/manage_results.html', {'results': results})

@login_required
def add_result(request):
    if request.user.user_type != 'admin':
        messages.error(request, 'Access denied.')
        return redirect('dashboard')
    
    if request.method == 'POST':
        form = ResultForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Result added successfully!')
            return redirect('manage_results')
    else:
        form = ResultForm()
    
    return render(request, 'results/add_result.html', {'form': form})
