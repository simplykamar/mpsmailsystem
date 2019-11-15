from django.db import models
from django.contrib.auth.models import User
from account.models import Profile
# Create your models here.

class Inbox(models.Model):
	profile=models.ForeignKey(Profile,on_delete=models.CASCADE,related_name="inbox_profile")
	#from_name=models.CharField(max_length=80)
	#from_email=models.CharField(max_length=100)
	from_user=models.ForeignKey(Profile,on_delete=models.CASCADE,related_name="from_user",default='')
	#to_email=models.CharField(max_length=100)
	#to_name=
	#to_pic=
	sub=models.CharField(max_length=200)
	msg=models.TextField()
	attach=models.FileField(upload_to="attach_data/",default="")
	date=models.DateField(auto_now_add=True)
	starred=models.BooleanField(default=False)
	def __str__(self):
		return self.from_user.user.username+" "+self.profile.user.username

class Sentmail(models.Model):
	profile=models.ForeignKey(Profile,on_delete=models.CASCADE,related_name="sentmail_profile")
	to_user=models.ForeignKey(Profile,on_delete=models.CASCADE,related_name="to_user",default='')
	#to_name=models.CharField(max_length=80)
	#to_email=models.CharField(max_length=100)
	#to_pic=models.ImageField(upload_to='sentmail/to_pic')
	#from_email=models.CharField(max_length=100)
	#from_name=
	#from_pic=
	sub=models.CharField(max_length=200)
	msg=models.TextField()
	attach=models.FileField(upload_to="attach_data/",default="",blank=True)
	date=models.DateField(auto_now_add=True)

class Notification(models.Model):
	profile=models.ForeignKey(Profile,on_delete=models.CASCADE,related_name="to_notification")
	from_user=models.ForeignKey(Profile,on_delete=models.CASCADE,related_name="from_notification")
	mail_id=models.IntegerField()
	check=models.BooleanField(default=False)
	def __str__(self):
	    return self.profile.user.username
