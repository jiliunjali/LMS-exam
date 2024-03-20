from django.contrib import admin
from django.urls import path
from .views import (
    CourseListView, 
    ClientAdminCourseListView,
    CostumerListView,
    ClientAdminEmployeeListView,
    AssignCourseEnrollmentView,
    UnAssignCourseEnrollmentView,
    CourseEnrollmentDisplayView,
    )

urlpatterns = [
    path('courses/', CourseListView.as_view(), name='courses-list'),
    path('customers/', CostumerListView.as_view(), name='customers-list'),
    path('client-admin-courses/', ClientAdminCourseListView.as_view(), name='client-admin-courses-list'),
    path('client-admin-employees/', ClientAdminEmployeeListView.as_view(), name='client-admin-employees-list'),
    path('enrollments/assign/', AssignCourseEnrollmentView.as_view(), name='assign-course-enrollment'),
    path('enrollments/unassign/', UnAssignCourseEnrollmentView.as_view(), name='unassign-course-enrollment'),
    path('enrollments/', CourseEnrollmentDisplayView.as_view(), name='enrollments-list'),
]

# urlpatterns = [
#     path('course-list/', CourseListView.as_view(), name='course_list'),
#     path('costumer-list/', CostumerListView.as_view(), name='costumer-list'),
#     path('client-admin-course-list/', ClientAdminCourseListView.as_view(), name='client_admin_course_list'),
#     path('client-admin-employee-list/', ClientAdminEmployeeListView.as_view(), name='client_admin_employee_list'),
#     path('assign-course-enrollment/', AssignCourseEnrollmentView.as_view(), name='assign_course_enrollment'),
#     path('unassign-course-enrollment/', UnAssignCourseEnrollmentView.as_view(), name='unassign_course_enrollment'),
#     path('enrollment-list/', CourseEnrollmentDisplayView.as_view(), name='enrollment-list'),
# ]