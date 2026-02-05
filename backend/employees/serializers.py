from rest_framework import serializers
from .models import Employee
from django.core.validators import EmailValidator
from django.core.exceptions import ValidationError

class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = ['id', 'employee_id', 'full_name', 'email', 'department', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def validate_employee_id(self, value):
        if not value or not value.strip():
            raise serializers.ValidationError("Employee ID is required.")
        return value.strip()
    
    def validate_full_name(self, value):
        if not value or not value.strip():
            raise serializers.ValidationError("Full name is required.")
        return value.strip()
    
    def validate_email(self, value):
        if not value or not value.strip():
            raise serializers.ValidationError("Email is required.")
        value = value.strip().lower()
        validator = EmailValidator()
        try:
            validator(value)
        except ValidationError:
            raise serializers.ValidationError("Enter a valid email address.")
        return value
    
    def validate_department(self, value):
        if not value or not value.strip():
            raise serializers.ValidationError("Department is required.")
        return value.strip()
    
    def validate(self, data):
        if self.instance is None:
            if Employee.objects.filter(employee_id=data.get('employee_id')).exists():
                raise serializers.ValidationError({"employee_id": "Employee with this ID already exists."})            
            if Employee.objects.filter(email=data.get('email')).exists():
                raise serializers.ValidationError({"email": "Employee with this email already exists."})
        return data