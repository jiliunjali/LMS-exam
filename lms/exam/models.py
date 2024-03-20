from django.db import models
from django.core.validators import FileExtensionValidator
from django.urls import reverse
from django.db.models import Q
from django.db.models.signals import pre_save, post_save, post_delete
from django.dispatch import receiver


import re
import json
from django.db import models
from django.urls import reverse
from django.core.exceptions import ValidationError, ImproperlyConfigured
from django.core.validators import (
    MaxValueValidator,
    validate_comma_separated_integer_list,
)
from django.utils.translation import gettext_lazy as _
from django.utils.timezone import now
from django.conf import settings
from django.db.models.signals import pre_save
from django.db.models import Q
from model_utils.managers import InheritanceManager
from .models import User
from .models import Course
from .utils import unique_slug_generator



# project import
from .utils import *

# Create your models here.
class User(models.Model):
    pass



class Customer(models.Model):
    pass


# -------------------------------------
# -------------------------------------

class ActivityLog(models.Model):
    message = models.TextField()
    created_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"[{self.created_at}]{self.message}"
    
# -------------------------------------
    # course models
# -------------------------------------

class CourseManager(models.Manager):
    def search(self, query=None):
        queryset = self.get_queryset()
        if query is not None:
            or_lookup = (
                Q(title__icontains=query)
                | Q(summary__icontains=query)
                | Q(slug__icontains=query)
            )
            queryset = queryset.filter(
                or_lookup
            ).distinct()  # distinct() is often necessary with Q lookups
        return queryset
    
class Course(models.Model):
    slug = models.SlugField(blank=True, unique=True)
    title = models.CharField(max_length=200, null=True)
    summary = models.TextField(max_length=200, blank=True, null=True)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default= False)
    original_course = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)
    
    objects = CourseManager()

    def __str__(self):
        return "{0} ({1})".format(self.title, self.code)

    # def get_absolute_url(self):
    #     return reverse("course_detail", kwargs={"slug": self.slug})
    
def course_pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)

pre_save.connect(course_pre_save_receiver, sender=Course)

@receiver(post_save, sender=Course)
def log_save(sender, instance, created, **kwargs):
    verb = "created" if created else "updated"
    ActivityLog.objects.create(message=f"The course '{instance}' has been {verb}.")


@receiver(post_delete, sender=Course)
def log_delete(sender, instance, **kwargs):
    ActivityLog.objects.create(message=f"The course '{instance}' has been deleted.")
    
# -------------------------------------
    # course version record models
# -------------------------------------
class CourseVersion(models.Model):
    version_number = models.IntegerField()
    created_at = models.DateTimeField(auto_now=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)

    def __str__(self):
        return f"Version {self.version_number} of {self.course}"
    
    
    
class Section(models.Model):
    TITLE_NAME = [
        ('reading', 'Reading Material'),
        ('video', 'Video'),
        ('quiz', 'Quiz'),
    ]
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    title = models.CharField(max_length=10, choices=TITLE_NAME)
    section_number = models.PositiveBigIntegerField() # need to make logic to keep it unique within each course

    class Meta:
        ordering = ['section_number']
        
class SectionContent(models.Model):
    section = models.ForeignKey(Section, on_delete=models.CASCADE)
    content_type = models.CharField(max_length=10)
    content_id = models.PositiveIntegerField()
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.section.title == 'reading':
            self.content_type = 'reading'
        elif self.section.title == 'video':
            self.content_type = 'video'
        elif self.section.title == 'quiz':
            self.content_type = 'quiz'

    def get_content(self):
        if self.section.title == 'reading':
            return UploadReadingMaterial.objects.get(pk=self.content_id)
        elif self.section.title == 'video':
            return UploadVideo.objects.get(pk=self.content_id)
        elif self.section.title == 'quiz':
            return Quiz.objects.get(pk=self.content_id)
        return None
    
# -------------------------------------
    # course register record models
# -------------------------------------

class CourseRegisterRecord(models.Model):
    customer = models.ForeignKey(Customer, related_name='registered_courses', on_delete=models.CASCADE)
    course = models.ForeignKey(Course, related_name='registered_costumer', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default= True)
    
    def __str__(self):
        return self.customer.name+" - "+self.course.title
    
# -------------------------------------
    # course enrollment models
# -------------------------------------
    
