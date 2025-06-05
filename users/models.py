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
    
    def __str__(self):
        return self.username
    
    
    def is_following(self, other_user):
        return self.following.filter(user=other_user).exists()
        
    

class UserFollowers(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="following")
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name="followers")
    deleted = models.BooleanField(default=False)

    class Meta:
        unique_together = ('user', 'follower')

    def __str__(self):
        return f"{self.user.username} - {self.follower.username}"
