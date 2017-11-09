from django.db import models

# Create your models here.
class Greeting(models.Model):
    when = models.DateTimeField('date created', auto_now_add=True)

class TimeBlock(models.Model):
    day = models.CharField(max_length=20)
    start = models.IntegerField()
    end = models.DecimalField()
