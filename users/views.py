from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm, UserPasswordResetForm


def register(request):
    if request.method == 'POST':
        register_form = UserRegisterForm(request.POST)
        if register_form.is_valid():
            register_form.save()
            return redirect('create_profile')

    else:
        register_form = UserRegisterForm()

    return render(request, 'users/register.html', {'r_form': register_form, 'title': "Register"})


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
