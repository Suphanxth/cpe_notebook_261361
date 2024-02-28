from django.core.mail import EmailMessage
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.template.loader import render_to_string
from django.urls import reverse
from app_users.forms import RegisterForm, UserProfileForm, ExtendedProfileForm
from django.http import HttpRequest, HttpResponseRedirect
from app_users.models import CustomUser
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from app_users.utils.activation_token_generator import activation_token_generator

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
    favourite_notebook_pivots = request.user.favourite_notebook_pivot_set.order_by("level")
    context = {"favourite_notebook_pivots": favourite_notebook_pivots}
    return render(request, "app_users/dashboard.html", context)


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

            response = HttpResponseRedirect(reverse("profile"))
            response.set_cookie("is_saved", "1")
            return response
    else:
        form = UserProfileForm(instance=user)
        try:
            extended_form = ExtendedProfileForm(instance=user.profile)
        except:
            extended_form = ExtendedProfileForm()

    #GET
    is_saved = request.COOKIES.get("is_saved") == "1"
    flash_massage = "บันทึกเรียบร้อย✅" if is_saved else None
    context = {
        "form": form,
        "extended_form": extended_form,
        "flash_massage": flash_massage,
    }
    response = render(request, "app_users/profile.html", context)
    if is_saved:
        response.delete_cookie("is_saved")
    return response