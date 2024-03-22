from rest_framework import serializers
from exam.models.allmodels import Course, CourseRegisterRecord
from exam.models.coremodels import Customer


class FirstVersionActiveCourseListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ['id', 'title', 'updated_at', 'version_number']
        
class DerivedVersionActiveCourseListSerializer(serializers.ModelSerializer):
    original_course = serializers.CharField(source='original_course.title', read_only=True)
    updated_at = serializers.SerializerMethodField()
    
    def get_updated_at(self, obj):
        return obj.created_at.strftime("%Y-%m-%d")
    
    class Meta:
        model = Course
        fields = ['id', 'title', 'updated_at','original_course', 'version_number']

class CourseRegisterRecordSerializer(serializers.ModelSerializer):
    """
    Serializer for creating records in CourseRegisterRecord model.
    """
    class Meta:
        model = CourseRegisterRecord
        fields = '__all__'
    
class DisplayCourseRegisterRecordSerializer(serializers.ModelSerializer):
    """
    Serializer for displaying records in CourseRegisterRecord model.
    """
    customer = serializers.CharField(source='customer.name', read_only=True)
    course = serializers.CharField(source='course.title', read_only=True)
    created_at = serializers.SerializerMethodField()  # Custom method to format created_at

    def get_created_at(self, obj):
        return obj.created_at.strftime("%Y-%m-%d")  # Format the created_at field as date only

    class Meta:
        model = CourseRegisterRecord
        fields = ['id', 'customer', 'course', 'created_at', 'active']
        
class CustomerSerializer(serializers.ModelSerializer):
    """
    Serializer for the Customer model.
    """
    class Meta:
        model = Customer
        fields = ['id', 'name']

