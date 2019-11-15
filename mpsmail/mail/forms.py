from django import forms
from .models import Sentmail

class CreatemailForm(forms.ModelForm):
	class Meta:
		model=Sentmail
		fields=['msg','sub','attach']
		labels = {
            "sub":"Subject",
            "msg":"Message",
            "attach":"Attach File"
        }
		widgets={
			'sub':forms.TextInput(attrs={'class':"form-control"}),
			#'msg':forms.Textarea(attrs={'cols':"50"})
			'attach':forms.FileInput(attrs={'class':"form-control-file"})
			}

