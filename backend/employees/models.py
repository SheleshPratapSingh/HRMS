from django.db import models
from django.core.validators import EmailValidator

class Employee(models.Model):
    employee_id = models.CharField(max_length=50, unique=True, db_index=True)
    full_name = models.CharField(max_length=200)
    email = models.EmailField(unique=True, validators=[EmailValidator()])
    department = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'employees'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['employee_id']),
            models.Index(fields=['email']),
        ]
    
    def __str__(self):
        return f"{self.employee_id} - {self.full_name}"