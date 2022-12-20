
from django import forms
from .models import Feedback,Site_User

class Site_User_Form(forms.ModelForm):
    class Meta:
        model = Site_User
        exclude = ['']

class Form_Site_User(forms.Form):
    name = forms.CharField(widget = forms.TextInput(attrs={'class':'form-control','id':'firstname','placeholder':'Name', 'autofocus':'autofocus','required': True}))
    dob = forms.CharField(widget=forms.widgets.DateInput(attrs={"type": "date",'class':'form-control','id':'dob','placeholder':'Date Of Brith'})) 
    email = forms.EmailField(widget = forms.EmailInput(attrs={'class':'form-control','id':'email','name':'email','placeholder':'Email'}))
    mobile_no = forms.IntegerField(widget = forms.TextInput(attrs={'class':'form-control','id':'mobile','name':'mobile','placeholder':'Mobile No'}))
    password1 = forms.CharField(max_length=32, widget=forms.PasswordInput(attrs={'class':'form-control','id':'password1','name':'password1','placeholder':'Password'}))
    password2 = forms.CharField(max_length=32, widget=forms.PasswordInput(attrs={'class':'form-control','id':'password2','name':'password2','placeholder':'Confirm Password'}), label="Repeat your password")

    def clean_email(self):
        email = self.cleaned_data['email']
        if Site_User.objects.filter(email=email).exists():
            raise forms.ValidationError("Email Already Exists")
        return email

    def clean_password1(self):
        if self.data['password1'] != self.data['password2']:
            raise forms.ValidationError('Passwords are not the same')
        return self.data['password1']
    
class Form_Login(forms.ModelForm):
    class Meta:
        model = Site_User
        fields = ['email','password']

class ContactForm(forms.ModelForm):
    class Meta:
        model=Feedback
        exclude=[]
        fields=['name','phone','email','message']
