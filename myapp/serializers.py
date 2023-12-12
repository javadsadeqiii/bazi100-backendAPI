from rest_framework.serializers import ModelSerializer
from .models import *
from django.contrib.auth import authenticate, login
from django.urls import path
from django.core.validators import EmailValidator
from django.contrib.auth.models import User
from rest_framework import serializers


class platformSeriallizer(ModelSerializer):

    class Meta:
        model = platform
        fields = ('__all__')


class contactUsSerializer(ModelSerializer):

    class Meta:

        model = contactUs
        fields = ('__all__')


class oldPollsSerializer(ModelSerializer):

    class Meta:

        model = oldPolls
        fields = ('__all__')


class pollsSerializer(ModelSerializer):

    class Meta:

        model = polls
        fields = ('__all__')


class choiceSerializer(ModelSerializer):

    class Meta:
        model = choice
        fields = ('__all__')


class commentReplySerializer(ModelSerializer):

    class Meta:

        model = commentReply
        fields = ('__all__')


class commentsSerializer(ModelSerializer):

    class Meta:

        model = comments
        fields = ('__all__')


class contactUsSerializer(ModelSerializer):

    class Meta:

        model = contactUs
        fields = ('__all__')


class updateUsernameSerializer(ModelSerializer):

    class Meta:

        model = updateUsername
        fields = ('currentUsername', 'newUsername')


class updatePasswordSerializer(ModelSerializer):

    class Meta:
        model = updatePassword
        fields = ('currentPassword', 'newPassword', 'confirmNewPassword')


# class userRegisterSerializer(serializers.ModelSerializer):

  #  email = serializers.EmailField()  # Disable default email validation
    # Disable default username validation
  #  username = serializers.CharField(validators=[])
  #  password = serializers.CharField()

  #  class Meta:
   #     model = User
   #     fields = ['email', 'username', 'password']

   # def validate(self, attrs):
    #    email = attrs.get('email')
    #    username = attrs.get('username')

        # Check if email is unique
    #    if User.objects.filter(email=email).exists():
        #       raise serializers.ValidationError("ایمیل قبلا ثبت شده")

        # Check if username is unique
      #  if User.objects.filter(username=username).exists():
      #      raise serializers.ValidationError("نام کاربری قبلا ثبت شده")

        #   return attrs


# class userLoginSerializer(ModelSerializer):

  #  email = serializers.EmailField()  # Disable default email validation
  #  password = serializers.CharField()

  #  class Meta:
   #     model = User
  #      fields = ['email', 'password']

  #  def validate(self, attrs):
    #    email = attrs.get('email')
        #   password = attrs.get('password')

        # Perform custom validation for email and password combination
        #   user = authenticate(email=email, password=password)
        #   if not user:
        #    raise serializers.ValidationError("Invalid email or password.")

        #   return attrs


class allPostsSerializer(ModelSerializer):

    class Meta:
        model = allPosts
        fields = ('__all__')


class wallpapersSerializer(ModelSerializer):
    class Meta:
        model = wallpapers
        fields = ('__all__')


class albumsSerializer(ModelSerializer):

    class Meta:

        model = albums

        fields = ('__all__')


class tracksSerializer(ModelSerializer):

    class Meta:

        model = tracks

        fields = ('__all__')


class bazi100TeamSerializer(ModelSerializer):

    class Meta:

        model = bazi100Team
        fields = ('__all__')


class advertisementsSerializer(ModelSerializer):

    class Meta:

        model = advertisements
        fields = ('__all__')
