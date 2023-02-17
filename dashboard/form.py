from django import forms
from .models import Pointers
from .validator import text_validate
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User



class pointer_form(forms.ModelForm):
    class Meta:
        model = Pointers
        fields = ["title", "longitude", "latitude", "typee","filee","station_id","terminal_id"]

    def clean_title(self):
        title = self.cleaned_data['title']
        if text_validate(title):
            raise ValidationError("Invalid title please enter only alphabet ")

        return title


class user_form(forms.ModelForm):
   confirm_password = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)
   class Meta:
       model = User
       fields = ["username", "password", "first_name", "last_name"]

   def clean_confirm_password(self):
       confirm_password = self.cleaned_data['confirm_password']
       password = self.cleaned_data['password']

       if password != confirm_password:
           raise ValidationError("The two password fields didn’t match.")
       return confirm_password


   def clean_first_name(self):
       first_name = self.cleaned_data['first_name']
       if text_validate(first_name):
           raise ValidationError("Invalid first name please enter only alphabet ")

       return first_name

   def clean_last_name(self):
       last_name = self.cleaned_data['last_name']
       if text_validate(last_name):
           raise ValidationError("Invalid last name please enter only alphabet ")

       return last_name






class user_update_form(forms.ModelForm):
   class Meta:
       model = User
       fields = ["username", "first_name", "last_name"]

   def clean_first_name(self):
       first_name = self.cleaned_data['first_name']
       if text_validate(first_name):
           raise ValidationError("Invalid first name please enter only alphabet ")

       return first_name

   def clean_last_name(self):
       last_name = self.cleaned_data['last_name']
       if text_validate(last_name):
           raise ValidationError("Invalid last name please enter only alphabet ")

       return last_name


