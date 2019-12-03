from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField
from django.contrib.contenttypes.models import ContentType
from django.urls import reverse

from read_statistics.models import ReadNum, ReadNumExpendMethd, ReadDetail


class BlogType(models.Model):
    type_name = models.CharField(max_length=15)

    def __str__(self):
        return self.type_name

    # def blog_count(self):
    #     return self.blog_set.count()

class Blog(models.Model, ReadNumExpendMethd):
    title = models.CharField(max_length=50)
    blog_type = models.ForeignKey(BlogType, on_delete=models.CASCADE)
    content = RichTextUploadingField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_time = models.DateTimeField(auto_now_add=True)
    last_updated_time = models.DateTimeField(auto_now=True)
    read_details = GenericRelation(ReadDetail)

    def __str__(self):
        return "<Blog: %s>" % self.title

    def get_url(self):
        return reverse('blog_detail', args=[self.id])

    def get_email(self):
        return self.author.email

    class Meta:
        ordering = ['-created_time']
