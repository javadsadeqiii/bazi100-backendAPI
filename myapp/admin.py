from django.contrib import admin
from django.contrib import admin
from .models import *
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin






class PasswordResetLinkAdmin(admin.ModelAdmin):
    
    
    list_display = ('__all__')
    
admin.site.register(PasswordResetLink, PasswordResetLinkAdmin)






class SubscriberAdmin(admin.ModelAdmin):

    list_display = ('email',)
    ordering = ('id',)


admin.site.register(Subscriber, SubscriberAdmin)


class CommentLikeHistoryAdmin(admin.ModelAdmin):

    list_display = ['user', 'comment', 'liked_at']

    ordering = ('id',)


admin.site.register(CommentLikeHistory, CommentLikeHistoryAdmin)


      
class CustomUserAdmin(BaseUserAdmin):
    
  
    list_display = ['id', 'username', 'email']
    ordering = ('id',)


admin.site.unregister(User)

admin.site.register(User, CustomUserAdmin)


class AllPostsAdmin(admin.ModelAdmin):

    list_display = ('id', 'title', 'date', 'tags')
    ordering = ('id',)


admin.site.register(AllPosts, AllPostsAdmin)


class platformAdmin(admin.ModelAdmin):

    list_display = ("name",)


admin.site.register(platform, platformAdmin)


class pollsAdmin(admin.ModelAdmin):

    list_display = ('id', 'expiryTimestamp', 'question', 'isActive')
    ordering = ('id',)


admin.site.register(Polls, pollsAdmin)


class ChoiceAdmin(admin.ModelAdmin):

    list_display = ('id', 'title', 'numVotes')
    ordering = ('id',)


admin.site.register(Choice, ChoiceAdmin)


class VoteAdmin(admin.ModelAdmin):

    list_display = ('id', 'user', 'poll')
    ordering = ('id',)


admin.site.register(Vote, VoteAdmin)


class contactUsAdmin(admin.ModelAdmin):

    list_display = ('id', 'message')
    ordering = ('id',)


admin.site.register(contactUs, contactUsAdmin)


class CommentsAdmin(admin.ModelAdmin):

    list_display = ('id', 'userId')

    ordering = ('id',)


admin.site.register(Comments, CommentsAdmin)


class ReplyAdmin(admin.ModelAdmin):

    list_display = ('id', 'userId', 'replyText')
    ordering = ('id',)


admin.site.register(Reply, ReplyAdmin)


class ReplyLikeHistoryAdmin(admin.ModelAdmin):

    list_display = ('id', 'user', 'reply', 'liked_at')


admin.site.register(ReplyLikeHistory, ReplyLikeHistoryAdmin)


class wallpapersAdmin(admin.ModelAdmin):

    list_display = ('title', 'id', 'device', 'resolution', 'date')

    list_filter = ('title', 'id')

    ordering = ('id',)


admin.site.register(wallpapers, wallpapersAdmin)


class tracksAdmin(admin.ModelAdmin):

    list_display = ('title', 'id', 'artists', 'album', 'date')

    list_filter = ('title', 'id')

    ordering = ('id',)


admin.site.register(tracks, tracksAdmin)


class albumsAdmin(admin.ModelAdmin):

    list_display = ('title', 'id', 'date', 'slug', 'date')

    list_filter = ('title', 'id')

    ordering = ('id',)


admin.site.register(albums, albumsAdmin)


class bazi100TeamAdmin(admin.ModelAdmin):

    list_display = ('id', 'position', 'email', 'expertise')

    ordering = ('id',)


admin.site.register(bazi100Team, bazi100TeamAdmin)


class advertisementsAdmin(admin.ModelAdmin):

    list_display = ('adType', 'brandName', 'brandLink',
                    'startsDate', 'endsDate')

    list_filter = ('endsDate',)

    ordering = ('endsDate',)


admin.site.register(advertisements, advertisementsAdmin)
