from django.urls import path
from . import views
urlpatterns = [
    path('login/',views.login),
    path('logout/',views.logout),
    path('signup/',views.signup),
    path('profile/',views.profile),
    path('edit_profile/',views.edit_profile),
    path('change_password_confirm/',views.change_password_confirm),
    path('change_password_with_old/',views.change_password_with_old),
    path('change_password_with_security/',views.change_password_with_security),
    path('change_pic/',views.change_pic),
    path('forgot_pwd/',views.forgot_pwd)
]