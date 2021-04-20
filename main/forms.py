from django import forms
from django.forms import fields

from main.models import (
    UserDetail,
    UserPicture,
    UserSocialUrl,
    UserConfig,
    UserIssue,
    UserMessage,
    BloodRequest,
    PlasmaDonor, )
    
from django.contrib.auth.models import User

from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from PIL import Image

from django.core.files.storage import default_storage as storage


class RegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["username", "email"]

    def clean_username(self):
        """
        Validate that the supplied username is unique insensitive for the
        site.
        """
        if User.objects.filter(username__iexact=self.cleaned_data.get("username")):
            raise forms.ValidationError("A user with that username already exists.")

        return self.cleaned_data["username"]

    def clean_email(self):
        """
        Validate that the supplied email address is unique for the
        site.
        """
        if User.objects.filter(email__iexact=self.cleaned_data["email"]):
            raise forms.ValidationError("This email address is already in use. Please supply a different email address.")

        return self.cleaned_data["email"]


class blood_donor_search_form(forms.ModelForm):
    class Meta:
        model = UserDetail
        fields = ["district", "blood_group"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['district'].widget.attrs.update(name='district')
        self.fields['blood_group'].widget.attrs.update(name='blood_group')


class user_profile_edit_form(forms.ModelForm):
    class Meta:
        model = UserDetail
        fields = ["name", "status", "bio"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].required = True
        self.fields['status'].required = True


class user_complete_profile_info_form(forms.ModelForm):
    class Meta:
        model = UserDetail
        fields = ["name", "date_of_birth", "blood_group"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].required = True
        self.fields['date_of_birth'].required = True
        self.fields['blood_group'].required = True


# Settings Forms
class user_username_edit_form(forms.ModelForm):
    class Meta:
        model = User
        fields = ["username"]

    def clean_username(self):
        """
        Validate that the supplied username is unique insensitive for the
        site.
        """
        if self.instance.username.lower() == self.cleaned_data["username"].lower():
            return self.cleaned_data["username"]

        elif User.objects.filter(username__iexact=self.cleaned_data.get("username")):
            raise forms.ValidationError("A user with that username already exists.")

        return self.cleaned_data["username"]
        

class user_email_edit_form(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].required = True
    
    def clean_email(self):
        """
        Validate that the supplied email address is unique for the
        site.
        """
        if self.instance.email == self.cleaned_data["email"]:
            return self.cleaned_data["email"]

        elif User.objects.filter(email__iexact=self.cleaned_data["email"]):
            raise forms.ValidationError("This email address is already in use. Please supply a different email address.")

        return self.cleaned_data["email"]
        

class user_profile_picture_edit_form(forms.ModelForm):
    x = forms.FloatField(widget=forms.HiddenInput())
    y = forms.FloatField(widget=forms.HiddenInput())
    width = forms.FloatField(widget=forms.HiddenInput())
    height = forms.FloatField(widget=forms.HiddenInput())

    class Meta:
        model = UserPicture
        fields = ('profile_picture', 'x', 'y', 'width', 'height', )
        widgets = {
            'profile_picture': forms.FileInput,
        }

    def save(self):
        photo = super(user_profile_picture_edit_form, self).save()

        x = self.cleaned_data.get('x')
        y = self.cleaned_data.get('y')
        w = self.cleaned_data.get('width')
        h = self.cleaned_data.get('height')

        image = Image.open(photo.profile_picture)
        cropped_image = image.crop((x, y, w+x, h+y))
        resized_image = cropped_image.resize((200, 200), Image.ANTIALIAS)

        storage_path = storage.open(photo.profile_picture.name, "wb")

        resized_image.save(storage_path, 'png')

        storage_path.close()

        return photo


class user_email_config_form(forms.ModelForm):
    class Meta:
        model = UserConfig
        fields = ["show_email_address_on_profile"]


class user_userdetail_edit_form(forms.ModelForm):
    class Meta:
        model = UserDetail
        fields = ["name", "status", "bio", "date_of_birth", "blood_group"]
        
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].required = True
        self.fields['date_of_birth'].required = True
        self.fields['blood_group'].required = True
        self.fields['bio'].widget.attrs.update(placeholder='Add something in your bio')


class user_location_edit_form(forms.ModelForm):
    class Meta:
        model = UserDetail
        fields = ["address", "district"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['address'].required = True
        self.fields['district'].required = True
        

class user_location_config_form(forms.ModelForm):
    class Meta:
        model = UserConfig
        fields = ["show_address_on_profile", "show_district_on_profile"]


class user_mobile_edit_form(forms.ModelForm):
    class Meta:
        model = UserDetail
        fields = ["mobile_number"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['mobile_number'].required = True


class user_mobile_config_form(forms.ModelForm):
    class Meta:
        model = UserConfig
        fields = ["show_mobile_number_on_profile"]


class user_social_edit_form(forms.ModelForm):
    class Meta:
        model = UserSocialUrl
        fields = ["website", "facebook", "twitter", "instagram"]


class user_account_deactivate_form(forms.Form):
    password = forms.CharField(label="Password", widget=forms.PasswordInput, required=True)


class user_issue_form(forms.ModelForm):
    class Meta:
        model = UserIssue
        fields = ["category", "heading", "description", "attachment"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['description'].widget.attrs.update(placeholder='Please describe your issue properly and attach the screenshot if possible...')


class user_message_form(forms.ModelForm):
    class Meta:
        model = UserMessage
        fields = ["name", "email", "message"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['message'].widget.attrs.update(placeholder='Type your message here...')

class certificate_search_form(forms.Form):
    certificate_number = forms.CharField(max_length=50)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['certificate_number'].widget.attrs.update(placeholder='Eg: FITP-20XX-XX-XX')


class blood_request_form(forms.ModelForm):
    class Meta:
        model = BloodRequest
        fields = ["patient_name", "your_name", "district", "hospital_address", "mobile_number", "alternate_mobile_number", "blood_group_required", "units_required"]
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['hospital_address'].widget.attrs.update(placeholder='Please provide full address of hospital with distict name, state name, pincode etc...')
        self.fields['alternate_mobile_number'].widget.attrs.update(placeholder='optional')


class plasma_donor_registration_form(forms.ModelForm):
    class Meta:
        model = PlasmaDonor
        fields = ["name", "gender", "age", "blood_group", "mobile_number", "alternate_mobile_number", "email_address", "district", "address", "status"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['address'].widget.attrs.update(placeholder='Please provide full address with distict name, state name, pincode etc...')
        self.fields['alternate_mobile_number'].widget.attrs.update(placeholder='optional')
