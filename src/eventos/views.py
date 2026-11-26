from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render, get_object_or_404
from .models import Evento


def inicio(request):
    return render(request, "eventos/inicio.html")


@login_required
def crear_evento(request):
    if request.method == "POST":
        nombre = request.POST.get("nombre", "").strip()
        if nombre:
            Evento.objects.create(
                organizador=request.user,
                nombre=nombre,
            )
            return redirect("crear_evento")

    eventos = Evento.objects.filter(organizador=request.user)
    return render(request,"eventos/crear_evento.html",{"eventos": eventos},)

@login_required
def eliminar_evento(request, evento_id):
    if request.method == "POST":
        evento = get_object_or_404(
            Evento,
            id=evento_id,
            organizador=request.user,
        )
        evento.delete()
    return redirect("crear_evento")