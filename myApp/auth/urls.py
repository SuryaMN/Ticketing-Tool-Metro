from django.urls import path, include
from . import views

urlpatterns = [
    path('', include('djoser.urls')),
    path('', include('djoser.urls.authtoken')),
    path('getUser/<int:uid>', views.getUser, name='getUser'),
    path('getUserFromToken', views.getUserFromToken, name='getUserFromToken'),
    path('login', views.login, name='login')
]
