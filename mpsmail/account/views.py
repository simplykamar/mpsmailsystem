from django.shortcuts import render,redirect
from django.contrib import messages
from . import forms
from django.contrib.auth.decorators import login_required
from django.utils.safestring import mark_safe
from django.http import JsonResponse
from mail.models import Profile,Notification,Inbox
from django.contrib.auth.models import User,auth
#from django.views.generic import
# Create your views here.

@login_required(login_url="/account/login")
def profile(req):
	id=req.user.id
	profile=Profile.objects.get(user__id=id)
	return render(req,"account/profile.html",{"profile":profile})

def forgot_pwd(req):
	if req.method=="POST":
		email=req.POST['email'].lower()
		security=req.POST['security']
		try:
			profile=Profile.objects.get(user__email=email,security=security)
			pwd=req.POST['pwd']
			cnfpwd=req.POST['cnfpwd']
			print("yes")
			if pwd==cnfpwd:
				profile.user.set_password(pwd)
				profile.user.save()
				print("pwd change")
				messages.success(req,mark_safe("password successfully Reset <a href='/account/login'>click here to login</a>"))
				from_user=Profile.objects.get(user__username="support")
				inbox=Inbox.objects.create(profile=profile,from_user=from_user,sub="Your Password has been changed",msg="Hello <{}> Your Password Successfully Changed. For any help mail us on support@mps.edu".format(profile.user.username))
				Notification.objects.create(profile=profile,mail_id=inbox.id,from_user=from_user)
			else:messages.error(req,"Confirm password not match...!")
		except Exception as e:
			print(e)
			messages.error(req,"Incorrcet email address or Security")
	return render(req,"account/forgot_pwd.html")

@login_required(login_url="/account/login")
def change_pic(req):
	if req.method=="POST":
		pic=req.FILES['img']
		profile=Profile.objects.get(user__id=req.user.id)
		profile.pic=pic
		profile.save()
		return JsonResponse({"img_upload":"ok"})

def logout(req):
	auth.logout(req)
	return redirect('/account/login')

@login_required(login_url="/account/login")
def change_password_confirm(req):
	id=req.user.id
	profile=Profile.objects.get(user__id=id)
	return render(req,"account/change_password_confirm.html",{"profile":profile})

@login_required(login_url="/account/login")
def change_password_with_security(req):
	profile=Profile.objects.get(user__id=req.user.id)
	verify=False
	if req.method=="POST":
		security_verify=req.POST.get('security_verify',False)
		security=req.POST.get('security',"")
		if security is not "":
			if profile.security==security:
				verify=True
				return render(req,"account/change_password_with_security.html",{"profile":profile,"verify":verify})
			else:messages.error(req,"Invalid Security Question..1.!")
		else:
			if security_verify=="True":
				pwd=req.POST.get('pwd',"")
				cnfpwd=req.POST.get('cnfpwd',1)
				if pwd==cnfpwd:
					profile.user.set_password(pwd)
					profile.user.save()
					messages.success(req,mark_safe("Your password has been successfully changed <a href='/account/login'>click here to login</a>"))
					from_user=Profile.objects.get(user__username="support")
					profile=Profile.objects.get(user__username=req.user)
					inbox=Inbox.objects.create(profile=profile,from_user=from_user,sub="Your Password has been changed",msg="Hello <{}> Your Password Successfully Changed. For any help mail us on support@mps.edu".format(req.user))
					Notification.objects.create(profile=profile,mail_id=inbox.id,from_user=from_user)
				else:
					messages.error(req,"confirm password not match...!")
			else:messages.error(req,"Invalid Security Question..2.!")
	return render(req,"account/change_password_with_security.html",{"profile":profile,"verify":verify})

