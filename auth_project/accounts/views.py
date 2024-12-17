from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required


def home(request):
    # If user is already authenticated, redirect to dashboard
    if request.user.is_authenticated:
        return redirect('dashboard')
    return render(request, 'accounts/home.html') 


# User registration view
from django.contrib.auth.models import Group

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            
            # Ensure the 'User' group exists
            group, created = Group.objects.get_or_create(name='User')
            user.groups.add(group)  # Add the user to the 'User' group
            
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'accounts/register.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('dashboard')
    else:
        form = AuthenticationForm()
    return render(request, 'accounts/login.html', {'form': form})

# User logout view
def user_logout(request):
    logout(request)
    return redirect('login')

# Protected dashboard view
@login_required
def dashboard(request):
    # Role-based content
    user_groups = request.user.groups.values_list('name', flat=True)
    return render(request, 'accounts/dashboard.html', {'user_groups': user_groups})
