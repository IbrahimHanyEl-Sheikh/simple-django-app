from django.shortcuts import render
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseNotAllowed, Http404
from .models import Student, Course, Student_Course
from django.views.decorators.csrf import csrf_exempt, ensure_csrf_cookie
import json
from django.core import serializers

# Create your views here.

# def home(request):
#     return HttpResponse('<h1>Blog Home</h1>')
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
    new_name = new_student_data.get("name")
    new_email = new_student_data.get("email")
    new_phone = new_student_data.get("phone")
    new_address = new_student_data.get("address")
    new_city = new_student_data.get("city")
    try:
        student = Student.objects.get(pk=student_id)
    except Student.DoesNotExist:
        raise Http404("Student does not exist")
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
