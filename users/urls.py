from django.urls import path
from .views import sign_up,group_list,sign_out,activate_user,admin_dashboard,assign_role,create_group,EditProfileView,CustomPasswordConfirmView,CustomPasswordResetView,LoginView,ProfileView
from django.contrib.auth.views import LogoutView,PasswordChangeView,PasswordChangeDoneView

urlpatterns = [
    path('sign-up/',sign_up,name="sign-up"),
    # path('sign-in/',sign_in,name="sign-in"),
    path('sign-in/',LoginView.as_view(),name="sign-in"),
    # path('sign-out/',sign_out,name="logout"),
    path('sign-out/',LogoutView.as_view(),name="logout"),
    path('activate/<int:user_id>/<str:token>/',activate_user),
    path('admin-dashboard/',admin_dashboard,name='admin'),
    path('admin/<int:user_id>/assign-role',assign_role,name='assign-role'),
    path('admin/create-group/',create_group,name='create-group'),
    path('admin/group-list/',group_list,name = 'group-list'),
    path('profile/',ProfileView.as_view(),name='profile'),
    path('password-change/',PasswordChangeView.as_view(template_name = 'accounts/password_change.html'),name='password_change'),
    path('password-change/done/',PasswordChangeDoneView.as_view(template_name='accounts/password_change_done.html'),name='password_change_done'),
    path('password-reset/',CustomPasswordResetView.as_view(),name="password_reset"),
    path('password-reset/done/<uidb64>/<token>/',CustomPasswordConfirmView.as_view(),name="password_reset_confirm"),
     path('edit-profile/',EditProfileView.as_view(),name='edit_profile')

]
