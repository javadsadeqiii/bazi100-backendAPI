from django.contrib import admin
from .models import *
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth import get_user_model





CustomUserModel = get_user_model()


class CustomUserAdmin(BaseUserAdmin):
    list_display = ['id', 'username', 'email', 'selectedAvatar','customAvatar']  
    ordering = ('id',)

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email', 'selectedAvatar','customAvatar')}),  
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2', 'email', 'avatar')
        }),
        ('Personal info', {'fields': ('first_name', 'last_name' )}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')})
    )


if CustomUserModel != CustomUser:
    admin.site.unregister(CustomUserModel)

admin.site.register(CustomUser, CustomUserAdmin)










class CommentReportAdmin(admin.ModelAdmin):
    
    list_display = ('commentText','commentId','userId')
    ordering = ('id',)
    
admin.site.register(CommentReport, CommentReportAdmin)
    









class ReplyReportAdmin(admin.ModelAdmin):
    
    list_display = ('replyText','reply','userId')
    ordering = ('id',)
    
admin.site.register(ReplyReport, ReplyReportAdmin)
    







class SubscriberAdmin(admin.ModelAdmin):

    list_display = ('email',)
    ordering = ('id',)


admin.site.register(Subscriber, SubscriberAdmin)






class CommentLikeHistoryAdmin(admin.ModelAdmin):

    list_display = ['user', 'comment', 'liked_at']

    ordering = ('id',)


admin.site.register(CommentLikeHistory, CommentLikeHistoryAdmin)





      





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






class ContactUsAdmin(admin.ModelAdmin):

    list_display = ('id', 'message')
    ordering = ('id',)


admin.site.register(ContactUs, ContactUsAdmin)





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





class bazikachoTeamAdmin(admin.ModelAdmin):

    list_display = ('id', 'position', 'email', 'expertise')

    ordering = ('id',)


admin.site.register(bazikachoTeam, bazikachoTeamAdmin)






class AdvertisementsAdmin(admin.ModelAdmin):

    list_display = ('adType', 'brandName', 'brandLink',
                    'startsDate', 'endsDate')

    list_filter = ('endsDate',)

    ordering = ('endsDate',)


admin.site.register(Advertisements, AdvertisementsAdmin)
