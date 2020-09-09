from django.http import HttpResponse
from django.shortcuts import redirect



def allowed_users(allowed_roles=[]):
	def decorator(view_func):
		def wrapper_func(request, *args, **kwargs):

			groups = [group.name for group in request.user.groups.all()]

			if len(set(groups)&set(allowed_roles))!=0:
				return view_func(request, *args, **kwargs)
			else:
				return HttpResponse('You are not authorized to view this page')
		return wrapper_func
	return decorator

def allowed_usersprofile(allowed_roles=[]):
	def decorator(view_func):
		def wrapper_func(request, *args, **kwargs):

			groups = [group.name for group in request.user.groups.all()]

			if len(set(groups)&set(allowed_roles))!=0:
				return view_func(request, *args, **kwargs)
			else:
				return redirect(groups[0]+':profile')
		return wrapper_func
	return decorator
