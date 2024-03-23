from django.contrib import admin
from django.urls import path
# from .views import (
#     CourseListView, 
#     ClientAdminCourseListView,
#     CostumerListView,
#     ClientAdminEmployeeListView,
#     # AssignCourseEnrollmentView,
#     # UnAssignCourseEnrollmentView,
#     CourseEnrollmentDisplayView,
#     )
from .views.courseviews import (
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
from .views.registercourseviews import (
    FirstVersionActiveCourseListView,
    DerivedVersionActiveCourseListView,
    LMSCustomerListView,
    CreateCourseRegisterRecordView,
    DisplayCourseRegisterRecordView,
    DeleteCourseRegisterRecordView
)
from .views.enrollcourseviews import (
    RegisteredCourseListView,
    UserListForEnrollment,
    CreateCourseEnrollmentView,
    DisplayCourseEnrollmentView,
    UnAssignCourseEnrollmentView,
    AssignCourseEnrollmentView
)
from .views.createcourseviews import (
    CreateCourseView,
    CreateReadingMaterialView,
    CreateVideoView,
    CreateQuizView,
    CreateCourseStructureForCourseView,
    CreateQuestionView,
    CreateChoiceView,
    ActivateCourseView,
    InActivateCourseView,
    CreateNewVersionCourseView
)
from .views.editcourseviews import (
    EditCourseInstanceDetailsView,
    EditReadingMaterialView,
    EditVideoMaterialView,
    EditQuizDetailView,
    EditExistingQuestionDetailsView,
    EditQuestionChoicesView
)

urlpatterns = [
    # path('courses/', CourseListView.as_view(), name='courses-list'),
    # path('customers/', CostumerListView.as_view(), name='customers-list'),
    # path('client-admin-courses/', ClientAdminCourseListView.as_view(), name='client-admin-courses-list'),
    # path('client-admin-employees/', ClientAdminEmployeeListView.as_view(), name='client-admin-employees-list'),
    # path('enrollments/', CourseEnrollmentDisplayView.as_view(), name='enrollments-list'),
    
    #courseview.py  views url
    path('courses/', AllCourseListDisplayView.as_view(), name='courses-list'),
    path('courses/active/', ActiveCourseListDisplayView.as_view(), name='active-courses-list'),
    path('courses/registered/', RegisterCoursesOnCostumerListDisplayView.as_view(), name='registered-courses-list'),
    path('courses/unregistered/', UnRegisteredCoursesOnCostumerListDisplayView.as_view(), name='un-registered-courses-list'),
    path('courses/enrolled/', EnrolledCoursesListDisplayView.as_view(), name='enrolled-courses-list'),
    path('course/<int:course_id>/', CourseInstanceDetailDisplayView.as_view(), name='course'),
    path('course-structure/<int:course_id>/', SingleCourseStructureListDisplayView.as_view(), name='course-structure'),
    path('course/<int:course_id>/reading/<int:content_id>', ReadingMaterialInstanceDisplayView.as_view(), name='course-reading-material-instance'),
    path('course/<int:course_id>/video/<int:content_id>', VideoInstanceDisplayView.as_view(), name='course-video-instance'),
    path('course/<int:course_id>/quiz/<int:content_id>', QuizInstanceDisplayView.as_view(), name='course-quiz-instance'),
    
    
    #registercourseviews.py views url
    path('courses/active/v1/', FirstVersionActiveCourseListView.as_view(), name='active-first-version-courses-list'),
    path('courses/derived-active/<int:course_id>/', DerivedVersionActiveCourseListView.as_view(), name='active-derived-version-course-list'),
    path('lms-customer/', LMSCustomerListView.as_view(), name='lms-customer-list'),
    path('create/course-register-record/', CreateCourseRegisterRecordView.as_view(), name='create-course-register-record'),
    path('display/course-register-record/', DisplayCourseRegisterRecordView.as_view(), name='course-register-record-list'),
    path('delete/course-register-record/', DeleteCourseRegisterRecordView.as_view(), name='delete-course-register-record-list'),

    
    #enrollcourseviews.py views url
    path('display/registered-course/', RegisteredCourseListView.as_view(), name='register-course-list'),
    path('display/users/', UserListForEnrollment.as_view(), name='users-list'),
    path('create/course-enrollments/', CreateCourseEnrollmentView.as_view(), name='create-course-enrollments-record'),
    path('display/course-enrollments/', DisplayCourseEnrollmentView.as_view(), name='course-enrollments-list'),
    path('enrollments/unassign/', UnAssignCourseEnrollmentView.as_view(), name='unassign-course-enrollment'),
    path('enrollments/assign/', AssignCourseEnrollmentView.as_view(), name='assign-course-enrollment'),
    
    #createcourseview.py views url
    path('create/course/v1/', CreateCourseView.as_view(), name='create-course-v1'),
    path('create/course/<int:course_id>/reading-material/', CreateReadingMaterialView.as_view(), name='create-course-reading-material'),
    path('create/course/<int:course_id>/video/', CreateVideoView.as_view(), name='create-course-video'),
    path('create/course/<int:course_id>/quiz/', CreateQuizView.as_view(), name='create-course-quiz'),
    path('create/course/<int:course_id>/course-structure/', CreateCourseStructureForCourseView.as_view(), name='create-course-structure'),
    path('create/<int:course_id>/quiz/<int:quiz_id>/question/', CreateQuestionView.as_view(), name='create-quiz-question'),
    path('create/question/<int:question_id>/choices/', CreateChoiceView.as_view(), name='create-question-choice'),
    path('active/course/<int:course_id>/', ActivateCourseView.as_view(), name='activate-course'),
    path('inactive/course/<int:course_id>/', InActivateCourseView.as_view(), name='inactivate-course'),
    path('create/course/<int:course_id>/versions/', CreateNewVersionCourseView.as_view(), name='create-course-v1'),

    
    #editcourseviews.py views url
    
    

    
    



    
    
    
]
