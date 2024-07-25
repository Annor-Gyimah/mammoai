from django.urls import path
from userauths import views

app_name = "userauths"

urlpatterns =[
    path('sign-up/', views.RegisterView, name='sign-up'),
    path('sign-in/', views.loginViewTemp, name='sign-in'),
    path("sign-out/", views.LogoutView, name="sign-out"),
    path('activate/<uidb64>/<token>', views.activate, name='activate'),

    path("password_reset", views.password_reset_request, name="password_reset"),
    path('reset/<uidb64>/<token>', views.passwordResetConfirm, name='password_reset_confirm'),
    path("profile/", views.profile, name="profile"),
    path("password_change/", views.password_change, name='password_change'),

]