from django import forms
from .models import User
from django.contrib.auth import password_validation
from django.utils.translation import ugettext_lazy as _

class RegistrationForm(forms.ModelForm):
    password1 = forms.CharField(label=_("Password"), strip=False, widget=forms.PasswordInput)
    password2 = forms.CharField(label=_("Confirm password"), strip=False, widget=forms.PasswordInput)

    class Meta:
        fields = ('username', 'email', 'password1', 'password2')
        model = User

    def clean_password1(self):
        self.instance.username = self.cleaned_data.get('username')
        password_validation.validate_password(self.cleaned_data.get('password1'), self.instance)
        return self.cleaned_data.get('password1')

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                _("The password fields didn't match.")
            )
        return password2

    def save(self, commit=True):
        user = super(RegistrationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])

        if commit:
            user.is_active = True
            user.save()
        elif commit:
            user.save()
        return user