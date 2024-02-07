from django.db import models

# Create your models here.
from django.db import models

class Attendance(models.Model):
    employee_id = models.CharField(max_length=10)
    check_in = models.DateTimeField(null=True, blank=True)
    check_out = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.employee_id
