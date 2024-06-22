from rest_framework import serializers
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


class ClassSerializer(serializers.ModelSerializer):
	courseName = serializers.ReadOnlyField(source='course.name')
	classNumber = serializers.ReadOnlyField(source='number')
	students = serializers.PrimaryKeyRelatedField(queryset=Student.objects.all(), many=True)

	class Meta:
		model = Class
		fields = '__all__'
		read_only_fields = ('courseName', 'classNumber')

	def update(self, instance, validated_data):
		students = validated_data.pop('students', None)
		instance = super().update(instance, validated_data)

		if students is not None:
			instance.students.set(students)
		else:
			instance.students.clear()  # Clear students if students is empty

		return instance


class GroupSerializer(serializers.ModelSerializer):
	class Meta:
		model = Group
		fields = ('name',)


class UserSerilizer(serializers.ModelSerializer):
	groups = GroupSerializer(many=True, required=False)

	class Meta:
		model = User
		fields = ['id', 'username', 'password', 'groups']
		extra_kwargs = {
			'password': {'write_only': True, 'required': True}
		}


class StudentEnrollmentSerializer(serializers.ModelSerializer):
	courseName = serializers.ReadOnlyField(source='classID.course.name')
	classNumber = serializers.ReadOnlyField(source='classID.number')
	studentFirstName = serializers.ReadOnlyField(source='studentID.firstname')
	studentLastName = serializers.ReadOnlyField(source='studentID.lastname')

	class Meta:
		model = StudentEnrollment
		fields = '__all__'
		read_only_fields = ('courseName', 'classNumber', 'studentFirstName', 'studentLastName')
