from django.urls import path, include
from . import viewsets
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('semesters', viewset=viewsets.SemesterViewSet, basename='semesters')
router.register('classes', viewset=viewsets.ClassViewSet, basename='classes')
router.register('courses', viewset=viewsets.CourseViewSet, basename='courses')
router.register('lecturers', viewset=viewsets.LecturerViewSet, basename='lecturers')
router.register('students', viewset=viewsets.StudentViewSet, basename='students')
router.register('enrollments', viewset=viewsets.StudentEnrollmentViewSet, basename='enrollments')
router.register('users', viewset=viewsets.UserViewSet, basename='users')
router.register('grade/students', viewset=viewsets.StudentGradeViewSet, basename='student-grades')
router.register('grade/lecturers', viewset=viewsets.LecturerGradeViewSet, basename='lecturer-classes')

urlpatterns = [
   path('', include(router.urls)),
]
