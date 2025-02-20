from django.db import models


class AdminId(models.Model):
    userName = models.CharField(max_length=100, null=False, blank=False, unique=True)
    password = models.CharField(max_length=100, null=False, blank=False)

    def __str__(self):
        return self.userName


class AdminLoggedIn(models.Model):
    user = models.OneToOneField(AdminId, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.userName