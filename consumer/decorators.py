from django.http import HttpResponse
from django.shortcuts import redirect,render



def allowed_users(allowed_roles=[],redirect_to=None):
	def decorator(view_func):
		def wrapper_func(request, *args, **kwargs):

			groups = [group.name for group in request.user.groups.all()]

			if len(set(groups)&set(allowed_roles))!=0:
				return view_func(request, *args, **kwargs)
			else:
				if redirect_to==None:
					return render(request,'unauthorised_access.html',{'message':'You are not authorized to view this page'})
				return redirect( groups[0]+':'+redirect_to )
		return wrapper_func
	return decorator

def check_profile_exist(view_func):
	def wrapper_func(request, *args, **kwargs):
		if request.user.lastupdated.update_date:
			return view_func(request, *args, **kwargs)
		else:
			groups = [group.name for group in request.user.groups.all()]
			return redirect( groups[0]+':updateprofile' )
	return wrapper_func