class Course_Enrollment(models.Model):
    user = models.ForeignKey(User, related_name='enrollments', on_delete=models.CASCADE)
    course = models.ForeignKey(Course, related_name='enrolled_courses', on_delete=models.CASCADE)
    enrolled_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now=True) # to ensure that if person's active status i changed after course update , then no signal is send to him about course change
    active = models.BooleanField(default= True)
    
    def __str__(self):
        return self.user.name+"-"+self.course.title

    # def get_absolute_url(self):
    #     return reverse("edit_allocated_course", kwargs={"pk": self.pk})
    
# -------------------------------------
    # upload reading material models
# -------------------------------------
    
class UploadReadingMaterial(models.Model):
    title = models.CharField(max_length=100)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    reading_content =models.TextField()
    # reading_content = models.FileField(
    #     upload_to="course_files/",
    #     help_text="Valid Files: pdf, docx, doc, xls, xlsx, ppt, pptx, zip, rar, 7zip",
    #     validators=[
    #         FileExtensionValidator(
    #             [
    #                 "pdf",
    #                 "docx",
    #                 "doc",
    #                 "xls",
    #                 "xlsx",
    #                 "ppt",
    #                 "pptx",
    #                 "zip",
    #                 "rar",
    #                 "7zip",
    #             ]
    #         )
    #     ],
    # )
    uploaded_at = models.DateTimeField(auto_now=False, auto_now_add=True, null=True) # needed to passed when material is uploaded for better working
    updated_at = models.DateTimeField(auto_now=True, auto_now_add=False, null=True)
    
    def __str__(self):
        return self.title
    
    # def get_extension_short(self):
    #     ext = str(self.file).split(".")
    #     ext = ext[len(ext) - 1]

    #     if ext in ("doc", "docx"):
    #         return "word"
    #     elif ext == "pdf":
    #         return "pdf"
    #     elif ext in ("xls", "xlsx"):
    #         return "excel"
    #     elif ext in ("ppt", "pptx"):
    #         return "powerpoint"
    #     elif ext in ("zip", "rar", "7zip"):
    #         return "archive"
        
        def delete(self, *args, **kwargs):
            self.reading_content.delete()
            super().delete(*args, **kwargs)
            
@receiver(post_save, sender=UploadReadingMaterial)
def log_save(sender, instance, created, **kwargs):
    if created:
        ActivityLog.objects.create(
            message=f"The file '{instance.title}' has been uploaded to the course '{instance.course}'."
        )
    else:
        ActivityLog.objects.create(
            message=f"The file '{instance.title}' of the course '{instance.course}' has been updated."
        )


@receiver(post_delete, sender=UploadReadingMaterial)
def log_delete(sender, instance, **kwargs):
    ActivityLog.objects.create(
        message=f"The file '{instance.title}' of the course '{instance.course}' has been deleted."
    )
    
# TODO: to know how updated_at is updated and how will we will be able to use to update updated at of course
    
# -------------------------------------
    # upload video models
# -------------------------------------
    
