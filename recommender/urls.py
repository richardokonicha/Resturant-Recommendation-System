from django.urls import path
from recommender import views

urlpatterns = [
    path('', views.index)
]
