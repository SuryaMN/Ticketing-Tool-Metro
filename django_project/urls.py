"""django_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from myApp import rest, views
from django.contrib.auth import views as auth_views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.home,name='home'),
    path('dashboard/',views.dashboard,name='dashboard'),
    path('tickets/',views.tickets,name='tickets'),
    path('raiseticket/',views.raiseticket,name='raiseticket'),
    path('raiseticket/<int:id>',views.raiseticket,name='raiseticket'),
    path('deleteticket/',views.deleteticket,name='deleteticket'),
    path('viewticket/<int:id>',views.viewticket,name='viewticket'),
    path('changestatus/',views.changestatus,name='changestatus'),
    path('getsummary/',views.getsummary,name='getsummary'),
    path('forbidden/',views.forbidden,name='forbidden'),
    path('notfound/',views.notfound,name='notfound'),

    # API
    path('get_tickets/',rest.get_tickets,name='get_tickets'),

    #AUTH
    path('signup',views.signupuser,name='signupuser'),
    path('login',views.loginuser,name='loginuser'),
    path('logout',views.logoutuser,name='logoutuser'),


    #PASSWORD RESET
    path('reset_password/',auth_views.PasswordResetView.as_view(template_name='myApp/password_reset_form.html'),name='reset_password'),
    path('reset_password_sent/',auth_views.PasswordResetDoneView.as_view(template_name='myApp/password_reset_done.html'),name='password_reset_done'),
    path('reset/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(template_name='myApp/password_reset_confirm.html'),name='password_reset_confirm'),
    path('reset_password_complete/',auth_views.PasswordResetCompleteView.as_view(template_name='myApp/password_reset_complete.html'),name='password_reset_complete'),
    
]
urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)

handler404 = "myApp.views.notfound"