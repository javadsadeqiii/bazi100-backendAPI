from django.http import JsonResponse
from . models import *
from .serializers import *
import re
from django.http import JsonResponse
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
from myapp.models import ContactUs
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework import generics
from rest_framework import viewsets
from rest_framework.decorators import action
from django.conf import settings
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.core.cache import cache
from django.contrib.auth.models import User
from .authentication import TokenAuthentication 
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from django.utils.html import strip_tags
import datetime
from django.http import HttpResponse
from datetime import datetime
from django.core.cache import cache
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from datetime import timezone
import datetime
from datetime import timezone, datetime 
from PIL import Image
from django.utils import timezone
from .serializers import CustomUserSerializer
from django.utils.translation import gettext_lazy as _
from django.db.models import F
from datetime import timedelta

DATE_FORMAT = 'Y-m-d'
DATETIME_FORMAT = 'Y-m-d H:i:s'






class DownloadLimitView(APIView):
    
    def reset_download_count(self, user):
        current_time = timezone.now()
        if (current_time - user.resetDate) > timedelta(minutes=10):
            user.wallpaperDownloads = 3
            user.soundtrackDownloads = 3
            user.resetDate = current_time
            user.save()

  #  def get(self, request, user_id):
   #     user = get_object_or_404(CustomUser, id=userId)
   #     self.reset_download_count(user)
   #     return Response({
    #        'wallpaperDownloads': user.wallpaperDownloads,
    #        'soundtrackDownloads': user.soundtrackDownloads,
     #   })

    def post(self, request):
        userId = request.data.get('userId')
        downloadType = request.data.get('downloadType')

        try:
            user = CustomUser.objects.get(id=userId)
        except CustomUser.DoesNotExist:
            return Response({'message': 'کاربری با این شناسه یافت نشد.'}, status=status.HTTP_404_NOT_FOUND)

        self.reset_download_count(user)

        if downloadType == 'wallpaper' and user.wallpaperDownloads <= 0:
            return Response({'error': 'تعداد دانلود مجاز والپیپر به اتمام رسیده'}, status=status.HTTP_400_BAD_REQUEST)
        elif downloadType == 'soundtrack' and user.soundtrackDownloads <= 0:
            return Response({'error': 'تعداد دانلود مجاز ساندترک به اتمام رسیده '}, status=status.HTTP_400_BAD_REQUEST)

        user.downloadType = downloadType
        user.save()

        if downloadType == 'wallpaper':
            user.decrease_wallpaperDownloads()
        elif downloadType == 'soundtrack':
            user.decrease_soundtrackDownloads()
        else:
            return Response({'error': 'نوع فایل دانلودی نامعتبر است'}, status=status.HTTP_400_BAD_REQUEST)

        return Response({
            'message': 'دانلود با موفقیت انجام شد',
            'wallpaperDownloads': user.wallpaperDownloads,
            'soundtrackDownloads': user.soundtrackDownloads,
        })





       # time_since_last_reset = timezone.now() - user.resetDate
      #  if time_since_last_reset.days >= 30:
        #    user.reset_download_limits()



class CustomAvatarUploadView(APIView):
    def post(self, request, *args, **kwargs):
        try:
            userId = request.data.get('userId')
            customAvatar = request.FILES.get('customAvatar')

            user = CustomUser.objects.get(pk=userId)
        except CustomUser.DoesNotExist:
            return Response({'error': 'کاربر یافت نشد'}, status=status.HTTP_400_BAD_REQUEST)

        if not customAvatar or not customAvatar.name:
            return Response({'error': 'فایلی ارائه نشد'}, status=status.HTTP_400_BAD_REQUEST)

        valid_extensions = ['jpg', 'jpeg', 'png', 'webp']
        ext = customAvatar.name.split('.')[-1].lower()
        if ext not in valid_extensions:
            return Response({'error': 'فرمت تصویر آپلود شده صحیح نیست فرمت های مجاز jpg, jpeg, png, webp'},
                            status=status.HTTP_400_BAD_REQUEST)

        max_file_size_kb = 100
        max_file_size_bytes = max_file_size_kb * 1024
        if customAvatar.size > max_file_size_bytes:
            return Response({'error': 'حجم تصویر نمی تواند بیشتر از 100 کیلوبایت باشد'},
                            status=status.HTTP_400_BAD_REQUEST)

        user.customAvatar = customAvatar
        user.save()

        serializer = CustomUserSerializer(user)
        return Response({'message': 'تصویر با موفقیت بارگذاری شد', 'avatar_data': serializer.data})









