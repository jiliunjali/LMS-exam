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
from .views.courseview import (
    ActiveCourseListDisplayView,
    AllCourseListDisplayView,
    RegisterCoursesOnCostumerListDisplayView,
    UnRegisteredCoursesOnCostumerListDisplayView,
    EnrolledCoursesListDisplayView,
    CourseInstanceDetailDisplayView,
    SingleCourseStructureListDisplayView,
    ReadingMaterialInstanceDisplayView,
    VideoInstanceDisplayView,
    QuizInstanceDisplayView,
)

urlpatterns = [
    path('courses/', CourseListView.as_view(), name='courses-list'),
    path('customers/', CostumerListView.as_view(), name='customers-list'),
    path('client-admin-courses/', ClientAdminCourseListView.as_view(), name='client-admin-courses-list'),
    path('client-admin-employees/', ClientAdminEmployeeListView.as_view(), name='client-admin-employees-list'),
    path('enrollments/assign/', AssignCourseEnrollmentView.as_view(), name='assign-course-enrollment'),
    path('enrollments/unassign/', UnAssignCourseEnrollmentView.as_view(), name='unassign-course-enrollment'),
    path('enrollments/', CourseEnrollmentDisplayView.as_view(), name='enrollments-list'),
    
    #courseview.py  views url
    path('courses/', AllCourseListDisplayView.as_view(), name='courses-list'),
    path('courses/active/', ActiveCourseListDisplayView.as_view(), name='active-courses-list'),
    path('courses/registered/', RegisterCoursesOnCostumerListDisplayView.as_view(), name='registered-courses-list'),
    path('courses/unregistered/', UnRegisteredCoursesOnCostumerListDisplayView.as_view(), name='un-registered-courses-list'),
    path('courses/enrolled/', EnrolledCoursesListDisplayView.as_view(), name='enrolled-courses-list'),
    path('course/<int:course_id>/', CourseInstanceDetailDisplayView.as_view(), name='course'),
    path('course-structure/<int:course_id>/', SingleCourseStructureListDisplayView.as_view(), name='course-structure'),
    path('course/<int:course_id>/reading/<int : content_id>', ReadingMaterialInstanceDisplayView.as_view(), name='course-reading-material-instance'),
    path('course/<int:course_id>/video/<int : content_id>', VideoInstanceDisplayView.as_view(), name='course-video-instance'),
    path('course/<int:course_id>/quiz/<int : content_id>', QuizInstanceDisplayView.as_view(), name='course-quiz-instance'),



    
    
    
]
