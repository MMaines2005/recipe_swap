from django.db import models
import re
import bcrypt
email_regex = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

#Create your modelsManagers here.
class UserManager(models.Manager):
    def validate_registration(self, post_data):
        errors = {}
        
        if len(post_data['nick_name']) < 3:
            errors['nick_name']="User name must be at least 3 characters."
        if len(post_data['email']) == 0:
            errors['email'] = "Email must not be blank."
        if len(post_data['password']) < 8:
            errors['password'] = "Password must be at least 8 characters."
        if post_data['password'] != post_data['confirm_password']:
            errors['confirm_password'] ="Password and confirm password must match."
        if len(User.objects.filter(email=post_data['email'])) > 0:
            errors['email'] = "Email already in use."
        if errors:
            return (False, errors)
        else:
            hashed_pw = bcrypt.hashpw(post_data['password'].encode(),
            bcrypt.gensalt()).decode()
            user = User.objects.create(
                nick_name=post_data['nick_name'],
                email=post_data['email'],
                password=hashed_pw,
            )
            return (True, user)

    def validate_login(self, post_data):
        errors = {}
        if len(post_data['email']) < 1:
            errors['email'] = "Email must not be blank."
        if len(post_data['password']) < 1:
            errors['password'] = "Password must not be blank."
        if len(User.objects.filter(email=post_data['email'])) < 1:
            errors['email'] = "Email/password is incorrect."
        if errors:
            return (False, errors)
        else:
            user = User.objects.filter(email=post_data['email'])[0]
            return (True, user)

# Create your models here.
class User(models.Model):
    nick_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()
