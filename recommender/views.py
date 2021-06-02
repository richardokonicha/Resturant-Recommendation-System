from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect
from django.contrib.auth import login, logout
from django.views import generic
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin

from .forms import SignUpForm, RestaurantCreationForm, DishCreationForm
from .models import Restaurant, Dish
from .permissions import IsStaffMixin


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


class DishCreateView(LoginRequiredMixin, IsStaffMixin, CreateView):

    form_class = DishCreationForm
    template_name = "recommender/dish_form.html"

    def dispatch(self, request, *args, **kwargs):
        self.restaurant = get_object_or_404(Restaurant, pk=self.kwargs["restaurant_id"])
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["restaurant"] = self.restaurant
        return context

    def form_valid(self, form):
        form.instance.restaurant = self.restaurant
        return super().form_valid(form)


class DishListView(generic.ListView):
    model = Dish
    context_object_name = "dishes"
    template_name = "recommender/dish_list.html"
    paginate_by = 10


class DishDetailView(generic.DetailView):
    def dispatch(self, request, *args, **kwargs):
        self.restaurant = get_object_or_404(Restaurant, pk=self.kwargs["restaurant_id"])
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["restaurant"] = self.restaurant
        return context

    model = Dish
    pk_url_kwarg = "dish_id"
    context_object_name = "dish"
    template_name = "recommender/dish_detail.html"


class DishUpdateView(LoginRequiredMixin, IsStaffMixin, UpdateView):

    model = Dish
    pk_url_kwarg = "dish_id"
    form_class = DishCreationForm
    template_name = "recommender/dish_form.html"

    def dispatch(self, request, *args, **kwargs):
        self.restaurant = get_object_or_404(Restaurant, pk=self.kwargs["restaurant_id"])
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["restaurant"] = self.restaurant
        context["update"] = True
        return context


class DishDeleteView(LoginRequiredMixin, IsStaffMixin, DeleteView):
    def dispatch(self, request, *args, **kwargs):
        self.restaurant = get_object_or_404(Restaurant, pk=self.kwargs["restaurant_id"])
        return super().dispatch(request, *args, **kwargs)

    model = Dish
    pk_url_kwarg = "dish_id"
    template_name = "recommender/dish_confirm_delete.html"

    def get_success_url(self, *args, **kwargs):
        return reverse_lazy(
            "recommender:restaurant-dish-list",
            kwargs={"restaurant_id": self.restaurant.id},
        )


class RestaurantDishList(generic.ListView):

    template_name = "recommender/dish_list.html"
    context_object_name = "dishes"

    def get_queryset(self, *args, **kwargs):

        self.restaurant = get_object_or_404(Restaurant, pk=self.kwargs["restaurant_id"])
        return self.restaurant.dishes.all()

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["restaurant"] = self.restaurant
        return context


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


class RestaurantCreateView(
    LoginRequiredMixin, IsStaffMixin, SuccessMessageMixin, CreateView
):
    form_class = RestaurantCreationForm
    template_name = "recommender/restaurant_form.html"
    success_message = "Restaurant: %(name)s was created successfully."


class RestaurantUpdateView(LoginRequiredMixin, IsStaffMixin, UpdateView):
    form_class = RestaurantCreationForm
    template_name = "recommender/restaurant_form.html"
    model = Restaurant

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["update"] = True
        return context


class RestaurantDeleteView(LoginRequiredMixin, IsStaffMixin, DeleteView):
    model = Restaurant
    template_name = "recommender/restaurant_confirm_delete.html"
    success_url = reverse_lazy("recommender:restaurants-list")
    context_object_name = "restaurant"
