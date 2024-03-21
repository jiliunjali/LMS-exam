from django.shortcuts import get_object_or_404, render
from rest_framework import status
from django.contrib import messages
from django.db import transaction
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics
from exam.models import (
    # User,
    Course,
    Customer,
    CourseRegisterRecord,
    CourseEnrollment,
    Progress,
    Quiz,
    Question,
    QuizAttemptHistory
)
from exam.serializers import (
    CostumerDisplaySerializer,
    CourseDisplaySerializer,
)
from django.views.generic import (
    DetailView,
    ListView,
    TemplateView,
    FormView,
    CreateView,
    FormView,
    UpdateView,
)
from exam.forms import (
    QuestionForm,
)
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404, render, redirect
from django.utils.decorators import method_decorator
from exam.models.coremodels import *

# for enrollment feature
# will be displayed to employer/client-admin only

class RegisteredCourseListView(APIView):
    """
    view to display data about list of courses on which customer is registered to use.
    trigger with GET request
    should be allowed for only [Employer].
    
    table : Course, CourseRegisterRecord
    what will be displayed:
                    list course.id, course.title [course_id to be retrieved from CourseRegisterRecord]
    """
    '''
        what will happen:
                    user will be extracted from request
                    user's customer_id will be retrieved then
                    CourseRegisterRecord will be filtered on the basis of this customer_id
                    and list of course_ids will be made
                    list of course_ids will be used to retrieve the list of course titles associated with it from course table.
    '''
    pass

class UserListForEnrollment(APIView):
    """
    view to display data about list of user which have customer id same as that of user in request.
    trigger with GET request
    should be allowed for only [Employer].
    
    table : User
    what will be displayed:
                    id, first_name, last_name, status
                    
    """
    '''
        what will happen:
                    user will be extracted from request
                    user's customer_id will be retrieved then
                    CourseRegisterRecord will be filtered on the basis of this customer_id
                    and list of course_ids will be made
                    list of course_ids will be used to retrieve the list of course titles associated with it from course table.
    '''
    pass

class CreateCourseEnrollmentView(APIView):
    """
        view to create instances in CourseEnrollment.
        trigger with POST request
        should be allowed for only [Employer].
        
        table : CourseEnrollment
        
        in request body :
                        list of course_id =[..., ..., ..., ...]
                        list of user_id =[..., ..., ..., ...]
        in response body :
                        each course in list will be mapped for all users in list inside CourseEnrollment table
                        by default active will be true
    """
    pass

class DisplayCourseEnrollmentView(APIView):
    """
        view to display all instances of CourseEnrollment Table.
        trigger with GET request
        
        table : CourseEnrollment, User , Course
        
        what will be displayed:
                    id
                    course.title,
                    user.first_name,
                    user.last_name,
                    enrolled_at,
                    active
    """
    pass

class UnAssignCourseEnrollmentView(APIView):
    """
    this API is used to unassign course to specified user(s) by turning the active false , and hide visibility of course to user(s).
    required inputs : list of ids of instance of course enrollment table
    
    Method: POST
    Parameters:
        - enrollment_ids (list of integers): IDs of course enrollment instances to unassign.
    
    It is triggered with POST request.
    
    """
    def post(self,request, *args, **kwargs):
        pass
    
class AssignCourseEnrollmentView(APIView):
    """
    this API is used to assign course to specified user(s) for all users in courseenrollment table who have active false
    in request body : list of ids of instance of course enrollment table
    
    Method: POST
    Parameters:
        - enrollment_ids (list of integers): IDs of course enrollment instances to assign, who have active status false for now
    
    It is triggered with POST request.
    
    """
    def post(self,request, *args, **kwargs):
        pass