from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Player(models.Model):
    p1name=models.CharField(max_length=120)
    p2name=models.CharField(max_length=120)
    p1email=models.EmailField(max_length=100)
    p2email=models.EmailField(max_length=100)
    pid=models.OneToOneField(User,on_delete=models.CASCADE)
    p1mno=models.CharField(max_length=10)
    p2mno=models.CharField(max_length=10)
    time=models.IntegerField(default=0)
    score=models.IntegerField(default=0)
    def __str__(self):
        a = self.id
        a = str(a)
        return self.p1name + " " + self.p2name


class Questions(models.Model):
    title = models.CharField(max_length=10)
    completeques = models.CharField(max_length=120)
    qid = models.IntegerField(default=0)
    ac = models.IntegerField(default=0)

    def __str__(self):
        qid = str(self.qid)
        return self.title + " " + self.qid


class Attempt(models.Model):
    qid=models.CharField(max_length=10)
    ext=models.CharField(max_length=10)
    user=models.ForeignKey(User,default=0,on_delete=models.CASCADE)
    time=models.IntegerField(default=0)
    status=models.CharField(max_length=10)