from django.db import models
from django.contrib.auth.models import User

# Create your models here.
def profile_avatar_directory_path(instance: "Profile", filename: str) -> str:
    return "profile/profile_{pk}/avatar/{filename}".format(
        pk=instance.pk,
        filename=filename,
    )


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.IntegerField(max_length=11, null=True, blank=True)
    avatar = models.ImageField(null=True, blank=True, upload_to=profile_avatar_directory_path)


