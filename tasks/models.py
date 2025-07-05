from django.db import models
from datetime import datetime, time as time_obj
from django.utils import timezone

# Create your models here.

class Particpant(models.Model):
    name=models.CharField(max_length=100)
    email=models.EmailField(unique=True)

    def __str__(self):
        return self.name

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
    particpant=models.ManyToManyField(Particpant,related_name='human')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="upcoming")
    
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