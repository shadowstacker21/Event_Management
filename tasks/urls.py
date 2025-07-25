from django.urls import path

from .views import view,event_details,button,dashboard,add_event,update_event,delete_event,user_view,user_details,rsvp_event
from core.views import no_permission

urlpatterns = [
   path('view/', view,name="admin-dashboard"),
  
   path('user-dashboard/', user_view, name='user-dashboard'),
   path('event/',button,name='show-event'),
   path('participant/',button,name='show-participant'),
   path('category/',button,name='show-category'),
   path('add-event/',add_event,name='add-event'),
   path('update-event/<int:id>/',update_event,name='update-event'),
   path('delete-event/<int:id>/',delete_event,name='delete-event'),
   path('no-permission/',no_permission,name='no-permission'),
    path('dashboard',dashboard,name='dashboard'),
    path('event/<int:event_id>/details',event_details,name='event-details'),
    path('user/event/<int:event_id>/details/', user_details, name='user-details'), 
   path('event/<int:event_id>/details/rsvp/', rsvp_event, name='rsvp'),
]

