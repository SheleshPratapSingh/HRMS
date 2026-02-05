from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Attendance
from .serializers import AttendanceSerializer
from employees.models import Employee
from django.db import IntegrityError
from django.db.models import Count, Q

@api_view(['POST'])
def attendance_create(request):
    serializer = AttendanceSerializer(data=request.data)
    if serializer.is_valid():
        try:
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except IntegrityError:
            return Response(
                {'error': 'Attendance for this employee on this date already exists.'},
                status=status.HTTP_409_CONFLICT
            )
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def attendance_by_employee(request, employee_id):
    try:
        employee = Employee.objects.get(id=employee_id)
    except Employee.DoesNotExist:
        return Response(
            {'error': 'Employee not found.'},
            status=status.HTTP_404_NOT_FOUND
        )
    
    date_filter = request.query_params.get('date')
    
    attendance_records = Attendance.objects.filter(employee=employee)
    
    if date_filter:
        attendance_records = attendance_records.filter(date=date_filter)
    
    total_present = attendance_records.filter(status='Present').count()
    
    serializer = AttendanceSerializer(attendance_records, many=True)
    
    return Response({
        'attendance': serializer.data,
        'total_present_days': total_present
    }, status=status.HTTP_200_OK)

@api_view(['GET'])
def dashboard_stats(request):
    total_employees = Employee.objects.count()
    total_attendance_records = Attendance.objects.count()
    
    today = request.query_params.get('date')
    today_present = 0
    today_absent = 0
    
    if today:
        today_records = Attendance.objects.filter(date=today)
        today_present = today_records.filter(status='Present').count()
        today_absent = today_records.filter(status='Absent').count()
    
    return Response({
        'total_employees': total_employees,
        'total_attendance_records': total_attendance_records,
        'today_present': today_present,
        'today_absent': today_absent
    }, status=status.HTTP_200_OK)