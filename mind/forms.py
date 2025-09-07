from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User

class SignUpForm(UserCreationForm):
    """
    A custom user creation form that adds a required email field
    and styles the default fields. This form works only with the
    built-in Django User model.
    """
    email = forms.EmailField(
        max_length=254,
        required=True,
        help_text='Required. Please enter a valid email address.'
    )

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'email')

    def __init__(self, *args, **kwargs):
        """
        Add CSS classes and placeholders to the form fields for styling.
        """
        super().__init__(*args, **kwargs)
        
        self.fields['username'].widget.attrs.update({
            'class': 'form-input', 'placeholder': 'Choose a unique username'
        })
        self.fields['email'].widget.attrs.update({
            'class': 'form-input', 'placeholder': 'Enter your email address'
        })
        self.fields['password1'].widget.attrs.update({
            'class': 'form-input', 'placeholder': 'Create a strong password'
        })
        self.fields['password2'].widget.attrs.update({
            'class': 'form-input', 'placeholder': 'Confirm your password'
        })

class LoginForm(AuthenticationForm):
    """
    A custom login form to style the username and password fields.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update(
            {'class': 'form-input', 'placeholder': 'Enter your username'}
        )
        self.fields['password'].widget.attrs.update(
            {'class': 'form-input', 'placeholder': 'Enter your password'}
        )

