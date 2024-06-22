from rest_framework import viewsets, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.core.mail import send_mail


@api_view(['POST'])
# @permission_classes([IsAuthenticated])
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
