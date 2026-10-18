from django.urls import path

from datos import views

urlpatterns = [
    path("", views.index, name="index"),
]
