from django.urls import path
from recommender import views

app_name = "recommender"
urlpatterns = [
    path("", views.index, name="index"),
    path("sign_up/", views.sign_up, name="sign-up"),
    path("restaurants/", views.RestaurantListView.as_view(), name="restaurants-list"),
    path(
        "restaurant/create/",
        views.RestaurantCreateView.as_view(),
        name="restaurant-create",
    ),
    path("dishes/", views.DishListView.as_view(), name="dishes-list"),
    path(
        "restaurant/<int:pk>/",
        views.RestaurantDetailView.as_view(),
        name="restaurant-detail",
    ),
    path(
        "restaurant/<int:pk>/update",
        views.RestaurantUpdateView.as_view(),
        name="restaurant-update",
    ),
    path(
        "restaurant/dish/<int:pk>/", views.DishDetailView.as_view(), name="dish-detail"
    ),
]
