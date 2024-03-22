from django.shortcuts import get_object_or_404, render, redirect
from rest_framework import status
from rest_framework.response import Response
from django.contrib import messages
from django.db import transaction
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics
from django.core.exceptions import PermissionDenied
from django.utils.decorators import method_decorator

from exam.models.coremodels import *
from exam.serializers.registercourseserializers import *
from exam.models.allmodels import (
    Course,
    CourseRegisterRecord,
    CourseEnrollment,
    QuizAttemptHistory
)

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
    Response:
    [
        {
            "id": 1,
            "title": "Python Fundamentals",
            "updated_at": "2024-03-22",
            "version_number": 1
        },
        {
            "id": 2,
            "title": "Python Advanced",
            "updated_at": "2024-03-22",
            "version_number": 1
        }
    ]
    """
    '''
    courses will be filtered for which original_course = null and version_number = 1,
    list of such courses will be made and then displayed.
    '''
    def get(self, request):
        try:
            # Retrieve active courses with original_course null and version_number 1
            courses = Course.objects.filter(original_course__isnull=True, version_number=1, active=True)
            
            # Check if any courses are found
            if not courses:
                return Response({"error": "No active first version courses found."}, status=status.HTTP_404_NOT_FOUND)
            
            # Serialize the queryset
            serializer = FirstVersionActiveCourseListSerializer(courses, many=True)
            
            # Return the serialized data
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

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
                    original_course.name
                    version_number
    Response:
    {
        "id": 1,
        "title": "Python Advanced",
        "updated_at": "2024-03-22",
        "original_course": "Python Fundamentals",
        "version_number": 2
    }
    """
    '''
        for course id in url , filter will be set on original_course and active is true
        list of filtered course will be made which have same original_course value(id) and then listed on the basis of version_number (ascending)
    '''
    def get(self, request, course_id):
        try:
            # Fetch the derived courses with the given original_course ID that are active
            derived_courses = Course.objects.filter(original_course=course_id, active=True).order_by('version_number')
            
            # Check if any courses are found
            if not derived_courses:
                return Response({"error": "No active derived courses found for the provided course ID."}, status=status.HTTP_404_NOT_FOUND)
            
            # Serialize the data
            serializer = DerivedVersionActiveCourseListSerializer(derived_courses, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Course.DoesNotExist:
            return Response({"error": "Course not found."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

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
    def get(self, request, format=None):
        try:
            # Retrieve customers with LMS resource privilege and active status
            customer_ids_with_lms = CustomerResources.objects.filter(resource__resource_name='LMS').values_list('customer_id', flat=True)
            customers = Customer.objects.filter(id__in=customer_ids_with_lms, is_active=True)
            
            # Check if any customers are found
            if not customers:
                return Response({"error": "No customers found with LMS resource privilege and active status."}, status=status.HTTP_404_NOT_FOUND)
            
            # Serialize the queryset
            serializer = CustomerSerializer(customers, many=True)
            
            # Return the serialized data
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

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
                        
Request body :
        {
            "course_id": [1, 2, 3],
            "customer_id": [101, 102, 103]
        }
        
Response body :
        {
            "message": "Course register records created successfully."
            "record": [...]
        }
    """
    authentication_classes = []
    def post(self, request, *args, **kwargs):
        course_ids = request.data.get("course_id", [])
        customer_ids = request.data.get("customer_id", [])
        
        if not course_ids :
            return Response({"error": "Course IDs are missing"}, status=status.HTTP_400_BAD_REQUEST)
        if not customer_ids:
            return Response({"error": "Customer IDs are missing"}, status=status.HTTP_400_BAD_REQUEST)
        
        # List to hold created records
        created_records = []

        try:
            for course_id in course_ids:
                course = Course.objects.get(pk=course_id)
                for customer_id in customer_ids:
                    customer = Customer.objects.get(pk=customer_id)
                    
                    # Check if record already exists
                    if CourseRegisterRecord.objects.filter(course=course_id, customer=customer_id).exists():
                        continue  # Skip creation if the record already exists

                    record_data = {
                        'course': course_id,
                        'customer': customer_id,
                        'active': True
                    }
                    serializer = CourseRegisterRecordSerializer(data=record_data)
                    if serializer.is_valid():
                        record = serializer.save()
                        created_records.append(serializer.data)
                    else:
                        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
            return Response({"message": "Course register records created successfully.", "record": created_records }, status=status.HTTP_201_CREATED)
        except Course.DoesNotExist:
            return Response({"error": "One or more courses not found"}, status=status.HTTP_404_NOT_FOUND)
        except Customer.DoesNotExist:
            return Response({"error": "One or more customers not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

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
    def get(self, request, *args, **kwargs):
        # Retrieve all instances of CourseRegisterRecord from the database
        course_register_records = CourseRegisterRecord.objects.all()
        
        # Serialize the data
        serializer = DisplayCourseRegisterRecordSerializer(course_register_records, many=True)
        
        # Return the serialized data in the response
        return Response(serializer.data)
    
class DeleteCourseRegisterRecordView(APIView):
    """
    view to delete selected instance(s) of CourseRegisterRecord
    
    table : CourseRegisterRecord
    
    allowed to only super-admin.
    
    in request body :
                records : list of CourseRegisterRecord instances will be passed.
    selected instances will be deleted from the courseregistration record table , and hence along with this instance , all instances from course enrollment table , which users have same customer id as that in these records will be deleted too.
    and record of all users in course enrollment table with same customer id will have there record deleted from quizattempthistory , take if there is any.
    """
    def post(self, request, format=None):
        try:
            # Extract list of record IDs from request data
            record_ids = request.data.get("records", [])
            
            # Delete selected instances from CourseRegisterRecord table
            deleted_records_count = CourseRegisterRecord.objects.filter(id__in=record_ids).delete()
            
            # Check if any records were deleted
            if deleted_records_count[0] > 0:
                customer_ids = CourseRegisterRecord.objects.filter(id__in=record_ids).values_list('customer_id', flat=True)
                CourseEnrollment.objects.filter(user__customer__in=customer_ids).delete()
                QuizAttemptHistory.objects.filter(user__customer__in=customer_ids).delete()
                message = f"{deleted_records_count[0]} records deleted successfully."
                return Response({"message": message}, status=status.HTTP_200_OK)
            else:
                return Response({"message": "No records deleted."}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
