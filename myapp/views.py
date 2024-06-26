from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseNotAllowed, Http404,JsonResponse
from .models import Student, Course, Student_Course
from django.views.decorators.csrf import csrf_exempt, ensure_csrf_cookie
import json
from django.core import serializers
from django.contrib.auth import get_user_model
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.hashers import make_password
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.decorators import api_view
from django.contrib.auth.hashers import check_password
from .serializers import CourseSerializer


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
        print(data)
        return HttpResponse(data, content_type='application/json')
    else:
        return HttpResponseBadRequest('Invalid Course data')

@csrf_exempt
def get_all_add_student_course(request):
    #changed the code to expect username instead of id
    if request.method == 'POST':
        body = json.loads(request.body.decode('utf-8'))
        # student_id = body.get('student_id')
        student_username = body.get('username')
        student_id = Student.objects.filter(username=student_username).values_list('id', flat=True).first()
        # course_id = body.get('course_id')
        course_name = body.get('course')
        course_id = Course.objects.filter(name=course_name).values_list('id', flat=True).first()

        course = Student_Course(student_id=Student.objects.get(pk=student_id), course_id=Course.objects.get(pk=course_id))
        course.save()
        print(f"{course_id} {course_name} has a new member {student_id} {student_username}!!")
        return HttpResponse('Enrolled Student to Course successfully')
    elif request.method == 'GET':
        Courses = Student_Course.objects.all()
        data = serializers.serialize("json", Courses)
        return HttpResponse(data, content_type='application/json')
    else:
        return HttpResponseBadRequest('Invalid Course data')

@swagger_auto_schema(
    method='get',
    operation_description="Get courses enrolled by a student",
    manual_parameters=[
        openapi.Parameter(
            'student_username', openapi.IN_QUERY, description="Student's username", type=openapi.TYPE_STRING
        )
    ],
    responses={
        200: "OK",
        400: "Bad Request",
        'application/json': openapi.Schema(
            type=openapi.TYPE_ARRAY,
            items=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'id': openapi.Schema(type=openapi.TYPE_INTEGER),
                    'name': openapi.Schema(type=openapi.TYPE_STRING),
                    'duration': openapi.Schema(type=openapi.TYPE_INTEGER),
                }
            )
        )
    }
)
@csrf_exempt
@api_view(['GET'])
def get_courses_by_student(request):
    #changed the code to expect username instead of id
    if request.method == 'GET':
        student_username = request.GET.get('student_username')
        student_id = Student.objects.filter(username=student_username).values_list('id', flat=True).first()
        course_ids = Student_Course.objects.filter(student_id=student_id).values_list('course_id', flat=True)
        courses = Course.objects.filter(id__in=course_ids)
        data = []
        print(courses)
        for course in courses:
            course_data = {
                'id': course.id,
                'fields': {
                    'name': course.name,
                    'duration': course.duration
                }
            }
            data.append(course_data)
        print(data)
        return JsonResponse(data, safe=False)
        data = serializers.serialize("json", data)
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
    #changing the code to expect username instead of id
    if request.method == 'DELETE':
        data = json.loads(request.body)
        student_username = data['student_username']
        student_id = Student.objects.filter(username=student_username).values_list('id', flat=True).first()
        # student_id = request.GET.get('student_id')
        course_name = data['course']
        course_id = Course.objects.filter(name=course_name).values_list('id', flat=True).first()
        # course_id = request.GET.get('course_id')
        student_course = Student_Course.objects.filter(course_id=course_id, student_id=student_id)
        student_course.delete()
        return HttpResponse("Unenrolled Student successfully",status=200)
    else:
        return HttpResponseBadRequest('Invalid Request')
    
@swagger_auto_schema(
    method='post',
    operation_description="Login a user",
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'username': openapi.Schema(type=openapi.TYPE_STRING, description="User's username"),
            'password': openapi.Schema(type=openapi.TYPE_STRING, description="User's password"),
        },
        required=['username', 'password']
    ),
    responses={200: "Login successful", 401: "Login failed", 400: "Bad Request"}
)
@csrf_exempt
@api_view(['POST'])
def user_login(request):
    data = json.loads(request.body)
    if request.method == 'POST':
        username = data['username']
        password = data['password']
        # email = data['email']

        # if username:
        #     user = Student.objects.filter(username=username, password=password)
        # else:

        user = Student.objects.filter(username=username)
        if not user or not check_password(password, user.first().password):
            return HttpResponse("Login failed",status=401)
        else:
            return  HttpResponse("Login successful",status=200)
    return HttpResponseBadRequest('Invalid Request')

@swagger_auto_schema(
    method='post',
    operation_description="Register a new user",
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'username': openapi.Schema(type=openapi.TYPE_STRING, description="User's username"),
            'email': openapi.Schema(type=openapi.TYPE_STRING, description="User's email"),
            'password': openapi.Schema(type=openapi.TYPE_STRING, description="User's password"),
        },
        required=['username', 'email', 'password']
    ),
    responses={200: "Register successful", 409: "Student already exists", 400: "Bad Request"}
)
@csrf_exempt
@api_view(['POST'])
def register(request):
    data = json.loads(request.body)
    if request.method == 'POST':
        student = Student(
            username=data['username'],  # Assuming 'username' corresponds to the student's name
            email=data['email'],
            password=make_password(data['password']),  # Hash the password
        )
        # Check if student already exists
        if Student.objects.filter(username=student.username).exists():
            return HttpResponse('Student already exists', status=409)

        # If student does not exist, create a new student
        student.save()
        return HttpResponse("Register successful", status=200)
    return HttpResponseBadRequest('Invalid Request')