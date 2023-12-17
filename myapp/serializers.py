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


class pollsSerializer(ModelSerializer):

    class Meta:
        model = Polls
        fields = ('__all__')


class CustomDateTimeField(serializers.DateTimeField):
    def to_representation(self, value):
        formatted_date = value.strftime("%Y,%m,%d,%H,%M")
        formatted_date_parts = formatted_date.split(',')
        formatted_date_parts[1] = str(int(formatted_date_parts[1]))
        formatted_date_parts[2] = str(int(formatted_date_parts[2]))
        return formatted_date_parts


class VoteSerializer(ModelSerializer):
    class Meta:
        model = Vote
        fields = ('__all__')


class ChoiceSerializer(ModelSerializer):

    class Meta:
        model = Choice
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
