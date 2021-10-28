from django.http.response import HttpResponse
from django.shortcuts import redirect, reverse
from django.http import JsonResponse
from authentication.models import User
from posts.models import Restaurant, FoodType, Post, SavedList
from django.views.decorators.csrf import csrf_exempt
from django.db.models.query_utils import Q
from rest_framework.parsers import JSONParser
from rest_framework.decorators import api_view

"""
@csrf_exempt
def user_list(request):
    if request.method == 'GET':
        user_list = User.objects.all()
        serializer = UserSerializer(user_list, many=True)
        return JsonResponse(serializer.data, safe=False)

"""
@csrf_exempt
def get_posts(request):
    allposts = []
    post_list = Post.objects.all()
    for post in post_list:
        item = {}
        item['id'] = post.post_id        
        item['tags'] = FoodType.objects.filter(food_type_id = post.food_type_id_id).first().food_type
        item['name'] = Restaurant.objects.filter(restaurant_id = post.restaurant_id_id).first().name
        item['user'] = User.objects.filter(user_id = post.user_id_id).first().user_name
        item['image'] = post.food_image_url
        # item['status'] = post.approve_status
        allposts.append(item)
    # print(allposts)
    return JsonResponse(allposts, safe=False)
        # serializer = PostSerializer(post_list, many=True)
        # return JsonResponse(serializer.data, safe=False)

@csrf_exempt
def get_saved_list(request):
    if request.method == 'GET':
        user_email = request.GET['user_email']
        users = User.objects.filter(Q(email=user_email))
        user_id = users[0].user_id
        saved_list = SavedList.objects.filter(Q(user_id_id=user_id))
        post_ids = [item.post_id_id for item in saved_list]
        post_list = Post.objects.filter(Q(post_id__in=post_ids))
        allposts = []
        for post in post_list:
            item = {}
            item['post_id'] = post.post_id
            item['profile'] = User.objects.filter(user_id = post.user_id_id).first().user_name
            item['restaurant'] = Restaurant.objects.filter(restaurant_id = post.restaurant_id_id).first().name
            item['rest_url'] = Restaurant.objects.filter(restaurant_id = post.restaurant_id_id).first().website
            item['food_type'] = FoodType.objects.filter(food_type_id = post.food_type_id_id).first().food_type
            item['image_url'] = post.food_image_url
            item['status'] = post.approve_status
            allposts.append(item)
        return JsonResponse(allposts, safe=False)

@csrf_exempt
def remove_saved(request):
    if request.method == 'GET':
        user_email = request.GET['user_id']
        users = User.objects.filter(Q(email=user_email))
        user_id = users[0].user_id
        post_id = request.GET['post_id']
        SavedList.objects.filter(Q(user_id_id=user_id, post_id=post_id)).delete()
        return redirect(reverse('get_saved_list') + '?user_email={}'.format(user_email))

@csrf_exempt
def add_saved(request):
    if request.method == 'GET':
        user_email = request.GET['user_email']
        users = User.objects.filter(Q(email=user_email))
        user_id = users[0].user_id
        post_id = request.GET['post_id']
        sl = SavedList.objects.create(
            user_id_id = user_id,
            post_id_id = post_id
        )
        if sl:
            return HttpResponse(status=200)
        else:
            return HttpResponse(status=401)


@csrf_exempt
def getFoodType(request):
    if request.method == 'GET':
        foodtype = FoodType.objects.values_list('food_type', flat=True)
        # print(list(foodtype))
        return JsonResponse(list(foodtype),safe=False)

@csrf_exempt
def getRestaurant(request):
    if request.method == 'GET':
        restname = Restaurant.objects.values_list('name', flat=True)
        # print(list(restname))
        return JsonResponse(list(restname),safe=False)

@csrf_exempt
@api_view(['POST'])
def savePost(request):
    if request.method == 'POST':
        user_data = JSONParser().parse(request)
        users = User.objects.filter(Q(email=user_data['email']))
        user_id = users[0].user_id
        # print(user_id)
        foodtype=FoodType.objects.filter(Q(food_type=user_data['food_type']))
        # print(foodtype)
        food_type_id=foodtype[0].food_type_id
        # print(food_type_id)
        food_image_url = user_data['profile_photo_url']
        restaurant = Restaurant.objects.filter(Q(name=user_data['restaurant_name']))
        # print(restaurant[0])
        restaurant_id = restaurant[0].restaurant_id
        sl = Post.objects.create(
            user_id = users[0],
            food_type_id = foodtype[0],
            food_image_url = food_image_url,
            restaurant_id = restaurant[0],
        )
        if sl:
            return HttpResponse(status=200)
        else:
            return HttpResponse(status=401)

@csrf_exempt
def getIndvPosts(request):
    user_email = request.GET['user_email']
    users = User.objects.filter(Q(email=user_email))
    user_id = users[0].user_id
    postImage = Post.objects.filter(Q(user_id_id=user_id))
    images=[]
    for i in postImage:
        images.append(i.__dict__['food_image_url'])
    return JsonResponse(images,safe=False)