from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.urls import reverse
from app_users.forms import RegisterForm, UserProfileForm, ExtendedProfileForm
from django.http import HttpRequest, HttpResponseRedirect

# Create your views here.
def register(request:HttpRequest):
    #POST
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return HttpResponseRedirect(reverse("home"))
    else:
        form = RegisterForm()
    #GET
    context = {"form": form}
    return render(request, "app_users/register.html", context)

@login_required
def dashboard(request: HttpRequest):
    return render(request, "app_users/dashboard.html")

@login_required
def profile(request: HttpRequest):
    user = request.user
    # POST
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=user)
        is_new_profile =False

        try:
            # will update
            extended_form = ExtendedProfileForm(request.POST, instance=user.profile)
        except:
            # will create
            extended_form = ExtendedProfileForm(request.POST)
            is_new_profile =True

        if form.is_valid() and extended_form.is_valid():
            form.save()
            if is_new_profile:
                # create
                profile = extended_form.save(commit=False)
                profile.user = user
                profile.save()
            else:
                # update
                extended_form.save()

            return HttpResponseRedirect(reverse("profile"))
    else:
        form = UserProfileForm(instance=user)
        try:
            extended_form = ExtendedProfileForm(instance=user.profile)
        except:
            extended_form = ExtendedProfileForm()

    #GET
    context = {
        "form": form,
        "extended_form": extended_form
    }
    return render(request, "app_users/profile.html", context)