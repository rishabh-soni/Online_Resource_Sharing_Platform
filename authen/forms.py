from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from .models import CustomUser


class SignUpForm(UserCreationForm):
    full_name = forms.CharField(max_length=100, help_text='Required. 100 characters or fewer.')
    phone_no = forms.CharField(max_length=100, help_text='Required. 10 digits.')
    email = forms.EmailField(help_text='Required.')

    class Meta:
        model = CustomUser
        fields = UserCreationForm.Meta.fields + ('full_name', 'phone_no', 'email',)


class ContactForm(forms.Form):
    name = forms.CharField(max_length=500, label="Name")
    email = forms.EmailField(max_length=500, label="Email")
    subject = forms.CharField(max_length=500, label="Subject")
    message = forms.CharField(label='Message', widget=forms.Textarea(
        attrs={'placeholder': 'Your Message Here'}))
