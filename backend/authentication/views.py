# Create your views here.
from datetime import datetime
from django.core.mail import send_mail
from django.conf import settings
from django.http import JsonResponse, HttpResponse
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.parsers import JSONParser
from authentication.models import User, FreemiumUser, Friends
from authentication.serializers import UserSerializer
from django.db.models.query_utils import Q
from django.core.mail import send_mail, BadHeaderError
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.contrib.auth.hashers import make_password, check_password
from django.views.decorators.csrf import csrf_exempt 
from django.shortcuts import redirect, reverse
import random
import string


@csrf_exempt
@api_view(['POST'])
def register(request):
	user_data = JSONParser().parse(request)
	user_serializer = UserSerializer(data=user_data)
	if user_serializer.is_valid():
		user = User.objects.create(user_name = user_data['user_name'],first_name = user_data['first_name'],last_name = user_data['last_name'],email = user_data['email'],password = make_password(user_data['password']),phone_number = user_data['phone_number'],dob = user_data['dob'],last_login = datetime.now())
		user.save()
		send_mail(subject='Food Court Registration',message='Thank you for Registering',from_email=settings.EMAIL_HOST_USER,recipient_list=[user_data['email']])
		return HttpResponse("success",status=status.HTTP_201_CREATED)
	return JsonResponse(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@csrf_exempt
@api_view(['POST'])
def postImage(request):
	user_data = JSONParser().parse(request)
	user = User.objects.filter(Q(email= user_data['email'])).first()
	print(user)
	user.profile_photo_url=user_data['profile_photo_url']
	user.save()
	return HttpResponse("success",status=status.HTTP_201_CREATED)


@csrf_exempt
def get_user(request):
	user_email = request.GET['user_email']
	# print(user_email)
	users = User.objects.filter(Q(email=user_email))
	# print(users)
	user_detail={}
	user_detail['user_name'] = users[0].user_name
	user_detail['first_name'] = users[0].first_name
	user_detail['last_name'] = users[0].last_name
	user_detail['phone_number'] = users[0].phone_number
	user_detail['profile_photo_url'] = users[0].profile_photo_url
	# print(user_detail)
	return JsonResponse(user_detail, safe=False)

@csrf_exempt
@api_view(['POST'])
def update(request):
	user_data = JSONParser().parse(request)
	email = user_data['email']
	user = User.objects.filter(email= user_data['email']).first()
	user.first_name=user_data['first_name']
	user.last_name=user_data['last_name']
	user.user_name=user_data['user_name']
	user.phone_number=user_data['phone_number']
	user.save()
	# updated_user = User.objects.filter(email= user_data['email']).first()
	return redirect('/auth/get_user' + f'?user_email={email}')
	# return HttpResponse('User profile updated successfully',status=200)

@csrf_exempt
@api_view(['POST'])
def login(request):
	data = JSONParser().parse(request)
	try:
		user = User.objects.filter(email= data['email']).first()
		if(check_password(data['password'], user.password)):
			user.last_login = datetime.now()
			user.is_active = True
			user.save()
			request.session['user'] = user.email
			return HttpResponse('login success',status=200)
		else:
			return HttpResponse('login failure',status=401)
	except User.DoesNotExist:
		return HttpResponse("user not registered",status=status.HTTP_404_NOT_FOUND)


@csrf_exempt
@api_view(['GET'])
def check_email(request):
	user_email = request.GET['user_email']
	try:
		user = User.objects.filter(email=user_email).first()
		if user:
			return HttpResponse('user exists',status=200)
		else:
			return HttpResponse("user doesn't exist",status=404)
	except User.DoesNotExist:
		return HttpResponse("user doesn't exist",status=404)

"""
@csrf_exempt
@api_view(['POST'])
def password_reset_request(request):
	data = JSONParser().parse(request)
	email = data['email']
	allusers = User.objects.filter(Q(email=email))
	if allusers.exists():
		for user in allusers:
			email = user.email
			subject = 'Password Reset Requested'
			email_template_name = 'registration/password_reset_email.txt'
			c = {
			'email': email,
			'domain':'127.0.0.1:8000',
			'site_name': 'The Food Court',
			'uid': urlsafe_base64_encode(force_bytes(user.user_id)),
			'token': default_token_generator.make_token(user),
			'protocol': 'http',
			}
			emailstr = render_to_string(email_template_name, c)
			try:
				send_mail(subject, emailstr, settings.EMAIL_HOST_USER , [email], fail_silently=False)
			except BadHeaderError:
				return HttpResponse('Invalid header found.', status=400)
		return HttpResponse(status=200)
		

""" 
def id_generator(size=11, chars=string.ascii_uppercase + string.digits):
	return ''.join(random.choice(chars) for _ in range(size))

@csrf_exempt
@api_view(['POST'])
def forgotPassword(request):
	data = JSONParser().parse(request)
	email = data['email']
	try:
		pass_code = id_generator()
		# print("pass", pass_code)
		User.objects.filter(email=email).update(forget_pass_code=pass_code)
	except User.DoesNotExist:
		return HttpResponse("user not registered",status=status.HTTP_404_NOT_FOUND)
	subject = 'Food Court Change Password'
	html_message="<h1>Forgot your password?</h1><p>Please use the code "+pass_code+" to reset your password.</p>"
	from_email = settings.EMAIL_HOST_USER
	to = email
	send_mail(subject=subject, message='content', from_email = from_email , recipient_list=[to], html_message=html_message)
	return HttpResponse("success",status=status.HTTP_201_CREATED)


@csrf_exempt
@api_view(['POST'])
def changePassword(request):
	user_data = JSONParser().parse(request)
	try:
		user_pass = User.objects.filter(email=user_data['email']).first().forget_pass_code
		if(user_pass != user_data['passcode'] or user_pass == ''):
			return HttpResponse("Link not valid",status=status.HTTP_404_NOT_FOUND)
		User.objects.filter(email=user_data['email']).update(password=make_password(user_data['password']), forget_pass_code='')
		return HttpResponse("password changed",status=status.HTTP_201_CREATED)
	except User.DoesNotExist:
		return HttpResponse("user not registered",status=status.HTTP_404_NOT_FOUND)

@csrf_exempt
@api_view(['POST'])
def invite_user(request):
	data = JSONParser().parse(request)
	invitee = data['invitee']
	inviter = data['inviter']
	inv = User.objects.filter(email=inviter).first()
	user_name = inv.user_name
	newuser = User.objects.filter(email=invitee).first()
	if newuser:
		return HttpResponse('User already exists', status=404)
	try:
		send_mail(
		subject = 'Food Court Registration',
		message = f'Your friend {user_name} is inviting you to try The Food Court app',
		from_email=settings.EMAIL_HOST_USER,
		recipient_list=[invitee],
		fail_silently=False)
		return HttpResponse('Invite sent', status=200)
	except BadHeaderError:
		return HttpResponse('Invalid header found.', status=400)


@csrf_exempt
@api_view(['POST'])
def add_friend(request):
	data = JSONParser().parse(request)
	initiator = data['initiator']
	friend = data['friend']
	init = User.objects.only('email').get(email=initiator)
	try:
		frnd = User.objects.only('email').get(email=friend)
	except:
		return HttpResponse("No such user exists", status = 500)
	try:
		frnd_req = Friends.objects.create(
			initiator = init,
			friend = frnd,
			init = init.user_id
		)
		if frnd_req:
			return HttpResponse('Friend request sent', status = 200)
	except:
		return HttpResponse("You may already be friends!", status = 500)

@csrf_exempt
@api_view(['GET'])	
def get_friend_requests(request):
	email = request.GET['user_email']
	user = User.objects.only('email').get(email=email)
	user_id = user.user_id
	all_requests = Friends.objects.filter(friend=user, request_status=0)
	friend_requests = []
	for req in all_requests:
		item = {}
		item['id'] = req.id
		item['sender'] = User.objects.get(user_id=req.initiator_id).user_name
		item['sender_email'] = User.objects.get(user_id=req.initiator_id).email
		if (user_id != req.init):
			friend_requests.append(item)
	return JsonResponse(friend_requests, safe=False)

@csrf_exempt
@api_view(['GET'])	
def accept_friend_request(request):
	request_id = request.GET['request_id']
	req = Friends.objects.filter(id=request_id).first()
	try:
		req.request_status = 1
		print(req.request_status)
		req.save()
		return HttpResponse('Request Accepted', status = 200)
	except:
		return HttpResponse('An error has occured', status = 500)

@csrf_exempt
@api_view(['GET'])	
def decline_friend_request(request):
	request_id = request.GET['request_id']
	req = Friends.objects.filter(id=request_id).first()
	try:
		req.request_status = -1
		req.save()
		return HttpResponse('Request Declined', status = 200)
	except:
		return HttpResponse('An error has occured', status = 500)

@csrf_exempt
@api_view(['GET'])	
def delete_friend(request):
	request_id = request.GET['request_id']
	req = Friends.objects.filter(id=request_id).first()
	user1 = req.initiator_id
	user2 = req.friend_id
	try:
		rel1 = Friends.objects.filter(initiator_id=user1, friend_id=user2).first()
		rel2 = Friends.objects.filter(initiator_id=user2, friend_id=user1).first()
	except:
		return HttpResponse('Users not found', status=404)
	try:
		rel1.delete()
		rel2.delete()
		return HttpResponse('Friend deleted', status = 200)
	except:
		return HttpResponse('An error has occured', status = 500)

@csrf_exempt
@api_view(['GET'])
def get_friends(request):
	email = request.GET['user_email']
	user = User.objects.only('email').get(email=email)
	all_requests = Friends.objects.filter(initiator=user, request_status=1)
	friend_requests = []
	for req in all_requests:
		item = {}
		item['id'] = req.id
		item['friend'] = User.objects.get(user_id=req.friend_id).user_name
		item['friend_email'] = User.objects.get(user_id=req.friend_id).email
		friend_requests.append(item)
	return JsonResponse(friend_requests, safe=False)

"""
@csrf_exempt
@api_view(['POST'])
def fetchPostsForSavedList(request):
		per_request = 30
		data = JSONParser().parse(request)
		email = data['email']
		try:
			user = User.objects.filter(email= data['email']).first()
		except User.DoesNotExist:
			return HttpResponse("user not registered",status=status.HTTP_404_NOT_FOUND)
		count = int(data['count']) * 30; 
		posts = Post.objects.filter(user_id = user).order_by('post_time')[count : count + per_request]
		scroll_serializer = ScrollDataSerializer(posts, many=True) 
		return HttpResponse(json.dumps(scroll_serializer.data), content_type="application/json")

@csrf_exempt
@api_view(['POST'])
def fetchPostsForRegularUser(request):
		per_request = 30
		data = JSONParser().parse(request)
		email = data['email']
		try:
			user = User.objects.filter(email= data['email']).first()
		except User.DoesNotExist:
			return HttpResponse("user not registered",status=status.HTTP_404_NOT_FOUND)
		count = int(data['count']) * 30; 
		posts = Post.objects.filter(user_id = user).order_by('post_time')[count : count + per_request]
		swipe_serializer = SwipeDataSerializer(posts, many=True) 
		return HttpResponse(json.dumps(swipe_serializer.data), content_type="application/json")

@csrf_exempt
@api_view(['POST'])
def RegisterAndFetchPostsForFreemiumUser(request):
	quota = 15
	data = JSONParser().parse(request)
	user=''
	try:
		user = FreemiumUser.objects.get(device_id = data['device_id'])
		print("user is there already", user.device_id)
	except:
		user = FreemiumUser.objects.create(device_id = data['device_id'])
		print("no user", user.device_id)
	print("user out ", user.device_id)
	if(user.quota_done == True):
		return HttpResponse("Your quota has finished, Please register to see more posts",status = status.HTTP_400_BAD_REQUEST)
	else:
		user.quota_done=True
		user.save()
		posts = Post.objects.all().order_by('post_time')[:quota]
		swipe_serializer = SwipeDataSerializer(posts, many=True) 
		return HttpResponse(json.dumps(swipe_serializer.data), content_type="application/json")

"""

