from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class Semester(models.Model):
	semester_items = (
		(1, 1),
		(2, 2),
	)
	year = models.IntegerField()
	semester = models.IntegerField(choices=semester_items)

	def __str__(self):
		return f"{self.year} {self.semester}"


class Course(models.Model):
	code = models.CharField(max_length=50)
	name = models.CharField(max_length=50)

	def __str__(self):
		return self.name


class Lecturer(models.Model):
	staffID = models.PositiveIntegerField(unique=True)
	firstname = models.CharField(max_length=50)
	lastname = models.CharField(max_length=50)
	email = models.EmailField(unique=True)
	DOB = models.DateField()
	user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)

	def __str__(self):
		return f"{self.firstname} {self.lastname}"


class Student(models.Model):
	studentID = models.PositiveIntegerField(unique=True)
	firstname = models.CharField(max_length=50)
	lastname = models.CharField(max_length=50)
	email = models.EmailField(unique=True)
	DOB = models.DateField()
	user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, related_name='student')

	def __str__(self):
		return f"{self.firstname} {self.lastname}"


class Class(models.Model):
	number = models.PositiveIntegerField(unique=True)
	semester = models.ForeignKey(Semester, on_delete=models.PROTECT)
	course = models.ForeignKey(Course, on_delete=models.PROTECT)
	lecturer = models.ForeignKey(Lecturer, on_delete=models.PROTECT, blank=True, null=True, related_name='classes')
	students = models.ManyToManyField(Student, through='StudentEnrollment', related_name='classes', blank=True)

	def __str__(self):
		return f"{self.number}  {self.course}"


class StudentEnrollment(models.Model):
	studentID = models.ForeignKey(Student, on_delete=models.PROTECT, related_name='enrollments')
	classID = models.ForeignKey(Class, on_delete=models.PROTECT, related_name='enrollme'
																			  'nts')
	grade = models.PositiveIntegerField(blank=True, null=True)
	enrolTime = models.DateTimeField(auto_now=True)
	gradeTime = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return f"{self.classID} + {self.studentID}"