class AvatarSelectionView(APIView):
    
    authentication_classes = [TokenAuthentication]
    def post(self, request, *args, **kwargs):
        userId = request.data.get('userId')
        selectedAvatar = request.data.get('selectedAvatar')

        try:
            user = CustomUser.objects.get(pk=userId)
        except CustomUser.DoesNotExist:
            return Response({'error': 'کاربر یافت نشد'}, status=status.HTTP_400_BAD_REQUEST)

          
        if user.customAvatar and selectedAvatar in [avatar[0] for avatar in user.AVATAR_CHOICES]:
            user.customAvatar = None

        user.selectedAvatar = selectedAvatar
        user.save()


     
        serializer = CustomUserSerializer(user)
        return Response({'message': 'آواتار با موفقیت بارگداری شد', 'avatar_data': serializer.data}, status=status.HTTP_200_OK)








class CommentReportView(APIView):
    
    authentication_classes = [TokenAuthentication] 
    
    def post(self, request):
        commentId = request.data.get('commentId')
        userId = request.data.get('userId')

        existing_reports = CommentReport.objects.filter(
            commentId=commentId,
        )
        
        if existing_reports.filter(userId=userId).exists():
            return Response({'error': "شما قبلا این کامنت را گزارش کرده اید"}, status=status.HTTP_400_BAD_REQUEST)

        serializer = CommentReportSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'success': "گزارش شما با موفقیت ارسال شد و مورد بررسی قرار خواهد گرفت"}, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    









class ReplyReportView(APIView):
    
    authentication_classes = [TokenAuthentication] 
    
    def post(self, request):
        reply = request.data.get('reply')
        userId = request.data.get('userId')

        existing_reports = ReplyReport.objects.filter(
            reply=reply,
        )
        
        if existing_reports.filter(userId=userId).exists():
            return Response({'error': "شما قبلا این کامنت را گزارش کرده اید"}, status=status.HTTP_400_BAD_REQUEST)

        serializer = ReplyReportSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'success': "گزارش شما با موفقیت ارسال شد و مورد بررسی قرار خواهد گرفت"}, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    








class ResetPasswordView(APIView):
    
    
    @method_decorator(cache_page(60*5))  
    def post(self, request):
        email = request.data.get('email')

        if email:
            cache_key = f"reset_password_{email}"
            if cache.get(cache_key):
                return Response({'error': "برای ارسال درخواست جدید جهت بازیابی رمزعبور لطفا 5 دقیقه منتظر بمانید"}, status=status.HTTP_429_TOO_MANY_REQUESTS)
            
            try:
                user = CustomUser.objects.get(email=email)
            except CustomUser.DoesNotExist:
                return Response({'error': "ایمیل وارد شده یافت نشد"}, status=status.HTTP_404_NOT_FOUND)
            
           
            token_generator = PasswordResetTokenGenerator()
            token = token_generator.make_token(user)

            html_message = render_to_string('resetpassword.html', {'user_id': user.id, 'token': token})
            subject = "درخواست بازیابی رمز عبور"
            from_email = settings.EMAIL_HOST_USER
            to_email = [email]

            send_mail(subject, '', from_email, to_email, html_message=html_message, fail_silently=False)
            cache.set(cache_key, True, timeout=60*5)

            return Response({'message': "ایمیل جهت بازیابی رمزعبور ارسال شد"}, status=status.HTTP_200_OK)
        else:
            return Response({'error': "لطفا ایمیل خود را وارد کنید"}, status=status.HTTP_400_BAD_REQUEST)
    
    
    def invalidate_token(self, user, token):
      
        if not hasattr(self, 'used_tokens'):
            self.used_tokens = {}

        if user.id in self.used_tokens:
            self.used_tokens[user.id].append(token)
        else:
            self.used_tokens[user.id] = [token]

    def token_already_used(self, user, token):
        
        if hasattr(self, 'used_tokens') and user.id in self.used_tokens:
            return token in self.used_tokens[user.id]
        return False

    


    def put(self, request):
        
        id = request.data.get('id')
        token = request.data.get('token')
        newPassword = request.data.get('newPassword')
        confirmPassword = request.data.get('confirmPassword')

        if id and token and newPassword == confirmPassword:
            try:
                user = CustomUser.objects.get(pk=id)
            except CustomUser.DoesNotExist:
                return Response({'error': "کاربری با این شناسه یافت نشد"}, status=status.HTTP_400_BAD_REQUEST)

            token_generator = PasswordResetTokenGenerator()
            
            if token_generator.check_token(user, token):
                cache_key = f"used_token_{token}_{user.id}"
                
                if cache.get(cache_key):
                    return Response({'error':"توکن قبلاً استفاده شده است"}, status=status.HTTP_400_BAD_REQUEST)

                user.set_password(newPassword)
                user.save()
                
                cache.set(cache_key, True, timeout=5184000)   

                return Response({'message': "کاربر عزیز رمزعبور شما با موفقیت بازیابی شد"}, status=status.HTTP_200_OK)
            else:
                return Response({'error': "توکن بازنشانی رمزعبور شما منقضی شده است لطفا دوباره تلاش کنید"}, status=status.HTTP_400_BAD_REQUEST)

        return Response({'error': "لطفا تمامی اطلاعات را به درستی وارد کنید"}, status=status.HTTP_400_BAD_REQUEST)








