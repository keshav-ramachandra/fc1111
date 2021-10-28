from rest_framework import serializers
from posts.models import Restaurant, FoodType, Post, SavedList

class RestaurantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restaurant
        fields = ('name', 'website', 'contact', 'address', )

class FoodTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = FoodType
        fields = ('food_type', )

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('user_id', 'restaurant_id', 'food_type_id', 'food_image_url', 'approve_status', )

class SavedListSerializer(serializers.ModelSerializer):
    class Meta:
        model = SavedList
        fields = ('user_id', 'post_id', )