class UploadVideo(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField(blank=True, unique=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    video = models.FileField(
        upload_to="course_videos/",
        help_text="Valid video formats: mp4, mkv, wmv, 3gp, f4v, avi, mp3",
        validators=[
            FileExtensionValidator(["mp4", "mkv", "wmv", "3gp", "f4v", "avi", "mp3"])
        ],
    )
    summary = models.TextField(null=True, blank=True)
    uploaded_at = models.DateTimeField(auto_now=False, auto_now_add=True, null=True)
    
    def __str__(self):
        return str(self.title)

    def get_absolute_url(self):
        return reverse(
            "video_single", kwargs={"slug": self.course.slug, "video_slug": self.slug}
        )

    def delete(self, *args, **kwargs):
        self.video.delete()
        super().delete(*args, **kwargs)


def video_pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)


pre_save.connect(video_pre_save_receiver, sender=UploadVideo)

@receiver(post_save, sender=UploadVideo)
def log_save(sender, instance, created, **kwargs):
    if created:
        ActivityLog.objects.create(
            message=f"The video '{instance.title}' has been uploaded to the course {instance.course}."
        )
    else:
        ActivityLog.objects.create(
            message=f"The video '{instance.title}' of the course '{instance.course}' has been updated."
        )


@receiver(post_delete, sender=UploadVideo)
def log_delete(sender, instance, **kwargs):
    ActivityLog.objects.create(
        message=f"The video '{instance.title}' of the course '{instance.course}' has been deleted."
    )
    
    
# -------------------------------------
    # Quiz models
# -------------------------------------


CHOICE_ORDER_OPTIONS = (
    ("content", _("Content")),
    ("random", _("Random")),
    ("none", _("None")),
)

class Quiz(models.Model):
    quizzes = models.ManyToManyField(Question, through='QuizQuestion')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, null=True)
    title = models.CharField(verbose_name=_("Title"), max_length=60, blank=False)
    slug = models.SlugField(blank=True, unique=True)
    description = models.TextField(
        verbose_name=_("Description"),
        blank=True,
        help_text=_("A detailed description of the quiz"),
    )
    
    random_order = models.BooleanField(
        blank=False,
        default=False,
        verbose_name=_("Random Order"),
        help_text=_("Display the questions in a random order or as they are set?"),
    )
    answers_at_end = models.BooleanField(
        blank=False,
        default=False,
        verbose_name=_("Answers at end"),
        help_text=_(
            "Correct answer is NOT shown after question. Answers displayed at the end."
        ),
    )

    exam_paper = models.BooleanField(
        blank=False,
        default=False,
        verbose_name=_("Exam Paper"),
        help_text=_(
            "If yes, the result of each attempt by a user will be stored. Necessary for marking."
        ),
    )
    single_attempt = models.BooleanField(
        blank=False,
        default=False,
        verbose_name=_("Single Attempt"),
        help_text=_("If yes, only one attempt by a user will be permitted."),
    )

    pass_mark = models.SmallIntegerField(
        blank=True,
        default=50,
        verbose_name=_("Pass Mark"),
        validators=[MaxValueValidator(100)],
        help_text=_("Percentage required to pass exam."),
    )
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
    active = models.BooleanField(default=False)
    
    def save(self, force_insert=False, force_update=False, *args, **kwargs):
        if self.single_attempt is True:
            self.exam_paper = True

        if self.pass_mark > 100:
            raise ValidationError("%s is above 100" % self.pass_mark)
        if self.pass_mark < 0:
            raise ValidationError("%s is below 0" % self.pass_mark)

        super(Quiz, self).save(force_insert, force_update, *args, **kwargs)

    class Meta:
        verbose_name = _("Quiz")
        verbose_name_plural = _("Quizzes")

    def __str__(self):
        return self.title

    def get_questions(self):
        return self.question_set.all().select_subclasses()

    @property
    def get_max_score(self):
        return self.get_questions().count()

    def get_absolute_url(self):
        # return reverse('quiz_start_page', kwargs={'pk': self.pk})
        return reverse("quiz_index", kwargs={"slug": self.course.slug})

def quiz_pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)
pre_save.connect(quiz_pre_save_receiver, sender=Quiz)
    
    
class Question(models.Model):
    figure = models.ImageField(                             
        upload_to="uploads/%Y/%m/%d",
        blank=True,
        null=True,
        verbose_name=_("Figure"),
        help_text=_("Add an image for the question if it's necessary."),
    )
    content = models.CharField(
        max_length=1000,
        blank=False,
        help_text=_("Enter the question text that you want displayed"),
        verbose_name=_("Question"),
    )
    explanation = models.TextField(
        max_length=2000,
        blank=True,
        help_text=_("Explanation to be shown after the question has been answered."),
        verbose_name=_("Explanation"),
    )
    choice_order = models.CharField(
        max_length=30,
        null=True,
        blank=True,
        choices=CHOICE_ORDER_OPTIONS,
        help_text=_(
            "The order in which multi choice choice options are displayed to the user"
        ),
        verbose_name=_("Choice Order"),
    )
    active = models.BooleanField(default=False)
    
    class Meta:
        verbose_name = _("Question")
        verbose_name_plural = _("Questions")

    def __str__(self):
        return self.content


class Choice(models.Model):
    question = models.ForeignKey(
        Question, verbose_name=_("Question"), on_delete=models.CASCADE
    )

    choice = models.CharField(
        max_length=1000,
        blank=False,
        help_text=_("Enter the choice text that you want displayed"),
        verbose_name=_("Content"),
    )
    correct = models.BooleanField(
        blank=False,
        default=False,
        help_text=_("Is this a correct answer?"),
        verbose_name=_("Correct"),
    )

    def __str__(self):
        return self.choice

    class Meta:
        verbose_name = _("Choice")
        verbose_name_plural = _("Choices")
        
