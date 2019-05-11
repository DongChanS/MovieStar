from .models import Profile
from django import forms
from django.contrib.auth import get_user_model

class ProfileModelForm(forms.ModelForm):
    
    class Meta:
        model = Profile
        fields = ['age','description','nickname','profile_image']
        
class CustomUserChangeForm(forms.ModelForm):
    
    class Meta:
        model = get_user_model()
        fields = ['username','email']