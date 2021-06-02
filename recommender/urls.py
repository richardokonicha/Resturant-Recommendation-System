from django.urls import path
from recommender import views

app_name = "recommender"
urlpatterns = [
    path("", views.index, name="index"),
    path("sign_up/", views.sign_up, name="sign-up"),
    path("dishes/", views.DishListView.as_view(), name="dishes-list"),
    path("restaurants/", views.RestaurantListView.as_view(), name="restaurants-list"),
    path(
        "restaurant/create/",
        views.RestaurantCreateView.as_view(),
        name="restaurant-create",
    ),
    path(
        "restaurant/<int:pk>/",
        views.RestaurantDetailView.as_view(),
        name="restaurant-detail",
    ),
    path(
        "restaurant/<int:pk>/update/",
        views.RestaurantUpdateView.as_view(),
        name="restaurant-update",
    ),
    path(
        "restaurant/<int:pk>/delete/",
        views.RestaurantDeleteView.as_view(),
        name="restaurant-delete",
    ),
    path(
        "restaurant/<int:restaurant_id>/dish/create",
        views.DishCreateView.as_view(),
        name="dish-create",
    ),
    path(
        "restaurant/<int:restaurant_id>/dish/<int:dish_id>/",
        views.DishDetailView.as_view(),
        name="dish-detail",
    ),
    path(
        "restaurant/<int:restaurant_id>/dish/<int:dish_id>/update/",
        views.DishUpdateView.as_view(),
        name="dish-update",
    ),
]
