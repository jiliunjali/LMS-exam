from rest_framework import serializers
from .models import (
    Course,
    Costumer,
)

class ActiveCourseDisplaySerializer(serializers.ModelSerializer):
    """
    only active courses will be displayed
    """
    class Meta:
        model = Course
        fields = ('title', 'summary', 'created_at', 'updated_at')
        
class CourseDisplaySerializer(serializers.ModelSerializer):
    """
    all courses will be displayed- both active and inactive
    """
    class Meta:
        model = Course
        fields = ('title', 'summary', 'created_at', 'updated_at', 'active')
    
        
class CostumerDisplaySerializer(serializers.ModelSerializer):
    # class Meta:
    #     model = Costumer
    #     fields = ('name')
    pass