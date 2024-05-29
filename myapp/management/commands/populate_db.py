from django.core.management.base import BaseCommand
from myapp.models import Student, Course, Student_Course
from faker import Faker
import random
from django.contrib.auth.hashers import make_password

class Command(BaseCommand):
    help = 'Populates the database with dummy data'

    def add_arguments(self, parser):
        parser.add_argument('--count', type=int, default=10, help='The number of dummy records to create')

    def handle(self, *args, **kwargs):
        count = kwargs['count']
        fake = Faker()

        # Predefined course names
        courses = [
            "Python", "Docker", "Jenkins", "Linux",
            "OOP", "Unit Testing", "ROBOT Framework",
            "5G", "Agile", "System Design"
        ]

        for i in range(count):
            # Create a Student instance
            student = Student.objects.create(
                username=fake.user_name(),
                name=fake.name(),
                email=fake.email(),
                phone=fake.phone_number(),
                address=fake.address(),
                city=fake.city(),
                password=make_password(fake.password())
            )

            # Choose a random course from predefined names
            if i < len(courses):
                course_name = courses[i]
            else:
                course_name = random.choice(courses)

            # Create or get the Course instance
            course, _ = Course.objects.get_or_create(name=course_name, defaults={'duration': random.randint(1, 4)})

            # Enroll student in the course
            Student_Course.objects.create(
                student_id=student,
                course_id=course
            )

        self.stdout.write(self.style.SUCCESS(f'Successfully populated database with {count} dummy records'))