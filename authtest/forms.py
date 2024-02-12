from django import forms
from .models import Attendance

class AttendanceForm(forms.ModelForm):
    class Meta:
        model = Attendance
        fields = ['employee_id', 'check_in', 'check_out']
        labels = {
            'employee_id': '社員ID',
            'check_in': '出勤時刻',
            'check_out': '退勤時刻',
        }
