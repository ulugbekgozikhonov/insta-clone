from django.db import models
from django.contrib.auth.models import AbstractUser
from posts.models import BaseModel

class User(AbstractUser, BaseModel):
    
    GENDER_TYPES = (
        ('Male', 'male'),
        ('Female', 'female')
    )

    photo = models.ImageField(upload_to="users/posts/", null=True, blank=True, default="users/avatar/default.png")
    gender = models.CharField(choices=GENDER_TYPES, max_length=6, null=True, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)

