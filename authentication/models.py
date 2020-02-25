from django.db import models

from django.contrib.auth.models import User

class memory(models.Model):
    title = models.TextField()
    desc = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class ExtendedUser(models.Model):

    phone_no = models.CharField( max_length=50)
    age = models.IntegerField()
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username

    


   