from rest_framework.serializers import ModelSerializer
from .models import *
from rest_framework import serializers
# from django.core.validators import RegexValidator
from rest_framework import serializers
from django.core.validators import validate_email
from django.core.exceptions import ValidationError as DjangoValidationError
from django.contrib.auth.forms import PasswordResetForm


class PasswordResetSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        PasswordResetForm({'email': value})  
        return value



class SubscriberSerializer(serializers.ModelSerializer):
    
    createdAt = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S')
    class Meta:
        model = Subscriber
        fields = '__all__'

    def validate_email(self, value):

        try:
            validate_email(value)
        except DjangoValidationError:
            raise serializers.ValidationError("فرمت ایمیل نادرست است")
        existing_subscriber = Subscriber.objects.filter(email=value).exists()
        existing_user = User.objects.filter(email=value).exists()

        if existing_subscriber or existing_user:
            raise serializers.ValidationError(
                "ایمیل وارد شده وجود دارد")

        return value

    def create(self, validated_data):
        return Subscriber.objects.create(**validated_data)


class ReplyLikeHistorySerializer(ModelSerializer):

    class Meta:

        model = ReplyLikeHistory
        fields = ('__all__')


class CommentLikeHistorySerializer(ModelSerializer):

    class Meta:
        model = CommentLikeHistory
        fields = ('__all__')


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


class CommentsSerializer(ModelSerializer):

    createdAt = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S')

    class Meta:
        model = Comments
        fields = ('__all__')


class CommentLikeSerializer(ModelSerializer):

    class Meta:
        model = CommentLike
        fields = ('__all__')


class ReplySerializer(ModelSerializer):

    createdAt = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S')

    class Meta:
        model = Reply
        fields = ('__all__')


class ReplyLikeSerializer(ModelSerializer):

    class Meta:
        model = ReplyLike
        fields = ('__all__')


class contactUsSerializer(ModelSerializer):

    class Meta:

        model = contactUs
        fields = ('__all__')


class AllPostsSerializer(ModelSerializer):

    class Meta:
        model = AllPosts
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
