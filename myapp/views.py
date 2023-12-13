from django.http import JsonResponse
from rest_framework import permissions
from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from . models import *
from .serializers import *
import re
from django.http import JsonResponse
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
import datetime
from django.core.mail import send_mail
from django.contrib.auth.models import User
from rest_framework.permissions import AllowAny
from django.core.exceptions import ValidationError
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from django.core.validators import validate_email
from django.contrib.auth import authenticate, get_user_model


DATE_FORMAT = 'Y-m-d'
DATETIME_FORMAT = 'Y-m-d H:i:s'


class SignUpView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        email = request.data.get('email')
        if not username or not password:
            return Response({'error': 'لطفا تمامی فیلد هارا پرکنید'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # اعتبارسنجی فرمت ایمیل
            validate_email(email)
        except ValidationError:
            return Response({'error': 'ایمیل وارد شده معتبر نیست'}, status=status.HTTP_400_BAD_REQUEST)

        if User.objects.filter(username=username).exists():
            return Response({'error': 'نام کاربری وجود دارد'}, status=status.HTTP_400_BAD_REQUEST)

        if User.objects.filter(email=email).exists():
            return Response({'error': 'ایمیل وجود دارد'}, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.create_user(
            username=username, password=password, email=email)
        refresh = RefreshToken.for_user(user)
 # غیرفعال کردن refresh token و access token
        refresh.blacklist()
        refresh.access_token.blacklist()

        return Response({
            'message': "کاربر با موفقیت ایجاد شد"
        }, status=status.HTTP_201_CREATED)


class LoginView(APIView):
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        if not email or not password:
            return Response({'error': 'لطفا هر دو بخش را کامل کنید'}, status=status.HTTP_400_BAD_REQUEST)

        User = get_user_model()
        user = User.objects.filter(email=email).first()

        if user:
            user = authenticate(username=user.username, password=password)

            if user:
                refresh = RefreshToken.for_user(user)
                # غیرفعال کردن refresh token و access token
                refresh.blacklist()
                refresh.access_token.blacklist()

                return Response({
                    'message': 'شما با موفقیت وارد شدید و توکن‌ها غیرفعال شدند.'
                }, status=status.HTTP_200_OK)
        return Response({'error': 'پسوورد یا ایمیل اشتباه است'}, status=status.HTTP_401_UNAUTHORIZED)


def index(request):
    return render(request, 'index.html')


class contactUsViewSet(ModelViewSet):

    queryset = contactUs.objects.all()
    serializer_class = contactUsSerializer


def save_message_and_send_email(request):
    if request.method == 'POST':
        full_name = request.POST.get('full_name')
        email = request.POST.get('email')
        message = request.POST.get('message')

        # Save the received message
        contact = contactUs(fullName=full_name,
                            emailContact=email, message=message)
        contact.save()

        # Send an email to the user
        send_mail(
            'Message Received',
            f'{full_name}, کاربر عزیز سایت 100 پیغام شما دریافت شد ممنون از اینکه با ما در ارتباط هستید',
            'contact@bazi100.ir',
            [email],
            fail_silently=False,
        )


class bazi100TeamViewSet(ModelViewSet):

    queryset = bazi100Team.objects.all()
    serializer_class = bazi100TeamSerializer
    permission_classes = [AllowAny]


class commentReplyViewSet(ModelViewSet):

    queryset = commentReply.objects.all()
    serializer_class = commentReplySerializer
    permission_classes = [AllowAny]


# با هر بار لایک کامنت تعداد ان آپدیت میشود
def update_likes_count(self):

    self.likeCount = self.likes.count()
    self.save()


class commentsViewSet(ModelViewSet):

    queryset = comments.objects.all()
    serializer_class = commentsSerializer
    permission_classes = [AllowAny]


@receiver([post_save, post_delete], sender=comments)
def update_post_comment_counts(sender, instance, **kwargs):
    instance.postId.update_comment_counts()


# با هر بار لایک کامنت تعداد ان آپدیت میشود
def update_likes_count(self):

    self.likeCount = self.likes.count()
    self.save()


PROHIBITED_WORDS = ["جمهوری اسلامی", "خامنه ای", "کیر", "کص", "کون", "حرومزاده", "کیری", "کسشر", "فاک", "گاییدم", "مادرتو", "اسکل", "کصخل",
                    "fuck", "dick", "pussy", "wtf", "خفه شو", "مادر جنده", "کسخل", "کونی", "سکس", "sex", "porn", "پورن", "جنده", "گی", "ترنس",
                    "kos", "kon", "koni", "kiri", "kir", "sexy", "فیلم سوپر", "xxx", "لواط", "همجنس بازی", "لز", "لزبین", "عوضی", "خفه شو",
                    "کس نگو", "siktir"]

# بخش ممنوع کردن کلمات


def contains_prohibited_words(text):

    for word in PROHIBITED_WORDS:
        if word in text:
            return True
    return False


# بخش ممنوع کردن گذاشتن لینک
def contains_url(text):
    url_pattern = re.compile(
        r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')
    return bool(url_pattern.search(text))

    # بخش اعتبار سنجی کلمات و لینک ها


def validate_comment_text(value):

    if contains_prohibited_words(value):

        raise ValidationError("کامنت شامل محتوای نامناسب میباشد")

    if contains_url(value):

        raise ValidationError("کامنت حاوی لینک میباشد")


class updateUsernameViewSet(ModelViewSet):

    queryset = updateUsername.objects.all()
    serializer_class = updateUsernameSerializer


def update_Username(request):

    if request.method == 'POST':

        current_username = request.POST['currentUsername']

        new_username = request.POST['newUsername']

        try:
            # Check if the currentUsername exists in the database
            user = updateUsername.objects.get(currentUsername=current_username)

            # Update the newUsername
            user.newUsername = new_username
            user.save()

            return JsonResponse({'message': 'نام کاربری با موفقیت تغییر کرد'})

        except updateUsername.DoesNotExist:
            return JsonResponse({'error': 'نام کاربری وجود ندارد'}, status=404)


class updatePasswordViewSet(ModelViewSet):

    queryset = updatePassword.objects.all()
    serializer_class = updatePasswordSerializer
    permission_classes = [AllowAny]

    def updatePassword(request):

        if request.method == 'POST':

            current_password = request.POST['currentPassword']
            new_password = request.POST['newPassword']
            confirm_password = request.POST['confirmPassword']

            try:
                # Check if the current password matches the one in the database
                user = updatePassword.objects.get(
                    currentPassword=current_password)

                # Check if the new password matches the confirmation password
                if new_password == confirm_password:
                    # Check if the new password meets the minimum length requirement
                    if len(new_password) >= 8:
                        # Update the new password
                        user.newPassword = new_password
                        user.save()
                        return JsonResponse({'message': 'رمز عبور با موفقیت به‌روزرسانی شد'})
                    else:
                        return JsonResponse({'error': 'رمز عبور جدید باید حداقل 8 کاراکتر داشته باشد'}, status=400)
                else:
                    return JsonResponse({'error': 'تأییدیه رمز عبور جدید مطابقت ندارد'}, status=400)

            except updatePassword.DoesNotExist:
                return JsonResponse({'error': 'رمز عبور فعلی اشتباه است'}, status=404)


class pollsViewSet(ModelViewSet):

    queryset = polls.objects.all()
    serializer_class = pollsSerializer
    permission_classes = [AllowAny]


class oldPollsViewSet(ModelViewSet):

    queryset = oldPolls.objects.all()
    serializer_class = oldPollsSerializer
    permission_classes = [AllowAny]


def move_expired_polls():
    currentTime = datetime.datetime.now()
    expired_polls = polls.objects.filter(expiryTimestamp__lt=currentTime)

    for poll in expired_polls:
        old_poll = oldPolls(
            expiryTimestamp=poll.expiryTimestamp, question=poll.question)
        old_poll.save()
        poll.delete()


class choiceViewSet(ModelViewSet):

    queryset = choice.objects.all()
    serializer_class = choiceSerializer
    permission_classes = [AllowAny]


class allPostsViewSet(ModelViewSet):

    queryset = allPosts.objects.all()
    serializer_class = allPostsSerializer
    permission_classes = [AllowAny]


def update_comment_counts(self):
    self.numComments = self.comments.count()
    self.numReplies = self.comments.exclude(commentReply=None).count()
    self.save()


class wallpapersViewSet(ModelViewSet):

    queryset = wallpapers.objects.all()
    serializer_class = wallpapersSerializer
    permission_classes = [AllowAny]


class albumsViewSet(ModelViewSet):

    queryset = albums.objects.all()
    serializer_class = albumsSerializer
    permission_classes = [AllowAny]


class tracksViewSet(ModelViewSet):

    queryset = tracks.objects.all()
    serializer_class = tracksSerializer
    permission_classes = [AllowAny]


class advertisementsViewSet(ModelViewSet):

    queryset = advertisements.objects.all()
    serializer_class = advertisementsSerializer
    permission_classes = [AllowAny]
