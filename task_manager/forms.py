from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

from task_manager.models import Task, Tag, Position


class TaskForm(forms.ModelForm):
    # tags field to allow multiple selection of tags using checkboxes
    tags = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label="Теги завдання"
    )
    class Meta:
        model = Task
        fields = ["name", "description", "deadline", "priority", "assignees", "tags"]
        widgets = {
            # Widget for the deadline field to use a datetime-local input type
            "deadline": forms.DateTimeInput(
                attrs={
                    "type": "datetime-local",
                    "class": "form-control",
                }
            ),
        }


class WorkerCreationForm(UserCreationForm):
    position = forms.ModelChoiceField(
        queryset=Position.objects.all(),
        required=False,
        label="Position",
        empty_label="Select position..."
    )

    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        # Add standard profile fields + our position to the registration fields
        fields = UserCreationForm.Meta.fields + (
            "first_name",
            "last_name",
            "email",
            "position",
        )
