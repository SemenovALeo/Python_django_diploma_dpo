import json
import logging
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.models import User
from django.db import transaction
from django.shortcuts import render
from rest_framework.request import Request
from rest_framework.utils.json import loads
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from user_profile.models import Profile, Image
# from api.models import Image

logger = logging.getLogger(__name__)

# Create your views here.

class SignInView(APIView):
    def post(self, request: Request) -> Response:

        try:
            body = json.loads(request.body)
            user_auth_kwargs = dict(
                username=body['username'],
                password=body['password']
            )
            user = authenticate(request, **user_auth_kwargs)
            if user is not None:
                login(request, user)
                logger.debug(f'User {user.username!r} successful sign in')
                return Response(status=status.HTTP_200_OK)
            else:
                logger.error('Authentication failed')
                return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except json.JSONDecodeError:
            logger.error('body parsing JSON error')
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def get(self, request: Request) -> Response:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

class SignUpView(APIView):
    def post(self, request: Request) -> Response:
        data = loads(request.body)

        name = data.get('name', None)
        username = data.get('username', None)
        password = data.get('password', '')

        if not name or not username or not password:
            logger.error('Required fields missing')
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        try:
            first_name, last_name = name.split(maxsplit=1)
        except ValueError:
            first_name, last_name = name, ''

        user_kwargs = {
            'username': username,
            'password': password,
            'first_name': first_name,
            'last_name': last_name
        }

        try:
            with transaction.atomic():
                user = User.objects.create_user(**user_kwargs)
                profile, is_created = Profile.objects.get_or_create(user=user)
                user.profile = profile
                user.save()
        except Exception as e:
            logger.error(f'User creating error: {str(e)}')
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        logger.debug(f'User {user.username!r} successful registered')
        return Response(status=status.HTTP_201_CREATED)

    def get(self, request: Request) -> Response:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

class SignOutView(APIView):
    def post(self, request: Request) -> Response:
        user = request.user
        logout(request)
        logger.debug(f'User {user.username!r} sign out')
        return Response(status=status.HTTP_200_OK)

    def get(self, request: Request) -> Response:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

class ProfileView(APIView):
    def get(self, request: Request) -> Response:

        try:
            profile = self.get_profile()
            avatar = None if not profile.avatar else {
                "src": profile.avatar.avatar.url,
                "alt": "Аватарка отсутсвует",
            }
            data = {
                "fullName": profile.full_name,
                "email": profile.user.email,
                "phone": profile.phone,
                "avatar": avatar
            }
            return Response(data=data, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error(f'Error retrieving user profile: {str(e)}')
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request: Request) -> Response:
        try:
            user = request.user
            if user.is_authenticated:
                name = request.data.get('fullName', '')
                email = request.data.get('email', '')
                phone = request.data.get('phone', '')
                avatar_data = request.data.get('avatar', None)

                try:
                    first_name, last_name = name.split(maxsplit=1)
                except ValueError:
                    first_name, last_name = name, ''

                user.first_name = first_name
                user.last_name = last_name
                user.email = email
                user.save()

                profile = user.profile
                profile.full_name = name
                profile.phone = phone
                profile.save()

                if avatar_data:
                    avatar_src = avatar_data.get('src', '')
                    avatar_alt = avatar_data.get('alt', '')
                    avatar = profile.avatar

                    if avatar:
                        avatar.image.delete()  # Delete previous avatar image if exists
                    else:
                        avatar = Image.objects.create()

                    avatar.image = request.FILES['avatar']
                    avatar.alt_text = avatar_alt
                    avatar.save()

                    profile.avatar = avatar
                    profile.save()

                logger.debug(f'User {user.username!r} updated successful')
                return Response(status=status.HTTP_200_OK)
            else:
                raise Exception('Not authenticated')
        except Exception as e:
            logger.error(f'Error updating user profile: {str(e)}')
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def get_profile(self):
        return self.request.user.profile

class ProfilePasswordView(APIView):

    def post(self, request: Request) -> Response:
        print(type(request))
        try:
            user = request.user
            if user.is_authenticated:
                current_password = request.data.get('currentPassword', '')
                new_password = request.data.get('newPassword', '')
                print(request.POST.dict())
                print(current_password)
                print(new_password)

                if user.check_password(current_password):
                    user.set_password(new_password)
                    user.save()
                    return Response(status=status.HTTP_200_OK)
                else:
                    raise Exception('Current password invalid!')
            else:
                raise Exception('Not authenticated')
        except Exception as e:
            logger.error(f'Error updating user password: {str(e)}')
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class ProfileAvatarView(APIView):
    def post(self, request: Request) -> Response:

        try:
            user = request.user
            if user.is_authenticated:
                avatar_src = request.FILES['avatar']
                avatar = Image.objects.create(avatar=avatar_src)

                profile = user.profile
                if profile.avatar:
                    profile.avatar.delete()  # Delete previous avatar image if exists
                profile.avatar = avatar
                profile.save()

                return Response(status=status.HTTP_200_OK)
            else:
                raise Exception('Not authenticated')
        except Exception as e:
            logger.error(f'Error updating user avatar: {str(e)}')
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
