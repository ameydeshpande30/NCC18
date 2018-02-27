from django.db import models
from django.contrib.auth.models import User


# Create your models here.


class Player(models.Model):
    p1name = models.CharField(max_length=120)
    p2name = models.CharField(max_length=120)
    p1email = models.EmailField(max_length=100)
    p2email = models.EmailField(max_length=100)
    pid = models.OneToOneField(User, on_delete=models.CASCADE)
    p1mno = models.CharField(max_length=10)
    p2mno = models.CharField(max_length=10)
    time = models.IntegerField(default=0)
    score = models.IntegerField(default=0)
    level = models.IntegerField(default=0)
    q1_score = models.IntegerField(default=0)
    q2_score = models.IntegerField(default=0)
    q3_score = models.IntegerField(default=0)
    q4_score = models.IntegerField(default=0)
    q5_score = models.IntegerField(default=0)
    q6_score = models.IntegerField(default=0)
    subtime = models.IntegerField(default=0)
    rank = models.IntegerField(default=0)
    gender1 = models.IntegerField(default=0)
    gender2 = models.IntegerField(default=0)


    def __str__(self):
        a = self.id
        a = str(a)
        return self.p1name + " " + self.p2name


class Questions(models.Model):
    title = models.CharField(max_length=100)
    completeques = models.CharField(max_length=5000)
    qid = models.IntegerField(default=0)
    ac = models.IntegerField(default=0)
    qlevel = models.IntegerField(default=0)
    qsub = models.IntegerField(default=0)

    def __str__(self):
        qidv = str(self.qid)
        return self.title + " " + qidv


class Attempt(models.Model):
    qid = models.CharField(max_length=10)
    ext = models.CharField(max_length=10)
    user = models.ForeignKey(User, default=0, on_delete=models.CASCADE)
    time = models.IntegerField(default=0)
    status = models.CharField(max_length=10)
