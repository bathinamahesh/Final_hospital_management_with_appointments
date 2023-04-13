from django.db import models
from datetime import datetime

# Create your models here.
##For blogs
from ckeditor.fields import RichTextField

class Category(models.Model):
    name = models.TextField(max_length=255,default='Unknown')
    created = models.DateTimeField(default=datetime.now)
    
    
    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'



class Post(models.Model):
    category = models.ForeignKey(Category,on_delete=models.CASCADE,related_name='categories')
    user = models.TextField(max_length=255)
    title = models.TextField(max_length=255)
    thumbnail = models.ImageField(upload_to='post/thumbanail')
    description = RichTextField(blank=True,null=True)
    summary = RichTextField(blank=True,null=True)
    tags = models.TextField(max_length=255,blank=True,null=True)
    posted_at = models.DateField(default=datetime.now)
    is_published = models.TextField(max_length=255,default=1)
    

    class Meta:
        verbose_name = ("Post")
        verbose_name_plural = ("Posts")

    def __str__(self):
        return self.title


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    name = models.TextField(max_length=255)
    email = models.TextField(max_length=255)
    website = models.TextField(null=True,blank=True,max_length=100)
    comment = models.TextField()
    commented_at = models.DateTimeField(default=datetime.now)
    is_resolved = models.BooleanField(default=False)

    
    def __str__(self):
        return self.email

    class Meta:
        verbose_name = 'Comment'
        verbose_name_plural = 'Comments'
   
