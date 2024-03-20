from django.shortcuts import render
from rest_framework import status

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
)
from exam.serializers import (
    CostumerDisplaySerializer,
    CourseDisplaySerializer,
)

class AllCourseListDisplayView(APIView):
    """
        view to display all of the courses from course table irrespective of active status
        triggers with GET request
        should be allowed for only [super admin].
        
        table : Course
        
        what will be displayed:
                    slug
                    title
                    created_at
                    updated_at
                    active
                    original_course 
                    version_number
    """
    pass

class ActiveCourseListDisplayView(APIView):
    """
        view to display [active] courses list from course table 
        trigger with GET request
        should be allowed for only [super admin].
        
        table : Course
        
        what will be displayed:
                    title 
                    updated_at
                    original_course [title to be extracted on frontend]
                    version_number
    """
    pass

class RegisterCoursesOnCostumerListDisplayView(APIView):
    """
        view to display courses that are registered for that customer, whose's id is owned by user in request.
        trigger with GET request
        should be allowed for only [client-admin / Employer].
        
        table : CourseRegisterRecord, Courses
        
        what will be displayed:
                    title
                    updated_at # to see how old is this course
                    original_course [title to be extracted on frontend]
                    version_number
    """
    '''
    how will we do it ?
            first extract user from request and then extract it's customer id
            filter CourseRegisterRecord with that customer id
            make list of courses that are filtered 
            get the instances of Courses whose id is in list.
    '''
    pass

class UnRegisteredCoursesOnCostumerListDisplayView(APIView):
    """
        view to display courses that are unregistered for that customer, whose's id is owned by user in request.
        trigger with GET request
        should be allowed for only [client-admin / Employer].
        
        table : CourseRegisterRecord, Courses
        
        what will be displayed:
                    title
                    updated_at # to see how old is this course
                    original_course [title to be extracted on frontend]
                    version_number
    """
    '''
    how will we do it ?
            first extract user from request and then extract it's customer id
            filter CourseRegisterRecord with that customer id
            make list of courses that are filtered 
            get the instances of Courses whose id is not in list.
    '''
    pass

class EnrolledCoursesListDisplayView(APIView):
    """
        view to display courses that user in request is enrolled on.
        trigger with GET request
        should be allowed for [Employee / client].
        
        table : CourseEnrollment, Courses
        
        what will be displayed :
                    title
    """
    '''
    how will we do it ?
            first extract user from request and then extract it's id /pk
            filter CourseEnrollment with that user id
            make list of courses that are filtered 
            get the instances of Courses whose id is in list.
    '''
    pass

class CourseInstanceDetailDisplayView(APIView):
    """
        view to display the instance of selected course.
        trigger with GET request.
        should be allowed for all users who have access to lms.
        
        table : Courses
        
        what will be displayed:
                    title,
                    summary,
                    updated_at,
                    original_course [title to be extracted on frontend],
                    version_number
    """
    pass

class SingleCourseStructureListDisplayView(APIView):
    """
        view will be used to display the list of instances of course structure table, whose course id is in url.
        trigger with GET request.
        should be allowed for all users who have access to lms.
        
        in URL : course_id
        
        table : CourseStructure
        
        what will be displayed:
                    order_number,
                    content_type,
                    content_id,
    """
    pass

class ReadingMaterialInstanceDisplayView(APIView):
    """
        view will be used to display the instance of reading material which is selected, of selected course.
        trigger with GET request.
        should be allowed to all users who have access to it and lms.
        
        in URL : course_id, content_id (passed through course structure that will be displayed first)
        
        table : UploadReadingMaterial
        
        what will be displayed:
                    title,
                    reading_content
    """
    pass

class VideoInstanceDisplayView(APIView):
    """
        view will be used to display the instance of video which is selected, of selected course.
        trigger with GET request.
        should be allowed to all users who have access to it and lms.
        
        in URL : course_id, content_id (passed through course structure that will be displayed first)
        
        table : UploadVideo
        
        what will be displayed:
                    title,
                    video,
                    summary
    """
    pass

class QuizInstanceDisplayView(APIView):
    """
        view will be used to display the instance of quiz which is selected if they are active , of selected course.
        trigger with GET request.
        should be allowed to all users who have access to it and lms.
        
        in URL : course_id, content_id (passed through course structure that will be displayed first)
        
        table : Quiz
        
        what will be displayed:
                    title,
                    description
    """
    pass

# now sitting function will come that will start the quiz and display it's related questions and choices, and update quiz attempt history table for the user in request.