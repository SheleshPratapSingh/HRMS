#!/usr/bin/env python3
"""
HRMS Lite Backend API Testing Suite
Tests all Django REST Framework endpoints for Employee and Attendance management
"""

import requests
import sys
import json
from datetime import datetime, date
from typing import Dict, Any, List, Tuple

class HRMSAPITester:
    def __init__(self, base_url: str = "https://localhost:5432"):
        self.base_url = base_url
        self.tests_run = 0
        self.tests_passed = 0
        self.test_results = []
        self.created_employees = []  # Track created employees for cleanup
        
    def log_test(self, name: str, success: bool, details: str = ""):
        """Log test result"""
        self.tests_run += 1
        if success:
            self.tests_passed += 1
            
        result = {
            "test": name,
            "success": success,
            "details": details,
            "timestamp": datetime.now().isoformat()
        }
        self.test_results.append(result)
        
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} - {name}")
        if details:
            print(f"    Details: {details}")
        print()

    def make_request(self, method: str, endpoint: str, data: Dict = None, params: Dict = None) -> Tuple[bool, Dict, int]:
        """Make HTTP request and return success, response data, status code"""
        url = f"{self.base_url}/api/{endpoint}"
        headers = {'Content-Type': 'application/json'}
        
        try:
            if method == 'GET':
                response = requests.get(url, headers=headers, params=params, timeout=30)
            elif method == 'POST':
                response = requests.post(url, json=data, headers=headers, timeout=30)
            elif method == 'DELETE':
                response = requests.delete(url, headers=headers, timeout=30)
            else:
                return False, {"error": f"Unsupported method: {method}"}, 0
                
            try:
                response_data = response.json()
            except:
                response_data = {"raw_response": response.text}
                
            return response.status_code < 400, response_data, response.status_code
            
        except requests.exceptions.RequestException as e:
            return False, {"error": str(e)}, 0

    def test_employee_list_empty(self):
        """Test GET /api/employees/ when no employees exist"""
        success, data, status = self.make_request('GET', 'employees/')
        
        if success and status == 200:
            self.log_test("Employee List (Empty)", True, f"Status: {status}, Count: {len(data)}")
            return True
        else:
            self.log_test("Employee List (Empty)", False, f"Status: {status}, Error: {data}")
            return False

    def test_employee_create_valid(self):
        """Test POST /api/employees/ with valid data"""
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S%f')[:-3]  # More unique timestamp
        test_employee = {
            "employee_id": f"EMP{timestamp}",
            "full_name": f"John Doe Test {timestamp}",
            "email": f"john.test.{timestamp}@company.com",
            "department": "Engineering"
        }
        
        success, data, status = self.make_request('POST', 'employees/', test_employee)
        
        if success and status == 201:
            self.created_employees.append(data.get('id'))
            self.log_test("Employee Create (Valid)", True, f"Created employee ID: {data.get('id')}")
            return True, data
        else:
            self.log_test("Employee Create (Valid)", False, f"Status: {status}, Error: {data}")
            return False, {}

    def test_employee_create_duplicate_id(self):
        """Test POST /api/employees/ with duplicate employee_id"""
        # First create an employee
        success, employee_data = self.test_employee_create_valid()
        if not success:
            self.log_test("Employee Create (Duplicate ID Setup)", False, "Failed to create initial employee")
            return False
            
        # Try to create another with same employee_id
        duplicate_employee = {
            "employee_id": employee_data.get('employee_id'),
            "full_name": "Jane Doe Test",
            "email": f"jane.test.{datetime.now().strftime('%Y%m%d%H%M%S%f')[:-3]}@company.com",
            "department": "Marketing"
        }
        
        success, data, status = self.make_request('POST', 'employees/', duplicate_employee)
        
        if not success and status in [400, 409]:
            self.log_test("Employee Create (Duplicate ID)", True, f"Correctly rejected duplicate ID with status: {status}")
            return True
        else:
            self.log_test("Employee Create (Duplicate ID)", False, f"Should have rejected duplicate ID. Status: {status}")
            return False

    def test_employee_create_duplicate_email(self):
        """Test POST /api/employees/ with duplicate email"""
        # First create an employee
        success, employee_data = self.test_employee_create_valid()
        if not success:
            self.log_test("Employee Create (Duplicate Email Setup)", False, "Failed to create initial employee")
            return False
            
        # Try to create another with same email
        duplicate_employee = {
            "employee_id": f"EMP{datetime.now().strftime('%Y%m%d%H%M%S%f')[:-3]}_DUP",
            "full_name": "Jane Doe Test",
            "email": employee_data.get('email'),
            "department": "Marketing"
        }
        
        success, data, status = self.make_request('POST', 'employees/', duplicate_employee)
        
        if not success and status in [400, 409]:
            self.log_test("Employee Create (Duplicate Email)", True, f"Correctly rejected duplicate email with status: {status}")
            return True
        else:
            self.log_test("Employee Create (Duplicate Email)", False, f"Should have rejected duplicate email. Status: {status}")
            return False

    def test_employee_create_invalid_email(self):
        """Test POST /api/employees/ with invalid email format"""
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S%f')[:-3]
        invalid_employee = {
            "employee_id": f"EMP{timestamp}_INV",
            "full_name": "Invalid Email Test",
            "email": "invalid-email-format",
            "department": "Testing"
        }
        
        success, data, status = self.make_request('POST', 'employees/', invalid_employee)
        
        if not success and status == 400:
            self.log_test("Employee Create (Invalid Email)", True, f"Correctly rejected invalid email with status: {status}")
            return True
        else:
            self.log_test("Employee Create (Invalid Email)", False, f"Should have rejected invalid email. Status: {status}")
            return False

    def test_employee_list_with_data(self):
        """Test GET /api/employees/ when employees exist"""
        success, data, status = self.make_request('GET', 'employees/')
        
        if success and status == 200 and len(data) > 0:
            self.log_test("Employee List (With Data)", True, f"Status: {status}, Count: {len(data)}")
            return True, data
        else:
            self.log_test("Employee List (With Data)", False, f"Status: {status}, Count: {len(data) if isinstance(data, list) else 0}")
            return False, []

    def test_employee_delete(self):
        """Test DELETE /api/employees/<id>/"""
        # Create an employee first
        success, employee_data = self.test_employee_create_valid()
        if not success:
            self.log_test("Employee Delete (Setup)", False, "Failed to create employee for deletion test")
            return False
            
        employee_id = employee_data.get('id')
        success, data, status = self.make_request('DELETE', f'employees/{employee_id}/')
        
        if success and status == 200:
            # Remove from cleanup list since it's deleted
            if employee_id in self.created_employees:
                self.created_employees.remove(employee_id)
            self.log_test("Employee Delete", True, f"Successfully deleted employee {employee_id}")
            return True
        else:
            self.log_test("Employee Delete", False, f"Status: {status}, Error: {data}")
            return False

    def test_attendance_create_valid(self):
        """Test POST /api/attendance/ with valid data"""
        # Need an employee first
        success, employee_data = self.test_employee_create_valid()
        if not success:
            self.log_test("Attendance Create (Setup)", False, "Failed to create employee for attendance test")
            return False, {}
            
        attendance_data = {
            "employee": employee_data.get('id'),
            "date": date.today().isoformat(),
            "status": "Present"
        }
        
        success, data, status = self.make_request('POST', 'attendance/', attendance_data)
        
        if success and status == 201:
            self.log_test("Attendance Create (Valid)", True, f"Created attendance record ID: {data.get('id')}")
            return True, data
        else:
            self.log_test("Attendance Create (Valid)", False, f"Status: {status}, Error: {data}")
            return False, {}

    def test_attendance_create_duplicate(self):
        """Test POST /api/attendance/ with duplicate employee+date"""
        # Create first attendance record
        success, attendance_data = self.test_attendance_create_valid()
        if not success:
            self.log_test("Attendance Create (Duplicate Setup)", False, "Failed to create initial attendance")
            return False
            
        # Try to create duplicate
        duplicate_attendance = {
            "employee": attendance_data.get('employee'),
            "date": attendance_data.get('date'),
            "status": "Absent"
        }
        
        success, data, status = self.make_request('POST', 'attendance/', duplicate_attendance)
        
        if not success and status in [400, 409]:
            self.log_test("Attendance Create (Duplicate)", True, f"Correctly rejected duplicate attendance with status: {status}")
            return True
        else:
            self.log_test("Attendance Create (Duplicate)", False, f"Should have rejected duplicate attendance. Status: {status}")
            return False

    def test_attendance_by_employee(self):
        """Test GET /api/attendance/<employee_id>/"""
        # Create employee and attendance first
        success, employee_data = self.test_employee_create_valid()
        if not success:
            return False
            
        employee_id = employee_data.get('id')
        
        # Create attendance record
        attendance_data = {
            "employee": employee_id,
            "date": date.today().isoformat(),
            "status": "Present"
        }
        self.make_request('POST', 'attendance/', attendance_data)
        
        # Test getting attendance records
        success, data, status = self.make_request('GET', f'attendance/{employee_id}/')
        
        if success and status == 200 and 'attendance' in data and 'total_present_days' in data:
            self.log_test("Attendance By Employee", True, f"Records: {len(data['attendance'])}, Present days: {data['total_present_days']}")
            return True, data
        else:
            self.log_test("Attendance By Employee", False, f"Status: {status}, Error: {data}")
            return False, {}

    def test_attendance_by_employee_with_date_filter(self):
        """Test GET /api/attendance/<employee_id>/ with date filter"""
        # Get existing employee and attendance
        success, data = self.test_attendance_by_employee()
        if not success:
            return False
            
        # Extract employee ID from attendance data
        if data and data.get('attendance') and len(data['attendance']) > 0:
            employee_id = data['attendance'][0]['employee']
            test_date = data['attendance'][0]['date']
            
            # Test with date filter
            success, filtered_data, status = self.make_request('GET', f'attendance/{employee_id}/', params={'date': test_date})
            
            if success and status == 200:
                self.log_test("Attendance By Employee (Date Filter)", True, f"Filtered records: {len(filtered_data['attendance'])}")
                return True
            else:
                self.log_test("Attendance By Employee (Date Filter)", False, f"Status: {status}")
                return False
        else:
            self.log_test("Attendance By Employee (Date Filter)", False, "No attendance data to filter")
            return False

    def test_dashboard_stats(self):
        """Test GET /api/attendance/stats/"""
        success, data, status = self.make_request('GET', 'attendance/stats/')
        
        expected_fields = ['total_employees', 'total_attendance_records', 'today_present', 'today_absent']
        
        if success and status == 200 and all(field in data for field in expected_fields):
            self.log_test("Dashboard Stats", True, f"Employees: {data['total_employees']}, Records: {data['total_attendance_records']}")
            return True, data
        else:
            self.log_test("Dashboard Stats", False, f"Status: {status}, Missing fields or error: {data}")
            return False, {}

    def test_dashboard_stats_with_date_filter(self):
        """Test GET /api/attendance/stats/ with date filter"""
        test_date = date.today().isoformat()
        success, data, status = self.make_request('GET', 'attendance/stats/', params={'date': test_date})
        
        expected_fields = ['total_employees', 'total_attendance_records', 'today_present', 'today_absent']
        
        if success and status == 200 and all(field in data for field in expected_fields):
            self.log_test("Dashboard Stats (Date Filter)", True, f"Date: {test_date}, Present: {data['today_present']}, Absent: {data['today_absent']}")
            return True
        else:
            self.log_test("Dashboard Stats (Date Filter)", False, f"Status: {status}, Error: {data}")
            return False

    def cleanup_created_employees(self):
        """Clean up employees created during testing"""
        print("\n🧹 Cleaning up test data...")
        for employee_id in self.created_employees:
            try:
                success, _, status = self.make_request('DELETE', f'employees/{employee_id}/')
                if success:
                    print(f"✅ Deleted employee {employee_id}")
                else:
                    print(f"❌ Failed to delete employee {employee_id}")
            except:
                print(f"❌ Error deleting employee {employee_id}")

    def clear_test_data(self):
        """Clear any existing test data"""
        print("🧹 Clearing existing test data...")
        try:
            # Get all employees
            success, employees, status = self.make_request('GET', 'employees/')
            if success and employees:
                for employee in employees:
                    if 'EMP' in employee.get('employee_id', '') and 'test' in employee.get('full_name', '').lower():
                        self.make_request('DELETE', f'employees/{employee["id"]}/')
                        print(f"  Deleted test employee: {employee['employee_id']}")
        except Exception as e:
            print(f"  Warning: Could not clear test data: {e}")

    def run_all_tests(self):
        """Run comprehensive test suite"""
        print("🚀 Starting HRMS Lite Backend API Tests")
        print(f"🌐 Testing against: {self.base_url}")
        print("=" * 60)
        
        # Clear existing test data
        self.clear_test_data()
        
        # Employee Management Tests
        print("\n📋 EMPLOYEE MANAGEMENT TESTS")
        print("-" * 40)
        self.test_employee_list_empty()
        self.test_employee_create_valid()
        self.test_employee_create_duplicate_id()
        self.test_employee_create_duplicate_email()
        self.test_employee_create_invalid_email()
        self.test_employee_list_with_data()
        self.test_employee_delete()
        
        # Attendance Management Tests
        print("\n📅 ATTENDANCE MANAGEMENT TESTS")
        print("-" * 40)
        self.test_attendance_create_valid()
        self.test_attendance_create_duplicate()
        self.test_attendance_by_employee()
        self.test_attendance_by_employee_with_date_filter()
        
        # Dashboard Tests
        print("\n📊 DASHBOARD TESTS")
        print("-" * 40)
        self.test_dashboard_stats()
        self.test_dashboard_stats_with_date_filter()
        
        # Cleanup
        self.cleanup_created_employees()
        
        # Results Summary
        print("\n" + "=" * 60)
        print("📊 TEST RESULTS SUMMARY")
        print("=" * 60)
        print(f"Total Tests: {self.tests_run}")
        print(f"Passed: {self.tests_passed}")
        print(f"Failed: {self.tests_run - self.tests_passed}")
        print(f"Success Rate: {(self.tests_passed/self.tests_run*100):.1f}%")
        
        if self.tests_passed == self.tests_run:
            print("\n🎉 All tests passed!")
            return 0
        else:
            print(f"\n⚠️  {self.tests_run - self.tests_passed} test(s) failed")
            print("\nFailed Tests:")
            for result in self.test_results:
                if not result['success']:
                    print(f"  ❌ {result['test']}: {result['details']}")
            return 1

def main():
    """Main test execution"""
    tester = HRMSAPITester()
    return tester.run_all_tests()

if __name__ == "__main__":
    sys.exit(main())
