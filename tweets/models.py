from django.db import models
# Connect Users to Tweet
from django.conf import settings 
import random


# Connect User to Tweet
User = settings.AUTH_USER_MODEL



# Create your models here.

class Tweet(models.Model):
    # Maps to SQL data
    # id = models.Autofield(primary_key=True)
    #User
    # CASCADE makes sure all tweets are deleted if the User is deleted.
    # You can also have the tweets user foreign key point to null if you want to save the tweets, <--There's 3 args
    # Create superuser
    user = models.ForeignKey(User, on_delete=models.CASCADE) # User can have many tweets



    content = models.TextField(blank=True, null=True)
    image = models.FileField(upload_to='images/', blank=True, null=True)

    # This is how you could change the toString of the model's objects
    # def __str__(self):
    #     return self.content

    #Reverse the ordering
    class Meta:
        ordering = ['-id']

    #Serialize DMO
    def serialize(self):
        return{
            "id": self.id,
            "content": self.content,
            "likes": random.randint(0,200)
        }