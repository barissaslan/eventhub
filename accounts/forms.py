from django.contrib.auth import authenticate
from accounts.models import User
from django import forms


class RegisterForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password Confirmation', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = [
            'email',
            'password1',
            'password2',
        ]

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2


class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)

    def clean(self):
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')
        if email and password:
            user = authenticate(email=email, password=password)
            if not user:
                raise forms.ValidationError("This user does not exist")
        return super(LoginForm, self).clean()


class ProfileForm(forms.ModelForm):
    email = forms.EmailField(disabled=True, required=False)

    class Meta:
        model = User
        fields = [
            'email',
            'first_name',
            'last_name',
            'cell_phone',
            'date_of_birth',
        ]
