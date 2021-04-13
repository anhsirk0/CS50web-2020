from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    imgurl = models.CharField(default="https://cdn.iconscout.com/icon/free/png-512/account-profile-avatar-man-circle-round-user-30452.png", max_length=64)

    def __str__(self):
        return self.username

class Post(models.Model):
    owner = models.ForeignKey(User, related_name="post", on_delete=models.CASCADE)
    text = models.CharField(max_length=64)
    date = models.DateTimeField(auto_now_add=True, blank=True)

    def __str__(self):
        return f"{self.text} by {self.owner} on {self.date}"


class Comment(models.Model):
    text = models.CharField(max_length=64)
    post = models.ForeignKey(Post, related_name="comment", on_delete=models.CASCADE)
    commented_by = models.ForeignKey(User, related_name="comment", on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.text} by {self.commented_by}"

class Like(models.Model):
    post = models.ForeignKey(Post, related_name="like", on_delete=models.CASCADE)
    liked_by = models.ForeignKey(User, related_name="like", on_delete=models.CASCADE)

    def __str__(self):
        return f"Liked by {self.liked_by}"

class Follow(models.Model):
    follower = models.ForeignKey(User, related_name="follower", on_delete=models.CASCADE)
    following = models.ForeignKey(User, related_name="following", on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.follower} follows {self.following}"

