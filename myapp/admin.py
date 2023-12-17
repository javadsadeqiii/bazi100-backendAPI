from django.contrib import admin

# Register your models here.
from typing import Self
from django.contrib import admin
from .models import *
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin


# Register your models here.


class allPostsAdmin(admin.ModelAdmin):

    list_display = ('id', 'title', 'date', 'tags')
    ordering = ('id',)


admin.site.register(allPosts, allPostsAdmin)


class platformAdmin(admin.ModelAdmin):

    list_display = ("name",)


admin.site.register(platform, platformAdmin)


class pollsAdmin(admin.ModelAdmin):

    list_display = ('id', 'expiryTimestamp', 'question')
    ordering = ('id',)


admin.site.register(Polls, pollsAdmin)


class oldPollsAdmin(admin.ModelAdmin):

    list_display = ('id', 'question')
    ordering = ('id',)


admin.site.register(oldPolls, oldPollsAdmin)


class ChoiceAdmin(admin.ModelAdmin):

    list_display = ('id', 'title', 'numVotes')
   # ordering = ('id',)


admin.site.register(Choice, ChoiceAdmin)


class VoteAdmin(admin.ModelAdmin):

    list_display = ('id', 'user', 'poll')


admin.site.register(Vote, VoteAdmin)


class contactUsAdmin(admin.ModelAdmin):

    list_display = ('id', 'message')
    ordering = ('id',)


admin.site.register(contactUs, contactUsAdmin)


class commentReplyAdmin(admin.ModelAdmin):

    list_display = ('id', 'replyText')
    ordering = ('id',)


admin.site.register(commentReply, commentReplyAdmin)


class commentsAdmin(admin.ModelAdmin):

    list_display = ('id', 'userId', 'postId', 'likeCount')

    ordering = ('id',)


admin.site.register(comments, commentsAdmin)


class CustomUserAdmin(admin.ModelAdmin):

    list_display = ('id', 'username', 'email', 'first_name',
                    'last_name', 'date_joined', 'is_staff')

    ordering = ('id',)


admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)


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


# class allPostsAdmin(admin.ModelAdmin):

#  list_display = ('id','title','date')

#  list_filter = ('title','id')

#  ordering = ('id',)

# admin.site.register(allPosts,allPostsAdmin)


class bazi100TeamAdmin(admin.ModelAdmin):

    list_display = ('id', 'position', 'email', 'expertise')

    list_filter = ('id',)

    ordering = ('id',)


admin.site.register(bazi100Team, bazi100TeamAdmin)


class advertisementsAdmin(admin.ModelAdmin):

    list_display = ('adType', 'brandName', 'brandLink',
                    'startsDate', 'endsDate')

    list_filter = ('endsDate',)

    ordering = ('endsDate',)


admin.site.register(advertisements, advertisementsAdmin)
