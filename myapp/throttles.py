from rest_framework.throttling import UserRateThrottle
from django.utils import timezone
from rest_framework.response import Response



class CommentThrottle(UserRateThrottle):
    rate = '1/2m'  # هر 2 دقیقه بتونه کامنت بزاره

    def allow_request(self, request, view):
        if request.user.is_authenticated:
            last_comment_time = request.user.last_comment_time if hasattr(request.user, 'last_comment_time') else None
            if last_comment_time and (timezone.now() - last_comment_time).seconds < 120:
                return False
        return super().allow_request(request, view)

    def wait(self):
        return Response({'error':'لطفا پس از 2 دقیقه کامنت خود را ارسال کنید'}) 
    