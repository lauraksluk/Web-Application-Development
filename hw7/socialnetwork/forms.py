from django import forms
from socialnetwork.models import *
from django.contrib.auth.models import User
from django.contrib.auth import authenticate


class LoginForm(forms.Form):
    username = forms.CharField(max_length = 20, widget=forms.TextInput(attrs={'style': 'font-size: 18px',}))
    password = forms.CharField(max_length = 200, widget = forms.PasswordInput(attrs={'style': 'font-size: 18px',}))

    # Customizes form validation for properties that apply to more
    # than one field.  Overrides the forms.Form.clean function.
    def clean(self):
        # Calls our parent (forms.Form) .clean function, gets a dictionary
        # of cleaned data as a result
        cleaned_data = super().clean()

        # Confirms that the two password fields match
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        if not user:
            raise forms.ValidationError("Invalid username/password")

        # We must return the cleaned data we got from our parent.
        return cleaned_data


class RegisterForm(forms.Form):
    username = forms.CharField(max_length = 20, widget=forms.TextInput(attrs={'style': 'font-size: 18px',}))
    password = forms.CharField(max_length = 200, widget = forms.PasswordInput(attrs={'style': 'font-size: 18px',}))
    confirm_password = forms.CharField(max_length = 200, widget = forms.PasswordInput(attrs={'style': 'font-size: 18px',}))
    email = forms.CharField(max_length = 20, widget=forms.TextInput(attrs={'style': 'font-size: 18px',}))
    first_name = forms.CharField(max_length = 20, widget=forms.TextInput(attrs={'style': 'font-size: 18px',}))
    last_name = forms.CharField(max_length = 20, widget=forms.TextInput(attrs={'style': 'font-size: 18px',}))

    # Customizes form validation for properties that apply to more
    # than one field.  Overrides the forms.Form.clean function.
    def clean(self):
        # Calls our parent (forms.Form) .clean function, gets a dictionary
        # of cleaned data as a result
        cleaned_data = super().clean()

        # Confirms that the two password fields match
        password1 = cleaned_data.get('password')
        password2 = cleaned_data.get('confirm_password')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords did not match.")

        # We must return the cleaned data we got from our parent.
        return cleaned_data

    # Customizes form validation for the username field.
    def clean_username(self):
        # Confirms that the username is not already present in the
        # User model database.
        username = self.cleaned_data.get('username')
        if User.objects.filter(username__exact=username):
            raise forms.ValidationError("Username is already taken.")

        # We must return the cleaned data we got from the cleaned_data
        # dictionary
        return username

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('bio', 'picture')
        widgets = {
            'bio': forms.Textarea(attrs={'id':'id_bio_input_text', 'rows': '3'}),
            'picture': forms.FileInput(attrs={'id':'id_profile_picture'})
        }
        labels = {
            'bio': "Bio",
            'picture': "Upload image"
        }
    
    def clean_picture(self):
        picture = self.cleaned_data['picture']
        #if not picture or not hasattr(picture, 'con')
        return picture

