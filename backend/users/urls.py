from django.urls import path
from .views import CustomUserCreate, BlacklistTokenUpdateView, LoginView, LogoutAllView, UserList,  ChangePasswordView
# , VerifyEmail


app_name = 'users'

urlpatterns = [

    path('register/', CustomUserCreate.as_view(), name="register_user"),
    path('logout/', BlacklistTokenUpdateView.as_view(), name="blacklist"),
    path('login/', LoginView.as_view(), name='login to the system'),
    path('user-list/', UserList, name="list of all the users in the db"),
    path('change_password/<int:pk>/', ChangePasswordView.as_view(), name='auth_change_password'),
    path('logout_all/', LogoutAllView.as_view(), name='auth_logout_all')
]

# path('email-verify/', VerifyEmail.as_view(), name="email-verify"),


#  {
#         "email": "kak@kkk.com",
#         "firstname": "kalebasss",
#         "username": "kaleba1234",
#         "password": "1234567890qwer"
# }
