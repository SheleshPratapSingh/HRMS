from rest_framework import serializers
from .models import Attendance
from employees.models import Employee
from datetime import datetime

class AttendanceSerializer(serializers.ModelSerializer):
    employee_name = serializers.CharField(source='employee.full_name', read_only=True)
    employee_id = serializers.CharField(source='employee.employee_id', read_only=True)
    
    class Meta:
        model = Attendance
        fields = ['id', 'employee', 'employee_name', 'employee_id', 'date', 'status', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def validate_employee(self, value):
        if not value:
            raise serializers.ValidationError("Employee is required.")
        if not Employee.objects.filter(id=value.id).exists():
            raise serializers.ValidationError("Employee does not exist.")
        return value
    
    def validate_date(self, value):
        if not value:
            raise serializers.ValidationError("Date is required.")
        return value
    
    def validate_status(self, value):
        if value not in ['Present', 'Absent']:
            raise serializers.ValidationError("Status must be either 'Present' or 'Absent'.")
        return value
    
    def validate(self, data):
        if self.instance is None:
            employee = data.get('employee')
            date = data.get('date')
            if Attendance.objects.filter(employee=employee, date=date).exists():
                raise serializers.ValidationError("Attendance for this employee on this date already exists.")
        return data