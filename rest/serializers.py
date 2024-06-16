from rest_framework import serializers
from .models import Class, Course, Lecturer, Student, StudentEnrollment, Semester
from django.contrib.auth.models import User, Group
from rest_framework.authtoken.models import Token


class SemesterSerializer(serializers.ModelSerializer):
	class Meta:
		model = Semester
		fields = '__all__'


class ClassSerializer(serializers.ModelSerializer):
	class Meta:
		model = Class
		fields = '__all__'


class CourseSerializer(serializers.ModelSerializer):
	class Meta:
		model = Course
		fields = '__all__'


class LecturerSerializer(serializers.ModelSerializer):
	class Meta:
		model = Lecturer
		fields = '__all__'


def delete(instance):

	user = instance.user
	try:
		token = Token.objects.get(user=user)
		token.delete()
	except Token.DoesNotExist:
		pass
	user.delete()
	instance.delete()


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


class StudentEnrollmentSerializer(serializers.ModelSerializer):
	class Meta:
		model = StudentEnrollment
		fields = '__all__'


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
