from django.db import models
from django.core import serializers

# Create your models here.
class Student(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    password = models.CharField(max_length=100)

    def __str__(self) -> str:
        return f"name:{self.name}"

class Course(models.Model):
    name = models.CharField(max_length=100)
    duration = models.IntegerField()
    def __str__(self) -> str:
        return f"name:{self.name}"

class Student_Course(models.Model):
    student_id = models.ForeignKey(Student, on_delete=models.CASCADE)
    course_id = models.ForeignKey(Course, on_delete=models.CASCADE)
    def __str__(self) -> str:
        return super().__str__()