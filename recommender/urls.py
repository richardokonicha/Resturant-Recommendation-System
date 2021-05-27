from django.urls import path
from recommender import views

app_name = "recommender"
urlpatterns = [
    path("", views.index, name="index"),
    path("sign_up", views.sign_up, name="sign_up"),
]
