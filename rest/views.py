from rest_framework import viewsets
from .models import Class, Course, Lecturer, Student, StudentEnrollment, Semester
from . import serializers
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User

class SemesterViewSet(viewsets.ModelViewSet):
	serializer_class = serializers.SemesterSerializer
	queryset = Semester.objects.all()
	permission_classes = [IsAuthenticated]
	authentication_classes = (TokenAuthentication, )

class ClassViewSet(viewsets.ModelViewSet):
	serializer_class = serializers.ClassSerializer
	queryset = Class.objects.all()

class CourseViewSet(viewsets.ModelViewSet):
	serializer_class = serializers.CourseSerializer
	queryset = Course.objects.all()

class LecturerViewSet(viewsets.ModelViewSet):
	serializer_class = serializers.LecturerSerializer
	queryset = Lecturer.objects.all()

class StudentViewSet(viewsets.ModelViewSet):
	serializer_class = serializers.StudentSerializer
	queryset = Student.objects.all()

class StudentEnrollmentViewSet(viewsets.ModelViewSet):
	serializer_class = serializers.StudentEnrollmentSerializer
	queryset = StudentEnrollment.objects.all()

class UserViewSet(viewsets.ModelViewSet):
	serializer_class = serializers.UserSerilizer
	queryset = User.objects.all()