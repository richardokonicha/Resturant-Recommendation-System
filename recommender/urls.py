from django.urls import path
from recommender import views

app_name = "recommender"
urlpatterns = [
    path("", views.index, name="index"),
    path("sign_up/", views.sign_up, name="sign-up"),
    path("dishes/", views.dish_list, name="dishes-list"),
    path("restaurants/", views.restaurant_list, name="restaurants-list"),
    path("restaurant/create/", views.restaurant_create, name="restaurant-create"),
    path(
        "restaurant/<int:restaurant_id>/",
        views.restaurant_detail,
        name="restaurant-detail",
    ),
    path(
        "restaurant/<int:restaurant_id>/update/",
        views.restaurant_update,
        name="restaurant-update",
    ),
    path(
        "restaurant/<int:restaurant_id>/delete/",
        views.restaurant_delete,
        name="restaurant-delete",
    ),
    path(
        "restaurant/<int:restaurant_id>/dishes/",
        views.restaurant_dish_list,
        name="restaurant-dish-list",
    ),
    path(
        "restaurant/<int:restaurant_id>/dish/create",
        views.dish_create,
        name="dish-create",
    ),
    path(
        "restaurant/<int:restaurant_id>/dish/<int:dish_id>/",
        views.dish_detail,
        name="dish-detail",
    ),
    path(
        "restaurant/<int:restaurant_id>/dish/<int:dish_id>/update/",
        views.dish_update,
        name="dish-update",
    ),
    path(
        "restaurant/<int:restaurant_id>/dish/<int:dish_id>/delete/",
        views.dish_delete,
        name="dish-delete",
    ),
]
