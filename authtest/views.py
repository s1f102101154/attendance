from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Attendance
from django.utils import timezone

# Create your views here.
def home(request):
    if request.method == 'POST':
        employee_id = request.POST.get('employee_id')
        action = request.POST.get('action')
        if action == 'check_in':
            # 出勤記録
            Attendance.objects.create(employee_id=employee_id, check_in=timezone.now())
        elif action == 'check_out':
            # 退勤記録
            try:
                record = Attendance.objects.filter(employee_id=employee_id, check_out=None).latest('check_in')
                record.check_out = timezone.now()
                record.save()
            except Attendance.DoesNotExist:
                pass  # 退勤記録がない場合の処理
        return redirect('home')

    return render(request, 'authtest/home.html', {})

@login_required
def private_page(request):
    return render(request, 'authtest/private.html', {})

def public_page(request):
    return render(request, 'authtest/public.html', {})
