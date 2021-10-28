from django.urls import path
from authentication import views as auth_views
# from django.contrib.auth import views as django_auth_views


urlpatterns = [
    path('auth/register',auth_views.register, name="auth_register"),
    path('auth/login', auth_views.login, name="auth_login"),
    path('auth/update', auth_views.update, name="auth_update"),
    path('auth/get_user', auth_views.get_user, name="auth_get_user"),
    path('auth/password_reset', auth_views.forgotPassword, name='password_reset_request'),
    path('auth/change_password', auth_views.changePassword, name='password_change_request'),
    path('auth/check_email', auth_views.check_email, name='check_email'),
    path('auth/invite_user', auth_views.invite_user, name='invite_user'),
    path('auth/add_friend', auth_views.add_friend, name='add_friend'),
    path('auth/get_friend_requests', auth_views.get_friend_requests, name='get_friend_requests'),
    path('auth/get_friends', auth_views.get_friends, name='get_friends'),
    path('auth/accept_friend_request', auth_views.accept_friend_request, name='accept_friend_request'),
    path('auth/decline_friend_request', auth_views.decline_friend_request, name='decline_friend_request'),
    path('auth/delete_friend', auth_views.delete_friend, name='delete_friend'),
    path('auth/postImage', auth_views.postImage, name='postImage'),
    # path('password_reset/done/', django_auth_views.PasswordResetDoneView.as_view(template_name='registration/password_reset_done.html'), name='password_reset_done'),
    # path('reset/<uidb64>/<token>/', django_auth_views.PasswordResetConfirmView.as_view(template_name="registration/password_reset_confirm.html"), name='password_reset_confirm'),
    # path('reset/done/', django_auth_views.PasswordResetCompleteView.as_view(template_name='registration/password_reset_complete.html'), name='password_reset_complete'),      
    
    # path('auth/change-password',auth_views.changePassword),
    # path('posts',auth_views.fetchPostsForRegularUser),
    # path('auth/freemium-register',auth_views.RegisterAndFetchPostsForFreemiumUser)
]