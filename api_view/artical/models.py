from django.db import models

# Create your models here.

class Author(models.Model):
    name=models.CharField(max_length=250)
    email=models.EmailField(unique=True)

    def __str__(self):
        return self.name

class Artical(models.Model):
    title=models.CharField(max_length=200)
    description=models.TextField()
    body=models.TextField()
    author=models.ForeignKey('Author',related_name='articals',on_delete=models.CASCADE)


    def __str__(self):
        return self.title