from django.shortcuts import render, get_object_or_404, redirect
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Attendance
from django.utils import timezone
from .forms import AttendanceForm
from django.http import HttpResponseRedirect
from django.http import JsonResponse
from django.http import JsonResponse, HttpResponseNotAllowed

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

    return render(request, 'authtest/index.html', {})

@login_required
def private_page(request):
    # 編集や削除の要求を処理
    if 'edit' in request.GET:
        id = request.GET['edit']
        attendance = get_object_or_404(Attendance, id=id)
        attendances = Attendance.objects.all()
        total_salary = sum([attendance.calculate_salary() for attendance in attendances if attendance.check_out])

        return render(request, 'authtest/private.html', {'attendances': attendances, 'total_salary': total_salary})

    if 'delete' in request.GET:
        id = request.GET['delete']
        attendance = get_object_or_404(Attendance, id=id)
        attendance.delete()
        return redirect('priv')

    # 通常の表示処理
    attendances = Attendance.objects.all()
    return render(request, 'authtest/private.html', {'attendances': attendances})


def public_page(request):
    # データベースから全ての出勤・退勤記録を取得
    attendances = Attendance.objects.all()
    # 取得したデータをテンプレートに渡す
    return render(request, 'authtest/public.html', {'attendances': attendances})

def edit_attendance(request, id):
    attendance = get_object_or_404(Attendance, id=id)
    if request.method == 'POST':
        form = AttendanceForm(request.POST, instance=attendance)
        if form.is_valid():
            form.save()
            return redirect('priv')
    else:
        form = AttendanceForm(instance=attendance)
    return render(request, 'authtest/edit_attendance.html', {'form': form})

def delete_attendance(request, id):
    if request.method == 'POST':
        attendance = get_object_or_404(Attendance, id=id)
        attendance.delete()
        if request.is_ajax():
            return JsonResponse({'status': 'ok'})
        else:
            return redirect('priv')
    else:
        # POSTメソッド以外でアクセスされた場合、エラーレスポンスを返す
        return HttpResponseNotAllowed(['POST'])