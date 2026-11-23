from django.contrib.auth.decorators import login_required
from django.shortcuts import render


def inicio(request):
    return render(request, "eventos/inicio.html")


@login_required
def crear_evento(request):
    return render(request, "eventos/crear_evento.html")