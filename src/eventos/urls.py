from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path
from . import views

urlpatterns = [
    path("", views.inicio, name="inicio"),
    path("login/", LoginView.as_view(template_name="eventos/login.html"), name="login"),
    path("logout/", LogoutView.as_view(next_page="inicio"), name="logout"),
    path("eventos/crear/", views.crear_evento, name="crear_evento"),
    path("<int:evento_id>/eliminar/", views.eliminar_evento, name="eliminar_evento"),
]