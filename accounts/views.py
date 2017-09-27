from django.shortcuts import render, redirect

from django.contrib.auth import (
authenticate,
get_user_model,
login,
logout
)
from accounts.form import UserLoginForm, UserRegisterForm
def login_view(request):
    # print(request.user.is_authenticate())
    next = request.GET.get("next")
    title = "Login"
    form = UserLoginForm(request.POST or None)
    if form.is_valid():
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")
        user = authenticate(username=username, password=password)

        login(request, user)
        if next:
            return redirect(next)
        return redirect("/")
    return render(request, "form.html", {"form": form, "title": title})

def register_view(request):
    # print(request.user.is_authenticate())
    title = "Register"
    next = request.GET.get("next")
    form = UserRegisterForm(request.POST or None)
    if form.is_valid():
        user = form.save(commit=False)
        password = form.cleaned_data.get("password")
        user.set_password(password)
        user.save()
        new_user = authenticate(user=user.username, password=password)
        login(request, new_user)
        if next:
            return redirect(next)
        return redirect("/")

    content = {
        "form": form,
        "title": title,
    }
    return render(request, "form.html", content)

def logout_view(request):
    logout(request)
    return redirect("/")
