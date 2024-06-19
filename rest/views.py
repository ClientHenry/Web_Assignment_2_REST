from rest_framework import viewsets, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import permissions
from .models import Student, StudentEnrollment, Lecturer, Class
from .serializers import StudentEnrollmentSerializer, ClassSerializer
from django.core.mail import send_mail


# class StudentGradeViewSet(viewsets.ViewSet):
# 	# permission_classes = [permissions.IsAuthenticated]
#
# 	def list(self, request):
# 		user_groups = request.user.groups.values_list('name', flat=True)
# 		if 'Student' in user_groups:
# 			email = request.user.username
# 			student = Student.objects.get(email=email)
# 			enrollments = student.enrollments.all()
# 			serializer = StudentEnrollmentSerializer(enrollments, many=True)
# 			return Response(serializer.data)
#
# 		return Response(status=404)
#
#
# class LecturerViewSet(viewsets.ViewSet):
#     def list(self, request):
#         lecturer = Lecturer.objects.get(email=request.user.username)
#         classes = lecturer.classes.all()
#         serializer = ClassSerializer(classes, many=True)
#         return Response(serializer.data)
#
#     def retrieve(self, request, pk=None):
#         try:
#             current_class = Class.objects.get(id=pk)
#             enrollments = current_class.enrollments.all()
#             serializer = StudentEnrollmentSerializer(enrollments, many=True)
#             return Response(serializer.data)
#         except Class.DoesNotExist:
#             return Response(status=status.HTTP_404_NOT_FOUND)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def send_email_to_class(request):
    try:
        send_mail(
            'Your Grade is Ready',
            'Your Grade is Ready',
            'wanghao0628@hotmail.com',
            ['wangh159@myunitec.ac.nz']
        )
        return Response({'success': 'Email sent successfully'}, status=200)
    except Exception as e:
        return Response({'error': str(e)}, status=500)
