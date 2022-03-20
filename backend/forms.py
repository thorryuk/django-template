from django import forms
from django.forms import CharField, TextInput, EmailField, ChoiceField, Select, Textarea, FileField, \
    DecimalField, FloatField
from django.forms.fields import FloatField
from django.forms.forms import Form
from django.forms.widgets import NumberInput
from django.contrib.auth.models import User


from backend.models import UserArea, RoleGroup


class ChoiceFieldNoValidation(ChoiceField):
    def validate(self, value):
        pass


class LoginForm(forms.Form):

    email = CharField(
        error_messages={'required': 'Email tidak boleh kosong'},
        widget=TextInput(attrs={'id': 'email', 'class': 'input1 input50',
                                'placeholder': "Masukkan Email"}),
        required=True,
    )

    password = CharField(
        error_messages={'required': 'Password tidak boleh kosong'},
        strip=False,
        widget=forms.PasswordInput(attrs={'id': 'password', 'class': 'input1 input50',
                                'placeholder': "Masukkan Password"}),
        required=True,
    )


class ChangePasswordForm(forms.Form):

    old_password = CharField(
        error_messages={'required': 'Password Lama tidak boleh kosong'},
        strip=False,
        widget=forms.PasswordInput(attrs={'id': 'old_password', 'class': 'input1 input50',
                                'placeholder': "Masukkan Password Lama"}),
        required=True,
    )

    new_password = CharField(
        error_messages={'required': 'Password Baru tidak boleh kosong'},
        strip=False,
        widget=forms.PasswordInput(attrs={'id': 'new_password', 'class': 'input1 input50',
                                          'placeholder': "Masukkan Password Baru"}),
        required=True,
    )

    confirm_new_password = CharField(
        error_messages={'required': 'Password Baru tidak boleh kosong'},
        strip=False,
        widget=forms.PasswordInput(attrs={'id': 'confirm_new_password', 'class': 'input1 input50',
                                          'placeholder': "Masukkan Password Baru"}),
        required=True,
    )


class AddUserForm(forms.Form):

    GENDER_CHOICES = (('male', 'Male',), ('female', 'Female',))

    first_name = CharField(
        error_messages={'required': 'Please fill First Name Column'},
        widget=TextInput(attrs={'id': 'first_name', 'class': '', 'placeholder': ""}),
        required=True,
    )

    last_name = CharField(
        error_messages={'required': 'Please fill Last Name column'},
        widget=TextInput(attrs={'id': 'last_name', 'class': '', 'placeholder': ""}),
        required=True,
    )

    email = EmailField(
        error_messages={'required': 'Please fill Email column'},
        widget=TextInput(attrs={'id': 'email', 'class': '', 'placeholder': ""}),
        required=True,
    )

    gender = ChoiceField(
        widget=Select(),
        choices=GENDER_CHOICES,
        required=True
    )

    address = CharField(
        error_messages={'required': 'Please fill Address column'},
        widget=Textarea(attrs={'id': 'address', 'class': '', 'placeholder': ""}),
        required=True,
    )

    # phone = CharField(
    #     error_messages={'required': 'Please fill Phone Number column'},
    #     widget=TextInput(attrs={'id': 'phone', 'class': '', 'placeholder': ""}),
    #     required=True,
    # )

    # email_signature = CharField(
    #     error_messages={'required': 'Please fill Email Signature column'},
    #     widget=Textarea(attrs={'id': 'email_signature', 'class': '', 'placeholder': ""}),
    #     required=True,
    # )

    roles = ChoiceFieldNoValidation(
        widget=Select(attrs={'class': 'choice__chosen', 'id': 'name'}),
        choices=RoleGroup.objects.values_list('id', 'name').filter().order_by('id'),
        required=True
    )

    images = FileField(required=False)


class EditUserForm(forms.Form):

    GENDER_CHOICES = (('male', 'Male',), ('female', 'Female',))

    first_name = CharField(
        error_messages={'required': 'Please fill First Name Column'},
        widget=TextInput(attrs={'id': 'first_name', 'class': '', 'placeholder': ""}),
        required=True,
    )

    last_name = CharField(
        error_messages={'required': 'Please fill Last Name column'},
        widget=TextInput(attrs={'id': 'last_name', 'class': '', 'placeholder': ""}),
        required=True,
    )

    gender = ChoiceField(
        widget=Select(),
        choices=GENDER_CHOICES,
        required=True
    )

    address = CharField(
        error_messages={'required': 'Please fill Address column'},
        widget=Textarea(attrs={'id': 'address', 'class': '', 'placeholder': ""}),
        required=True,
    )

    # phone = CharField(
    #     error_messages={'required': 'Please fill Phone Number column'},
    #     widget=TextInput(attrs={'id': 'phone', 'class': '', 'placeholder': ""}),
    #     required=True,
    # )

    # email_signature = CharField(
    #     error_messages={'required': 'Please fill Email Signature column'},
    #     widget=Textarea(attrs={'id': 'email_signature', 'class': '', 'placeholder': ""}),
    #     required=True,
    # )

    roles = ChoiceField(
        widget=Select(),
        choices=RoleGroup.objects.values_list('id', 'name').filter().order_by('id'),
        required=True
    )

    images = FileField(required=False)


class NewRoleForm(forms.Form):
    name = CharField(
        error_messages={'required': 'Please fill Name Column'},
        widget=TextInput(attrs={'id': 'name', 'class': '', 'placeholder': ""}),
        required=True,
    )

    description = CharField(
        error_messages={'required': 'Please fill Description Column'},
        widget=TextInput(attrs={'id': 'description', 'class': '', 'placeholder': ""}),
        required=True,
    )

class ProfileForm(forms.Form):

    GENDER_CHOICES = (('male', 'Male',), ('female', 'Female',))

    first_name = CharField(
        error_messages={'required': 'Please fill First Name Column'},
        widget=TextInput(attrs={'id': 'first_name', 'class': '', 'placeholder': ""}),
        required=True,
    )

    last_name = CharField(
        error_messages={'required': 'Please fill Last Name column'},
        widget=TextInput(attrs={'id': 'last_name', 'class': '', 'placeholder': ""}),
        required=True,
    )

    gender = ChoiceField(
        widget=Select(),
        choices=GENDER_CHOICES,
        required=True
    )

    address = CharField(
        error_messages={'required': 'Please fill Address column'},
        widget=Textarea(attrs={'id': 'address', 'class': '', 'placeholder': ""}),
        required=True,
    )

    phone = CharField(
        error_messages={'required': 'Please fill Phone Number column'},
        widget=TextInput(attrs={'id': 'phone', 'class': '', 'placeholder': ""}),
        required=True,
    )

    email_signature = CharField(
        error_messages={'required': 'Please fill Email Signature column'},
        widget=Textarea(attrs={'id': 'email_signature', 'class': '', 'placeholder': ""}),
        required=True,
    )
