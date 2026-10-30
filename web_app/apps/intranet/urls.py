from django.urls import path

from apps.intranet import views

app_name = "intranet"

urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path("corvee/", views.corvee, name="corvee"),
    path("picnic/", views.picnic, name="picnic"),
]
