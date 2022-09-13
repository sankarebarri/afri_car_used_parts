from django.shortcuts import render, redirect
from . forms import RegistrationForm
def registration(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("username")
            # messages.success(request, f"{username} successfully created")
            return redirect("login")
    else:
        form = RegistrationForm()

    context = {
        "form": form,
    }

    return render(request, "users/registration.html", context)
