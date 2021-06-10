from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.urls.base import reverse
from django.core.paginator import Paginator

from .forms import SignUpForm, RestaurantCreationForm, DishCreationForm
from .models import Restaurant, Dish
from .permissions import is_staff

PAGINATE_COUNT = 10  # Number of items to show on a page


def index(request):
    return render(request, "recommender/index.html")


def sign_up(request):
    # log out an already existing user if they try accessing this endpoint
    if request.user.is_authenticated:
        logout(request)
        return redirect("recommender:sign-up")

    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return HttpResponseRedirect("/")
    else:
        form = SignUpForm()
    return render(request, "recommender/sign_up.html", context={"form": form})


def dish_list(request):
    dishes = Dish.objects.all()
    paginator = Paginator(dishes, PAGINATE_COUNT)

    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(
        request,
        "recommender/dish_list.html",
        {"page_obj": page_obj},
    )


def restaurant_dish_list(request, restaurant_id):
    restaurant = get_object_or_404(Restaurant, id=restaurant_id)
    dishes = restaurant.dishes.all()

    paginator = Paginator(dishes, PAGINATE_COUNT)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(
        request,
        "recommender/dish_list.html",
        context={
            "restaurant": restaurant,
            "page_obj": page_obj,
            "restaurant": restaurant,
        },
    )


@login_required
@user_passes_test(is_staff)
def dish_create(request, restaurant_id):
    restaurant = get_object_or_404(Restaurant, id=restaurant_id)

    if request.method == "POST":
        form = DishCreationForm(request.POST)
        if form.is_valid():
            # Temporarily save the object and register its restaurant
            dish = form.save(commit=False)
            dish.restaurant = restaurant
            dish.save()
            return redirect(
                "recommender:dish-detail", restaurant_id=restaurant.id, dish_id=dish.id
            )
    else:
        form = DishCreationForm()
    return render(
        request,
        "recommender/dish_form.html",
        context={"restaurant": restaurant, "form": form, "update": False},
    )


def dish_detail(request, restaurant_id, dish_id):
    restaurant = get_object_or_404(Restaurant, id=restaurant_id)
    dish = get_object_or_404(Dish, id=dish_id)
    return render(
        request,
        "recommender/dish_detail.html",
        context={"restaurant": restaurant, "dish": dish},
    )


@login_required
@user_passes_test(is_staff)
def dish_update(request, restaurant_id, dish_id):
    restaurant = get_object_or_404(Restaurant, id=restaurant_id)
    dish = get_object_or_404(Dish, id=dish_id)

    if request.method == "POST":
        form = DishCreationForm(request.POST, instance=dish)
        if form.is_valid():
            dish = form.save()
            return redirect(dish)
    else:
        form = DishCreationForm(instance=dish)
    return render(
        request,
        "recommender/dish_form.html",
        {"restaurant": restaurant, "form": form, "update": True, "dish": dish},
    )


@login_required
@user_passes_test(is_staff)
def dish_delete(request, restaurant_id, dish_id):
    restaurant = get_object_or_404(Restaurant, id=restaurant_id)
    dish = get_object_or_404(Dish, id=dish_id)
    if request.method == "POST":
        dish.delete()
        return redirect("recommender:restaurant-dish-list", restaurant_id=restaurant.id)
    else:
        return render(
            request,
            "recommender/dish_confirm_delete.html",
            context={"dish": dish},
        )


def restaurant_list(request):
    restaurants = Restaurant.objects.all()
    paginator = Paginator(restaurants, PAGINATE_COUNT)

    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(
        request,
        "recommender/restaurant_list.html",
        {"page_obj": page_obj},
    )


@login_required
@user_passes_test(is_staff)
def restaurant_create(request):

    if request.method == "POST":
        form = RestaurantCreationForm(request.POST)
        if form.is_valid():
            restaurant = form.save()
            return redirect(restaurant)
    else:
        form = RestaurantCreationForm()
    return render(
        request,
        "recommender/restaurant_form.html",
        context={"form": form, "update": False},
    )


def restaurant_detail(request, restaurant_id):

    restaurant = get_object_or_404(Restaurant, id=restaurant_id)
    # Get the 5 highest rated dishes by the restaurant
    highest_rated_dishes = restaurant.dishes.order_by("-rating")[:5]

    return render(
        request,
        "recommender/restaurant_detail.html",
        context={
            "restaurant": restaurant,
            "highest_rated_dishes": highest_rated_dishes,
        },
    )


@login_required
@user_passes_test(is_staff)
def restaurant_update(request, restaurant_id):
    restaurant = get_object_or_404(Restaurant, id=restaurant_id)
    if request.method == "POST":
        form = RestaurantCreationForm(request.POST, instance=restaurant)
        if form.is_valid():
            restaurant = form.save()
            return redirect(restaurant)
    else:
        form = RestaurantCreationForm(instance=restaurant)

    return render(
        request,
        "recommender/restaurant_form.html",
        context={"form": form, "update": True, "restaurant": restaurant},
    )


@login_required
@user_passes_test(is_staff)
def restaurant_delete(request, restaurant_id):
    restaurant = get_object_or_404(Restaurant, id=restaurant_id)
    if request.method == "POST":
        restaurant.delete()
        return redirect("recommender:restaurants-list")
    else:
        return render(
            request,
            "recommender/restaurant_confirm_delete.html",
            context={"restaurnat": restaurant},
        )
