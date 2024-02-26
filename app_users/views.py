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
            # Register
            user: CustomUser = form.save(commit=False)
            user.is_active = False
            user.save()

            # login(request, user)

            # email body
            context = {
                "protocol": request.scheme,
                "host": request.get_host(),
                "uid64": urlsafe_base64_encode(force_bytes(user.id)),
                "token": activation_token_generator.make_token(user)
            }
            email_body = render_to_string("app_users/activate_email.html", context)

            # Send email
            email = EmailMessage(
                to=[user.email], 
                subject="Activate your account", 
                body=email_body)
            email.send()



            return HttpResponseRedirect(reverse("register_thankyou"))
    else:
        form = RegisterForm()
    #GET
    context = {"form": form}
    return render(request, "app_users/register.html", context)


def register_thankyou(request: HttpRequest):
    return render(request, "app_users/register_thankyou.html")


def activate(request:HttpRequest, uid64: str, token: str):
    title = "Thank you💕"
    status = "ยืนยันตัวตนสำเร็จ"
    description = "คุณสามารถเข้าสู่ระบบได้ทันที"

    # decode user id
    id = urlsafe_base64_decode(uid64).decode()

    try:
        user: CustomUser = CustomUser.objects.get(id=id)
        if not activation_token_generator.check_token(user, token):
            raise Exception("Check token false")
        user.is_active = True
        user.save()
    except:
        print("ยืนยันตัวตนไม่สำเร็จ")
        title = "Sorry🥲"
        status = "ยืนยันตัวตนไม่สำเร็จ"
        description = "ลิงค์หมดอายุหรือถูกใช้ไปแล้ว"

    context = {"title": title, "status": status, "description": description}
    return render(request, "app_users/activate.html", context)


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