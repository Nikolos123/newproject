from . import views as inc
from django.urls import path
from django.contrib.auth import views as auth_view


urlpatterns = [
    path('', inc.dashboard, name='dashboard'),
    # path('login/', views.user_login,name='login')
    path('login/', auth_view.LoginView.as_view(), name='login'),
    path('logout/', inc.AccountLogoutView.as_view(), name='logout'),

    # Шаблоны для доступа к обработчикам смены пароля.
    path('password_change/', auth_view.PasswordChangeView.as_view(), name='password_change'),
    path('password_change/done/', auth_view.PasswordChangeDoneView.as_view(), name='password_change_done'),

    # Обработчики восстановления пароля.
    path('password_reset/', auth_view.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_view.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_view.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_view.PasswordResetCompleteView.as_view(), name='password_reset_complete'),

    #Регистрация
    path('register/', inc.register, name='register'),

    #Изменить данные профиля
    path('edit/', inc.edit, name='edit'),

]
