

# Create your views here.
from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm, ProfileUpdateForm, UserUpdateForm
from .models import CustomUser, UserProfile
from django.contrib.auth.models import Group
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages


def signupView(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            signup_user = CustomUser.objects.get(username=username)
            customer_group = Group.objects.get(name='Customer')
            customer_group.user_set.add(signup_user)
            #user_profile = UserProfile(user=signup_user)
            #user_profile.save()
    else:
        form = CustomUserCreationForm()
    return render(request, 'signup.html', {'form':form})


def signinView(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('main:home')
            else:
                return redirect('signup')
    else:
        form = AuthenticationForm()
    return render(request,'signin.html', {'form':form })


def signoutView(request):
    logout(request)
    return redirect('signin')

@login_required
def profileView(request):
    if request.method == "POST":
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.userprofile)

        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, 'Account Updated!')
            return redirect('profile')

    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.userprofile)


    context = {
        'u_form': u_form,
        'p_form': p_form
    }
    return render(request, 'profile.html', context)
