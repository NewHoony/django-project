from tkinter import CASCADE
from django.db import models
from acc.models import User
# Create your models here.

class Board(models.Model):
    subject = models.CharField(max_length=100)
    writer = models.ForeignKey(User, on_delete=models.CASCADE, related_name="writer") # 1:N 관계
    content = models.TextField()
    pubdate = models.DateTimeField()    # 최신 글 가장 위로 
    likey = models.ManyToManyField(User, blank=True, related_name="likey")    # 투표 기능 할때!! N:N 관계

    def __str__(self):
        return self.subject

    def summary(self):
        if len(self.content) > 70:
            return f"{self.content[:70]}..."
        return self.content

    def hot(self):
        if self.likey.count() >=2:
            return True
        return False

class Reply(models.Model):
    board = models.ForeignKey(Board, on_delete= models.CASCADE)
    replyer = models.ForeignKey(User, on_delete= models.CASCADE)
    comment = models.TextField()

    def __str__(self):
        return f"{self.board}_{self.replyer}"



