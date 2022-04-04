from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from .models import CustomSession
from django.contrib.auth import login, authenticate
from django.core.mail import send_mail
from blogWebsite import settings
from .forms import UserRegisterForm, UserLoginForm, UserUpdateForm, ProfileUpdateForm,\
    UserPasswordResetForm, OtpVerificationForm
import random, math
from main import get_time_difference


def register(request):
    if request.method == 'POST':
        register_form = UserRegisterForm(request.POST)
        if register_form.is_valid():
            user = register_form.save()
            # print(f'user returned form save method: {user}')
            login(request, user)
            return redirect('create_profile')
    else:
        register_form = UserRegisterForm()

    return render(request, 'users/register.html', {'r_form': register_form, 'title': "Register"})


def user_login(request):
    digits = "0123456789"
    otp = ""
    for i in range(6):
        otp += digits[math.floor(random.random() * 10)]
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        user_email = request.POST.get('email')
        user_password = request.POST.get('password')
        if form.is_valid():
            user = authenticate(request, username=user_email, password=user_password)
            request.session['user'] = user.id
            if not request.session.session_key:
                request.session.save()
            request.session['key'] = request.session.session_key
            # print(request.session['user'])
            # print(f'session key: {request.session.session_key}')
            if user is not None:
                print(otp)
                new_session = CustomSession()
                new_session.session_key = request.session.session_key
                new_session.otp_field = otp
                # print(f'session object session_key: {new_session.session_key},'
                #       f' session object otp: {new_session.otp_field}')
                new_session.save()
                send_mail(
                    'OTP Verification',
                    f'Your code is : {otp}',
                    settings.EMAIL_HOST_USER,
                    [user_email],
                    fail_silently=False
                )
                return redirect('verify-otp')
            else:
                return None

    form = UserLoginForm()
    context = {
        'title': 'Login',
        'form': form,
    }
    return render(request, 'users/login.html', context=context)


def verify_otp(request):
    user = User.objects.get(id=request.session['user'])
    session_obj = CustomSession.objects.filter(session_key=request.session['key']).last()
    generated_otp = int(session_obj.otp_field)

    if request.method == 'POST':
        next_url = request.POST.get('next-url')
        user_otp = int(request.POST.get('otp_field'))
        difference_in_seconds = get_time_difference(session_obj.created_time)

        if user_otp == generated_otp and difference_in_seconds <= 30:
            if user.is_active:
                login(request, user)
                if next_url == '':
                    return redirect('blog-home')
                else:
                    return redirect(next_url)
            else:
                return None
        else:
            return render(request, 'users/login_fail.html', {'title': 'Login unsuccessful', 'time_diff':
                                                             difference_in_seconds})

    form = OtpVerificationForm()
    return render(request, 'users/verify_otp.html', {'title': 'OTP Verification', 'form': form})


@login_required(login_url='login')
def create_profile(request):
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, request.FILES)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.user = request.user
            instance.save()
            return redirect('blog-posts-list')

    form = ProfileUpdateForm()
    return render(request, 'users/create_profile.html', {'title': "Create Profile", 'form': form})


@login_required(login_url='login')
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST,
                                   request.FILES,
                                   instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            return redirect('profile')

    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

        context = {
            'title': "Profile",
            'u_form': u_form,
            'p_form': p_form
        }
        return render(request, 'users/profile.html', context=context)


def password_reset(request):
    if request.method == 'POST':
        form = UserPasswordResetForm(request.POST)
        if form.is_valid():
            try:
                user_to_update = User.objects.get(email=form.cleaned_data['email'])
            except ObjectDoesNotExist:
                return False
            user_to_update.password = make_password(form.cleaned_data['password2'])
            user_to_update.save()
            return redirect('login')

    form = UserPasswordResetForm()
    return render(request, "users/password_reset.html", {'title': "Password reset", 'form': form})
