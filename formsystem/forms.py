from django import forms
from django.contrib.auth.models import User
from .models import Student, HOD, CourseForm, SignedCourseForm

class UserRegistrationForm(forms.ModelForm):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name',  'password']

class StudentRegistrationForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['department']

class HODRegistrationForm(forms.ModelForm):
    class Meta:
        model = HOD
        fields = ['department']

class CourseFormSubmission(forms.ModelForm):
    class Meta:
        model = CourseForm
        fields = ['form_content']

    def clean_form_content(self):
        file = self.cleaned_data.get('form_content')
        if file and not file.name.endswith('.pdf'):
            raise forms.ValidationError("Only PDF files are allowed.")
        return file


