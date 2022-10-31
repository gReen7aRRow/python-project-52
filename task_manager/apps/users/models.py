from django.contrib.auth.models import AbstractUser


class TaskUser(AbstractUser):
    def __str__(self):
        return self.get_full_name()
