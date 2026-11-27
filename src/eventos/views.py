from decimal import Decimal, InvalidOperation
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from .models import Evento, Gasto


def inicio(request):
    return render(request, "eventos/inicio.html")


@login_required
def crear_evento(request):
    if request.method == "POST":
        nombre = request.POST.get("nombre", "").strip()
        if nombre:
            evento = Evento.objects.create(
                organizador=request.user,
                nombre=nombre,
            )
            return redirect("detalle_evento", evento_id=evento.id)

    eventos = Evento.objects.filter(organizador=request.user)
    return render(
        request,
        "eventos/crear_evento.html",
        {"eventos": eventos},
    )


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


@login_required
def detalle_evento(request, evento_id):
    evento = get_object_or_404(
        Evento,
        id=evento_id,
        organizador=request.user,
    )
    error = None

    if request.method == "POST":
        descripcion = request.POST.get("descripcion", "").strip()
        monto_raw = request.POST.get("monto", "").strip().replace(",", ".")
        dividir_raw = request.POST.get("dividir_entre", "1").strip()

        try:
            monto = Decimal(monto_raw)
            dividir_entre = int(dividir_raw)
            if not descripcion:
                error = "Ingresá una descripción para el gasto."
            elif monto <= 0:
                error = "El monto tiene que ser mayor a cero."
            elif dividir_entre < 1:
                error = "La cantidad para dividir tiene que ser al menos 1."
            else:
                Gasto.objects.create(
                    evento=evento,
                    cargado_por=request.user,
                    descripcion=descripcion,
                    monto=monto,
                    dividir_entre=dividir_entre,
                )
                return redirect("detalle_evento", evento_id=evento.id)
        except (InvalidOperation, ValueError):
            error = "Revisá que el monto y la cantidad sean números válidos."

    gastos = evento.gastos.all()
    total_gastado = sum((g.monto for g in gastos), Decimal("0.00"))
    return render(
        request,
        "eventos/detalle_evento.html",
        {
            "evento": evento,
            "gastos": gastos,
            "total_gastado": total_gastado,
            "error": error,
        },
    )