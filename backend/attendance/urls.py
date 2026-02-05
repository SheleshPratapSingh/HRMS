from django.urls import path
from . import views

urlpatterns = [
    path('', views.attendance_create, name='attendance-create'),
    path('<int:employee_id>/', views.attendance_by_employee, name='attendance-by-employee'),
    path('stats/', views.dashboard_stats, name='dashboard-stats'),
]