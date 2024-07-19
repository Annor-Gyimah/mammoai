from home import views
from django.urls import path

from userauths.views import loginViewTemp

app_name = "home"

urlpatterns = [
    path('', views.index, name='index'),

    
    
    path('sign-in/', loginViewTemp, name='sign-in')
]
