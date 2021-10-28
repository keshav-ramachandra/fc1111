from django.urls import path
from adminconsole import views as admin_views

urlpatterns = [
    path('', admin_views.index, name='index'),
    path('admin_login', admin_views.admin_login, name='admin_login'),
    path('logout', admin_views.logout_request, name='logout'),
    path('admin_login/', admin_views.admin_login, name='admin_login'),
    path('admin_register/', admin_views.admin_register, name='admin_register'),
    path('admin_register', admin_views.admin_register, name='admin_register'),
    path('add_food_type/', admin_views.add_food_type, name='add_food_type'),
    path('add_food_type', admin_views.add_food_type, name='add_food_type'),
    path('add_restaurant/', admin_views.add_restaurant, name='add_restaurant'),
    path('add_restaurant', admin_views.add_restaurant, name='add_restaurant'),
    path('admin_home/', admin_views.admin_home, name='admin_home'),
    path('admin_home', admin_views.admin_home, name='admin_home'),
    path('approve_images/', admin_views.approve_images, name='approve_images'),
    path('approve_images', admin_views.approve_images, name='approve_images'),
    # path('dummy_data_generator_posts/', admin_views.dummy_data_generator_posts, name='dummy_data_generator_posts'),
    path('remove_tag', admin_views.remove_tag, name='remove_tag'),
    path('remove_restaurant', admin_views.remove_restaurant, name='remove_restaurant'),
    path('approve_post', admin_views.approve_post, name='approve_post'),
    path('discard_post', admin_views.discard_post, name='discard_post'),
    path('dummy_data_generator_user', admin_views.dummy_data_generator_user, name='dummy_data_generator_user'),
    path('dummy_data_generator_food', admin_views.dummy_data_generator_food, name='dummy_data_generator_food'),
    path('dummy_data_generator_user/', admin_views.dummy_data_generator_user, name='dummy_data_generator_user'),
    path('dummy_data_generator_food/', admin_views.dummy_data_generator_food, name='dummy_data_generator_food'),
    path('dummy_data_generator_restaurant', admin_views.dummy_data_generator_restaurant, name='dummy_data_generator_restaurant'),
    path('edit_food_tag', admin_views.edit_food_tag, name='edit_food_tag'),
    path('edit_restaurant_details', admin_views.edit_restaurant_details, name='edit_restaurant_details'),
    
]