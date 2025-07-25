from django.urls import path
from .views import sign_up,group_list,sign_in,sign_out,activate_user,admin_dashboard,assign_role,create_group

urlpatterns = [
    path('sign-up/',sign_up,name="sign-up"),
    path('sign-in/',sign_in,name="sign-in"),
    path('sign-out/',sign_out,name="logout"),
    path('activate/<int:user_id>/<str:token>/',activate_user),
    path('admin-dashboard/',admin_dashboard,name='admin'),
    path('admin/<int:user_id>/assign-role',assign_role,name='assign-role'),
    path('admin/create-group/',create_group,name='create-group'),
    path('admin/group-list/',group_list,name = 'group-list'),
]
