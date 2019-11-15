from django.conf import settings
from django.contrib.auth.models import User
class EmailAuthBackend(object):
	def authenticate(self,request,username=None,password=None):
		print("hdfh")
		try:
			user=User.objects.get(email=username)
			if user.check_password(password):
				return user
			return None
		except User.DoesNotExist:
			return None
	def get_user(self,userid):
		try:
			return User.objects.get(pk=userid)
		except User.DoesNotExist:
			return None