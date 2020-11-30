import os

from django.db.models.signals import pre_save, post_save, post_delete
from django.contrib.auth.models import User
from django.dispatch import receiver
from main.models import UserDetail, UserPicture, UserSocialUrl, UserConfig


@receiver(post_save, sender=User)
def create_user_detail(sender, instance, created, **kwargs):
    if created:
        UserDetail.objects.create(username=instance)


@receiver(post_save, sender=User)
def save_user_detail(sender, instance, **kwargs):
    instance.userdetail.save()


@receiver(post_save, sender=User)
def create_user_picture(sender, instance, created, **kwargs):
    if created:
        UserPicture.objects.create(username=instance)


@receiver(post_save, sender=User)
def save_user_picture(sender, instance, **kwargs):
    instance.userpicture.save()


@receiver(post_save, sender=User)
def create_user_social_url(sender, instance, created, **kwargs):
    if created:
        UserSocialUrl.objects.create(username=instance)


@receiver(post_save, sender=User)
def save_user_social_url(sender, instance, **kwargs):
    instance.usersocialurl.save()


@receiver(post_save, sender=User)
def create_user_config(sender, instance, created, **kwargs):
    if created:
        UserConfig.objects.create(username=instance)


@receiver(post_save, sender=User)
def save_user_config(sender, instance, **kwargs):
    instance.userconfig.save()


# @receiver(post_delete, sender=UserPicture)
# def auto_delete_file_on_delete(sender, instance, **kwargs):
#     if instance.profile_picture:
#         if os.path.isfile(instance.profile_picture.path) and os.path.basename(instance.profile_picture.path)!='default_profile_picture.png':
#             os.remove(instance.profile_picture.path)


# @receiver(pre_save, sender=UserPicture)
# def auto_delete_file_on_change(sender, instance, **kwargs):
#     if not instance.pk:
#         return False

#     try:
#         old_file = sender.objects.get(pk=instance.pk).profile_picture
#     except sender.DoesNotExist:
#         return False

#     new_file = instance.profile_picture
#     if not old_file == new_file:
#         if os.path.isfile(old_file.path) and os.path.basename(old_file.path)!='default_profile_picture.png':
#             os.remove(old_file.path)
