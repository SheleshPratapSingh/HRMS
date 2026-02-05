from django.contrib import admin
from .models import Attendance

@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ['employee', 'date', 'status', 'created_at']
    search_fields = ['employee__full_name', 'employee__employee_id']
    list_filter = ['status', 'date', 'created_at']
    ordering = ['-date']