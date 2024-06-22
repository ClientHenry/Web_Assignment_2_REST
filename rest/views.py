from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.core.mail import send_mail
from rest.models import Class
from rest.permissions import IsLecturer
from rest.serializers import StudentEnrollmentSerializer


@api_view(['POST'])
@permission_classes([IsAuthenticated, IsLecturer])
def send_email_to_class(request, pk):
    selected_class = get_object_or_404(Class, id=pk)
    enrollments = selected_class.enrollments.all()

    sent_emails = []
    for enrollment in enrollments:
        if enrollment.studentID.email:
            subject = 'Your Grade is Ready'
            body = f'Hello {enrollment.studentID.firstname}, Your Grade is Ready'
            from_email = 'wanghao0628@hotmail.com'
            to_email = enrollment.studentID.email
            send_mail(subject, body, from_email, [to_email])
            sent_emails.append(enrollment.studentID.email)

    serializer = StudentEnrollmentSerializer(enrollments, many=True)
    response_data = {
        'emails_sent_to': sent_emails
    }

    return Response(response_data, status=200)
