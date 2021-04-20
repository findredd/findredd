from django.db import models
from django.contrib.auth.models import User

from multiselectfield import MultiSelectField
from ckeditor.fields import RichTextField


class Post(models.Model):
    TAGS_CHOICES = [
        ('Health', 'Health'),
        ('Engineering', 'Engineering'),
        ('Foundation', 'Foundation'),
        ('Campaign', 'Campaign'),
        ('Safety', 'Safety'),
        ('Policy', 'Policy'),
        ('Partnership', 'Partnership'),
    ]

    author = models.ForeignKey(User, on_delete=models.CASCADE)
    header = models.ImageField(upload_to='post_headers', blank=True, null=True)
    title = models.CharField(max_length=500)
    slug = models.SlugField(max_length=511, unique=True)
    content = RichTextField()
    posted_date = models.DateTimeField(auto_now_add=True)
    tags = MultiSelectField(choices=TAGS_CHOICES)
    featured_status = models.BooleanField(default=False)
