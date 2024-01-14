
from django.conf import settings
from django.urls import path, include
from myapp import views
from django.conf.urls.static import static
from django.urls import include, path
from django.contrib import admin
from django.urls import path
from . import views
from .views import SignUpView, LoginView
from .views import ContactUsView
from .views import *
from django.urls import include, path



urlpatterns = [
    
 
    
    path('api/allPosts/', AllPostsView.as_view(), name='all_posts'),
    
    path('api/wallpapers/', WallpapersView.as_view(), name='wallpapers'),
    
    path('api/polls/', PollsView.as_view(), name='polls'),
    
    path('api/albums/', AlbumsView.as_view(), name='albums'),
    
    path('api/selectavatar/', AvatarSelectionView.as_view(), name='select_avatar'),
    
    path('api/uploadcustomavatar/', CustomAvatarUploadView.as_view(), name='upload_custom_avatar'),
    
    path('api/downloadlimit/', DownloadLimitView.as_view(), name='download-limit-view'),
    
    path('api/tracks/', TracksView.as_view(), name='tracks'),
    
    path('api/tracks/<int:track_id>/', TracksDetailView.as_view(), name='track-detail'),
    
    path('api/Advertisements/', AdvertisementsView.as_view(), name='advertisements'),
    
    path('api/send-newsletter/', SendNewsLetterViewSet.as_view({'get': 'send_newsletter'}), name='send_newsletter'),
    
    path('admin/', admin.site.urls),
    
    path('api/signup/', SignUpView.as_view(), name='signup'),
    
    path('api/login/', LoginView.as_view(), name='login'),
    
    path('api/change-username/', ChangeUsernameView.as_view(), name='change-username'),
    
    path('api/change-password/', ChangePasswordView.as_view(), name='change-password'),
    
    path('api/contactUs/', ContactUsView.as_view(), name='contact_us'),
    
    path('api/commentreport/', CommentReportView.as_view(), name='comment-reports'),
    
    path('api/replyreport/', ReplyReportView.as_view(), name='reply-reports'),
    
    path('api/user/<int:user_id>/', UserDetailsAPIView.as_view(), name='user-details'),
    
    path('ckeditor/', include('ckeditor_uploader.urls')),
    
    path('api/vote/', views.voteChoice, name='voteChoice'),
    
    path('api/choice/', ChoiceView.as_view(), name='choices'),
    
    path('api/choice/<int:choice_id>/', ChoiceDetailView.as_view(), name='choice-detail'),
    
    path('api/comment/', commentAPIView.as_view(), name='comment'),
    
    path('api/comment/<int:pk>/',CommentDetailAPIView.as_view(), name='comment-detail'),
    
    path('api/reply/', ReplyAPIView.as_view(), name='reply'),

    path('api/replyLike/', ReplyLikeAPIView.as_view(), name='replyLike'),

    path('api/parentreply/<int:comment_id>/replies/', CommentRepliesAPIView.as_view(), name='comment-replies'),

    path('api/childreplies/<int:reply_id>/child/',RetrieveChildRepliesAPIView.as_view(), name='retrieve-child-replies'),

    path('api/posts/<int:post_id>/replies/',PostReplyView.as_view(), name='post-replies'),

    path('api/replyLikedetail/<int:reply_id>/likes/',ReplyLikesDetailAPIView.as_view(), name='reply_likes_api'),

    path('api/posts/<int:post_id>/comments/',PostCommentsView.as_view(), name='post-comments'),

    path('api/allPosts/<slug:slug>/',AllPostsDetailView.as_view(), name='allposts-detail'),

    path('api/albums/<slug:slug>/',AlbumsDetailView.as_view(), name='albums-detail'),

    path('api/LikeComment/', LikeCommentAPIView.as_view(), name='like-comment'),
    
    path('api/BaziKachoTeam/', BaziKachoTeamView.as_view(), name='bazikacho_team'),
    
    path('api/BaziKachoTeam/<username>/',BaziKachoTeamByUsernameView.as_view(), name='team-member-by-username'),
    
    path('api/commentLike/<int:comment_id>/likes/',CommentLikesAPIView.as_view(), name='comment_likes_api'),
    
    path('bazikacho-newsletter', AllPostsDetailView.as_view(), name='bazikachto-newsletter'),
    
    path('api/subscribenewsletter/', SubscriberView.as_view(), name='subscribe'),
    
    path('api/unsubscribenewsletter/', UnsubscriberView.as_view(), name='unsubscribe'),
    
    path('api/resetpassword/', ResetPasswordView.as_view(), name='reset_password'), 
    
    path('api/resetpasswordconfirm/', ResetPasswordView.as_view(), name='reset_password_confirm'),
    
  
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)





if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
