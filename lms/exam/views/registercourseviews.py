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

'''
courseview.py----
AllCourseListDisplayView
ActiveCourseListDisplayView
'''

class FirstVersionActiveCourseListView(APIView):
    """
        view to display [active] courses list from course table that have original_course = null and version_number = 1
        trigger with GET request
        should be allowed for only [super admin].
                
        table : Course
        
        what will be displayed:
                    id
                    title 
                    updated_at
                    version_number
    """
    '''
    courses will be filtered for which original_course = null and version_number = 1,
    list of such courses will be made and then displayed.
    '''
    pass

class DerivedVersionActiveCourseListView(APIView):
    """
        view to display [active] courses list from course table that have original_course != null and active
        trigger with GET request
        should be allowed for only [super admin].
        
        in URL : course_id
            
        table : Course
        
        what will be displayed:
                    id
                    title 
                    updated_at
                    version_number
    """
    '''
        for course id in url , filter will be set on original_course and active is true
        list of filtered course will be made which have same original_course value(id) and then listed on the basis of version_number (ascending)
    '''
    pass

class LMSCustomerListView(APIView):
    """
        view to display  list of customers who have resource privilege of LMS and are active
        trigger with GET request
        should be allowed for only [super admin].
        
        table : Customer_Resources, Resources , Customer 
        
        what will be displayed:
                    id
                    titles of customer
    """
    pass

class CreateCourseRegisterRecordView(APIView):
    """
        view to create instances in CourseRegisterRecord.
        trigger with POST request
        should be allowed for only [super admin].
        
        table : CourseRegisterRecord
        
        in request body :
                        list of course_id =[..., ..., ..., ...]
                        list of customer_id =[..., ..., ..., ...]
        in response body :
                        each course in list will be mapped for all customers in list inside CourseRegisterRecord table
                        by default active will be true
    """
    pass

class DisplayCourseRegisterRecordView(APIView):
    """
        view to display all instances of CourseRegisterRecord Table.
        trigger with GET request
        
        table : CourseRegisterRecord, Customer , Course
        
        what will be displayed:
                    id
                    customer.title,
                    course.title,
                    created_at,
                    active
    """
    pass

