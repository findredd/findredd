import os

from django.db.models.signals import pre_save, post_delete
from django.dispatch import receiver
from blog.models import Post


# @receiver(post_delete, sender=Post)
# def auto_delete_file_on_delete(sender, instance, **kwargs):
#     if instance.header:
#         if os.path.isfile(instance.header.path):
#             os.remove(instance.header.path)


# @receiver(pre_save, sender=Post)
# def auto_delete_file_on_change(sender, instance, **kwargs):
#     if not instance.pk:
#         return False

#     try:
#         old_file = sender.objects.get(pk=instance.pk).header

#     except sender.DoesNotExist:
#         return False

#     new_file = instance.header
#     if not old_file == new_file:
#         try:
#             if os.path.isfile(old_file.path):
#                 os.remove(old_file.path)
#         except Exception:
#             return False
