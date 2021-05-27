from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.contrib.auth import login, logout
from recommender.forms import SignUpForm


def index(request):
    return render(request, "recommender/index.html")


def sign_up(request):
    # log out an already existing user if they try accessing this endpoint
    if request.user.is_authenticated:
        logout(request)
        return redirect("recommender:sign_up")

    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return HttpResponseRedirect("/")
    else:
        form = SignUpForm()
    return render(request, "recommender/sign_up.html", context={"form": form})
