from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Profile(models.Model):
	user=models.OneToOneField(User,on_delete=models.CASCADE)
	gender=models.CharField(max_length=10,choices=(('Male','Male'),('Female','Female')),default='Male')
	tel=models.CharField(max_length=10)
	pic=models.ImageField(upload_to='profile/profile_pic',default="profile/profile_pic/profile_image.jpg")
	type=models.CharField(max_length=10,choices=(('Student','Student'),('Teacher','Teacher')),default='Student')
	security=models.CharField(max_length=50,default="")
	def __str__(self):
		return self.user.username