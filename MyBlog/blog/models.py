from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
# Create your models here.
class PublishedManager(models.Model):
    def get_queryset(self):
        return super (PublishedManager,self).get_queryset().filter(status='published')


class Post(models.Model):
    status_choices=(
        ('draft', 'Draft'), ('published', 'Published'))
    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250, unique_for_date='publish')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_posts')
    body = models.TextField(blank=True, null=True)
    publish = models.DateField(default=timezone.now)
    created = models.DateField(auto_now_add=True)
    updated = models.DateField(auto_now=True)
    status = models.CharField(max_length=10, choices=status_choices,
                              default='draft')
    class Meta:
        ordering=('-publish',)

    def __str__(self):
        return self.title
    objects = models.Manager()#default
    published = PublishedManager()#custom Manager

    def get_absolute_urls(self):
        return reverse('blog:post_detail', args=[self.publish.year,
                                                self.publish.month,
                                                self.publish.day,
                                                self.slug])