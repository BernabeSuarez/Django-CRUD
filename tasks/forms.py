from django.forms import ModelForm, TextInput, Textarea
from .models import Task


class TaskForm(ModelForm):
    class Meta:
        model = Task
        fields = ["title", "description", "important"]
        # widget para pasar atributos a los inputs como clases placeholders,etc
        widgets = {
            "title": TextInput(
                attrs={"placeholder": "Titulo de la tarea", "class": "form-control"}
            ),
            "description": Textarea(
                attrs={
                    "placeholder": "Descripcion de la tarea",
                    "class": "form-control",
                }
            ),
        }
