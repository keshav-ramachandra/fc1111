from django.db import models
from authentication.models import User
from django.core.validators import RegexValidator

class Restaurant(models.Model):

    restaurant_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, unique=True)
    website = models.URLField(max_length = 500, blank=True)
    phone_regex = RegexValidator(regex=r'^\d{9,15}$', message="Phone number must be entered in the format: '999999999'. From 9 to 15 digits allowed.")
    contact = models.CharField(validators=[phone_regex], max_length=15, blank=True) # validators should be a list
    # contact = models.IntegerField(min_length=10, max_length=10, default=0)
    address = models.TextField(max_length=500, default='')

    def __str__(self):
        return self.name

class FoodType(models.Model):

    food_type_id = models.AutoField(primary_key=True)
    food_type = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.food_type

class Post(models.Model):
    
    post_id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    restaurant_id = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    food_type_id = models.ForeignKey(FoodType, on_delete=models.CASCADE)
    food_image_url = models.URLField(max_length = 200, blank=True)
    approve_status = models.SmallIntegerField(default=0)

class SavedList(models.Model):

    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    post_id = models.ForeignKey(Post, on_delete=models.CASCADE)
    
    class Meta:
        unique_together = ('user_id', 'post_id',) 
