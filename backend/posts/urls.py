from django.urls import path
from posts import views as post_views

urlpatterns = [
    path('posts/get_saved_list', post_views.get_saved_list, name='get_saved_list'),
    path('posts/remove_saved', post_views.remove_saved, name='remove_saved'),
    path('posts/add_saved', post_views.add_saved, name='add_saved'),
    path('posts/get_posts', post_views.get_posts, name='get_posts'),
    path('posts/getFoodType', post_views.getFoodType, name='getFoodType'),
    path('posts/getRestaurant', post_views.getRestaurant, name='getRestaurant'),
    path('posts/savePost', post_views.savePost, name='savePost'),
    path('posts/getIndvPosts', post_views.getIndvPosts, name='getIndvPosts'),
]