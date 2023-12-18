from django.http import JsonResponse
from rest_framework.viewsets import ModelViewSet
from . models import *
from .serializers import *
import re
from django.http import JsonResponse
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.core.mail import send_mail
from django.contrib.auth.models import User
from rest_framework.permissions import AllowAny
from django.core.exceptions import ValidationError
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.core.validators import validate_email
from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.hashers import make_password
from django.views import View
from myapp.models import contactUs
from rest_framework.decorators import action
from rest_framework.decorators import api_view


DATE_FORMAT = 'Y-m-d'
DATETIME_FORMAT = 'Y-m-d H:i:s'


class SignUpView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        confirmPassword = request.data.get('confirmPassword')
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
            return Response({'error': "ایمیل وارد شده قبلا ثبت شده است"}, status=status.HTTP_400_BAD_REQUEST)

        if len(password) < 8:
            return Response({'error': 'رمز عبور نمی‌تواند کمتر از 8 کاراکتر باشد'}, status=status.HTTP_400_BAD_REQUEST)

        if password != confirmPassword:
            return Response({'error': 'رمز عبور و تایید آن باید یکسان باشند'}, status=status.HTTP_400_BAD_REQUEST)

        if len(password) < 8:
            return Response({'error': "رمز عبور نمیتواند کمتر از 8 کاراکتر باشد"}, status=status.HTTP_400_BAD_REQUEST)

        # ساخت کاربر با هش شده کردن رمز عبور
        user = User.objects.create(
            username=username, password=make_password(password), email=email)

        # بازگرداندن اطلاعات کاربری به عنوان پاسخ
        response_data = {
            'username': user.username,
            'password': user.password,
            'email': user.email,
            'message': 'ثبت نام با موفقیت انجام شد'
        }
        return Response(response_data, status=status.HTTP_201_CREATED)


class LoginView(APIView):
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        if not email or not password:
            return Response({'error': "لطفا هردو فیلد ایمیل و رمزعبور را وارد کنید"}, status=status.HTTP_400_BAD_REQUEST)

        User = get_user_model()
        user = User.objects.filter(email=email).first()

        if user:
            user_auth = authenticate(username=user.username, password=password)

            if user_auth:
                return Response({
                    'message': 'با موفقیت وارد شدید',
                    'user': {
                        'id': user.id,
                        'username': user.username,
                        'email': user.email,
                    }
                }, status=status.HTTP_200_OK)

        return Response({'error': 'ایمیل یا رمز عبور اشتباه است'}, status=status.HTTP_401_UNAUTHORIZED)


