from django.db import models
from django.conf import settings
from django.utils import timezone
from django.shortcuts import reverse
from ckeditor.fields import RichTextField

# Create your models here.
def upload_location(instance, filename):
    return '%s/%s' %(instance.id, filename)

class Post(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    text = RichTextField(blank=True, null=True)
    created_date = models.DateTimeField(default = timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)
    image = models.ImageField(upload_to=upload_location, null=True, blank=True, height_field='height_field', width_field='width_field')
    height_field = models.IntegerField(default=0)
    width_field = models.IntegerField(default=0)

    def __str__(self):
        return self.title

    def publish(self):
        self.published_date = timezone.now()
        self.save()
    
    def get_absolute_url(self):
        return reverse("blog:post_detail", args=[self.pk])

    def approved_comments(self):
        return self.comments.filter(approved_comment=True)

class Comment(models.Model):
    post = models.ForeignKey('blog.Post', on_delete=models.CASCADE, related_name='comments')#related_names allows us access within the Post model
    author = models.CharField(max_length=200)
    text = RichTextField(blank=True, null=True)
    created_date = models.DateTimeField(default=timezone.now)
    approved_comment = models.BooleanField(default=False)

    def approve(self):
        self.approved_comment =True
        self.save()

    def __str__(self):
        return self.text

