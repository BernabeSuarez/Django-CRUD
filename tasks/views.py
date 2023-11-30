from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError
from django.utils import timezone
from .forms import TaskForm
from .models import Task


# Create your views here.
def home(request):
    return render(request, "index.html")


def signup(request):
    if request.method == "GET":
        return render(request, "signup.html", {"form": UserCreationForm})
    else:
        if request.POST["password1"] == request.POST["password2"]:
            try:
                user = User.objects.create_user(
                    username=request.POST["username"],
                    password=request.POST["password1"],
                )
                user.save()
                login(request, user)  # generar la cookie de sessionId y almacenarla
                # una vez logueado te redirecciona a la parte de crear tareas

                return redirect("/tasks/")
            except IntegrityError:
                # manejar los errores y mostrarlos
                return render(
                    request,
                    "signup.html",
                    {"form": UserCreationForm, "error": "El usuario ya existe"},
                )

    return render(
        request,
        "signup.html",
        {"form": UserCreationForm, "error": "Las contraseñas no coinciden"},
        # renderizar el error de las contraseñas diferentes
    )


def viewtasks(request):
    tasks = Task.objects.filter(
        user=request.user, datecompleted__isnull=True
    )  # mostrar solo las tareas del usuario activo

    return render(request, "tasks.html", {"tasks": tasks})


def taskdetail(request, task_id):
    if request.method == "GET":
        task = get_object_or_404(
            Task,
            pk=task_id,
            user=request.user,  # mostrar solo las tareas creadas por el usuario
        )  # mostrar un 404 si no se encuentra la pagina asi no se cae el servidor
        form = TaskForm(instance=task)
        return render(request, "task_detail.html", {"task": task, "form": form})
    else:
        try:
            task = get_object_or_404(
                Task,
                pk=task_id,
                user=request.user,  # solamente poder actualizar las tareas creada por el usuario
            )  # mostrar un 404 si no se encuentra la pagina asi no se cae el servidor
            form = TaskForm(request.POST, instance=task)
            form.save()
            return redirect("/tasks/")
        except ValueError:
            return render(
                request,
                "task_detail.html",
                {
                    "task": task,
                    "form": TaskForm,
                    "error": "La tarea no pudo ser actualizada revise la informacion",
                },
            )


def completedtask(request, task_id):
    task = get_object_or_404(
        Task,
        pk=task_id,
        user=request.user,
    )
    if request.method == "POST":
        task.datecompleted = timezone.now()
        task.save()
        return redirect("/tasks")


def deletedtask(request, task_id):
    task = get_object_or_404(
        Task,
        pk=task_id,
        user=request.user,
    )
    if request.method == "POST":
        task.delete()
        return redirect("/tasks")


def signin(request):
    if request.method == "GET":
        return render(request, "login.html", {"form": AuthenticationForm})
    else:
        user = authenticate(
            request,
            username=request.POST["username"],
            password=request.POST["password"],
        )
        if user is None:
            return render(
                request,
                "login.html",
                {
                    "form": AuthenticationForm,
                    "error": "Username or Password is incorrect",
                },
            )
        else:
            login(request, user)  # generar la cookie de sessionId y almacenarla
            # una vez logueado te redirecciona a la parte de crear tareas
            return redirect("/tasks")


def signout(request):
    logout(request)
    return redirect("/")


def createtasks(request):
    if request.method == "GET":
        return render(request, "create_tasks.html", {"form": TaskForm})
    else:
        try:
            form = TaskForm(request.POST)  # tomar los datos del formulario
            new_task = form.save(commit=False)
            new_task.user = request.user  # agregar el usuario activo a la tarea
            new_task.save()  # guardar la tarea en la BD
            return redirect("/tasks")
        except ValueError:
            return render(
                request,
                "create_tasks.html",
                {"form": TaskForm, "error": "Los Datos ingresados no son correctos"},
            )
