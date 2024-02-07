from django import forms

class AttendanceForm(forms.Form):
    employee_id = forms.CharField(label='社員ID', max_length=10)
