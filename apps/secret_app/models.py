from __future__ import unicode_literals
from django.db import models
import re
import bcrypt
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
NAME_REGEX = re.compile(r'^[a-zA-Z.-]+$')

class UserManager(models.Manager):
    def login(self, PostData):
        messages = []
        if len(PostData['first_name']) < 1 or len(PostData['last_name']) < 1 or len(PostData['email']) < 1 or len(PostData['password']) < 1:
            messages.append("You Suck!")
        if not NAME_REGEX.match(PostData['first_name']) or not NAME_REGEX.match(PostData['last_name']):
            messages.append("You stink!")
        if not EMAIL_REGEX.match(PostData['email']):
            messages.append("Buzz off!")
        if PostData['password'] != PostData['confirm_password']:
            messages.append("Password does not match!")
        if User.objects.filter(email=PostData['email']):
            messages.append("user stinks")
        return messages

    def create_user(self, PostData):
        hashed_pw = bcrypt.hashpw(PostData['password'].encode('utf-8'), bcrypt.gensalt())
        new_user = User.objects.create(first_name = PostData['first_name'], last_name = PostData['last_name'], email=PostData['email'], password = hashed_pw)
        return new_user.id

    def register(self, PostData):
        messages = []
        if not User.objects.filter(email=PostData['email']):
            messages.append("Username and/or password are invalid.")
        else:
            if bcrypt.hashpw(PostData['password'].encode('utf-8'), User.objects.get(email=PostData['email']).password.encode('utf-8')) != User.objects.get(email=PostData['email']).password:
                messages.append('Wrong Password')
        return messages

class CommentManager(models.Manager):
    def add_comment(self, PostData):
        comment = Comment.objects.create(comment = PostData['comment'], user=User.objects.get(id=PostData['user_id']))
        comment_id = comment.id
        return comment_id
    def like(self, PostData):
        user = User.objects.get(id=PostData['user_id'])
        comment = Comment.objects.get(id=PostData['comment_id'])
        comment.likes.add(user)
    def unlike(self,PostData):
        user = User.objects.get(id = PostData['user_id'])
        comment = Comment.objects.get(id=PostData['comment_id'])
        comment.likes.remove(user)
    

class User(models.Model):
    first_name = models.CharField(max_length=45)
    last_name = models.CharField(max_length=45)
    email = models.CharField(max_length=225)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = UserManager()

class Comment(models.Model):
    user = models.ForeignKey(User)
    comment = models.CharField(max_length=2000)
    likes = models.ManyToManyField(User, related_name = "comments")
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = CommentManager()
