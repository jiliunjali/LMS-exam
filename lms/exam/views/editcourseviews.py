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
                                                    update updated at too
                not null[means this is a derived course]:
                            check if course is active or not ?
                                            if active:
                                                    not allowed
                                            inactive:
                                                    ask if we want change to be reflected in others too, like earlier versions?
                                                                            if yes:
                                                                                    edit the same instance of reading material.
                                                                                    update updated at too
                                                                            if not:
                                                                                    check if editing have happened using validate of serializer?
                                                                                                if yes :
                                                                                                        open the edit reding content form with data of readingmaterial id in url, but on save
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
                                                                                                        open the edit video form with data of video_id in url, but on save
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
                                                                                                        open the edit quiz form with data of quiz_id in url, but on save
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

class EditExistingQuestionDetailsView(APIView):
    """
        view to edit the instance of question inside quiz
        triggers with POST request.
        in URL : course_id and quiz_id, question_id in which we are inputting the content will be passed
        
            check if course.original_course of course in url ?
                            if null :
                                        check if course is active or not ?
                                                        if active:
                                                                not allowed
                                                        inactive:
                                                                allow, means question should be editable for the quiz as it was create with this quiz only 
                            not null[means this is a derived course]:
                                        check if course is active or not ?
                                                        if active:
                                                                not allowed
                                                        inactive:
                                                                ask if we want change to be reflected in others too, like earlier versions?
                                                                                        if yes:
                                                                                                edit the same instance of question.
                                                                                        if not:
                                                                                               '''
                                                                                                TODO: to be done some other time , for now : not allowed.
                                                                                               check if request body is empty or not?
                                                                                                            if not empty :
                                                                                                                    create new instance of quiz in quiz table.
                                                                                                                                        want to keep questions of quiz in url in this one too?
                                                                                                                                            yes:
                                                                                                                                                map all questions with new instance of quiz that is created , which where mapped with quiz id in url except for question in url.
                                                                                                                                                copy the content of question in url, and make new instance

                                                                                                                                                for new quiz instance created quiz in quiz table for all relations quiz in url had with questions in manytomany relation copy them for it, using createquestionview for new instance of quizID
                                                                                                                                                create new instance of question in request body.
                                                                                                                                            no:
                                                                                                                                                then just make new instance of question in question tale and make relation of it with quiz.
                                                                                                                    and pass id of this instance to replace where instance was written in course_structure table for course in url
                                                                                                            if yes :
                                                                                                                    do nothing and return the earlier instance only.'''
                    
        while creating instance :
                    quiz = from url
                    figure = request body
                    content = request body
                    explanation = request body
                    choice_order = request body
                    active = false by default
    """
    pass

class EditQuestionChoicesView(APIView):
    """
    view to update content - reading material
    
    in url : question_id
    
    table : Course, Choices, CourseStructure
    
    check if course.original_course of course in url ?
                if null :
                            check if course is active or not ?
                                            if active:
                                                    not allowed
                                            inactive:
                                                    means choice is created along with course , so let it be edited.
                                                    update updated at too
                not null[means this is a derived course]:
                            not allowed
    in request:
                title, reading_content
            on updating update_at = now()
    """
    pass