class SubscriberView(APIView):
    
    authentication_classes = [TokenAuthentication] 
    queryset = Subscriber.objects.all()
    serializer_class = SubscriberSerializer
    
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        
        
    def post(self, request):
     email = request.data.get('email')

     try:
         validate_email(email)
         subscriber = Subscriber.objects.get(email=email)
         return Response({'error': 'ایمیل شما قبلا در خبرنامه ثبت شده'}, status=status.HTTP_400_BAD_REQUEST)
     except ValidationError:
        return Response({'error': 'ایمیل وارد شده معتبر نیست'}, status=status.HTTP_400_BAD_REQUEST)
     except Subscriber.DoesNotExist:
        subscriber = Subscriber(email=email)
        subscriber.save()
        return Response({'message': 'عضویت شما در خبرنامه با موفقیت ثبت شد'}, status=status.HTTP_201_CREATED)
     except Exception as e:
        return Response({'error': 'عملیات ثبت عضویت خبرنامه ناموفق بود', 'details': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
        
        
        
     
        
class UnsubscriberView(APIView):
   
    authentication_classes = [TokenAuthentication] 
    queryset = Subscriber.objects.all()
    serializer_class = SubscriberSerializer

    def post(self, request):
        email = request.data.get('email')

        try:
            validate_email(email)
            subscriber = Subscriber.objects.get(email=email)
            subscriber.delete()
            return Response({'message': 'عضویت شما درخبرنامه با موفقیت لغو شد'}, status=status.HTTP_200_OK)
        except Subscriber.DoesNotExist:
            return Response({'error': 'کاربری با این ایمیل درخبرنامه یافت نشد'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': 'عملیات لغو عضویت درخبرنامه ناموفق بود'}, status=status.HTTP_400_BAD_REQUEST)






class SendNewsLetterViewSet(viewsets.ViewSet):
    
    authentication_classes = [TokenAuthentication] 

    @action(detail=False, methods=['get'])
    def send_newsletter(self, request):
        
        latest_posts = AllPosts.objects.filter(isReportage=False).order_by('-date')[:3]
        
        

        subject = 'تازه ترین مطالب سایت بازیکاچو'
        from_email = settings.EMAIL_HOST_USER
        recipient_list = []
        post_url = '' 

        subscribers = Subscriber.objects.values_list('email', flat=True)
        recipient_list.extend(subscribers)
        
        for post in latest_posts:
            
            if post.isEvent and post.eventStage:
                post_url = f"http://bazikacho.ir/{post.eventStage}/{post.slug}/"
            elif post.isArticle:
                post_url = f"http://bazikacho/articles/{post.slug}/"
            elif post.isVideo and post.videoType:
                post_url = f"http://bazikacho/{post.videoType}/{post.slug}/"
            elif post.isNews:
                post_url = f"http://bazikacho/news/{post.slug}/"
            elif post.isStory:
                post_url = f"http://bazikacho/stories/{post.slug}/"
                
        
            post.post_url = post_url
            
        html_message = render_to_string('newsletter.html', {'latest_posts': latest_posts})

        for subscriber_email in recipient_list:
            send_mail(subject, '', from_email, [subscriber_email], html_message=html_message)

        return HttpResponse(html_message, content_type='text/html')
    






class SignUpView(APIView):
    
    authentication_classes = [TokenAuthentication] 
    
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        confirmPassword = request.data.get('confirmPassword')
        email = request.data.get('email')
        if not username or not password:
            return Response({'error': 'لطفا تمامی فیلد هارا پرکنید'}, status=status.HTTP_400_BAD_REQUEST)
        
        
        if ' ' in username:
            return Response({'error': 'نام کاربری نمی‌تواند شامل فاصله باشد'}, status=status.HTTP_400_BAD_REQUEST)

        
        if not re.match("^[a-zA-Z0-9_]*$", username):
            return Response({'error': 'نام کاربری فقط می‌تواند شامل حروف انگلیسی، اعداد و آندرلاین (_) باشد'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            
            validate_email(email)
        except ValidationError:
            return Response({'error': 'ایمیل وارد شده معتبر نیست'}, status=status.HTTP_400_BAD_REQUEST)

        if CustomUser.objects.filter(username=username).exists():
            return Response({'error': 'نام کاربری وجود دارد'}, status=status.HTTP_400_BAD_REQUEST)

        if CustomUser.objects.filter(email=email).exists():
            return Response({'error': "ایمیل وارد شده قبلا ثبت شده است"}, status=status.HTTP_400_BAD_REQUEST)

        if len(password) < 8:
            return Response({'error': 'رمز عبور نمی‌تواند کمتر از 8 کاراکتر باشد'}, status=status.HTTP_400_BAD_REQUEST)

        if password != confirmPassword:
            return Response({'error': 'رمز عبور و تایید آن باید یکسان باشند'}, status=status.HTTP_400_BAD_REQUEST)


        user = CustomUser.objects.create(
            username=username, password=make_password(password), email=email)

       
        response_data = {
            'username': user.username,
            'password': user.password,
            'email': user.email,
            'message': 'ثبت نام با موفقیت انجام شد'
        }
        return Response(response_data, status=status.HTTP_201_CREATED)







class LoginView(APIView):
    
    authentication_classes = [TokenAuthentication] 
    
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        if not email or not password:
            return Response({'error': "لطفا هردو فیلد ایمیل و رمزعبور را وارد کنید"}, status=status.HTTP_400_BAD_REQUEST)

        CustomUser = get_user_model()
        user = CustomUser.objects.filter(email=email).first()

        if user:
            user_auth = authenticate(username=user.username, password=password)

            if user_auth:
                selectedAvatar_url = user.selectedAvatar.url if user.selectedAvatar else None
                customAvatar_url = user.customAvatar.url if user.customAvatar else None

            return Response({
                    'message': 'ورود کاربر با موفقیت انجام شد',
                    'user': {
                        'id': user.id,
                        'username': user.username,
                        'email': user.email,
                        'selectedAvatar_url': selectedAvatar_url,
                        'customAvatar_url': customAvatar_url,
                        'wallpaperDownloads': user.wallpaperDownloads,
                        'soundtrackDownloads': user.soundtrackDownloads 
                        
                    }
                }, status=status.HTTP_200_OK)

        return Response({'error': 'ایمیل یا رمزعبور اشتباه است'}, status=status.HTTP_401_UNAUTHORIZED)







class ChangeUsernameView(APIView):
    
    authentication_classes = [TokenAuthentication] 
    
    def put(self, request):
        email = request.data.get('email')
        newUsername = request.data.get('newUsername')

        if not email or not newUsername:
            return Response({'error': 'لطفا هردو فیلد ایمیل و نام کاربری را وارد کنید'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = CustomUser.objects.get(email=email)
        except CustomUser.DoesNotExist:
            return Response({'error': "کاربر با این ایمیل یافت نشد"}, status=status.HTTP_404_NOT_FOUND)

        user.username = newUsername
        user.save()

        return Response({'message': 'نام کاربری به‌روزرسانی شد'}, status=status.HTTP_200_OK)








class ChangePasswordView(APIView):

    authentication_classes = [TokenAuthentication] 

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

            user = CustomUser.objects.get(email=email)
            if user.check_password(oldPassword):
                user.set_password(newPassword)
                user.save()
                return Response({'message': "رمز عبور شما با موفقیت تغییر کرد"}, status=status.HTTP_200_OK)
            else:
                return Response({'error': "رمز عبور فعلی نادرست است"}, status=status.HTTP_400_BAD_REQUEST)
        except CustomUser.DoesNotExist:
            return Response({'error':  " نام کاربری وارد شده یافت نشد"}, status=status.HTTP_404_NOT_FOUND)







class ContactUsView(APIView):
    
    authentication_classes = [TokenAuthentication]
    serializer_class = ContactUsSerializer
    queryset = ContactUs.objects.all()
   
   
    
    def get(self, request):
        contact = ContactUs.objects.all()
        serializer = ContactUsSerializer(contact, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


    def post(self, request):
        fullName = request.data.get('fullName')
        emailContact = request.data.get('emailContact')
        message = request.data.get('message')

        if not fullName or not emailContact or not message:
            return JsonResponse({'error': 'لطفاً تمام فیلدها را پر کنید'}, status=400)
        
        
           
      
        

        created_contact = ContactUs.objects.create(
            fullName=fullName, emailContact=emailContact, message=message)

        if created_contact:
           
            html_message = render_to_string('contactus.html', {'user_message': message})
            
           
            plain_message = strip_tags(html_message)

            
            html_message = html_message.replace('پیام کاربر', message)

            
            email = EmailMultiAlternatives(
                
                subject="ارتباط با تیم بازیکاچو",
                body=plain_message,
                from_email=settings.EMAIL_HOST_USER,
                to=[emailContact],
            )
            email.attach_alternative(html_message, "text/html")
            email.send(fail_silently=False)

            return Response({'message': 'اطلاعات با موفقیت ذخیره شد و ایمیل ارسال شد.'}, status=201)
        else:
            return Response({'error': 'خطایی در ذخیره‌سازی اطلاعات رخ داده است.'}, status=500)






class BaziKachoTeamByUsernameView(APIView):
    
    authentication_classes = [TokenAuthentication] 
    
    def get(self, request, username):
        team_member = get_object_or_404(bazikachoTeam, username=username)
        serializer = bazikachoTeamSerializer(team_member)
        return Response(serializer.data)






class BaziKachoTeamView(APIView):
    
    authentication_classes = [TokenAuthentication] 

    queryset = bazikachoTeam.objects.all()
    serializer_class = bazikachoTeamSerializer
    
    
    
    def get(self, request):
        bazi_kacho_team = bazikachoTeam.objects.all()
        serializer = bazikachoTeamSerializer(bazi_kacho_team, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)





class PostCommentsView(APIView):
    
    authentication_classes = [TokenAuthentication] 
    def get(self, request, post_id):
        post = get_object_or_404(AllPosts, pk=post_id)
        post_comments = Comments.objects.filter(post=post)
        serializer = CommentsSerializer(post_comments, many=True)
        return Response(serializer.data)









class LikeCommentAPIView(APIView):
    
    authentication_classes = [TokenAuthentication] 

    queryset = CommentLike.objects.all()
    serializer_class = CommentLikeSerializer
    permission_classes = [AllowAny]

    def get(self, request):
        likes = CommentLike.objects.all()
        serializer = CommentLikeSerializer(likes, many=True)
        return Response(serializer.data)

    def post(self, request):
        commentId = request.data.get('commentId')
        userId = request.data.get('userId')

        try:
            comment = Comments.objects.get(id=commentId)
            user = CustomUser.objects.get(id=userId)

           
            has_liked_before = CommentLikeHistory.objects.filter(
                user=user, comment=comment).exists()

            if has_liked_before:
               
                CommentLikeHistory.objects.filter(
                    user=user, comment=comment).delete()
                comment.likeCount -= 1
                comment.save()
                return Response({'message': 'لایک کامنت حذف شد'}, status=status.HTTP_200_OK)
            else:
             
                CommentLikeHistory.objects.create(user=user, comment=comment)
                comment.likeCount +=1
                comment.save()
                return Response({'message': 'کامنت با موفقیت لایک شد'}, status=status.HTTP_201_CREATED)

        except Comments.DoesNotExist:
            return Response({'error': 'کامنت موردنظر پیدا نشد'}, status=status.HTTP_404_NOT_FOUND)
        except CustomUser.DoesNotExist:
            return Response({'error': 'کاربر موردنظر پیدا نشد'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)





class CommentLikesAPIView(APIView):
    
    authentication_classes = [TokenAuthentication] 
    
    def get(self, request, comment_id):
       
        comment_likes = CommentLikeHistory.objects.filter(
            comment_id=comment_id)

   
        likes_info = []
        for like in comment_likes:
  
            like_info = {
                'like_id': like.id,
                'user_id': like.user_id,
                'comment_id': like.comment_id,
           
                'liked_at': like.liked_at.strftime('%Y-%m-%d %H:%M:%S')
            }
            likes_info.append(like_info)
        return JsonResponse({'comment_likes': likes_info})





class CommentDetailAPIView(APIView):
    serializer_class = CommentsSerializer
    authentication_classes = [TokenAuthentication] 

    def get(self, request, pk):
        try:
            comment = Comments.objects.get(pk=pk)
            serializer = CommentsSerializer(comment)
            return Response(serializer.data)
        except Comments.DoesNotExist:
            return Response({'error': 'کامنت یافت نشد'}, status=status.HTTP_404_NOT_FOUND)





class UserDetailsAPIView(APIView):
    authentication_classes = [TokenAuthentication] 

    def get(self, request, user_id):
        try:
            user = CustomUser.objects.get(id=user_id)
            selectedAvatar_url = user.selectedAvatar.url if user.selectedAvatar else None
            customAvatar_url = user.customAvatar.url if user.customAvatar else None

            user_data = {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'selectedAvatar_url': selectedAvatar_url,
                'customAvatar_url':customAvatar_url,
                'wallpaperDownloads': user. wallpaperDownloads,
                'soundtrackDownloads': user.soundtrackDownloads

            }
            
            return Response(user_data)
        except CustomUser.DoesNotExist:
            return Response({'error': 'کاربر مورد نظر یافت نشد'}, status=status.HTTP_404_NOT_FOUND)




class PostReplyView(APIView):
    
    authentication_classes = [TokenAuthentication] 
    def get(self, request, post_id):
        post = get_object_or_404(AllPosts, pk=post_id)
        post_replies = Reply.objects.filter(post=post)
        serializer = ReplySerializer(post_replies, many=True)
        return Response(serializer.data)




class CommentRepliesAPIView(APIView):
    serializer_class = ReplySerializer
    authentication_classes = [TokenAuthentication] 

    def get(self, request, comment_id):
        
        main_replies = Reply.objects.filter(
            commentId=comment_id, parentReplyId=None)
        serializer = ReplySerializer(main_replies, many=True)
        return Response(serializer.data)




class RetrieveChildRepliesAPIView(APIView):
    queryset = Reply.objects.all()
    serializer_class = ReplySerializer
    authentication_classes = [TokenAuthentication] 

    def get(self, request, reply_id):
        try:
           
            child_replies = Reply.objects.filter(parentReplyId=reply_id)
            serializer = ReplySerializer(child_replies, many=True)
            return Response(serializer.data)
        except Reply.DoesNotExist:
            return JsonResponse({'error': 'ریپلای مورد نظر یافت نشد'}, status=status.HTTP_404_NOT_FOUND)








class BaseAPIView(APIView):
    
    def get_last_activity_time(self, user_id, comment_model):
        last_activity = comment_model.objects.filter(userId=user_id).order_by('-createdAt').first()
        if last_activity:
            time_since_last_activity = timezone.now() - last_activity.createdAt
            return time_since_last_activity
        return None





class commentAPIView(BaseAPIView):
    
   
   # authentication_classes = [TokenAuthentication] 

    queryset = Comments.objects.all()
    serializer_class = CommentsSerializer
    permission_classes = [AllowAny]

    forbidden_words = ["جمهوری اسلامی", "ولایت فقیه", "خمینی", "خامنه ای", "کیر", "کص", "کون", "حرومزاده", "کیری", "کسشر", "فاک", "گاییدم", "مادرتو", "اسکل", "کصخل",
                       "fuck", "dick", "pussy", "wtf", "خفه شو", "مادر جنده", "کسخل", "کونی", "سکس", "sex", "porn", "پورن", "جنده", "گی", "ترنس","کردمت"
                       "kos", "kon", "koni", "kiri", "kir", "sexy", "فیلم سوپر", "xxx", "لواط", "همجنس بازی", "لز", "لزبین", "عوضی", "خفه شو","خارشوگاییدم"
                       "کس نگو", "siktir"]

    def get(self, request):
        all_comments = Comments.objects.all()
        serializer = CommentsSerializer(all_comments, many=True)
        return Response(serializer.data)

    def post(self, request):
        commentText = request.data.get('commentText')
        userId = request.data.get('userId')
        post = request.data.get('post')

        if commentText and userId and post:

            for word in self.forbidden_words:
                if word in commentText:
                    return JsonResponse({'error': 'کامنت حاوی الفاظ نامناسب است'}, status=status.HTTP_400_BAD_REQUEST)

            if re.search(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', commentText):
                return JsonResponse({'error': 'قرار دادن لینک در کامنت مجاز نیست'}, status=status.HTTP_400_BAD_REQUEST)
            
              
            last_comment_time = self.get_last_activity_time(userId, Comments)
            last_reply_time = self.get_last_activity_time(userId, Reply)

            if last_comment_time and last_comment_time.total_seconds() < 60 or last_reply_time and last_reply_time.total_seconds() < 60 :
                return JsonResponse({'error': 'جهت ارسال کامنت جدید لطفا 1 دقیقه منتظر بمانید'}, status=status.HTTP_400_BAD_REQUEST)



            post = AllPosts.objects.get(id=post)
            user = CustomUser.objects.get(id=userId)
            new_comment = Comments.objects.create(
                commentText=commentText,
                userId=user,
                post=post,
            )

            new_comment.save()
            return JsonResponse({'message': 'کامنت با موفقیت ثبت شد'}, status=status.HTTP_201_CREATED)
        else:
            return JsonResponse({'error': 'مشکلی در ثبت کامنت رخ داد'}, status=status.HTTP_400_BAD_REQUEST)






class ReplyAPIView(BaseAPIView):

    queryset = Reply.objects.all()
    serializer_class = ReplySerializer
   # authentication_classes = [TokenAuthentication] 

    forbidden_words = ["جمهوری اسلامی", "ولایت فقیه", "خمینی", "خامنه ای", "کیر", "کص", "کون", "حرومزاده", "کیری", "کسشر", "فاک", "گاییدم", "مادرتو", "اسکل", "کصخل",
                       "fuck", "dick", "pussy", "wtf", "خفه شو", "مادر جنده", "کسخل", "کونی", "سکس", "sex", "porn", "پورن", "جنده", "گی", "ترنس",
                       "kos", "kon", "koni", "kiri", "kir", "sexy", "فیلم سوپر", "xxx", "لواط", "همجنس بازی", "لز", "لزبین", "عوضی", "خفه شو",
                       "کس نگو", "siktir"]

    def get(self, request):

        all_replies = Reply.objects.all()
        serializer = ReplySerializer(all_replies, many=True)
        return Response(serializer.data)

    def post(self, request):
        replyText = request.data.get('replyText')
        parentReplyId = request.data.get('parentReplyId')
        commentId = request.data.get('commentId')
        userId = request.data.get('userId')
        post = request.data.get('post')

        if replyText and commentId and userId and post:

            if parentReplyId is not None and str(parentReplyId).isdigit():
                try:
                    parentReply = Reply.objects.get(id=parentReplyId)
                    parentReplyId = parentReply 
                except Reply.DoesNotExist:
                    return JsonResponse({'error': 'ریپلای والد نادرست'}, status=status.HTTP_400_BAD_REQUEST)
            else:
                parentReplyId = None

            for word in self.forbidden_words:
                if word in replyText:
                    return JsonResponse({'error': "پاسخ حاوی الفاظ نامناسب است"}, status=status.HTTP_400_BAD_REQUEST)

            if re.search(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', replyText):
                return JsonResponse({'error': 'قرار دادن لینک در پاسخ مجاز نیست'}, status=status.HTTP_400_BAD_REQUEST)
            
            
            last_reply_time = self.get_last_activity_time(userId, Reply)
            last_comment_time = self.get_last_activity_time(userId, Comments)

            if last_reply_time and last_reply_time.total_seconds() < 60 or last_comment_time and last_comment_time.total_seconds() < 60:
                return JsonResponse({'error': 'جهت ارسال کامنت جدید لطفا 1 دقیقه منتظر بمانید'}, status=status.HTTP_400_BAD_REQUEST)

            post = AllPosts.objects.get(id=post)
            user = CustomUser.objects.get(id=userId)
            new_reply = Reply.objects.create(
                replyText=replyText,
                userId=user,
                post=post,
                parentReplyId=parentReplyId
    
            )

            comment = Comments.objects.get(id=commentId)
            new_reply.commentId.set([comment])

            new_reply.save()
            return JsonResponse({'message': "پاسخ با موفقیت ثبت شد"}, status=status.HTTP_201_CREATED)
        else:
            return JsonResponse({'error': 'مشکلی در ثبت پاسخ رخ داد'}, status=status.HTTP_400_BAD_REQUEST)





class ReplyLikeAPIView(APIView):

    queryset = ReplyLike.objects.all()
    serializer_class = ReplyLikeSerializer
    authentication_classes = [TokenAuthentication] 

    def get(self, request):
        likes = ReplyLike.objects.all()
        serializer = ReplyLikeSerializer(likes, many=True)
        return Response(serializer.data)

    def post(self, request):
        replyId = request.data.get('replyId')
        userId = request.data.get('userId')

        try:
            reply = Reply.objects.get(id=replyId)
            user = CustomUser.objects.get(id=userId)

           
            has_liked_before = ReplyLikeHistory.objects.filter(
                user=user, reply=reply).exists()

            if has_liked_before:
              
                ReplyLikeHistory.objects.filter(
                    user=user, reply=reply).delete()
                reply.likeCount -= 1
                reply.save()
                return Response({'message': 'لایک کامنت حذف شد'}, status=status.HTTP_200_OK)
            else:
               
                ReplyLikeHistory.objects.create(user=user, reply=reply)
                reply.likeCount += 1
                reply.save()
                return Response({'message': 'کامنت با موفقیت لایک شد'}, status=status.HTTP_201_CREATED)

        except reply.DoesNotExist:
            return Response({'error': 'کامنت موردنظر پیدا نشد'}, status=status.HTTP_404_NOT_FOUND)
        except CustomUser.DoesNotExist:
            return Response({'error': 'کاربر موردنظر پیدا نشد'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)





class ReplyLikesDetailAPIView(APIView):
    authentication_classes = [TokenAuthentication] 
    def get(self, request, reply_id):
       
        reply_likes = ReplyLikeHistory.objects.filter(
            reply_id=reply_id)

      
        likes_info = []
        for like in reply_likes:
           
            like_info = {
                'like_id': like.id,
                'user_id': like.user_id,
                'reply_id': like.reply_id,
                'liked_at': like.liked_at.strftime('%Y-%m-%d %H:%M:%S')
            }
            likes_info.append(like_info)
        return JsonResponse({'reply_likes': likes_info})






class PollsView(APIView):
    queryset = Polls.objects.all()
    serializer_class = pollsSerializer
    authentication_classes = [TokenAuthentication] 
    
    def get(self, request):
        polls = Polls.objects.all()
        serializer = pollsSerializer(polls, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)






class ChoiceView(APIView):
    queryset = Choice.objects.all()
    serializer_class = ChoiceSerializer
    authentication_classes = [TokenAuthentication] 
    
    def get(self, request):
        choices = Choice.objects.all()
        serializer = ChoiceSerializer(choices, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    
    
    
    
    
    
class ChoiceDetailView(APIView):
    def get(self, request, choice_id):
        choice = get_object_or_404(Choice, pk=choice_id)
        serializer = ChoiceSerializer(choice)
        return Response(serializer.data)
    
    
    
    
    
    


class VoteView(APIView):
    queryset = Vote.objects.all()
    serializer_class = VoteSerializer
    authentication_classes = [TokenAuthentication] 


@api_view(['POST'])
def voteChoice(request):
    user = request.data.get('user')
    poll = request.data.get('poll')
    choice = request.data.get('choice')

    try:
        user = CustomUser.objects.get(pk=user)
        poll = Polls.objects.get(pk=poll)
        choice = Choice.objects.get(pk=choice)
    except (CustomUser.DoesNotExist, Polls.DoesNotExist, Choice.DoesNotExist) as e:
        raise ValidationError({'error': "یکی از مقادیر نادرست وارد شده"})

    user_voted = Vote.objects.filter(
        user=user, poll=poll).exists()
    if user_voted:
        return Response({'error': "شما دراین نظرسنجی شرکت کرده اید"}, status=status.HTTP_400_BAD_REQUEST)

    Vote.objects.create(user=user, poll=poll, choice=choice)

    
    choice.numVotes = Vote.objects.filter(choice=choice).count()
    choice.save()

    return Response({'message': 'انتخاب شما با موفقیت ثبت شد'}, status=status.HTTP_200_OK)







class AllPostsDetailView(generics.RetrieveAPIView):
    authentication_classes = [TokenAuthentication] 
    queryset = AllPosts.objects.all()
    serializer_class = AllPostsSerializer
    lookup_field = 'slug'







class AllPostsView(APIView):
    
    authentication_classes = [TokenAuthentication] 
    queryset = AllPosts.objects.all()
    serializer_class = AllPostsSerializer
    
    
    def get(self, request):
        all_posts = AllPosts.objects.all()
        serializer = AllPostsSerializer(all_posts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
   



class WallpapersView(APIView):

    queryset = wallpapers.objects.all()
    serializer_class = wallpapersSerializer
    authentication_classes = [TokenAuthentication] 
    
    
    def get(self, request):
        wallpapers_list = wallpapers.objects.all()
        serializer = wallpapersSerializer(wallpapers_list, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)





class AlbumsDetailView(generics.RetrieveAPIView):
    authentication_classes = [TokenAuthentication] 
    queryset = albums.objects.all()
    serializer_class = albumsSerializer
    lookup_field = 'slug'








class AlbumsView(APIView):

    queryset = albums.objects.all()
    serializer_class = albumsSerializer
    authentication_classes = [TokenAuthentication] 
    
    def get(self, request):
        albums_list = albums.objects.all()
        serializer = albumsSerializer(albums_list, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)







class TracksView(APIView):

    queryset = tracks.objects.all()
    serializer_class = tracksSerializer
    authentication_classes = [TokenAuthentication] 
    
    def get(self, request):
        tracks_list = tracks.objects.all()
        serializer = tracksSerializer(tracks_list, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)








class TracksDetailView(APIView):
    def get(self, request, track_id):
        track = get_object_or_404(tracks, pk=track_id)
        serializer = tracksSerializer(track)
        return Response(serializer.data)

    







class AdvertisementsView(APIView):

    queryset = Advertisements.objects.all()
    serializer_class = AdvertisementsSerializer
    authentication_classes = [TokenAuthentication] 
    
    
    def get(self, request):
        advertisements_list = Advertisements.objects.all()
        serializer = AdvertisementsSerializer(advertisements_list, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
