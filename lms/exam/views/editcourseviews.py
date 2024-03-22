from django.shortcuts import get_object_or_404, render
from rest_framework import status
from django.contrib import messages
from django.db import transaction
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics
from exam.models.allmodels import (
    Course,
    CourseRegisterRecord,
    CourseEnrollment,
    Progress,
    Quiz,
    Question,
    QuizAttemptHistory
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
# from exam.models.coremodels import *

class EditCourseInstanceDetailsView(APIView):
    """
    view to update course instance details.
    trigger with POST request
    should be allowed for only [super admin].

    table : Course
    
    in url : course_id 
    
    check if course.original_course of course in url ?
                if null :
                            check if course is active or not ?
                                            if active:
                                                    let edit title , summary with warning and updated_at = now()
                                            inactive:
                                                    just let it get edited.
                not null:
                            check if course is active or not ?
                                            if active:
                                                    let edit title , summary with warning and updated_at = now()
                                            inactive:
                                                    just let it get edited.
                                                    
    in request : 
                title , summary
    on validating that change have been made, post will be done else just return, the instance.
    """
    pass

class EditReadingMaterialView(APIView):
    """
    view to update content - reading material
    
    in url : course_id , reading_material_id
    
    table : Course, UploadReadingMaterial, CourseStructure
    
    check if course.original_course of course in url ?
                if null :
                            check if course is active or not ?
                                            if active:
                                                    not allowed
                                            inactive:
                                                    means reading material is created along with course , so let it be edited.
                not null[means this is a derived course]:
                            check if course is active or not ?
                                            if active:
                                                    not allowed
                                            inactive:
                                                    ask if we want change to be reflected in others too, like earlier versions?
                                                                            if yes:
                                                                                    edit the same instance of reading material.
                                                                            if not:
                                                                                    check if editing have happened using validate of serializer?
                                                                                                if yes :
                                                                                                        create new instance with data in request, and might as well use CreateReadingMaterialView for course in url.
                                                                                                        and pass id of this instance to replace where instance was written in course_structure table for course in url
                                                                                                if no :
                                                                                                        do nothing and return the earlier instance only.
    in request:
                title, reading_content
            on updating update_at = now()
    """
    pass

class EditVideoMaterialView(APIView):
    """
    view to update content - reading material
    
    in url : course_id , video_material_id
    
    table : Course, UploadVideo, CourseStructure
    
    check if course.original_course of course in url ?
                if null :
                            check if course is active or not ?
                                            if active:
                                                    not allowed
                                            inactive:
                                                    means video material is created along with course , so let it be edited.
                not null[means this is a derived course]:
                            check if course is active or not ?
                                            if active:
                                                    not allowed
                                            inactive:
                                                    ask if we want change to be reflected in others too, like earlier versions?
                                                                            if yes:
                                                                                    edit the same instance of video material.
                                                                            if not:
                                                                                    check if editing have happened using validate of serializer?
                                                                                                if yes :
                                                                                                        create new instance with data in request, and might as well use CreateVideoView for course in url.
                                                                                                        and pass id of this instance to replace where instance was written in course_structure table for course in url
                                                                                                if no :
                                                                                                        do nothing and return the earlier instance only.
    in request:
                title, video, summary
            on updating update_at = now()
    """
    pass

class EditQuizDetailView(APIView):
    """
    view to update content - reading material
    
    in url : course_id , Quiz_id
    
    table : Course, Quiz, CourseStructure
    
    check if course.original_course of course in url ?
                if null :
                            check if course is active or not ?
                                            if active:
                                                    not allowed
                                            inactive:
                                                    means quiz is created along with course , so let it be edited.
                not null[means this is a derived course]:
                            check if course is active or not ?
                                            if active:
                                                    not allowed
                                            inactive:
                                                    ask if we want change to be reflected in others too, like earlier versions?
                                                                            if yes:
                                                                                    edit the same instance of quiz.
                                                                            if not:
                                                                                    check if editing have happened using validate of serializer?
                                                                                                if yes :
                                                                                                        create new instance with data in request, and might as well use CreateQuestionView for course in url.
                                                                                                        and pass id of this instance to replace where instance was written in course_structure table for course in url
                                                                                                if no :
                                                                                                        do nothing and return the earlier instance only.
    in request:
                title,
                    random_order,
                    answers_at_end,
                    exam_paper,
                    pass_mark,
    on updating update_at = now()
    """
    pass