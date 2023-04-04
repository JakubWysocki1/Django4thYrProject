

# Create your views here.
from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm, ProfileUpdateForm, UserUpdateForm, BioUpdateForm
from .models import CustomUser, UserProfile
from django.contrib.auth.models import Group
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseForbidden


def signupView(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            signup_user = CustomUser.objects.get(username=username)
            customer_group = Group.objects.get(name='Customer')
            customer_group.user_set.add(signup_user)

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
                return redirect('accounts:signup')
    else:
        form = AuthenticationForm()
    return render(request,'signin.html', {'form':form })


def signoutView(request):
    logout(request)
    return redirect('accounts:signin')

# @login_required
def profileView(request, profile_name):
    user_profile = get_object_or_404(UserProfile, user__username=profile_name)

    
    if request.method == "POST":
        bio_form = BioUpdateForm(request.POST, instance=user_profile)
        if bio_form.is_valid():
            bio_form.save()
            messages.success(request, 'Bio Updated!')
            return redirect('accounts:profile', profile_name=profile_name)

    else:
        initial_data = {'bio': user_profile.bio} # set the initial value to the existing bio value
        bio_form = BioUpdateForm(initial=initial_data)

    return render(request, 'profile.html', {'user_profile': user_profile, 'bioform': bio_form})

@login_required
def profileDetailsView(request, profile_name):
    def test_func(user):
        return user.username == profile_name

    if not test_func(request.user):
        return HttpResponseForbidden()


    if request.method == "POST":
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, 'Account Updated!')
            return redirect('accounts:profile', profile_name=profile_name)

    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.userprofile)


    context = {
        'u_form': u_form,
        'p_form': p_form,
        'profile_name': profile_name
    }
    return render(request, 'profileDetails.html', context)