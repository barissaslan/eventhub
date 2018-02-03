from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import RegisterForm, LoginForm, ProfileForm
from django.contrib import messages
from django.contrib import messages


def login_view(request):
    form = LoginForm(request.POST or None)
    if form.is_valid():
        email = form.cleaned_data.get('email')
        password = form.cleaned_data.get('password')
        user = authenticate(email=email, password=password)
        login(request, user)
        next = request.GET.get('next')
        return redirect(next) if next else redirect('event:home')

    return render(request, "crispy/login_form.html", {"form": form, "title": "Login"})


def register_view(request):
    form = RegisterForm(request.POST or None)
    if form.is_valid():
        user = form.save(commit=False)
        password = form.cleaned_data.get('password1')
        user.set_password(password)
        user.save()
        new_user = authenticate(username=user.email, password=password)
        login(request, new_user)
        messages.success(request, "You have successfuly registered.")

        return redirect('accounts:profile')
    return render(request, "crispy/signup_form.html", {"form": form, "title": "Register"})


def logout_view(request):
    logout(request)
    return redirect('event:home')


def profile_view(request):
    form = ProfileForm(request.POST or None, instance=request.user)
    if form.is_valid():
        form.save()
        messages.success(request, "Changes has been saved")
        return redirect('accounts:profile')
    return render(request, "crispy/form.html", {"form": form, "title": "Edit Profile"})





