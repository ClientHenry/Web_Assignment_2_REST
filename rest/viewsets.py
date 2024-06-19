from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from rest_framework import viewsets, permissions
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Class, Course, Lecturer, Student, StudentEnrollment, Semester
from . import serializers
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User

from .permissions import IsLecturer, IsAdmin
from .serializers import StudentEnrollmentSerializer


class SemesterViewSet(viewsets.ModelViewSet):
	serializer_class = serializers.SemesterSerializer
	queryset = Semester.objects.all()


# permission_classes = [IsAuthenticated, IsAdmin]
# authentication_classes = (TokenAuthentication, )


class ClassViewSet(viewsets.ModelViewSet):
	serializer_class = serializers.ClassSerializer
	queryset = Class.objects.all()


# permission_classes = [IsAuthenticated, IsAdmin]
# authentication_classes = (TokenAuthentication, )


class CourseViewSet(viewsets.ModelViewSet):
	serializer_class = serializers.CourseSerializer
	queryset = Course.objects.all()


# permission_classes = [IsAuthenticated, IsAdmin]
# authentication_classes = (TokenAuthentication, )


class LecturerViewSet(viewsets.ModelViewSet):
	serializer_class = serializers.LecturerSerializer
	queryset = Lecturer.objects.all()


# permission_classes = [IsAuthenticated, IsAdmin]
# authentication_classes = (TokenAuthentication, )


class StudentViewSet(viewsets.ModelViewSet):
	serializer_class = serializers.StudentSerializer
	queryset = Student.objects.all()


# permission_classes = [IsAuthenticated, IsAdmin]
# authentication_classes = (TokenAuthentication, )


class StudentEnrollmentViewSet(viewsets.ModelViewSet):
	serializer_class = serializers.StudentEnrollmentSerializer
	queryset = StudentEnrollment.objects.all()


# permission_classes = [IsAuthenticated, IsAdmin]
# authentication_classes = (TokenAuthentication, )


class UserViewSet(viewsets.ModelViewSet):
	serializer_class = serializers.UserSerilizer
	queryset = User.objects.all()

	@api_view(['GET'])
	@permission_classes([IsAuthenticated])
	@authentication_classes([TokenAuthentication])
	def User_logout(request):
		request.user.auth_token.delete()
		logout(request)
		return Response("Logout successful")


