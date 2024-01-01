
from django.conf import settings
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from myapp import views
from rest_framework import routers
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from . import views
from .views import SignUpView, LoginView
from .views import ContactUsAPIView
from .views import *



#router = routers.DefaultRouter()
#router.register(r'Polls', views.pollsViewSet)
#router.register(r'choice', views.choiceViewSet)
#router.register(r'BaziKachoTeam', views.BaziKachoTeamViewSet)
#router.register(r'allPosts', views.allPostsViewSet)
#router.register(r'wallpapers', views.wallpapersViewSet)
#router.register(r'albums', views.albumsViewSet)
#router.register(r'advertisements', views.advertisementsViewSet)
#router.register(r'tracks', views.tracksViewSet)
#router.register(r'subscribers', SubscriberView, basename='subscribers')



urlpatterns = [
    
    path('api/allPosts/', AllPostsView.as_view(), name='all_posts'),
    
    path('api/wallpapers/', WallpapersView.as_view(), name='wallpapers'),
    
    path('api/polls/', PollsView.as_view(), name='polls'),
    
    path('api/albums/', AlbumsView.as_view(), name='albums'),
    
    path('api/tracks/', TracksView.as_view(), name='tracks'),
    
    path('api/advertisements/', AdvertisementsView.as_view(), name='advertisements'),
    
    path('api/send-newsletter/', SendNewsLetterViewSet.as_view({'get': 'send_newsletter'}), name='send_newsletter'),
    
    path('admin/', admin.site.urls),
    
    path('api/signup/', SignUpView.as_view(), name='signup'),
    
    path('api/login/', LoginView.as_view(), name='login'),
    
    path('api/change-username/', ChangeUsernameView.as_view(), name='change-username'),
    
    path('api/change-password/', ChangePasswordView.as_view(), name='change-password'),
    
    path('api/contactUs/', ContactUsAPIView.as_view(), name='contact_us'),
    
    path('api/user/<int:user_id>/', UserDetailsAPIView.as_view(), name='user-details'),
    
    path('ckeditor/', include('ckeditor_uploader.urls')),
    
    path('api/vote/', views.voteChoice, name='voteChoice'),
    
    path('api/choice/', ChoiceView.as_view(), name='choices'),
    
    path('api/comment/', commentAPIView.as_view(), name='comment'),
    
    path('api/comment/<int:pk>/',CommentDetailAPIView.as_view(), name='comment-detail'),
    
    path('api/reply/', ReplyAPIView.as_view(), name='reply'),

    path('api/replyLike/', ReplyLikeAPIView.as_view(), name='replyLike'),

    path('api/parentreply/<int:comment_id>/replies/', CommentRepliesAPIView.as_view(), name='comment-replies'),

    path('api/childreplies/<int:reply_id>/child/',RetrieveChildRepliesAPIView.as_view(), name='retrieve-child-replies'),

    path('api/posts/<int:post_id>/replies/',PostReplyView.as_view(), name='post-replies'),

    path('api/replyLikedetail/<int:reply_id>/likes/',ReplyLikesDetailAPIView.as_view(), name='reply_likes_api'),

    path('api/posts/<int:post_id>/comments/',PostCommentsView.as_view(), name='post-comments'),

    path('api/AllPosts/<slug:slug>/',AllPostsDetailView.as_view(), name='allposts-detail'),

    path('api/Albums/<slug:slug>/',AlbumsDetailView.as_view(), name='albums-detail'),

    path('api/LikeComment/', LikeCommentAPIView.as_view(), name='like-comment'),
    
    path('api/BaziKachoTeam/', BaziKachoTeamView.as_view(), name='bazikacho_team'),
    
    path('api/BaziKachoTeam/<username>/',BaziKachoTeamByUsernameView.as_view(), name='team-member-by-username'),
    
    path('api/commentLike/<int:comment_id>/likes/',CommentLikesAPIView.as_view(), name='comment_likes_api'),
    
    path('bazikacho-newsletter', AllPostsDetailView.as_view(), name='bazikachto-newsletter'),
    
    path('api/subscribenewsletter/', SubscriberView.as_view(), name='subscribe'),
    
    path('api/unsubscribenewsletter/', UnsubscriberView.as_view(), name='unsubscribe'),
    
    path('api/resetpassword/', ResetPasswordView.as_view(), name='reset_password'), #اندپوینت پست اول
    
    path('api/resetpasswordconfirm/', ResetPasswordView.as_view(), name='reset_password_confirm'),
    
  
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)





if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
