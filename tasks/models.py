from django.db import models
from datetime import datetime, time as time_obj
from django.utils import timezone
from django.conf import settings
# Create your models here.


class Category(models.Model):
    name=models.CharField(max_length=100)
    description=models.TextField()  

    def __str__(self):
        return self.name 

class Event(models.Model):
    STATUS_CHOICES = [
        ("upcoming", "Upcoming"),
        ("ongoing", "Ongoing"),
        ("completed", "Completed"),
         
    ]
    name=models.CharField(max_length=100)
    description=models.TextField()
    date=models.DateField()
    time=models.TimeField()
    location=models.CharField(max_length=250)
    category=models.ForeignKey(Category,on_delete=models.CASCADE,related_name='cat')
    # particpant=models.ManyToManyField(Particpant,related_name='human')
    participant=models.ManyToManyField(settings.AUTH_USER_MODEL,related_name='rsvps')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="upcoming")
    asset = models.ImageField(upload_to='events_asset',blank=True,null=True,default="events_asset/default.png")
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        now = timezone.localtime()
        event_datetime = timezone.make_aware(datetime.combine(self.date, self.time), timezone.get_current_timezone())

        if event_datetime > now:
            self.status = "upcoming"
        elif event_datetime.date() == now.date():
            self.status = "ongoing"
        else:
            self.status = "completed"

        super().save(*args, **kwargs)