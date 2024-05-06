from django.db import models
from django.core import serializers

# Create your models here.
class Student(models.Model):
    username = models.CharField(max_length=100, unique=True)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    password = models.CharField(max_length=100)

    def __str__(self) -> str:
        return f"name:{self.name}"

class Course(models.Model):
    name = models.CharField(max_length=100, unique=True)
    duration = models.IntegerField()
    students = models.ManyToManyField(Student, through='Student_Course')
    def __str__(self) -> str:
        return f"name:{self.name}"

class Student_Course(models.Model):
    student_id = models.ForeignKey(Student, on_delete=models.CASCADE)
    course_id = models.ForeignKey(Course, on_delete=models.CASCADE)
    def __str__(self) -> str:
        return super().__str__()