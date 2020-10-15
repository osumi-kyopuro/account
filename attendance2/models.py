from django.db import models
#from django.contrib.auth.models import User
from _datetime import timedelta
from _datetime import datetime
from django.utils import timezone
from myapp.models import CustomUser
# Create your models here.
class Attendance(models.Model): 
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, verbose_name="スタッフ名")
    scheduled_attend_time = models.DateTimeField(blank=True, null=True,verbose_name="出勤予定時刻")
    scheduled_leave_time = models.DateTimeField(blank=True, null=True,verbose_name="退勤予定時刻")
    attend_time = models.DateTimeField(blank=True, null=True, verbose_name="出勤時刻")
    leave_time = models.DateTimeField(blank=True, null=True, verbose_name="退勤時刻")
    work_time=models.DurationField(default=timedelta(), verbose_name="労働時間")
    remarks = models.TextField(blank=True, null=True, verbose_name="備考欄")
    def is_late(self): #遅刻判定フラグ
        if self.attend_time:
            if self.attend_time > self.scheduled_attend_time:
                return '○'
            else:
                return ' '

        else:
            return ' '

    def is_early(self): #早退判定フラグ
        if self.leave_time:
            if self.leave_time < self.scheduled_leave_time:
                return '○'
            else:
                return ' '
        else:
            return ' '

    def is_absence(self): #欠勤判定フラグ
        if self.attend_time== None and (self.scheduled_leave_time < timezone.now()):
            return '○'
        else:
            return ' '

