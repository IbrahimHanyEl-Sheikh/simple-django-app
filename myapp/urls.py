from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='myapp-home'),
    path('<int:id>', views.home_id, name='myapp-home-id'),
    path('students/',views.get_all_add_student, name='myapp-add-student'),
    path('students/<int:id>',views.get_update_delete_student_by_id, name='myapp-get-student-by-id'),
    path('courses/<int:id>',views.get_update_delete_course_by_id, name='myapp-get-course-by-id'),
    path('courses/',views.get_all_add_course, name='myapp-add-course')
]
