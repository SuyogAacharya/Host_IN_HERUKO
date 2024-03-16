from django import forms
from app.models import StudentProfile

class ProfileForm(forms.ModelForm):
    class Meta:
        model = StudentProfile
        fields = ['profile_picture']
