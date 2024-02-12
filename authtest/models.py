from django.db import models
from django.utils import timezone

class Attendance(models.Model):
    employee_id = models.CharField(max_length=10)
    check_in = models.DateTimeField(null=True, blank=True)
    check_out = models.DateTimeField(null=True, blank=True)

    def calculate_salary(self):
        if self.check_in and self.check_out:
            duration = self.check_out - self.check_in
            hours = duration.total_seconds() / 3600
            return round(hours * 1200, 2)  # ここでは時給1200円を使用
        return 0

    def __str__(self):
        return self.employee_id
