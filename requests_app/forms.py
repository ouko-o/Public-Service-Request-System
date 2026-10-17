from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User

from .models import ServiceRequest


class BootstrapFormMixin:
    """Adds Bootstrap classes to every field so forms look consistent."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            if isinstance(field.widget, forms.Select):
                field.widget.attrs["class"] = "form-select"
            else:
                field.widget.attrs["class"] = "form-control"


class RegistrationForm(BootstrapFormMixin, UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("username", "email")


class LoginForm(BootstrapFormMixin, AuthenticationForm):
    pass


class ServiceRequestForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = ServiceRequest
        fields = ("category", "location", "description", "image")
        widgets = {
            "location": forms.TextInput(
                attrs={"placeholder": "e.g. Kamau Street, Thika"}
            ),
            "description": forms.Textarea(
                attrs={"rows": 4, "placeholder": "Describe the problem"}
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["category"].empty_label = "Select a category"


class StatusUpdateForm(forms.ModelForm):
    class Meta:
        model = ServiceRequest
        fields = ("status",)