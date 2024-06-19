from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework import permissions
from .models import Student, StudentEnrollment, Lecturer, Class
from .serializers import StudentEnrollmentSerializer, ClassSerializer


class StudentGradeViewSet(viewsets.ViewSet):
	# permission_classes = [permissions.IsAuthenticated]

	def list(self, request):
		user_groups = request.user.groups.values_list('name', flat=True)
		if 'Student' in user_groups:
			email = request.user.username
			student = Student.objects.get(email=email)
			enrollments = student.enrollments.all()
			serializer = StudentEnrollmentSerializer(enrollments, many=True)
			return Response(serializer.data)

		return Response(status=404)


class LecturerViewSet(viewsets.ViewSet):
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

    # def partial_update(self, request, pk=None):
    #     try:
    #         current_class = Class.objects.get(id=pk)
    #         enrollments = current_class.enrollments.all()
    #         serializer = StudentEnrollmentSerializer(enrollments, data=request.data, many=True, partial=True)
    #         if serializer.is_valid():
    #             serializer.save()
    #             return Response(serializer.data)
    #         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    #     except Class.DoesNotExist:
    #         return Response(status=status.HTTP_404_NOT_FOUND)
