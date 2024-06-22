from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.core.mail import send_mail

from rest.models import Class
from rest.permissions import IsLecturer
from rest.serializers import StudentEnrollmentSerializer


# @api_view(['POST'])
# @permission_classes([IsAuthenticated, IsLecturer])
# def send_email_to_class(request, pk):
# 	selected_class = get_object_or_404(Class, id=pk)
# 	enrollments = selected_class.enrollments.all()
# 	StudentEnrollmentSerializer(enrollments, many=True)
#
# 	for enrollment in enrollments:
# 		student_name = enrollment.studentID
# 		subject = 'Your Grade is Ready'
# 		body = f'Hello {student_name}, Your Grade is Ready'
# 		from_email = 'wanghao0628@hotmail.com'
# 		to_email = enrollment.studentID.email
# 		send_mail(subject, body, from_email, [to_email])
#
# 	return Response({'success': 'Email sent successfully'}, status=200)

@api_view(['POST'])
@permission_classes([IsAuthenticated, IsLecturer])
def send_email_to_class(request, pk):
	selected_class = get_object_or_404(Class, id=pk)
	enrollments = selected_class.enrollments.all()

	for enrollment in enrollments:
		# student_name = enrollment.studentID
		subject = 'Your Grade is Ready'
		body = 'Your Grade is Ready'
		from_email = 'wanghao0628@hotmail.com'
		# to_email = enrollment.studentID.email
		to_email = 'wangh159@myunitec.ac.nz'
		send_mail(subject, body, from_email, [to_email])

	# Optionally, you can serialize the enrollments for response
	serializer = StudentEnrollmentSerializer(enrollments, many=True)

	return Response({'success': 'Email sent successfully', 'enrollments': serializer.data}, status=200)
