from django.db import models
from django.db import models
from django.contrib.auth.models import User
from django.conf.locale.en import formats as en_formats
from django.core.validators import FileExtensionValidator
from django_jsonform.models.fields import ArrayField
from ckeditor_uploader.fields import RichTextUploadingField
from django.db import models
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver



en_formats.DATETIME_FORMAT = 'Y-m-d'





class CommentReport(models.Model):
    
    commentText = models.TextField()
    commentId = models.ForeignKey('Comments', on_delete=models.CASCADE, related_name='comment_reports_id')
    userId = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_comment_reports')
    post = models.ForeignKey('AllPosts', on_delete=models.CASCADE, related_name='post_comment_reports')
    
    class Meta:
        verbose_name = "گزارش کامنت"
        verbose_name_plural = "کامنت های گزارش شده"







class ReplyReport(models.Model):
    replyText = models.TextField()
    reply = models.ForeignKey('Reply', on_delete=models.CASCADE, related_name='report_of_reply')
    userId = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_reply_reports')
    post = models.ForeignKey('AllPosts', on_delete=models.CASCADE, related_name='post_reply_reports')
    
    class Meta:
        verbose_name = "گزارش ریپلای"
        verbose_name_plural = "گزارش ریپلای ها"








class Subscriber(models.Model):
    email = models.CharField(max_length=50)
    
    def __str__(self):
        return self.email

    class Meta:
        verbose_name = "خبرنامه"
        verbose_name_plural = "خبرنامه"





class CommentLikeHistory(models.Model):
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.ForeignKey('Comments', on_delete=models.CASCADE)
    liked_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "لایک کامنت ها"
        verbose_name_plural = "لایک کامنت ها"





class CommentLike(models.Model):

    userId = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='userliker', verbose_name="آیدی کاربر")

    commentId = models.ForeignKey(
        'Comments', on_delete=models.CASCADE, default=None, related_name='likecount', verbose_name="آیدی کامنت")

    likeCount = models.IntegerField(default=0, verbose_name="تعداد لایک")

    class Meta:
        verbose_name = "لایک کامنت ها"
        verbose_name_plural = "لایک کامنت ها"






class Comments(models.Model):
    
    
    def save(self, *args, **kwargs):
        super(Comments, self).save(*args, **kwargs)
        self.post.update_comment_count()
        
        
    def delete(self, *args, **kwargs):
        self.post.update_comment_count()
        super(Comments, self).delete(*args, **kwargs)



    commentText = models.TextField(verbose_name="متن کامنت")

    createdAt = models.DateTimeField(
        auto_now_add=True, verbose_name="زمان و تاریخ انتشار کامنت")

    userId = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='user', verbose_name="آیدی کاربر")

    post = models.ForeignKey(
        'AllPosts', on_delete=models.CASCADE, default=None, related_name='post', verbose_name="آیدی پست")

    likeCount = models.IntegerField(default=0, verbose_name="تعداد لایک")

    def __str__(self):
        return f"Comment by {self.userId} on Post {self.post}"
    # نشان میدهد که کامنت توسط کدام کاربر بر روی کدام پست ایجاد شده

    class Meta:
        verbose_name = "کامنت"
        verbose_name_plural = "کامنت ها"




@receiver(post_save, sender=Comments)
def update_comment_count_on_create(sender, instance, created, **kwargs):
    if created:
        instance.post.update_comment_count()


@receiver(post_delete, sender=Comments)
def update_comment_count_on_delete(sender, instance, **kwargs):
    instance.post.update_comment_count()





class Reply(models.Model):
    
    
    
    def save(self, *args, **kwargs):
        super(Reply, self).save(*args, **kwargs)
        self.post.update_reply_count()
        
        
    def delete(self, *args, **kwargs):
        self.post.update_reply_count()
        super(Reply, self).delete(*args, **kwargs)

    replyText = models.TextField(verbose_name="متن پاسخ")

    createdAt = models.DateTimeField(
        auto_now_add=True, verbose_name="زمان و تاریخ انتشار پاسخ")

    userId = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name='user_replies', verbose_name="آیدی کاربر")

    commentId = models.ManyToManyField(
        Comments, related_name='replies_comment', verbose_name="کامنت")

    parentReplyId = models.ForeignKey('self', on_delete=models.CASCADE, null=True,
                                      blank=True, related_name='replies', verbose_name="پاسخ والد")

    post = models.ForeignKey(
        'AllPosts', on_delete=models.CASCADE, default=None, related_name='postreply', verbose_name="آیدی پست")

    likeCount = models.IntegerField(default=0, verbose_name="تعداد لایک")

    def __str__(self):
        return f"Reply by {self.userId} to Comment {self.commentId}"
