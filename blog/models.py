from django.db import models
from django.utils.text import slugify
import uuid

class category(models.Model):
    category_title = models.CharField(max_length=100)

    def __str__(self) :
        return self.category_title

class Post(models.Model):

    Title = models.CharField(max_length=100)
    Content = models.TextField()
    Img_url = models.URLField(null=True)
    Date_time = models.DateTimeField(auto_now_add=True)
    category = models.ForeignKey(category , on_delete = models.CASCADE)

    def __str__(self) :
        return self.Title

#    slug = models.SlugField()

#    def save(self, *args, **kwargs):
#        self.slug = slugify(self.Title)
#        super().save(*args,**kwargs)
    
class login(models.Model):
    username = models.CharField(max_length=100,unique=True)
    password = models.CharField(max_length=100)
    code = models.CharField(max_length=100,blank = True)
    verified = models.BooleanField(default=False)
    email= models.EmailField(max_length=100,unique=True)
    
    def generate_code(self):
        
        self.code = str(uuid.uuid4())
        self.save()