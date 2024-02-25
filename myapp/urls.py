from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='myapp-home'),
    path('<int:id>', views.home_id, name='myapp-home-id'),
    path('students/',views.get_all_add_student, name='myapp-add-student'),
    path('students/<int:id>',views.get_update_delete_student_by_id, name='myapp-get-student-by-id'),
    path('courses/<int:id>',views.get_update_delete_course_by_id, name='myapp-get-course-by-id'),
    path('courses/',views.get_all_add_course, name='myapp-add-course'),
    path('course_students/',views.get_all_add_student_course, name='myapp-get-all-add-student-course'),
    path('course_students/by_student/',views.get_courses_by_student, name='myapp-get-courses-by-student'),
    path('course_students/by_course/',views.get_students_by_course, name='myapp-get-students-by-course'),
    path('course_students/drop/',views.drop_course_for_student, name='myapp-get-course-student-by-id'),
    path('login',views.user_login, name='myapp-user-login'),
    path('register',views.register, name='myapp-register'),
]