@receiver(pre_save, sender=Choice)
def update_question_and_quiz_active_status(sender, instance, **kwargs):
    # Check if the associated question's active field is False
    if instance.question.active == False:
        # Set the question's active field to True
        instance.question.active = True
        instance.question.save()

        # Check if there's a quiz associated with the question
        if instance.question.quiz:
            # Check if the quiz's active field is False
            if instance.question.quiz.active == False:
                # Set the quiz's active field to True
                instance.question.quiz.active = True
                instance.question.quiz.save()


class QuizAttemptHistory(models.Model):
    enrolled_user = models.ForeignKey(User, on_delete=models.CASCADE)
    quiz = models.ForeignKey(Quiz, verbose_name=_("Quiz"), on_delete=models.CASCADE)
    course = models.ForeignKey(
        Course, null=True, verbose_name=_("Course"), on_delete=models.CASCADE
    )
    question_list_order = models.CharField(
        max_length=1024,
        verbose_name=_("Question Order"),
        validators=[validate_comma_separated_integer_list],
    )
    unattempted_question = models.CharField(max_length=255)
    incorrect_questions = models.CharField(
        max_length=1024,
        blank=True,
        verbose_name=_("Incorrect questions"),
        validators=[validate_comma_separated_integer_list],
    )
    current_score = models.IntegerField(verbose_name=_("Current Score"))
    complete = models.BooleanField(
        default=False, blank=False, verbose_name=_("Complete")
    )
    user_answers = models.TextField(
        blank=True, default="{}", verbose_name=_("User Answers")
    )
    start = models.DateTimeField(auto_now_add=True, verbose_name=_("Start"))
    end = models.DateTimeField(null=True, blank=True, verbose_name=_("End"))


    class Meta:
        permissions = (("view_sittings", _("Can see completed exams.")),)

    def get_first_question(self):
        if not self.question_list:
            return False

        first, _ = self.question_list.split(",", 1)
        question_id = int(first)
        return Question.objects.get_subclass(id=question_id)

    def remove_first_question(self):
        if not self.question_list:
            return

        _, others = self.question_list.split(",", 1)
        self.question_list = others
        self.save()

    def add_to_score(self, points):
        self.current_score += int(points)
        self.save()

    @property
    def get_current_score(self):
        return self.current_score

    def _question_ids(self):
        return [int(n) for n in self.question_order.split(",") if n]

    @property
    def get_percent_correct(self):
        dividend = float(self.current_score)
        divisor = len(self._question_ids())
        if divisor < 1:
            return 0  # prevent divide by zero error

        if dividend > divisor:
            return 100

        correct = int(round((dividend / divisor) * 100))

        if correct >= 1:
            return correct
        else:
            return 0

    def mark_quiz_complete(self):
        self.complete = True
        self.end = now()
        self.save()

    def add_incorrect_question(self, question):
        if len(self.incorrect_questions) > 0:
            self.incorrect_questions += ","
        self.incorrect_questions += str(question.id) + ","
        if self.complete:
            self.add_to_score(-1)
        self.save()

    @property
    def get_incorrect_questions(self):
        return [int(q) for q in self.incorrect_questions.split(",") if q]

    def remove_incorrect_question(self, question):
        current = self.get_incorrect_questions
        current.remove(question.id)
        self.incorrect_questions = ",".join(map(str, current))
        self.add_to_score(1)
        self.save()

    @property
    def check_if_passed(self):
        return self.get_percent_correct >= self.quiz.pass_mark

    @property
    def result_message(self):
        if self.check_if_passed:
            return f"You have passed this quiz, congratulation"
        else:
            return f"You failed this quiz, give it one chance again."

    def add_user_answer(self, question, guess):
        current = json.loads(self.user_answers)
        current[question.id] = guess
        self.user_answers = json.dumps(current)
        self.save()

    def get_questions(self, with_answers=False):
        question_ids = self._question_ids()
        questions = sorted(
            self.quiz.question_set.filter(id__in=question_ids).select_subclasses(),
            key=lambda q: question_ids.index(q.id),
        )

        if with_answers:
            user_answers = json.loads(self.user_answers)
            for question in questions:
                question.user_answer = user_answers[str(question.id)]

        return questions

    @property
    def questions_with_user_answers(self):
        return {q: q.user_answer for q in self.get_questions(with_answers=True)}

    @property
    def get_max_score(self):
        return len(self._question_ids())

    def progress(self):
        answered = len(json.loads(self.user_answers))
        total = self.get_max_score
        return answered, total

class QuizQuestion(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    # Additional fields specific to the relationship
    active = models.BooleanField(default=True)