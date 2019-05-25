from django.urls import path
from .views import login_for_medal, change_nickname, bind_email, send_verification_code, change_password, forgot_password, register, login, user_center_info, logout, user_center_order, user_center_site

app_name = "user"
urlpatterns = [
    path("register/", register, name="register"),
    path("login/", login, name="login"),
    path("logout/", logout, name="logout"),
    path('login_for_medal/', login_for_medal, name='login_for_medal'),
    path('change_nickname/', change_nickname, name='change_nickname'),
    path('bind_email/', bind_email, name='bind_email'),
    path('send_verification_code/', send_verification_code, name='send_verification_code'),
    path('change_password/', change_password, name='change_password'),
    path('forgot_password/', forgot_password, name='forgot_password'),
    path("info/", user_center_info, name="info"),
    path("order/<int:page_num>", user_center_order, name="order"),
    path("site/", user_center_site, name="site"),
]
