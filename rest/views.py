from django.contrib.auth.models import User, Group
from django.shortcuts import get_object_or_404
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.core.mail import send_mail
from rest.models import Class, Student
from rest.permissions import IsLecturer, IsAdmin
from rest.serializers import StudentEnrollmentSerializer, StudentSerializer


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


# @api_view(['POST'])
# @permission_classes([IsAuthenticated, IsAdmin])
# def bulk_create_students(request):
#     students_data = request.data.get('students', [])
#     created_students = []
#
#     for student_data in students_data:
#         try:
#             email = student_data.get('email')
#             dob = student_data.get('DOB')
#             first_name = student_data.get('firstName')
#             last_name = student_data.get('lastName')
#
#             user = User.objects.create_user(
#                 username=email,
#                 password=dob,
#                 email=email,
#                 first_name=first_name,
#                 last_name=last_name
#             )
#
#             student_group, _ = Group.objects.get_or_create(name='Student')
#             user.groups.add(student_group)
#
#             student = Student.objects.create(
#                 user=user,
#                 firstName=first_name,
#                 lastName=last_name,
#                 email=email,
#                 DOB=dob
#             )
#
#             created_students.append(student)
#         except Exception:
#             continue
#
#     serializer = StudentSerializer(created_students, many=True)
#     return Response(serializer.data)

from datetime import datetime

@api_view(['POST'])
def bulk_create_students(request):
    students_data = request.data.get('students', [])
    created_students = []

    for student_data in students_data:
        try:
            email = student_data.get('email')
            dob_str = student_data.get('DOB')  # Assuming it's in 'YYYY-MM-DD' format

            # Convert 'DOB' string to datetime object
            dob = datetime.strptime(dob_str, '%Y-%m-%d').date()

            first_name = student_data.get('firstName')
            last_name = student_data.get('lastName')
            studentID = student_data.get('studentID')

            # Create or retrieve User instance
            user, _ = User.objects.get_or_create(username=email)
            user.set_password(str(dob))
            user.set_first_name(first_name)
            user.set_last_name(last_name)
            user.save()

            # Ensure user belongs to 'Student' group
            student_group, _ = Group.objects.get_or_create(name='Student')
            user.groups.add(student_group)

            # Create or retrieve Token for the user
            Token.objects.get_or_create(user=user)

            # Prepare data for StudentSerializer
            student_data = {
                'user': user.id,
                'firstname': first_name,
                'lastname': last_name,
                'email': email,
                'DOB': dob,  # Assign datetime object here
                'studentID': studentID
            }

            # Use StudentSerializer for validation and saving
            serializer = StudentSerializer(data=student_data)

            if serializer.is_valid():
                student_instance = serializer.save()
                created_students.append(student_instance)
            else:
                # Handle serializer errors if needed
                continue

        except Exception as e:
            # Handle exceptions (logging, etc.) if needed
            continue

    # Serialize all created students
    serializer = StudentSerializer(created_students, many=True)
    return Response(serializer.data)
