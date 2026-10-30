from django.urls import path

from . import views

urlpatterns = [
    path("", views.dashboard_view, name="dashboard"),
    path("login/", views.login_view, name="login"),
    path("teg/<int:teg_id>/", views.detalle_view, name="detalle"),
    path("upload/", views.upload_view, name="upload"),
    path("hello/", views.hello_world, name="hello-world"),
]
