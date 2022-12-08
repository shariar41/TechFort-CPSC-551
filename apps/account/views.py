from django.shortcuts import render, HttpResponseRedirect, redirect
from django.urls import reverse, reverse_lazy
from django.http import HttpResponse

# Authentication
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate

# Forms and Models
from django.views.generic import CreateView

from .models import Profile
from ..order.models import Order
from .forms import ProfileForm, SignUpForm, LoginForm, UserUpdateForm
from .models import User

# Messages
from django.contrib import messages


# Create your views here.


# def home(request):
#     return render(request, 'home.html')


# def sign_up(request):
#     form = SignUpForm()
#     if request.method == 'POST':
#         print("start")
#         form = SignUpForm(request.POST)
#         if form.is_valid():
#             print("success")
#             form.save()
#             messages.success(request, "Account Created Successfully!")
#             return HttpResponseRedirect(reverse('account:login'))
#         elif form.password1 != form.password2:
#             error_msg = {'Passwords are not same'}
#             return render(request, 'account/register.html', context={'form': form, 'error_msg': error_msg})
#     return render(request, 'account/register.html', context={'form': form})


def sign_up(request):
    form = SignUpForm()
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            # post = form.save(commit=False)
            # post.save()
            print("valid")
            form.save()
            messages.success(request, "Your account has been created successfully!")
            return HttpResponseRedirect(reverse('account:login'))
            # return render(request, 'account/login.html', context=context)
        elif not form.is_valid():
            messages.error(request, form.error_messages)
            print(form.error_messages)
            return render(request, 'account/register.html', context={'form': form})
    # return HttpResponseRedirect("/signup/")
    return render(request, 'account/register.html', context={'form': form})


def login_user(request):
    # form = AuthenticationForm()
    form = LoginForm()
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, "You have logged in.")
                # return render(request, 'home.html')
                return HttpResponseRedirect(reverse('products:home'))
    # return HttpResponseRedirect(reverse('account:login'))
    return render(request, 'account/login.html', context={'form': form})


@login_required
def logout_user(request):
    logout(request)
    messages.warning(request, "You have been logged out!")
    return HttpResponseRedirect(reverse('products:home'))
    # return render(request, 'home.html')


@login_required
def user_profile(request, pk):
    profile = Profile.objects.get(id=pk)
    order_items = Order.objects.filter(created_by=request.user).exclude(order_id=None, payment_id=None)
    # a = Order.objects.filter(user=request.user, is_order=True)
    # items = a.order_items
    # for order in order_items:
    #     for i in order.order_items.objects.filter():
    #         print(i)
    form = ProfileForm(instance=profile)
    user_form = UserUpdateForm(instance=request.user)
    # form.fields['username'].widget.attrs['placeholder'] = profile.user
    user_form.fields['firstname'].widget.attrs['placeholder'] = request.user.first_name

    form.fields['lastname'].widget.attrs['placeholder'] = profile.lastname

    user_form.fields['phone'].widget.attrs['placeholder'] = profile.user.phone

    user_form.fields['email'].widget.attrs['placeholder'] = request.user.email

    # form.fields['phone'].widget.attrs['placeholder'] = profile.firstname
    form.fields['address_1'].widget.attrs['placeholder'] = profile.address_1

    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=profile)
        user_form = UserUpdateForm(request.POST, instance=request.user)
        form.save()
        user_form.save()
        return render(request, 'account/profile_page.html',
                      context={'form': form, 'user_form': user_form, 'order_items': order_items})

    return render(request, 'account/profile_page.html',
                  context={'form': form, 'user_form': user_form, 'order_items': order_items})


def forgot_pass(request):
    return render(request, 'account/forgot-password.html')
