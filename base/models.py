from django.db import models

# Create your models here.
from django.db import models
from django.utils.text import slugify
from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField

# Create your models here.

class Tag(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name 

class Image(models.Model):
    photo = models.ImageField(upload_to="images")

class Post(models.Model):
    headline = models.CharField(max_length=200)
    sub_headline = models.CharField(max_length=200, null=True, blank=True)
    user = models.CharField(max_length=200)
    thumbnail = models.ImageField(null=True, blank=True, upload_to="images", default="placeholder.jpg")
    body = RichTextUploadingField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=False)
    featured = models.BooleanField(default=False)
    tags = models.ManyToManyField(Tag, null=True)
    slug = models.SlugField(null=True, blank=True)

    def __str__(self):
        return self.headline 


    def save(self, *args, **kwargs):

            if self.slug == None:
                slug = slugify(self.headline)

                has_slug = Post.objects.filter(slug=slug).exists()
                count = 1
                while has_slug:
                    count += 1
                    slug = slugify(self.headline) + '-' + str(count) 
                    has_slug = Post.objects.filter(slug=slug).exists()

                self.slug = slug

            super().save(*args, **kwargs)


class Comment(models.Model):
    post = models.ForeignKey(Post, related_name="comments", on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    body = models.TextField(max_length=255)
    comment_created = models.DateTimeField(auto_now_add=True)
    

    def __str__(self):
        return '{} - {}'.format(self.post.headline, self.name)

