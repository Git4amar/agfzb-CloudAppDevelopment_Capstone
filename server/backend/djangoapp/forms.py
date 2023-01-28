from django import forms
from django.contrib.auth import get_user_model
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, Field
from crispy_forms.bootstrap import StrictButton
from crispy_bootstrap5.bootstrap5 import FloatingField


class RegistrationForm(forms.ModelForm):

    # definition
    class Meta:
        model = get_user_model()
        fields = ['username', 'first_name', 'last_name', 'password']
    
    # define form instance
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # define crispy form
        self.helper = FormHelper()
        self.helper.method = 'POST'
        self.helper.action = 'djangoapp:registration'

        # define form layout
        self.helper.layout = Layout(
            FloatingField(
                'username',
                'first_name',
                'last_name',
                'password',
            ),
            StrictButton('Sign Up', type='submit', css_class='mt-4 btn btn-primary w-auto position-relative start-50 top-50 translate-middle')
        )

    username = forms.CharField(
        label = 'Username',
        required = True,
        widget = forms.TextInput(attrs={'autofocus': 'autofocus'})
    )
    
    first_name = forms.CharField(
        label = 'First Name',
        required = True,
    )

    last_name = forms.CharField(
        label = 'Last Name',
        required = True,
    )

    password = forms.CharField(
        label = 'Password',
        required = True,
        widget = forms.PasswordInput()
    )