# نشان میدهد که این پاسخ توسط کدام کاربر به کدام کامنت با استفاده از آیدی آن مرتبط است

    class Meta:
        verbose_name = "ریپلای"
        verbose_name_plural = "ریپلای ها"


@receiver(post_save, sender=Reply)
def update_reply_count_on_create(sender, instance, created, **kwargs):
    if created:
        instance.post.update_reply_count()


@receiver(post_delete, sender=Reply)
def update_reply_count_on_delete(sender, instance, **kwargs):
    instance.post.update_reply_count()




class ReplyLikeHistory(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    reply = models.ForeignKey(Reply, on_delete=models.CASCADE)

    liked_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "لایک ریپلای"
        verbose_name_plural = "لایک ریپلای ها"




class ReplyLike(models.Model):

    userId = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name="آیدی کاربر")
    replyId = models.ForeignKey(
        Reply, on_delete=models.CASCADE, verbose_name="آیدی کامنت")

    likeCount = models.IntegerField(default=0, verbose_name="تعداد لایک")

    class Meta:
        verbose_name = "لایک های ریپلای"
        verbose_name_plural = "لایک های ریپلای"


class platform(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

    class Meta:

        verbose_name = "پلتفرم بازی ها"

        verbose_name_plural = "پلتفرم بازی ها"





class AllPosts(models.Model):

    EVENT_STAGE_CHOICES = (


        ('e3', 'e3'),

        ('game-awards', 'game-awards'),

        ('gamescom', 'gamescom'),

        ('tgs', 'tgs')


    )

    VIDEO_TYPE_CHOICES = (


        ('gameplays-trailers', 'gameplays-trailers'),

        ('blink', 'blink'),


    )
    
    def update_comment_count(self):
        count = Comments.objects.filter(post=self).count()  
        self.commentCount = count
        self.save()
        
    
    def update_reply_count(self):
        count = Reply.objects.filter(post=self).count()  
        self.replyCount = count
        self.save()
        

    title = models.CharField(max_length=255, verbose_name="عنوان")

    slug = models.SlugField(max_length=100, unique=True, verbose_name="آدرس")

    image = models.ImageField(upload_to='images/', verbose_name="تصویر تک صفحه ", null=True,
                              help_text=" WEBP & Transparent حجم عکس باید کمتر از 200 کیلوبایت باشد ترجیحا 100 کیلوبایت و در فرمت")

    content = RichTextUploadingField(verbose_name="محتوا")

    platformIds = models.ManyToManyField(platform, verbose_name="پلتفرم ها")

    date = models.DateField(verbose_name="تاریخ و ساعت")

    eventStage = models.CharField(
        max_length=100, null=True, choices=EVENT_STAGE_CHOICES, blank=True, verbose_name="برگزارکننده رویداد")

    videoType = models.CharField(
        max_length=40, null=True, choices=VIDEO_TYPE_CHOICES, blank=True, verbose_name="تایپ ویدیو")

    tags = ArrayField(models.CharField(max_length=100), blank=True, null=True)

    ogImage = models.ImageField(
        upload_to='images/', help_text=" سایز عکس 1200*630", verbose_name="عکس انتشار")

    postSummary = models.TextField(
        help_text="خلاصه شامل دو یا سه جمله باشد", verbose_name="خلاصه")

    memberId = models.ForeignKey(
        'bazikachoTeam', on_delete=models.CASCADE, verbose_name="آیدی نویسنده")
    
    commentCount = models.IntegerField(default=0, verbose_name="تعداد کامنت", blank=True)
    
    replyCount = models.IntegerField(default=0,verbose_name="تعداد ریپلای",blank=True)

    isEvent = models.BooleanField(default=False, null=True)

    isArticle = models.BooleanField(default=False, null=True)

    isVideo = models.BooleanField(default=False, null=True)

    isNews = models.BooleanField(default=False, null=True)

    isStory = models.BooleanField(default=False, null=True)
    
    

    class Meta:

        verbose_name = "جدول پست ها"

        verbose_name_plural = "جدول همه پست ها"

    def __str__(self):

        return self.title






class wallpapers(models.Model):

    DEVICE_CHOICES = (

        ('desktop', 'desktop'),

        ('mobile', 'mobile'),
    )

    title = models.CharField(max_length=80, verbose_name="عنوان")

    slug = models.SlugField(verbose_name="آدرس", unique=True, null=True)

    tags = ArrayField(models.CharField(max_length=100), blank=True, null=True)

    date = models.DateField(verbose_name="تاریخ  انتشار")

    thumbnail = models.ImageField(upload_to='images/', verbose_name="تصویر تک صفحه",
                                  help_text="  WEBP & Transparent حجم عکس باید کمتر از 200 کیلوبایت باشد ترجیحا 100 کیلوبایت و در فرمت ")

    device = models.CharField(max_length=60, blank=True, null=True,
                              choices=DEVICE_CHOICES, verbose_name="نوع دستگاه ")

    image = models.ImageField(upload_to='wallpapers/',
                              verbose_name="فایل والپیپر", null=True)

    resolution = models.CharField(
        max_length=50, blank=True, null=True, verbose_name="کیفیت")

    class Meta:

        verbose_name = "والپیپر"

        verbose_name_plural = "والپیپرها"

    def __str__(self):
        return self.title





class tracks(models.Model):

    title = models.CharField(max_length=240, verbose_name="عنوان")

    artists = ArrayField(models.CharField(
        max_length=120), verbose_name="آرتیست ها")

    duration = models.CharField(null=True, blank=True, verbose_name="مدت زمان")

    date = models.DateField(verbose_name="تاریخ  انتشار")

    tags = ArrayField(models.CharField(max_length=100), blank=True, null=True)

    image = models.ImageField(upload_to='images/', verbose_name="کاور آلبوم", null=True,
                              help_text="  WEBP & Transparent حجم عکس باید کمتر از 200 کیلوبایت باشد ترجیحا 100 کیلوبایت و در فرمت ")

    audioFile = models.FileField(
        upload_to='music/', verbose_name="فایل موسیقی")

    fileSize = models.CharField(null=True, blank=True, verbose_name="حجم فایل")

    album = models.CharField(max_length=300, verbose_name="آلبوم")

    class Meta:

        verbose_name = "ساندترک"

        verbose_name_plural = "ساندترک ها"

    def __str__(self):
        return self.title





class albums(models.Model):
    

    title = models.CharField(max_length=240, verbose_name="عنوان")

    tags = ArrayField(models.CharField(max_length=100), blank=True, null=True)

    artists = ArrayField(models.CharField(max_length=120),
                         verbose_name="آرتیست ها", blank=True, null=True)

    date = models.DateField(verbose_name="تاریخ  انتشار")

    image = models.ImageField(upload_to='images/', verbose_name="کاور آلبوم", null=True,
                              help_text="  WEBP & Transparent حجم عکس باید کمتر از 200 کیلوبایت باشد ترجیحا 100 کیلوبایت و در فرمت ")

    platforms = ArrayField(models.CharField(max_length=100))

    ogImage = models.ImageField(
        upload_to='images/', help_text="سایز عکس 630**1200", blank=True, null=True)

    totalFileSize = models.FloatField(
        null=True, blank=True, verbose_name="حجم فایل زیپ")

    zipFile = models.FileField(upload_to='zipfiles/', verbose_name="فایل زیپ")

    slug = models.SlugField(verbose_name="آدرس", unique=True, null=True)

    description = models.TextField(verbose_name="متن توضیحی")

    tracks = models.ManyToManyField('tracks', verbose_name="ساندترک ها")

    def __str__(self):

        return self.title

    class Meta:

        verbose_name = "آلبوم"

        verbose_name_plural = " آلبوم موسیقی ها"

    def __str__(self):
        return self.title




class bazikachoTeam(models.Model):
    

    POSITION_CHOICE = (

        ("developer", "developer"),

        ("author", "author"),

        ("advertisment", "advertisment"),

        ("cameraman", "cameraman"),

        ("socials", "socials")
    )

    position = models.CharField(
        choices=POSITION_CHOICE, blank=True, null=True, verbose_name="زمینه فعالیت")

    expertise = models.CharField(max_length=120, verbose_name="تخصص")

    memberName = models.CharField(max_length=80, verbose_name="اسم کاربر")

    username = models.CharField(max_length=80, verbose_name="نام کاربری", unique=True,
                                help_text="Usernames can contain letters(a-z),numbers(0-9),and periods(.).Usernames cannot contain an ampersand(&),equals sings(=),underscore(_),aposterophe('),dash(-),plus sign(+),comma(,),brackets(<,>),or more than one period(.) in a row")

    avatar = models.ImageField(upload_to='images/', verbose_name="آواتار", null=True,
                               help_text="Avatar file must be lowerthan 100kb and maximum size is : 300*300 pixels")

    createdAt = models.DateTimeField(
        auto_now_add=True, verbose_name="تاریخ و زمان عضویت")

    linkedin = models.CharField(
        max_length=80, verbose_name="لینکدین", blank=True, null=True)

    instagram = models.CharField(
        max_length=80, verbose_name="اینستاگرام", blank=True, null=True)

    twitter = models.CharField(
        max_length=80, verbose_name="توییتر", blank=True, null=True)

    email = models.EmailField(
        max_length=80, verbose_name="ایمیل", blank=True, null=True)

    about = models.TextField(verbose_name="درباره")

    class Meta:

        verbose_name = "تیم بازیکاچو"

        verbose_name_plural = "تیم بازیکاچو"

    def __str__(self):
        return self.memberName






class Advertisements(models.Model):


    TYPE_CHOICES = (

        ('100A', '100A'),

        ('100B', '100B'),

        ('100C', '100C'),

        ('100F', '100F'),

        ('100G', '100G'),

        ('100H', '100H')

    )

    adType = models.CharField(
        max_length=80, choices=TYPE_CHOICES, verbose_name="نوع تبلیغ")

    brandName = models.CharField(max_length=80, verbose_name="نام برند")

    brandLink = models.URLField(verbose_name="لینک برند")

    adFile = models.FileField(upload_to='filetype/', validators=[FileExtensionValidator(
        ['gif', 'jpg'])], help_text="Uploaded file must be .gif or .jpg", verbose_name="فایل تبلیغ")

    isTextAd = models.BooleanField(default=False)

    textAd = models.TextField(verbose_name="متن تبلیغ", blank=True, null=True)

    startsDate = models.DateField(verbose_name="تاریخ شروع تبلیغ")

    endsDate = models.DateField(verbose_name="تاریخ پایان تبلیغ")

    class Meta:
        verbose_name = "تبلیغ"
        verbose_name_plural = "تبلیغات"

    def __str__(self):
        return self.brandName





class Polls(models.Model):

    expiryTimestamp = models.DateField(
        verbose_name=" تاریخ  اتمام نظرسنجی")

    endTime = models.CharField(max_length=8, default='24:00:00')

    question = models.CharField(max_length=170, verbose_name="سوال نظر سنجی")

    choices = models.ManyToManyField('choice', verbose_name="گزینه ها")

    isActive = models.BooleanField(default=False, null=True)

    class Meta:

        verbose_name = "نظرسنجی"

        verbose_name_plural = "نظرسنجی ها"


class Choice(models.Model):

    title = models.CharField(max_length=100)

    image = models.ImageField(upload_to='choice_images/')

    numVotes = models.IntegerField(default=0)

    class Meta:

        verbose_name = "گزینه"

        verbose_name_plural = "گزینه ها"







class Vote(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    poll = models.ForeignKey(Polls, on_delete=models.CASCADE)
    choice = models.ForeignKey(Choice, on_delete=models.CASCADE)

    class Meta:

        verbose_name = "رای ها"

        verbose_name_plural = "رای ها"




class ContactUs(models.Model):

    fullName = models.CharField(max_length=150, verbose_name="نام کامل")

    emailContact = models.EmailField(verbose_name="ایمیل")

    message = models.TextField(verbose_name="متن پیغام")

    class Meta:

        verbose_name = "تماس با ما"

        verbose_name_plural = "تماس باما"
