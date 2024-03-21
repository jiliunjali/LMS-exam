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


class AllCourseListDisplayView(APIView):
    """
        view to display all of the courses from course table irrespective of active status what is in courseversion table
        triggers with GET request
        should be allowed for only [super admin].
        
        table : Course, CourseVersion
        
        what will be displayed:
                    id
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
                    id
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
                    id
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
                    id
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
                    id
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
                    id
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
                    id
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
                    id
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
                    id
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
                    id
                    title,
                    description
    """
    pass

# now sitting function will come that will start the quiz and display it's related questions and choices, and update quiz attempt history table for the user in request.

# @method_decorator([login_required], name="dispatch")
class QuizTake(FormView):
    form_class = QuestionForm
    template_name = "question.html"
    result_template_name = "result.html"
    # single_complete_template_name = 'single_complete.html'

    def dispatch(self, request, *args, **kwargs):
        self.quiz = get_object_or_404(Quiz, pk=self.kwargs["pk"])
        self.course = get_object_or_404(Course, pk=self.kwargs["pk"])
        quizQuestions = Question.objects.filter(quiz=self.quiz).count()
        course = get_object_or_404(Course, pk=self.kwargs["pk"])

        if quizQuestions <= 0:
            messages.warning(request, f"Question set of the quiz is empty. try later!")
            return redirect("quiz_index", self.course.slug)

        if self.quiz.draft and not request.user.has_perm("quiz.change_quiz"):
            raise PermissionDenied

        self.sitting = QuizAttemptHistory.objects.user_sitting(
            request.user, self.quiz, self.course
        )

        if self.sitting is False:
            # return render(request, self.single_complete_template_name)
            messages.info(
                request,
                f"You have already sat this exam and only one sitting is permitted",
            )
            return redirect("quiz_index", self.course.slug)

        return super(QuizTake, self).dispatch(request, *args, **kwargs)

    def get_form(self, *args, **kwargs):
        self.question = self.sitting.get_first_question()
        self.progress = self.sitting.progress()
        form_class = self.form_class

        return form_class(**self.get_form_kwargs())

    def get_form_kwargs(self):
        kwargs = super(QuizTake, self).get_form_kwargs()

        return dict(kwargs, question=self.question)

    def form_valid(self, form):
        self.form_valid_user(form)
        if self.sitting.get_first_question() is False:
            self.sitting.mark_quiz_complete()
            return self.final_result_user()

        self.request.POST = {}

        return super(QuizTake, self).get(self, self.request)

    def get_context_data(self, **kwargs):
        context = super(QuizTake, self).get_context_data(**kwargs)
        context["question"] = self.question
        context["quiz"] = self.quiz
        context["course"] = get_object_or_404(Course, pk=self.kwargs["pk"])
        if hasattr(self, "previous"):
            context["previous"] = self.previous
        if hasattr(self, "progress"):
            context["progress"] = self.progress
        return context

    def form_valid_user(self, form):
        progress, _ = Progress.objects.get_or_create(user=self.request.user)
        guess = form.cleaned_data["answers"]
        is_correct = self.question.check_if_correct(guess)

        if is_correct is True:
            self.sitting.add_to_score(1)
            progress.update_score(self.question, 1, 1)
        else:
            self.sitting.add_incorrect_question(self.question)
            progress.update_score(self.question, 0, 1)

        if self.quiz.answers_at_end is not True:
            self.previous = {
                "previous_answer": guess,
                "previous_outcome": is_correct,
                "previous_question": self.question,
                "answers": self.question.get_choices(),
                "question_type": {self.question.__class__.__name__: True},
            }
        else:
            self.previous = {}

        self.sitting.add_user_answer(self.question, guess)
        self.sitting.remove_first_question()

    def final_result_user(self):
        results = {
            "course": get_object_or_404(Course, pk=self.kwargs["pk"]),
            "quiz": self.quiz,
            "score": self.sitting.get_current_score,
            "max_score": self.sitting.get_max_score,
            "percent": self.sitting.get_percent_correct,
            "sitting": self.sitting,
            "previous": self.previous,
            "course": get_object_or_404(Course, pk=self.kwargs["pk"]),
        }

        self.sitting.mark_quiz_complete()

        if self.quiz.answers_at_end:
            results["questions"] = self.sitting.get_questions(with_answers=True)
            results["incorrect_questions"] = self.sitting.get_incorrect_questions

        if (
            self.quiz.exam_paper is False
            or self.request.user.is_superuser
            or self.request.user.is_lecturer
        ):
            self.sitting.delete()

        return render(self.request, self.result_template_name, results)
