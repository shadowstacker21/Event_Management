from django.urls import path
from tasks.views import event_details,button,dashboard,ManagerDashboardView,AddTask,UpdateEventView,DeleteEventView,UserView,user_details,rsvp_event
from core.views import no_permission

urlpatterns = [
   path('manager/view/',ManagerDashboardView.as_view(),name="admin-dashboard"),
   path('user-dashboard/', UserView.as_view(), name='user-dashboard'),
   path('event/',button,name='show-event'),
   path('participant/',button,name='show-participant'),
   path('category/',button,name='show-category'),
   path('add-event/',AddTask.as_view(),name='add-event'),
   path('update-event/<int:id>/',UpdateEventView.as_view(),name='update-event'),
   path('delete-event/<int:id>/',DeleteEventView.as_view(),name='delete-event'),
   path('no-permission/',no_permission,name='no-permission'),
    path('dashboard/',dashboard,name='dashboard'),
    path('event/<int:event_id>/details',event_details,name='event-details'),
    path('user/event/<int:event_id>/details/', user_details, name='user-details'), 


   path('event/<int:event_id>/details/rsvp/', rsvp_event, name='rsvp')
]

