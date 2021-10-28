from django.contrib import admin
from posts.models import Restaurant, FoodType, Post, SavedList

# Register your models here.
admin.site.register(Restaurant)
admin.site.register(FoodType)
admin.site.register(Post)
admin.site.register(SavedList)