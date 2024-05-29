from rest_framework import serializers as serial
from .models import *

class StudentSerializer(serial.ModelSerializer):
    class Meta:
        model = Student
        fields = ['name','email','password']
class CourseSerializer(serial.ModelSerializer):
    class Meta:
        model = Course
        fields = ['name','duration']
