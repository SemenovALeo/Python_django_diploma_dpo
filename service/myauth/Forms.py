from django.contrib.auth.models import User
from django.forms import forms
from .models import Profile

class UserEditorForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']


class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['avatar']
