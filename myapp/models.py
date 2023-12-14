from django.db import models
from django.db import models
from django.contrib.auth.models import User
from django.conf.locale.en import formats as en_formats
from django.core.validators import FileExtensionValidator
from django_jsonform.models.fields import ArrayField
from ckeditor_uploader.fields import RichTextUploadingField
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from django.conf import settings

en_formats.DATETIME_FORMAT = 'Y-m-d'


class commentReply(models.Model):

    replyText = models.TextField(verbose_name="متن پاسخ")

    createdAt = models.DateTimeField(
        auto_now_add=True, verbose_name="زمان و تاریخ انتشار پاسخ")

    userId = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='users', verbose_name="آیدی کاربر")

    replyTo = models.ForeignKey('self', on_delete=models.CASCADE, blank=True,
                                null=True, related_name='reply', verbose_name="پاسخ برای")

    likeCount = models.IntegerField(default=0, verbose_name="تعداد لایک‌ها")


class Meta:
    unique_together = ('userId', 'likeCount')
    verbose_name = "پاسخ"
    verbose_name_plural = "پاسخ ها"


class comments(models.Model):

    commentText = models.TextField(verbose_name="متن کامنت")

    createdAt = models.DateTimeField(
        auto_now_add=True, verbose_name="زمان و تاریخ انتشار کامنت")

    userId = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='user', verbose_name="آیدی کاربر")

    postId = models.ForeignKey(
        'allPosts', on_delete=models.CASCADE, related_name='comment', verbose_name="آیدی پست")

    commentReplies = models.ForeignKey(
        commentReply, on_delete=models.CASCADE, related_name='replies', verbose_name="آیدی کامنت")

    likeCount = models.IntegerField(default=0, verbose_name="تعداد لایک‌ها")

    class Meta:
        unique_together = ('userId', 'likeCount')
        verbose_name = "کامنت"
        verbose_name_plural = "کامنت ها"


class platform(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

    class Meta:

        verbose_name = "پلتفرم بازی ها"

        verbose_name_plural = "پلتفرم بازی ها"


class allPosts(models.Model):

    EVENT_STAGE_CHOICES = (


        ('E3', 'E3'),

        ('game-awards', 'game-awards'),

        ('gamescom', 'gamescom'),

        ('tgs', 'tgs')


    )

    VIDEO_TYPE_CHOICES = (


        ('gameplays trailers', 'gameplays trailers'),

        ('blink', 'blink'),


    )

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
        'bazi100Team', on_delete=models.CASCADE, verbose_name="آیدی نویسنده")

    comments = models.ForeignKey(comments, on_delete=models.CASCADE,
                                 related_name='post', verbose_name="کامنت ها", blank=True, null=True)

    numComments = models.IntegerField(default=0, verbose_name="تعداد کامنت‌ها")

    numReplies = models.IntegerField(default=0, verbose_name="تعداد ریپلای‌ها")

    isEvent = models.BooleanField(default=False, null=True)

    isArticle = models.BooleanField(default=False, null=True)

    isVideo = models.BooleanField(default=False, null=True)

    isNews = models.BooleanField(default=False, null=True)

    isStory = models.BooleanField(default=False, null=True)

    def update_comment_counts(self):
        self.numComments = self.comments.count()
        self.numReplies = self.comments.exclude(commentReply=None).count()
        self.save()

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


class bazi100Team(models.Model):

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

    username = models.CharField(max_length=80, verbose_name="نام کاربری",
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

        verbose_name = "تیم بازی 100"

        verbose_name_plural = "تیم بازی 100"

    def __str__(self):
        return self.memberName


class advertisements(models.Model):

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


class polls(models.Model):

    expiryTimestamp = models.DateTimeField(
        verbose_name=" تاریخ و ساعت نظرسنجی")

    question = models.CharField(max_length=170, verbose_name="سوال نظر سنجی")

    class Meta:

        verbose_name = "نظرسنجی"

        verbose_name_plural = "نظرسنجی ها"


class oldPolls(models.Model):

    expiryTimestamp = models.DateTimeField(
        verbose_name=" تاریخ و ساعت نظرسنجی")

    question = models.CharField(max_length=170, verbose_name="سوال نظر سنجی")

    class Meta:

        verbose_name = "نظرسنجی قبل"

        verbose_name_plural = "نظرسنجی های قبلی"


class choice(models.Model):

    polls = models.ForeignKey(
        polls, on_delete=models.CASCADE, verbose_name="نظرسنجی")

    title = models.CharField(max_length=100)

    image = models.ImageField(upload_to='choice_images/')

    numvotes = models.IntegerField(default=0)

    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['polls', 'user'], name='unique_user_choice')
        ]

    class Meta:

        verbose_name = "گزینه"

        verbose_name_plural = "گزینه ها"


class contactUs(models.Model):

    fullName = models.CharField(max_length=150, verbose_name="نام کامل")

    emailContact = models.EmailField(verbose_name="ایمیل")

    message = models.TextField(verbose_name="متن پیغام")

    class Meta:

        verbose_name = "تماس با ما"

        verbose_name_plural = "تماس باما"
