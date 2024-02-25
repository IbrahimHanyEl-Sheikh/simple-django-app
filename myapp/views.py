from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseNotAllowed, Http404
from .models import Student, Course, Student_Course
from django.views.decorators.csrf import csrf_exempt, ensure_csrf_cookie
import json
from django.core import serializers
from django.contrib.auth import get_user_model
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.hashers import make_password


# Create your views here.

# def home(request):
#     return HttpResponse('<h1>Blog Home</h1>')
User = get_user_model()

def home(request):
    return render(request, 'home.html')

def home_id(request, id):
    st = Student.objects.get(id=id)
    return render(request, 'home_with_ids.html', {'student': st})

@csrf_exempt
def get_update_delete_course_by_id(request, id):
    if request.method == 'GET':
        return get_course_by_id(id)
    elif request.method == 'PUT':
        return update_course_by_id(id, json.loads(request.body.decode('utf-8')))
    elif request.method == 'DELETE':
        return delete_course_by_id(id)
    else:
        raise HttpResponseNotAllowed("Method is not supported")

def get_course_by_id(course_id):
    try:
        query_set = Course.objects.filter(pk=course_id)
    except Course.DoesNotExist:
        raise Http404("Course does not exist")
    data = serializers.serialize("json", query_set)
    return HttpResponse(data)

def update_course_by_id(course_id, new_course_data):
    new_name = new_course_data.get("name")
    new_duration = new_course_data.get("duration")
    try:
        course = Course.objects.get(pk=course_id)
    except Course.DoesNotExist:
        raise Http404("Course does not exist")
    course.name = new_name
    course.duration = new_duration
    course.save()
    return HttpResponse("update Course successfully",status=200)
    
def delete_course_by_id(course_id):
    try:
        course = Course.objects.get(pk=course_id)
    except Course.DoesNotExist:
        raise Http404("Course does not exist")
    course.delete()
    return HttpResponse("deleted Course successfully",status=200)

@csrf_exempt
def get_update_delete_student_by_id(request, id):
    if request.method == 'GET':
        return get_student_by_id(id)
    elif request.method == 'PUT':
        return update_student_by_id(id, json.loads(request.body.decode('utf-8')))
    elif request.method == 'DELETE':
        return delete_student_by_id(id)
    else:
        raise HttpResponseNotAllowed("Method is not supported")

def get_student_by_id(student_id):
    try:
        query_set = Student.objects.filter(pk=student_id)
    except Course.DoesNotExist:
        raise Http404("Student does not exist")
    data = serializers.serialize("json", query_set)
    return HttpResponse(data)

def update_student_by_id(student_id, new_student_data):
    try:
        student = Student.objects.get(pk=student_id)
    except Student.DoesNotExist:
        raise Http404("Student does not exist")
    new_name = new_student_data.get("name")
    new_email = new_student_data.get("email")
    new_phone = new_student_data.get("phone")
    new_address = new_student_data.get("address")
    new_city = new_student_data.get("city")
    student.name = new_name
    student.email = new_email
    student.phone = new_phone
    student.address = new_address
    student.city = new_city
    student.save()
    return HttpResponse("update Student successfully",status=200)

def delete_student_by_id(student_id):
    try:
        student = Student.objects.get(pk=student_id)
    except Student.DoesNotExist:
        raise Http404("Student does not exist")
    student.delete()
    return HttpResponse("deleted Student successfully",status=200)

@csrf_exempt
def get_all_add_student(request):
    print(request.POST)
    if request.method == 'POST':
        body = json.loads(request.body.decode('utf-8'))
        name = body.get('name')
        email = body.get('email')
        phone = body.get('phone')
        address = body.get('address')
        city = body.get('city')
        if not name or not email or not phone or not address or not city:
            return HttpResponseBadRequest(f'Invalid student data name:{request.POST}')
        student = Student(name=name, email=email, phone=phone, address=address, city=city)
        student.save()
        return HttpResponse('Add Student successfully')
    elif request.method == 'GET':
        Students = Student.objects.all()
        data = serializers.serialize("json", Students)
        return HttpResponse(data, content_type='application/json')
    else:
        return HttpResponseBadRequest('Invalid student data')

@csrf_exempt
def get_all_add_course(request):
    if request.method == 'POST':
        body = json.loads(request.body.decode('utf-8'))
        name = body.get('name')
        duration = body.get('duration')
        course = Course(name=name, duration=duration)
        course.save()
        return HttpResponse('Add Course successfully')
    elif request.method == 'GET':
        Courses = Course.objects.all()
        data = serializers.serialize("json", Courses)
        return HttpResponse(data, content_type='application/json')
    else:
        return HttpResponseBadRequest('Invalid Course data')

@csrf_exempt
def get_all_add_student_course(request):
    if request.method == 'POST':
        body = json.loads(request.body.decode('utf-8'))
        student_id = body.get('student_id')
        course_id = body.get('course_id')
        course = Student_Course(student_id=Student.objects.get(pk=student_id), course_id=Course.objects.get(pk=course_id))
        course.save()
        return HttpResponse('Enrolled Student to Course successfully')
    elif request.method == 'GET':
        Courses = Student_Course.objects.all()
        data = serializers.serialize("json", Courses)
        return HttpResponse(data, content_type='application/json')
    else:
        return HttpResponseBadRequest('Invalid Course data')

@csrf_exempt
def get_courses_by_student(request):
    if request.method == 'GET':
        student_id = request.GET.get('student_id')
        course_ids = Student_Course.objects.filter(student_id=student_id).values_list('course_id', flat=True)
        Courses = Course.objects.filter(id__in=course_ids)
        data = serializers.serialize("json", Courses)
        return HttpResponse(data, content_type='application/json')
    else:
        return HttpResponseBadRequest('Invalid Request')

@csrf_exempt
def get_students_by_course(request):
    if request.method == 'GET':
        course_id = request.GET.get('course_id')
        student_ids = Student_Course.objects.filter(course_id=course_id).values_list('student_id', flat=True)
        student = Student.objects.filter(id__in=student_ids)
        data = serializers.serialize("json", student)
        return HttpResponse(data, content_type='application/json')
    else:
        return HttpResponseBadRequest('Invalid Request')
@csrf_exempt
def drop_course_for_student(request):
    if request.method == 'DELETE':
        student_id = request.GET.get('student_id')
        course_id = request.GET.get('course_id')
        student_course = Student_Course.objects.filter(course_id=course_id, student_id=student_id)
        student_course.delete()
        return HttpResponse("Unenrolled Student successfully",status=200)
    else:
        return HttpResponseBadRequest('Invalid Request')
@csrf_exempt
def user_login(request):
    data = json.loads(request.body.decode('utf-8'))
    if request.method == 'POST':
        username = data['username']
        password = data['password']
        user = User.objects.filter(username=username, password=password)

        if user is not None:
            return  HttpResponse("Login successful",status=200)
        else :
            return HttpResponse("Login failed",status=400)
    return HttpResponseBadRequest('Invalid Request')
@csrf_exempt
def register(request):
    data = json.loads(request.body.decode('utf-8'))
    if request.method == 'POST':
        user = User(
        username=data['username'],
        email=data['email'],
        password=(data['password']), 
        )
        user.save()
        return HttpResponse("Register successful",status=200)
    return HttpResponseBadRequest('Invalid Request')