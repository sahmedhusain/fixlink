from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from users.forms import UserLoginForm
from users.models import User


def LoginUserView(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            try:
                user_obj = User.objects.get(email=email)
                username = user_obj.username
            except User.DoesNotExist:
                username = None

            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('/')
            else:
                form.add_error(None, "Invalid email or password.")
    else:
        form = UserLoginForm()
    return render(request, 'users/login.html', {'form': form})
