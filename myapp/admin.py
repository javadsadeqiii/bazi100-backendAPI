from django.contrib import admin

# Register your models here.
from typing import Self
from django.contrib import admin
from .models import *
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin


# Register your models here.

# class PostCommentAdmin(admin.ModelAdmin):

#  list_display = ('id', 'post', 'comment')
# ordering = ('id',)


# admin.site.register(PostComment, PostCommentAdmin)


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


class CommentLikeAdmin(admin.ModelAdmin):

    list_display = ('id', 'userId')
    ordering = ('id',)


admin.site.register(CommentLike, CommentLikeAdmin)


class replyAdmin(admin.ModelAdmin):

    list_display = ('id', 'userId', 'replyText')
    ordering = ('id',)


admin.site.register(reply, replyAdmin)


class replyLikeAdmin(admin.ModelAdmin):

    list_display = ('id', 'replyId', 'userId')
    ordering = ('id',)


admin.site.register(replyLike, replyLikeAdmin)


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
