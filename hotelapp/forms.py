from django import forms
from hotelapp.models import *


# class UserRegistrationForm(forms.Form):
#     email = forms.EmailField()
#     name = forms.CharField(max_length=120)

#     def clean_email(self):
#         email = self.cleaned_data.get("email")
#         if email == "abc@gmail.com":
#             raise forms.ValidationError("this is not valid")
#         return email


### UserRegistration ###

class UserRegistrationForm(forms.ModelForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control input-lg',
        'placeholder': 'enter  username....'
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control input-lg',
        'placeholder': 'enter password....'
    }))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control input-lg',
        'placeholder': 'confirm password....'
    }))

    class Meta:
        model = UserProfile
        fields = ['fname', 'email', 'image']

        widgets = {
            'fname': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'enter title...'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
            }),
            'image': forms.FileInput(attrs={
                'class': 'form-control',
            }),

        }

    def clean_username(self):
        username = self.cleaned_data.get("username")
        user = User.objects.filter(username=username)
        if user.exists():
            raise forms.ValidationError(
                "user with this username already exist")

        return username

    def clean_confirm_password(self):
        password = self.cleaned_data.get("password")
        c_password = self.cleaned_data.get("confirm_password")
        if password != c_password:
            raise forms.ValidationError("password didn't match")

        return c_password


class UserLoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control input-lg',
        'placeholder': 'username..'
    }))

    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control input-lg',
        'placeholder': 'password'
    }))
    fields = ["username", "email", "password"]


### User Registration ends ####


class HotelForm(forms.ModelForm):
    class Meta:
        model = HotelInformation
        fields = ["name", "address", "contact_no", "map_location", "email",
                  "about_us", "facebook", "featured_photo", "featured_video_link"]
        widgets = {
            'name': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'name'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'address'}),
            'contact_no': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'contact_no'}),
            'map_location': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'map_location'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'email'}),
            'about_us': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'about_us'}),
            'facebook': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'facebook_link'}),
            'featured_photo': forms.FileInput(attrs={'class': 'form-control'}),
            'featured_video_link': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'featured_video_link'}),


        }


class RoomForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = ["room_type", "size", "image", "description", "cost"]

    widgets = {
        'room_type': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'room_type'}),
        'size': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'size'}),
        'image': forms.FileInput(attrs={'class': 'form-control', 'placeholder': 'size'}),
        'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'description'}),
        'cost': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'cost'}),

    }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["commenter", "email", "comment"]
        widgets = {
            'commenter': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'email'}),
            'comment': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'comment'}),


        }


class RoomBooking(forms.ModelForm):
    class Meta:
        model = RoomBooking
        fields = [
            "check_in", "check_out", 'number_of_adult', 'number_of_childern', "totalprice"]
        widgets = {
            "number_of_adult": forms.NumberInput(attrs={'class': 'form-control'}),
            'number_of_childern': forms.NumberInput(attrs={'class': 'form-control'}),
            'check_in': forms.DateInput(format=('%m/%d/%Y'), attrs={'class': 'form-control', 'placeholder': 'Select a date', 'type': 'date'}),
            'check_out': forms.DateInput(format=('%m/%d/%Y'), attrs={'class': 'form-control', 'placeholder': 'Select a date', 'type': 'date'}),
        }


class PersonalInfo(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['fname', 'email', 'phone', 'lname']
