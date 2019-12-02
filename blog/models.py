from django.db import models
from django.utils import timezone
# Create your models here.


class User(models.Model):
    '''
        用户表
    '''
    id = models.AutoField(primary_key=True)
    create_time = models.DateTimeField(default=timezone.now)
    name = models.CharField(null=False, max_length=20)
    email = models.EmailField(null=False)
    password = models.CharField(null=False, max_length=32)
    avatar = models.URLField(null=True, blank=True)

    class Meta:
        ordering = ['create_time']


class Article(models.Model):
    '''
        文章表
    '''
    id = models.AutoField(primary_key=True)
    status = models.IntegerField(null=False, default=0)
    title = models.CharField(null=False, max_length=100)
    create_time = models.DateTimeField(default=timezone.now)
    comment_count = models.IntegerField(null=False, default=0)
    content = models.TextField(null=False, max_length=30000)
    author_id = models.ForeignKey(to="User", related_name="user_id")
    author_name = models.CharField(null=False, max_length=20)


class Comment(models.Model):
    '''
        评论表
    '''
    id = models.AutoField(primary_key=True)
    create_time = models.DateTimeField(default=timezone.now)
    comment = models.CharField(null=False, max_length=500)
    article_id = models.ForeignKey(Article)
    author_id = models.ForeignKey(User)
    parent_comment_id = models.ForeignKey(to='Comment', related_name="comment_id")


class Expression(models.Model):
    '''
        短文表
    '''
    id = models.AutoField(primary_key=True)
    status = models.IntegerField(default=0)
    create_time = models.DateTimeField(default=timezone.now)
    content = models.TextField(null=False, max_length=1000)
    author_id = models.ForeignKey(to="User")

class ExpressionImage(models.Model):
    '''
        短文图片表
    '''
    expression_id = models.ForeignKey(to="Expression", default=None)
    url = models.URLField(null=False)