class ChangeUsernameView(APIView):

    permission_classes = [AllowAny]

    def put(self, request):
        email = request.data.get('email')
        newUsername = request.data.get('newUsername')

        if not email or not newUsername:
            return Response({'error': 'لطفا هردو فیلد ایمیل و نام کاربری را وارد کنید'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({'error': "کاربر با این ایمیل یافت نشد"}, status=status.HTTP_404_NOT_FOUND)

        user.username = newUsername
        user.save()

        return Response({'message': 'نام کاربری به‌روزرسانی شد'}, status=status.HTTP_200_OK)


class ChangePasswordView(APIView):

    permission_classes = [AllowAny]

    def put(self, request):
        oldPassword = request.data.get('oldPassword')
        newPassword = request.data.get('newPassword')
        confirmPassword = request.data.get('confirmPassword')
        email = request.data.get('email')

        if not oldPassword or not newPassword or not confirmPassword:
            return Response({'error': 'لطفا همه فیلدهارا وارد کنید'}, status=status.HTTP_400_BAD_REQUEST)

        if newPassword != confirmPassword:
            return Response({'error': 'رمزعبور جدید با تایید آن همخوانی ندارد'}, status=status.HTTP_400_BAD_REQUEST)

        if len(newPassword) < 8:
            return Response({'error':  "رمز عبور نمیتواند کمتر از 8 کاراکتر باشد"}, status=status.HTTP_400_BAD_REQUEST)

        try:

            user = User.objects.get(email=email)
            if user.check_password(oldPassword):
                user.set_password(newPassword)
                user.save()
                return Response({'message': "رمز عبور شما با موفقیت تغییر کرد"}, status=status.HTTP_200_OK)
            else:
                return Response({'error': "رمز عبور فعلی نادرست است"}, status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            return Response({'error':  " نام کاربری وارد شده یافت نشد"}, status=status.HTTP_404_NOT_FOUND)


class ContactUsAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        fullName = request.data.get('fullName')
        emailContact = request.data.get('emailContact')
        message = request.data.get('message')

        if not fullName or not emailContact or not message:
            return JsonResponse({'error': 'لطفاً تمام فیلدها را پر کنید'}, status=400)

        created_contact = contactUs.objects.create(
            fullName=fullName, emailContact=emailContact, message=message)

        if created_contact:
            # ارسال ایمیل
            send_mail(
                "درخواست کاربر از طریق بخش تماس باما سایت بازی 100",
                "کاربر عزیز بازی 100 درخواست شما با موفقیت ارسال شد و پس از بررسی پاسخ مورد نظر ارسال میشود",
                "javadjs197@gmail.com",
                [emailContact],
                fail_silently=False,
            )

            return JsonResponse({'message': 'اطلاعات با موفقیت ذخیره شد و ایمیل ارسال شد.'}, status=201)
        else:
            return JsonResponse({'error': 'خطایی در ذخیره‌سازی اطلاعات رخ داده است.'}, status=500)


class bazi100TeamViewSet(ModelViewSet):

    queryset = bazi100Team.objects.all()
    serializer_class = bazi100TeamSerializer
    permission_classes = [AllowAny]


class commentView(APIView):

    queryset = comments.objects.all()
    serializer_class = commentsSerializer
    permission_classes = [AllowAny]

    def post(self, request):
        commentId = request.data.get('commentId')
        userId = request.data.get('userId')

        try:
            comment = comments.objects.get(id=commentId)
        except comments.DoesNotExist:
            return Response({"message": "کامنت مورد نظر یافت نشد"}, status=status.HTTP_404_NOT_FOUND)

        # چک کردن اینکه کاربر قبلا لایک کرده یا نه
        if like.objects.filter(user=userId, comment=commentId).exists():
            return Response({"message": "شما قبلا این کامنت را لایک کرده‌اید"}, status=status.HTTP_400_BAD_REQUEST)

        # ایجاد لایک جدید برای کاربر
        like = like.objects.create(user=userId, comment=commentId)

        # به‌روزرسانی تعداد لایک‌های کامنت
        comment.likeCount = like.objects.filter(comment=commentId).count()
        comment.save()

        return Response({"message": "کامنت با موفقیت لایک شد"}, status=status.HTTP_201_CREATED)


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


class pollsViewSet(ModelViewSet):
    queryset = Polls.objects.all()
    serializer_class = pollsSerializer
    permission_classes = [AllowAny]


class choiceViewSet(ModelViewSet):
    queryset = Choice.objects.all()
    serializer_class = ChoiceSerializer
    permission_classes = [AllowAny]


class voteViewSet(ModelViewSet):
    queryset = Vote.objects.all()
    serializer_class = VoteSerializer
    permission_classes = [AllowAny]


@api_view(['POST'])
def voteChoice(request):
    user = request.data.get('user')
    poll = request.data.get('poll')
    choice = request.data.get('choice')

    try:
        user = User.objects.get(pk=user)
        poll = Polls.objects.get(pk=poll)
        choice = Choice.objects.get(pk=choice)
    except (User.DoesNotExist, Polls.DoesNotExist, Choice.DoesNotExist) as e:
        raise ValidationError({'error': "یکی از مقادیر نادرست وارد شده"})

    user_voted = Vote.objects.filter(
        user=user, poll=poll).exists()
    if user_voted:
        return Response({'error': "شما دراین نظرسنجی شرکت کرده اید"}, status=status.HTTP_400_BAD_REQUEST)

    Vote.objects.create(user=user, poll=poll, choice=choice)

    # Update numVotes in Choice model
    choice.numVotes = Vote.objects.filter(choice=choice).count()
    choice.save()

    return Response({'message': 'انتخاب شما با موفقیت ثبت شد'}, status=status.HTTP_200_OK)


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
