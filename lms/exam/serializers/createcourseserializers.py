from rest_framework import serializers
from exam.models.allmodels import Course, CourseStructure, UploadReadingMaterial, UploadVideo, Quiz

class CreateCourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ['title', 'summary']
        
class CreateUploadReadingMaterialSerializer(serializers.ModelSerializer):
    class Meta:
        model = UploadReadingMaterial
        fields = ['title', 'reading_content']
        
class CreateUploadVideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = UploadVideo
        fields = ['title', 'video', 'summary']
        
class CreateQuizSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quiz
        fields = ['title', 'random_order', 'answers_at_end', 'exam_paper', 'pass_mark']

class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = '__all__'

class CourseStructureSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseStructure
        fields = '__all__'

class UploadReadingMaterialSerializer(serializers.ModelSerializer):
    class Meta:
        model = UploadReadingMaterial
        fields = '__all__'

class UploadVideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = UploadVideo
        fields = '__all__'

class QuizSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quiz
        fields = '__all__'
