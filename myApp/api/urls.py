from django.urls import path, include
from . import views

urlpatterns = [
    path('get_tickets/<int:user_id>', views.get_tickets, name='get_tickets'),
    path('raiseTicket', views.raiseTicket, name='raiseTicket'),

]

# urlpatterns = [
#     url(r'^auth/login/$',
#         obtain_auth_token,
#         name='auth_user_login'),
#     url(r'^auth/register/$',
#         CreateUserAPIView.as_view(),
#         name='auth_user_create'),
#     url(r'^auth/logout/$',
#         LogoutUserAPIView.as_view(),
#         name='auth_user_logout')
# ]
