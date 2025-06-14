from django.db import models
from django.utils.timesince import timesince
from django.utils.timezone import now


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Post(BaseModel):
    title = models.CharField(max_length=150, null=True, blank=True)
    content = models.FileField(upload_to="users/posts")
    description = models.TextField(null=True, blank=True)
    user = models.ForeignKey(
        "users.User", on_delete=models.CASCADE, related_name="posts"
    )

    def __str__(self):
        return self.title if self.title else "No Title"

    @property
    def get_time_since_created(self):
        return timesince(self.created_at, now())

    @property
    def likes_count(self):
        return self.likes.filter(deleted=False).count()

    class Meta:
        verbose_name = "Post"
        verbose_name_plural = "Posts"
        ordering = ["-created_at"]


class PostLike(BaseModel):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="likes")
    user = models.ForeignKey(
        "users.User", on_delete=models.CASCADE, related_name="liked_posts"
    )
    deleted = models.BooleanField(default=False)

    class Meta:
        unique_together = ("post", "user")
        verbose_name = "Post Like"
        verbose_name_plural = "Post Likes"

    def __str__(self):
        return f"{self.user.username} liked {self.post.title}"


class Comment(BaseModel):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    user = models.ForeignKey(
        "users.User", on_delete=models.CASCADE, related_name="comments"
    )
    text = models.TextField()

    def __str__(self):
        return f"{self.user.username}: {self.text}"
