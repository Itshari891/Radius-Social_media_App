from django.forms import Form,ModelForm
from django import forms
from django.contrib.auth.models import User


class SignupForm(ModelForm):
    password2=forms.CharField(label=False,widget=forms.PasswordInput(attrs={"name":"password2","placeholder":"Confirm Password", "class":"bg-gray-200 mb-2 shadow-none  dark:bg-gray-800", "style":"border: 1px solid #d3d5d8 !important;"}))
    email=forms.EmailField(label=False,required=True,widget=forms.EmailInput(attrs={"name":"email","placeholder":"Email" ,"class":"bg-gray-200 mb-2 shadow-none  dark:bg-gray-800" ,"style":"border: 1px solid #d3d5d8 !important;"}))
    class Meta:
        model= User
        fields=[
            "username","email","password","password2",
        ]
        widgets={
            "username":forms.TextInput(attrs={"name":"username","placeholder":"Username" ,"class":"bg-gray-200 mb-2 shadow-none  dark:bg-gray-800" ,"style":"border: 1px solid #d3d5d8 !important;"}),
            
            "password":forms.PasswordInput(attrs={"name":"password","placeholder":"Password" ,"class":"bg-gray-200 mb-2 shadow-none  dark:bg-gray-800" ,"style":"border: 1px solid #d3d5d8 !important;"}),
            }
        labels={
            "username" :"",
            "email":"",
            "password":""
        }
        help_texts = {
            'username': None,
        }

class SigninForm(Form):
    username=forms.CharField(label=False,max_length=100,widget=forms.TextInput(attrs={"type":"text","name":"username","placeholder":"Username" ,"class":"bg-gray-200 mb-2 shadow-none dark:bg-gray-800" ,"style":"border: 1px solid #d3d5d8 !important;"}))
    password=forms.CharField(label=False,widget= forms.PasswordInput(attrs={"type":"password","name":"password","placeholder":"password" , "class":"bg-gray-200 mb-2 shadow-none dark:bg-gray-800", "style":"border: 1px solid #d3d5d8 !important;"}))