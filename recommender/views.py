from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.contrib.auth import login, logout
from django.views import generic
from django.views.generic.edit import CreateView, UpdateView
from django.contrib.messages.views import SuccessMessageMixin
from .forms import SignUpForm, RestaurantCreationForm
from .models import Restaurant, Dish


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


class DishListView(generic.ListView):
    model = Dish
    context_object_name = "dishes"
    template_name = "recommender/dish_list.html"
    paginate_by = 10


class DishDetailView(generic.DetailView):

    model = Dish
    context_object_name = "dish"
    template_name = "recommender/dish_detail.html"


class RestaurantListView(generic.ListView):

    paginate_by = 10
    model = Restaurant
    template_name = "recommender/restaurant_list.html"
    context_object_name = "restaurants"


class RestaurantDetailView(generic.DetailView):

    model = Restaurant
    template_name = "recommender/restaurant_detail.html"
    context_object_name = "restaurant"

    def get_context_data(self, *args, **kwargs):
        # Retrieve the restaurants top 5 dishes based on rating
        context = super().get_context_data(*args, **kwargs)
        highest_rated_dishes = self.get_object().dishes.order_by("-rating")[:5]
        context["highest_rated_dishes"] = highest_rated_dishes
        return context


class RestaurantCreateView(SuccessMessageMixin, CreateView):
    form_class = RestaurantCreationForm
    template_name = "recommender/restaurant_form.html"
    success_message = "Restaurant: %(name)s was created successfully."


class RestaurantUpdateView(UpdateView):
    form_class = RestaurantCreationForm
    template_name = "recommender/restaurant_form.html"
    model = Restaurant

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["update"] = True
        return context
