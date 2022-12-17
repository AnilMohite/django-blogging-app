from django.db import models
from django.utils.text import slugify

# Create your models here.

class Blog(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField(max_length=150, blank=True)
    img = models.ImageField(upload_to="images/blogs/", blank=True)
    short_content = models.CharField(max_length=200)
    long_content = models.TextField()
    created_by = models.CharField(max_length=50)
    created_date = models.DateTimeField()

    def __str__(self):
        return self.title +" : "+self.created_by 

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Blog,self).save(*args,**kwargs)



