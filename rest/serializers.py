from rest_framework import serializers, permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Class, Course, Lecturer, Student, StudentEnrollment, Semester
from django.contrib.auth.models import User, Group
from rest_framework.authtoken.models import Token


class SemesterSerializer(serializers.ModelSerializer):
	class Meta:
		model = Semester
		fields = '__all__'


class CourseSerializer(serializers.ModelSerializer):
	class Meta:
		model = Course
		fields = '__all__'


class LecturerSerializer(serializers.ModelSerializer):
	class Meta:
		model = Lecturer
		fields = ['id', 'staffID', 'firstname', 'lastname', 'email', 'DOB']

		extra_kwargs = {
			'user': {'write_only': True, 'required': False}
		}

	def create(self, validated_data):
		email = validated_data.get('email')
		dob = validated_data.get('DOB')

		user, _ = User.objects.get_or_create(username=email)
		user.set_password(str(dob))
		user.save()

		lecturer_group = Group.objects.get(name='Lecturer')
		user.groups.add(lecturer_group)

		Token.objects.create(user=user)

		validated_data['user'] = user
		lecturer = super().create(validated_data)

		return lecturer


# def delete(instance):
#
# 	user = instance.user
# 	try:
# 		token = Token.objects.get(user=user)
# 		token.delete()
# 	except Token.DoesNotExist:
# 		pass
# 	user.delete()
# 	instance.delete()


class StudentSerializer(serializers.ModelSerializer):
	class Meta:
		model = Student
		fields = ['id', 'studentID', 'firstname', 'lastname', 'email', 'DOB']

	extra_kwargs = {
		'user': {'write_only': True, 'required': False}
	}

	def create(self, validated_data):
		email = validated_data.get('email')
		dob = validated_data.get('DOB')

		user, _ = User.objects.get_or_create(username=email)
		user.set_password(str(dob))
		user.save()

		student_group = Group.objects.get(name='Student')
		user.groups.add(student_group)

		Token.objects.create(user=user)

		validated_data['user'] = user
		student = super().create(validated_data)

		return student


# 删除user可以删除student，但是反过来不行。上个作业就不行~

class ClassSerializer(serializers.ModelSerializer):
	class Meta:
		model = Class
		fields = '__all__'


class LecturerClassListView(APIView):
	# permission_classes = [permissions.IsAuthenticated]

	def get(self, request):
		# Check if the user is in the 'lecturer' group
		if request.user.groups.filter(name='x').exists():
			try:
				lecturer = Lecturer.objects.get(email=request.user.username)
			except Lecturer.DoesNotExist:
				return Response({'error': 'Lecturer not found'}, status=404)

			classes = lecturer.classes.all()
			serializer = ClassSerializer(classes, many=True, context={'request': request})

			# Customize the serialized data
			data = serializer.data
			for class_data in data:
				class_obj = Class.objects.get(id=class_data['id'])
				class_data['semester_details'] = {
					'id': class_obj.semester.id,
					'year': class_obj.semester.year,
					'semester': class_obj.semester.semester,
				}
				class_data['course_details'] = {
					'id': class_obj.course.id,
					'code': class_obj.course.code,
					'name': class_obj.course.name,
				}

			return Response(data)
		else:
			return Response({'error': 'You are not a lecturer'}, status=403)


class GroupSerializer(serializers.ModelSerializer):
	class Meta:
		model = Group
		fields = ('name',)


class UserSerilizer(serializers.ModelSerializer):
	groups = GroupSerializer(many=True, required=False)

	class Meta:
		model = User
		# fields = ['id', 'username', 'password', 'groups']
		fields = ['id', 'username', 'password', 'groups']

		extra_kwargs = {
			'password': {'write_only': True, 'required': True}
		}

	def create(self, validated_data):
		user = User.objects.create_user(**validated_data)

		# user.groups = "Lecturers"
		# 添加一个student group
		user.groups.add(2)
		Token.objects.create(user=user)
		return user


# class BulkStudentEnrollmentSerializer(serializers.ListSerializer):
# 	def update(self, instance, validated_data):
# 		# Create a mapping of id to enrollment instance
# 		enrollment_mapping = {enrollment.id: enrollment for enrollment in instance}
#
# 		# Ensure that each item in validated_data has an 'id' field
# 		if not all('id' in item for item in validated_data):
# 			raise serializers.ValidationError("Each item in the list must have an 'id' field.")
#
# 		# Create a mapping of id to data item
# 		data_mapping = {item['id']: item for item in validated_data}
#
# 		# Perform updates
# 		ret = []
# 		for enrollment_id, data in data_mapping.items():
# 			enrollment = enrollment_mapping.get(enrollment_id, None)
# 			if enrollment is not None:
# 				# Update the enrollment instance with new data
# 				for attr, value in data.items():
# 					setattr(enrollment, attr, value)
# 				enrollment.save()
# 				ret.append(enrollment)
# 		return ret
#

class StudentEnrollmentSerializer(serializers.ModelSerializer):
	class Meta:
		model = StudentEnrollment
		# fields = ['id', 'classID', 'grade', 'classNumber', 'courseName']
		fields = '__all__'
		# list_serializer_class = BulkStudentEnrollmentSerializer
