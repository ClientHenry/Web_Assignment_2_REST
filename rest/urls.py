from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('semesters', viewset=views.SemesterViewSet, basename='semesters')
router.register('classes', viewset=views.ClassViewSet, basename='classes')
router.register('courses', viewset=views.CourseViewSet, basename='courses')
router.register('lecturers', viewset=views.LecturerViewSet, basename='lecturers')
router.register('students', viewset=views.StudentViewSet, basename='students')
router.register('enrollments', viewset=views.StudentEnrollmentViewSet, basename='enrollments')
router.register('users', viewset=views.UserViewSet, basename='users')

urlpatterns = [
   path('', include(router.urls)),

]
