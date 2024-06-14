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


class StudentSerializer(serializers.ModelSerializer):
	class Meta:
		model = Student
		fields = '__all__'


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
		#user.groups = "Lecturers"
#添加一个student group
		user.groups.add(2)
		Token.objects.create(user=user)
		return user
