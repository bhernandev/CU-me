from django.db import models
from django.contrib.auth.models import User

class Class(models.Model):
    taker = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    times = models.CharField(max_length=100)
    instructor = models.CharField(max_length=100)
    rating = models.CharField(max_length=25)
    room = models.CharField(max_length=100)
    dates = models.CharField(max_length=50)

    def __str__(self):
        return self.name

    def as_dict(self):
        return {'name': self.name, 'times': self.tiimes, 'instructor': self.instructor, 'rating': self.rating, 'room': self.room, 'dates': self.dates}