@login_required(login_url="/account/login")
def change_password_with_old(req):
	profile=Profile.objects.get(user__id=req.user.id)
	if req.method=="POST":
		oldpwd=req.POST['oldpwd']
		pwd=req.POST['pwd']
		cnfpwd=req.POST['cnfpwd']
		if profile.user.check_password(oldpwd):
			if pwd==cnfpwd:
				profile.user.set_password(pwd)
				profile.user.save()
				messages.success(req,mark_safe("Your password has been successfully changed <a href='/account/login'>click here to login</a>"))
				from_user=Profile.objects.get(user__username="support")
				profile=Profile.objects.get(user__username=req.user)
				inbox=Inbox.objects.create(profile=profile,from_user=from_user,sub="Your Password has been changed",msg="Hello <{}> Your Password Successfully Changed. For any help mail us on support@mps.edu".format(req.user))
				Notification.objects.create(profile=profile,mail_id=inbox.id,from_user=from_user)
			else:
				messages.error(req,"confirm password not match...!")
		else:
			messages.error(req,"Incorrect old password")
	return render(req,"account/change_password_with_old.html",{"profile":profile})

def login(req):
	if req.user.is_authenticated:
		return redirect("/")
	form=forms.LoginForm()
	if req.method=='POST':
		form=forms.LoginForm(req.POST)
		if form.is_valid():
			user=auth.authenticate(username=form.cleaned_data['email'].lower(),password=form.cleaned_data['password'])
			if user is not None:
				auth.login(req,user)
				return redirect('/home/inbox')
			else:messages.error(req,"Incorrect email ID or password")
	return render(req,'account/login.html',{'form':form})

@login_required(login_url="/account/login")
def edit_profile(req):
	id=req.user.id
	profile=Profile.objects.get(user__id=id)
	if req.method=="POST":
		fname=req.POST['fname']
		lname=req.POST['lname']
		type=req.POST['type']
		gender=req.POST['gender']
		tel=req.POST['tel']
		try:
			user=User.objects.filter(id=id).update(first_name=fname,last_name=lname)
			count=Profile.objects.filter(user__id=id).update(tel=tel,type=type,gender=gender)
			messages.success(req,"your profile has been updated")
			from_user=Profile.objects.get(user__username="support")
			profile=Profile.objects.get(user__username=req.user)
			inbox=Inbox.objects.create(profile=profile,from_user=from_user,sub="Your Profile has been Updated",msg="Hello <{}> Your Account has been Updated, For any help mail us on support@mps.edu".format(req.user))
			Notification.objects.create(profile=profile,mail_id=inbox.id,from_user=from_user)
			return redirect("/account/profile")
		except:
			messages.error(req,"error in updating data")
	return render(req,"account/edit_profile.html",{"profile":profile})

def signup(req):
	if req.user.is_authenticated:
		return redirect("/")
	form=forms.SignupForm()
	if req.method=='POST':
		name=req.POST['name'].lower()
		fname=req.POST['fname']
		lname=req.POST['lname']
		pwd=req.POST['pwd']
		try:
			user=User.objects.create_user(first_name=fname,last_name=lname,username=name,password=pwd,email=name+"@mps.edu")
			user.save()
			form=forms.SignupForm(req.POST)
			if form.is_valid():
				f=form.save(commit=False)
				f.user=user
				f.save()
				profile=user.profile
				from_user=Profile.objects.get(user__username="support")
				inbox=Inbox.objects.create(profile=profile,from_user=from_user,sub="Account successfully created",msg="Hello <{}> Your Account successfully created welcome to @mps.edu".format(user.username))
				Notification.objects.create(profile=profile,mail_id=inbox.id,from_user=from_user)
				inbox=Inbox.objects.create(profile=profile,from_user=from_user,sub="Account successfully Activated",msg="Hello <{}> Your Account is Activated, Now You Can Able to Send, Receive Email,   For any help mail us on support@mps.edu".format(user.username))
				Notification.objects.create(profile=profile,mail_id=inbox.id,from_user=from_user)
				user=auth.authenticate(username=name+"@mps.edu",password=pwd)
				auth.login(req,user)
				return redirect('/home/inbox')
				#messages.success(req,mark_safe("Account successfully created <a href='/account/login'>click here to login</a>"))
		except Exception as e:messages.error(req,"username already exist choice another one")
	return render(req,'account/signup.html',{'form':form})