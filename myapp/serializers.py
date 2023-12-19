from rest_framework.serializers import ModelSerializer
from .models import *
from rest_framework import serializers
from django.core.validators import RegexValidator
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


class commentsSerializer(ModelSerializer):

    restricted_words = ["جمهوری اسلامی", "خامنه ای", "کیر", "کص", "کون", "حرومزاده", "کیری", "کسشر", "فاک", "گاییدم", "مادرتو", "اسکل", "کصخل",
                        "fuck", "dick", "pussy", "wtf", "خفه شو", "مادر جنده", "کسخل", "کونی", "سکس", "sex", "porn", "پورن", "جنده", "گی", "ترنس",
                        "kos", "kon", "koni", "kiri", "kir", "sexy", "فیلم سوپر", "xxx", "لواط", "همجنس بازی", "لز", "لزبین", "عوضی", "خفه شو",
                        "کس نگو", "siktir"]

    restricted_word_validator = RegexValidator(
        regex='|'.join(restricted_words),
        message='استفاده از کلمات ممنوعه مجاز نیست!'
    )

    link_validator = RegexValidator(
        regex=r'^((?!http[s]?://).)*$',
        message='آپلود هرگونه لینک مجاز نیست'
    )

    commentText = serializers.CharField(
        validators=[
            restricted_word_validator,
            link_validator,
        ]
    )

    class Meta:
        model = comments
        fields = ('__all__')

    def validate_commentText(self, value):
        for word in self.restricted_words:
            if word in value:
                raise serializers.ValidationError(
                    'استفاده از کلمات ممنوعه مجاز نیست!')
        return value


class commentLikeSerializer(ModelSerializer):

    class Meta:
        model = commentLike
        fields = ('__all__')


class replySerializer(ModelSerializer):

    restricted_words = ["جمهوری اسلامی", "خامنه ای", "کیر", "کص", "کون", "حرومزاده", "کیری", "کسشر", "فاک", "گاییدم", "مادرتو", "اسکل", "کصخل",
                        "fuck", "dick", "pussy", "wtf", "خفه شو", "مادر جنده", "کسخل", "کونی", "سکس", "sex", "porn", "پورن", "جنده", "گی", "ترنس",
                        "kos", "kon", "koni", "kiri", "kir", "sexy", "فیلم سوپر", "xxx", "لواط", "همجنس بازی", "لز", "لزبین", "عوضی", "خفه شو",
                        "کس نگو", "siktir"]

    # Validator برای جلوگیری از کلمات ممنوعه
    restricted_word_validator = RegexValidator(
        regex='|'.join(restricted_words),
        message='استفاده از کلمات ممنوعه مجاز نیست!'
    )

    link_validator = RegexValidator(
        regex=r'^((?!http[s]?://).)*$',
        message='آپلود هرگونه لینک مجاز نیست'
    )

    replyText = serializers.CharField(
        validators=[
            restricted_word_validator,
            link_validator,
        ]
    )

    class Meta:
        model = reply
        fields = ('__all__')

    def validate_replyText(self, value):
        for word in self.restricted_words:
            if word in value:
                raise serializers.ValidationError(
                    'استفاده از کلمات ممنوعه مجاز نیست!')
        return value


class replyLikeSerializer(ModelSerializer):

    class Meta:
        model = replyLike
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
