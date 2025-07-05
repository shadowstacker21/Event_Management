from django.urls import path
from .views import view,button,add_event,update_event,delete_event

urlpatterns = [
   path('event/',button,name='show-event'),
   path('participant/',button,name='show-participant'),
   path('category/',button,name='show-category'),
   path('add-event/',add_event,name='add-event'),
   path('update-event/<int:id>/',update_event,name='update-event'),
   path('delete-event/<int:id>/',delete_event,name='delete-event'),
]
