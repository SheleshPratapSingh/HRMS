from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Employee
from .serializers import EmployeeSerializer
from django.db import IntegrityError

@api_view(['POST', 'GET'])
def employee_list_create(request):
    if request.method == 'GET':
        employees = Employee.objects.all()
        serializer = EmployeeSerializer(employees, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    elif request.method == 'POST':
        serializer = EmployeeSerializer(data=request.data)
        if serializer.is_valid():
            try:
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            except IntegrityError as e:
                error_msg = str(e)
                if 'employee_id' in error_msg:
                    return Response(
                        {'error': 'Employee with this ID already exists.'},
                        status=status.HTTP_409_CONFLICT
                    )
                elif 'email' in error_msg:
                    return Response(
                        {'error': 'Employee with this email already exists.'},
                        status=status.HTTP_409_CONFLICT
                    )
                return Response(
                    {'error': 'Failed to create employee.'},
                    status=status.HTTP_400_BAD_REQUEST
                )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
def employee_delete(request, pk):
    try:
        employee = Employee.objects.get(pk=pk)
        employee.delete()
        return Response(
            {'message': 'Employee deleted successfully.'},
            status=status.HTTP_200_OK
        )
    except Employee.DoesNotExist:
        return Response(
            {'error': 'Employee not found.'},
            status=status.HTTP_404_NOT_FOUND
        )