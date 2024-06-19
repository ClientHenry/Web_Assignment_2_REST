from django.contrib.auth import logout
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.response import Response
from .models import Class, Course, Lecturer, Student, StudentEnrollment, Semester
from . import serializers
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User
from .permissions import IsLecturer, IsAdmin, IsStudent
from .serializers import StudentEnrollmentSerializer, ClassSerializer


class SemesterViewSet(viewsets.ModelViewSet):
	serializer_class = serializers.SemesterSerializer
	queryset = Semester.objects.all()
	permission_classes = [IsAuthenticated, IsAdmin]
	authentication_classes = (TokenAuthentication,)


class ClassViewSet(viewsets.ModelViewSet):
	serializer_class = serializers.ClassSerializer
	queryset = Class.objects.all()
	permission_classes = [IsAuthenticated, IsAdmin]
	authentication_classes = (TokenAuthentication,)


class CourseViewSet(viewsets.ModelViewSet):
	serializer_class = serializers.CourseSerializer
	queryset = Course.objects.all()
	permission_classes = [IsAuthenticated, IsAdmin]
	authentication_classes = (TokenAuthentication,)


class LecturerViewSet(viewsets.ModelViewSet):
	serializer_class = serializers.LecturerSerializer
	queryset = Lecturer.objects.all()
	permission_classes = [IsAuthenticated, IsAdmin]
	authentication_classes = (TokenAuthentication,)


class StudentViewSet(viewsets.ModelViewSet):
	serializer_class = serializers.StudentSerializer
	queryset = Student.objects.all()
	permission_classes = [IsAuthenticated, IsAdmin]
	authentication_classes = (TokenAuthentication,)


class StudentEnrollmentViewSet(viewsets.ModelViewSet):
	serializer_class = serializers.StudentEnrollmentSerializer
	queryset = StudentEnrollment.objects.all()
	permission_classes = [IsAuthenticated]
	authentication_classes = (TokenAuthentication,)


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


class StudentGradeViewSet(viewsets.ViewSet):

	permission_classes = [IsAuthenticated, IsStudent]
	authentication_classes = (TokenAuthentication,)
	def list(self, request):
		user_groups = request.user.groups.values_list('name', flat=True)
		if 'Student' in user_groups:
			email = request.user.username
			student = Student.objects.get(email=email)
			enrollments = student.enrollments.all()
			serializer = StudentEnrollmentSerializer(enrollments, many=True)
			return Response(serializer.data)

		return Response(status=404)


class LecturerGradeViewSet(viewsets.ViewSet):

	permission_classes = [IsAuthenticated, IsLecturer]
	authentication_classes = (TokenAuthentication,)
	def list(self, request):
		lecturer = Lecturer.objects.get(email=request.user.username)
		classes = lecturer.classes.all()
		serializer = ClassSerializer(classes, many=True)
		return Response(serializer.data)

	def retrieve(self, request, pk=None):
		try:
			current_class = Class.objects.get(id=pk)
			enrollments = current_class.enrollments.all()
			serializer = StudentEnrollmentSerializer(enrollments, many=True)
			return Response(serializer.data)
		except Class.DoesNotExist:
			return Response(status=status.HTTP_404_NOT_FOUND)
