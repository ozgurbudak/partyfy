from django.db import models

class Suser(models.Model):
    user_id = models.TextField()
    user_name= models.TextField()
# Create your models here.
class Playlist(models.Model):
    owner=models.TextField()
    title = models.TextField()
    allowed_users= models.ManyToManyField(Suser, blank=True,related_name="allowed_users")
    is_active= models.BooleanField(default=True)
    playlist_id= models.TextField()
    lat=models.DecimalField( max_digits=40, decimal_places=20)
    long=models.DecimalField( max_digits=40, decimal_places=20)
    requests= models.ManyToManyField(Suser, blank=True,related_name="requests")

