from django.db import models
from django.contrib.auth.models import AbstractUser
from rest_framework.authtoken.models import Token
from rest_framework import serializers
from django.dispatch import receiver
from django.db.models.signals import post_save


class User(AbstractUser):
    nickname = models.CharField(max_length=50, blank=True)

    class Meta(AbstractUser.Meta):
        pass


@receiver(post_save, sender=User)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


class UserSerialiser(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('username', 'email')


def unique_rand():
    while True:
        code = User.objects.make_random_password(length=8)
        while InviteCode.objects.filter(code=code).exists():
            code = User.objects.make_random_password(length=10)
        return code


class InviteCode(models.Model):
    code = models.CharField(
        "邀请码文本",
        max_length=20,
        default=unique_rand,
        unique=True,
        blank=True,
    )
    used_by = models.ForeignKey(
        User,
        null=True,
        on_delete=models.CASCADE,
        editable=False,
    )


class PotentialUser(models.Model):
    email = models.CharField(
        "联系邮箱",
        max_length=20,
    )
    favoritebrowser = models.CharField(
        "常用浏览器",
        max_length=20,
    )
    job = models.CharField(
        "职业",
        max_length=20,
    )
