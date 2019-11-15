from django import forms
from .models import Profile
class LoginForm(forms.Form):
	email=forms.CharField(widget=forms.TextInput(attrs={'class':"form-control",'placeholder':"Enter your mps email ID",'autocomplete':"off"}))
	password=forms.CharField(widget=forms.PasswordInput(attrs={'class':"form-control",'placeholder':"Enter your password",'autocomplete':"off"}))
	def clean_email(self):
		email=self.cleaned_data['email']
		if not email.endswith('@mps.edu'):
			print("ValidationError")
			raise forms.ValidationError('Entered email address is not an mps email id')
		return email
class SignupForm(forms.ModelForm):
	class Meta:
		model=Profile
		exclude=['user','email','pic']
		widgets={
				'tel':forms.TextInput(attrs={'class':"form-control",'placeholder':"enter your phone no..",'autocomplete':"off"}),
				'security':forms.TextInput(attrs={'class':"form-control",'placeholder':"this helps to reset your password",'type':"password",'autocomplete':"off"})
		}
		labels = {
        "tel": "Phone no.",
        "security":"Security Question"
    }
