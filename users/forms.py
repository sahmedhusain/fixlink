from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction
from django.core.exceptions import ValidationError

from .models import User, Company, Customer


class DateInput(forms.DateInput):
    input_type = 'date'


def validate_email(value):
    # In case the email already exists in an email input in a registration form, this function is fired
    if User.objects.filter(email=value).exists():
        raise ValidationError(
            value + " is already taken.")


class CustomerSignUpForm(UserCreationForm):
    email = forms.EmailField(required=True, validators=[validate_email])
    birth = forms.DateField(widget=DateInput(), required=True, label='Date of Birth')

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'email', 'birth')

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_customer = True
        user.email = self.cleaned_data.get('email')
        user.save()
        Customer.objects.create(user=user, birth=self.cleaned_data.get('birth'))
        return user


class CompanySignUpForm(UserCreationForm):
    email = forms.EmailField(required=True, validators=[validate_email])
    field = forms.ChoiceField(
        choices=(('Air Conditioner', 'Air Conditioner'),
                 ('All in One', 'All in One'),
                 ('Carpentry', 'Carpentry'),
                 ('Electricity', 'Electricity'),
                 ('Gardening', 'Gardening'),
                 ('Home Machines', 'Home Machines'),
                 ('House Keeping', 'House Keeping'),
                 ('Interior Design', 'Interior Design'),
                 ('Locks', 'Locks'),
                 ('Painting', 'Painting'),
                 ('Plumbing', 'Plumbing'),
                 ('Water Heaters', 'Water Heaters')),
        required=True,
        label='Field of Work'
    )

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'email', 'field')

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_company = True
        user.email = self.cleaned_data.get('email')
        user.save()
        Company.objects.create(user=user, field=self.cleaned_data.get('field'))
        return user


class UserLoginForm(forms.Form):
    email = forms.EmailField(widget=forms.TextInput(
        attrs={'placeholder': 'Enter Email'}))
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Enter Password'}))

    def __init__(self, *args, **kwargs):
        super(UserLoginForm, self).__init__(*args, **kwargs)
        self.fields['email'].widget.attrs['autocomplete'] = 'off'
