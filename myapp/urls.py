
"""
URL configuration for bazi100project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
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


# urlpatterns = [
#   path('admin/', admin.site.urls),
# ]
"""
URL configuration for myapp project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""


router = routers.DefaultRouter()
router.register(r'Polls', views.pollsViewSet)
router.register(r'choice', views.choiceViewSet)
router.register(r'bazi100Team', views.bazi100TeamViewSet)
router.register(r'allPosts', views.allPostsViewSet)
router.register(r'wallpapers', views.wallpapersViewSet)
router.register(r'albums', views.albumsViewSet)
router.register(r'advertisements', views.advertisementsViewSet)
router.register(r'tracks', views.tracksViewSet)


urlpatterns = [


    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api/signup/', SignUpView.as_view(), name='signup'),
    path('api/login/', LoginView.as_view(), name='login'),
    path('api/change-username/', ChangeUsernameView.as_view(),
         name='change-username'),
    path('api/change-password/', ChangePasswordView.as_view(),
         name='change-password'),
    path('api/contactUs/', ContactUsAPIView.as_view(), name='contact_us'),
    path('api/user/<int:user_id>/',
         UserDetailsAPIView.as_view(), name='user-details'),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('api/vote/', views.voteChoice, name='voteChoice'),
    path('api/comment/', commentAPIView.as_view(), name='comment'),
    path('api/comment/<int:pk>/',
         CommentDetailAPIView.as_view(), name='comment-detail'),
    path('api/reply/', replyAPIView.as_view(), name='reply'),
    path('api/LikeComment/', LikeCommentAPIView.as_view(), name='LikeComment'),
    path('api/replyLike/', replyAPIView.as_view(), name='replyLike'),
    path('api/posts/<int:post_id>/comments/',
         PostCommentsView.as_view(), name='post-comments'),
    path('api/allPosts/<slug:slug>/',
         allPostsDetailView.as_view(), name='allposts-detail'),
    path('api/albums/<slug:slug>/',
         AlbumsDetailView.as_view(), name='albums-detail'),


]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
