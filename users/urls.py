from django.urls import path
from .views import login_user, register_user, profile, change_password, delete_account

urlpatterns = [
    path('login/',           login_user,      name='login'),           # POST
    path('register/',        register_user,   name='register'),        # POST
    path('profile/',         profile,         name='profile'),         # GET + PUT + DELETE
    path('change-password/', change_password, name='change-password'), # POST
]