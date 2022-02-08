from django.db import models
import re
import bcrypt
email_regex = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

#Create your modelsManagers here.
class UserManager(models.Manager):
    def validate_registration(self, post_data):
        errors = {}

        #length of User Name
        if len(post_data['nick_name']) < 3:
            errors['nick_name']="User name must be at least 3 characters."


        # Email matches format
        if len(post_data['email']) == 0:
            errors['email'] = "Email must not be blank."
        elif not email_regex.match(post_data['email']):
            errors['email'] = "Email is not valid."

        #Email is unique
        current_users = User.objects.filter(email=post_data['email'])
        if len(current_users) > 0:
            errors['duplicate'] = "Email already in use."

        # Password was enter (less thn 8 characters)
        if len(post_data['password']) < 8:
            errors['password'] = "Password must be at least 8 characters."

        if post_data['password'] != post_data['confirm_password']:
            errors['mismatch'] ="Password and confirm password must match."

        return errors

    def validate_login(self, post_data):
        errors = {}
        existing_user = User.objects.filter(email=post_data['email'])
        # check existing email
        if len(existing_user) != 1:
            errors['email'] = "User does not exist."
        # email has been entered
        if len(post_data['email']) < 1:
            errors['email'] = "Email must not be blank."
        # Password has been entered
        if len(post_data['password']) < 8:
            errors['password'] = "Password must not be 8 character long."
        # if the email and password match
        elif bcrypt.checkpw(post_data['password'].encode(),
         existing_user[0].password.encode()) != True:
            errors['mismatch'] = "Password and Email do not match."
        return errors


# Create your models here.
class User(models.Model):
    nick_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()


class RecipeManager(models.Manager):
    def validate_recipe(self, post_data):
        errors = {}
        if len(post_data['recipe_name']) < 3:
            errors['recipe_name'] = "Recipe name must be at least 3 characters."
        if len(post_data['recipe_instructions']) < 15:
            errors['recipe_instructions'] = "Description must be at least 15 characters."
        return errors

class Recipe(models.Model):
    recipe_name = models.CharField(max_length=255)
    recipe_ingredients = models.TextField()
    recipe_instructions = models.TextField()
    recipe_servings = models.TextField()
    recipe_cook_time = models.TextField()
    created_by_user = models.ForeignKey(User, related_name="recipes", on_delete=models.CASCADE, null=True)
    # liked_by_users = models.ManyToManyField(User, related_name="liked_recipes")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = RecipeManager()

