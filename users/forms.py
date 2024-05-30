from django import forms
from django.contrib.auth.models import User, Group


class UserModeratorForm(forms.ModelForm):
    is_moderator = forms.BooleanField(label='Is Moderator', required=False)

    class Meta:
        model = User
        fields = ['is_moderator']
