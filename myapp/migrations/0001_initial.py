# Generated by Django 5.0 on 2023-12-16 17:05

import ckeditor_uploader.fields
import django.core.validators
import django.db.models.deletion
import django_jsonform.models.fields
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='advertisements',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('adType', models.CharField(choices=[('100A', '100A'), ('100B', '100B'), ('100C', '100C'), ('100F', '100F'), ('100G', '100G'), ('100H', '100H')], max_length=80, verbose_name='نوع تبلیغ')),
                ('brandName', models.CharField(max_length=80, verbose_name='نام برند')),
                ('brandLink', models.URLField(verbose_name='لینک برند')),
                ('adFile', models.FileField(help_text='Uploaded file must be .gif or .jpg', upload_to='filetype/', validators=[django.core.validators.FileExtensionValidator(['gif', 'jpg'])], verbose_name='فایل تبلیغ')),
                ('isTextAd', models.BooleanField(default=False)),
                ('textAd', models.TextField(blank=True, null=True, verbose_name='متن تبلیغ')),
                ('startsDate', models.DateField(verbose_name='تاریخ شروع تبلیغ')),
                ('endsDate', models.DateField(verbose_name='تاریخ پایان تبلیغ')),
            ],
            options={
                'verbose_name': 'تبلیغ',
                'verbose_name_plural': 'تبلیغات',
            },
        ),
        migrations.CreateModel(
            name='bazi100Team',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('position', models.CharField(blank=True, choices=[('developer', 'developer'), ('author', 'author'), ('advertisment', 'advertisment'), ('cameraman', 'cameraman'), ('socials', 'socials')], null=True, verbose_name='زمینه فعالیت')),
                ('expertise', models.CharField(max_length=120, verbose_name='تخصص')),
                ('memberName', models.CharField(max_length=80, verbose_name='اسم کاربر')),
                ('username', models.CharField(help_text="Usernames can contain letters(a-z),numbers(0-9),and periods(.).Usernames cannot contain an ampersand(&),equals sings(=),underscore(_),aposterophe('),dash(-),plus sign(+),comma(,),brackets(<,>),or more than one period(.) in a row", max_length=80, unique=True, verbose_name='نام کاربری')),
                ('avatar', models.ImageField(help_text='Avatar file must be lowerthan 100kb and maximum size is : 300*300 pixels', null=True, upload_to='images/', verbose_name='آواتار')),
                ('createdAt', models.DateTimeField(auto_now_add=True, verbose_name='تاریخ و زمان عضویت')),
                ('linkedin', models.CharField(blank=True, max_length=80, null=True, verbose_name='لینکدین')),
                ('instagram', models.CharField(blank=True, max_length=80, null=True, verbose_name='اینستاگرام')),
                ('twitter', models.CharField(blank=True, max_length=80, null=True, verbose_name='توییتر')),
                ('email', models.EmailField(blank=True, max_length=80, null=True, verbose_name='ایمیل')),
                ('about', models.TextField(verbose_name='درباره')),
            ],
            options={
                'verbose_name': 'تیم بازی 100',
                'verbose_name_plural': 'تیم بازی 100',
            },
        ),
        migrations.CreateModel(
            name='Choice',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('image', models.ImageField(upload_to='choice_images/')),
                ('numVotes', models.IntegerField(default=0)),
            ],
            options={
                'verbose_name': 'گزینه',
                'verbose_name_plural': 'گزینه ها',
            },
        ),
        migrations.CreateModel(
            name='contactUs',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fullName', models.CharField(max_length=150, verbose_name='نام کامل')),
                ('emailContact', models.EmailField(max_length=254, verbose_name='ایمیل')),
                ('message', models.TextField(verbose_name='متن پیغام')),
            ],
            options={
                'verbose_name': 'تماس با ما',
                'verbose_name_plural': 'تماس باما',
            },
        ),
        migrations.CreateModel(
            name='platform',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
            ],
            options={
                'verbose_name': 'پلتفرم بازی ها',
                'verbose_name_plural': 'پلتفرم بازی ها',
            },
        ),
        migrations.CreateModel(
            name='tracks',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=240, verbose_name='عنوان')),
                ('artists', django_jsonform.models.fields.ArrayField(base_field=models.CharField(max_length=120), size=None, verbose_name='آرتیست ها')),
                ('duration', models.CharField(blank=True, null=True, verbose_name='مدت زمان')),
                ('date', models.DateField(verbose_name='تاریخ  انتشار')),
                ('tags', django_jsonform.models.fields.ArrayField(base_field=models.CharField(max_length=100), blank=True, null=True, size=None)),
                ('image', models.ImageField(help_text='  WEBP & Transparent حجم عکس باید کمتر از 200 کیلوبایت باشد ترجیحا 100 کیلوبایت و در فرمت ', null=True, upload_to='images/', verbose_name='کاور آلبوم')),
                ('audioFile', models.FileField(upload_to='music/', verbose_name='فایل موسیقی')),
                ('fileSize', models.CharField(blank=True, null=True, verbose_name='حجم فایل')),
                ('album', models.CharField(max_length=300, verbose_name='آلبوم')),
            ],
            options={
                'verbose_name': 'ساندترک',
                'verbose_name_plural': 'ساندترک ها',
            },
        ),
        migrations.CreateModel(
            name='wallpapers',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=80, verbose_name='عنوان')),
                ('slug', models.SlugField(null=True, unique=True, verbose_name='آدرس')),
                ('tags', django_jsonform.models.fields.ArrayField(base_field=models.CharField(max_length=100), blank=True, null=True, size=None)),
                ('date', models.DateField(verbose_name='تاریخ  انتشار')),
                ('thumbnail', models.ImageField(help_text='  WEBP & Transparent حجم عکس باید کمتر از 200 کیلوبایت باشد ترجیحا 100 کیلوبایت و در فرمت ', upload_to='images/', verbose_name='تصویر تک صفحه')),
                ('device', models.CharField(blank=True, choices=[('desktop', 'desktop'), ('mobile', 'mobile')], max_length=60, null=True, verbose_name='نوع دستگاه ')),
                ('image', models.ImageField(null=True, upload_to='wallpapers/', verbose_name='فایل والپیپر')),
                ('resolution', models.CharField(blank=True, max_length=50, null=True, verbose_name='کیفیت')),
            ],
            options={
                'verbose_name': 'والپیپر',
                'verbose_name_plural': 'والپیپرها',
            },
        ),
        migrations.CreateModel(
            name='allPosts',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, verbose_name='عنوان')),
                ('slug', models.SlugField(max_length=100, unique=True, verbose_name='آدرس')),
                ('image', models.ImageField(help_text=' WEBP & Transparent حجم عکس باید کمتر از 200 کیلوبایت باشد ترجیحا 100 کیلوبایت و در فرمت', null=True, upload_to='images/', verbose_name='تصویر تک صفحه ')),
                ('content', ckeditor_uploader.fields.RichTextUploadingField(verbose_name='محتوا')),
                ('date', models.DateField(verbose_name='تاریخ و ساعت')),
                ('eventStage', models.CharField(blank=True, choices=[('E3', 'E3'), ('game-awards', 'game-awards'), ('gamescom', 'gamescom'), ('tgs', 'tgs')], max_length=100, null=True, verbose_name='برگزارکننده رویداد')),
                ('videoType', models.CharField(blank=True, choices=[('gameplays trailers', 'gameplays trailers'), ('blink', 'blink')], max_length=40, null=True, verbose_name='تایپ ویدیو')),
                ('tags', django_jsonform.models.fields.ArrayField(base_field=models.CharField(max_length=100), blank=True, null=True, size=None)),
                ('ogImage', models.ImageField(help_text=' سایز عکس 1200*630', upload_to='images/', verbose_name='عکس انتشار')),
                ('postSummary', models.TextField(help_text='خلاصه شامل دو یا سه جمله باشد', verbose_name='خلاصه')),
                ('numComments', models.IntegerField(default=0, verbose_name='تعداد کامنت\u200cها')),
                ('numReplies', models.IntegerField(default=0, verbose_name='تعداد ریپلای\u200cها')),
                ('isEvent', models.BooleanField(default=False, null=True)),
                ('isArticle', models.BooleanField(default=False, null=True)),
                ('isVideo', models.BooleanField(default=False, null=True)),
                ('isNews', models.BooleanField(default=False, null=True)),
                ('isStory', models.BooleanField(default=False, null=True)),
                ('memberId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myapp.bazi100team', verbose_name='آیدی نویسنده')),
            ],
            options={
                'verbose_name': 'جدول پست ها',
                'verbose_name_plural': 'جدول همه پست ها',
            },
        ),
        migrations.CreateModel(
            name='commentReply',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('replyText', models.TextField(verbose_name='متن پاسخ')),
                ('createdAt', models.DateTimeField(auto_now_add=True, verbose_name='زمان و تاریخ انتشار پاسخ')),
                ('likeCount', models.IntegerField(default=0, verbose_name='تعداد لایک\u200cها')),
                ('replyTo', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='reply', to='myapp.commentreply', verbose_name='پاسخ برای')),
                ('userId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='users', to=settings.AUTH_USER_MODEL, verbose_name='آیدی کاربر')),
            ],
            options={
                'verbose_name': 'پاسخ',
                'verbose_name_plural': 'پاسخ ها',
                'unique_together': {('userId', 'likeCount')},
            },
        ),
        migrations.CreateModel(
            name='comments',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('commentText', models.TextField(verbose_name='متن کامنت')),
                ('createdAt', models.DateTimeField(auto_now_add=True, verbose_name='زمان و تاریخ انتشار کامنت')),
                ('likeCount', models.IntegerField(default=0, verbose_name='تعداد لایک\u200cها')),
                ('commentReplies', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='replies', to='myapp.commentreply', verbose_name='آیدی کامنت')),
                ('postId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comment', to='myapp.allposts', verbose_name='آیدی پست')),
                ('userId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user', to=settings.AUTH_USER_MODEL, verbose_name='آیدی کاربر')),
            ],
            options={
                'verbose_name': 'کامنت',
                'verbose_name_plural': 'کامنت ها',
                'unique_together': {('userId', 'likeCount')},
            },
        ),
        migrations.AddField(
            model_name='allposts',
            name='comments',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='post', to='myapp.comments', verbose_name='کامنت ها'),
        ),
        migrations.CreateModel(
            name='oldPolls',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('expiryTimestamp', models.DateTimeField(verbose_name=' تاریخ و ساعت اتمام نظرسنجی')),
                ('question', models.CharField(max_length=170, verbose_name='سوال نظر سنجی')),
                ('choices', models.ManyToManyField(to='myapp.choice', verbose_name='گزینه ها')),
            ],
            options={
                'verbose_name': 'نظرسنجی قبل',
                'verbose_name_plural': 'نظرسنجی های قبلی',
            },
        ),
        migrations.AddField(
            model_name='allposts',
            name='platformIds',
            field=models.ManyToManyField(to='myapp.platform', verbose_name='پلتفرم ها'),
        ),
        migrations.CreateModel(
            name='Polls',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('expiryTimestamp', models.DateTimeField(verbose_name=' تاریخ و ساعت اتمام نظرسنجی')),
                ('question', models.CharField(max_length=170, verbose_name='سوال نظر سنجی')),
                ('choices', models.ManyToManyField(to='myapp.choice', verbose_name='گزینه ها')),
            ],
            options={
                'verbose_name': 'نظرسنجی',
                'verbose_name_plural': 'نظرسنجی ها',
            },
        ),
        migrations.CreateModel(
            name='albums',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=240, verbose_name='عنوان')),
                ('tags', django_jsonform.models.fields.ArrayField(base_field=models.CharField(max_length=100), blank=True, null=True, size=None)),
                ('artists', django_jsonform.models.fields.ArrayField(base_field=models.CharField(max_length=120), blank=True, null=True, size=None, verbose_name='آرتیست ها')),
                ('date', models.DateField(verbose_name='تاریخ  انتشار')),
                ('image', models.ImageField(help_text='  WEBP & Transparent حجم عکس باید کمتر از 200 کیلوبایت باشد ترجیحا 100 کیلوبایت و در فرمت ', null=True, upload_to='images/', verbose_name='کاور آلبوم')),
                ('platforms', django_jsonform.models.fields.ArrayField(base_field=models.CharField(max_length=100), size=None)),
                ('ogImage', models.ImageField(blank=True, help_text='سایز عکس 630**1200', null=True, upload_to='images/')),
                ('totalFileSize', models.FloatField(blank=True, null=True, verbose_name='حجم فایل زیپ')),
                ('zipFile', models.FileField(upload_to='zipfiles/', verbose_name='فایل زیپ')),
                ('slug', models.SlugField(null=True, unique=True, verbose_name='آدرس')),
                ('description', models.TextField(verbose_name='متن توضیحی')),
                ('tracks', models.ManyToManyField(to='myapp.tracks', verbose_name='ساندترک ها')),
            ],
            options={
                'verbose_name': 'آلبوم',
                'verbose_name_plural': ' آلبوم موسیقی ها',
            },
        ),
        migrations.CreateModel(
            name='Vote',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('choice', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myapp.choice')),
                ('poll', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myapp.polls')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'رای ها',
                'verbose_name_plural': 'رای ها',
            },
        ),
    ]
