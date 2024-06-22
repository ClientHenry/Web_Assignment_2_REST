from rest_framework import permissions


class IsLecturer(permissions.BasePermission):
	message = 'You must be a lecturer to access this resource'

	def has_object_permission(self, request, view, obj):
		user_groups = request.user.groups.values_list('name', flat=True)
		if 'Lecturer' in user_groups:
			return True
		return False


class IsStudent(permissions.BasePermission):
	message = 'You must be a student to access this resource'

	def has_object_permission(self, request, view, obj):
		user_groups = request.user.groups.values_list('name', flat=True)
		if 'Student' in user_groups:
			return True
		return False


class IsAdmin(permissions.BasePermission):
	message = 'You must be an admin to access this resource'

	def has_permission(self, request, view):
		user_groups = request.user.groups.values_list('name', flat=True)
		if 'Admin' in user_groups:
			return True
		return False
