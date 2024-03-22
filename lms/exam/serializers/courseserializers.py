from rest_framework import serializers
from exam.models.allmodels import Course
from exam.models.coremodels import *



class CourseDisplaySerializer(serializers.ModelSerializer):
    """
    Serializer for Course model.
    """
    original_course = serializers.CharField(source='original_course.title', read_only=True)
    updated_at = serializers.SerializerMethodField()
    created_at = serializers.SerializerMethodField()

    def get_created_at(self, obj):
        return obj.created_at.strftime("%Y-%m-%d")
    
    def get_updated_at(self, obj):
        return obj.created_at.strftime("%Y-%m-%d")
    
    class Meta:
        model = Course
        fields = ['id', 'slug', 'title', 'created_at', 'updated_at', 'active', 'original_course', 'version_number']
        
class ClientAdminRegisteredCourseDisplaySerializer(serializers.ModelSerializer):
    original_course = serializers.CharField(source='original_course.title', read_only=True)
    updated_at = serializers.SerializerMethodField()
    
    def get_updated_at(self, obj):
        return obj.created_at.strftime("%Y-%m-%d")
    
    class Meta:
        model = Course
        fields = ['id', 'title', 'updated_at', 'original_course', 'version_number']
