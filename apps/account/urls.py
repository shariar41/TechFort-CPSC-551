
from django.urls import path
from . import views

app_name = 'account'

urlpatterns = [
    # path('home/', views.home, name='home'),
    # path('signup/', views.SignUpView.as_view(), name='signup'),
    path('signup/', views.sign_up, name='signup'),
    # path('signup/', views.SignUpUser.as_view(), name='signup'),
    path('login/', views.login_user, name='login'),
    path('forgotpass/', views.forgot_pass, name='forgot_pass'),
    path('logout/', views.logout_user, name='logout'),
    path('profile/<str:pk>', views.user_profile, name='profile'),
]