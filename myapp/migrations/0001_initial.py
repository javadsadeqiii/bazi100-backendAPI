# Generated by Django 5.0 on 2024-01-13 10:49

import ckeditor_uploader.fields
import django.contrib.auth.models
import django.contrib.auth.validators
import django.core.validators
import django.db.models.deletion
import django.utils.timezone
import django_jsonform.models.fields
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Advertisements',
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
            name='bazikachoTeam',
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
                'verbose_name': 'تیم بازیکاچو',
                'verbose_name_plural': 'تیم بازیکاچو',
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
            name='ContactUs',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fullName', models.CharField(max_length=150, verbose_name='نام کامل')),
                ('emailContact', models.EmailField(max_length=254, verbose_name='ایمیل')),
                ('message', models.TextField(verbose_name='متن پیغام')),
                ('createdAt', models.DateTimeField(auto_now_add=True, null=True, verbose_name='زمان و تاریخ ')),
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
            name='Subscriber',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.CharField(max_length=50)),
            ],
            options={
                'verbose_name': 'خبرنامه',
                'verbose_name_plural': 'خبرنامه',
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
            name='CustomUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('selectedAvatar', models.FileField(blank=True, choices=[('images/avatar1.webp', 'Avatar 1'), ('images/avatar2.webp', 'Avatar 2'), ('images/avatar3.webp', 'Avatar 3'), ('images/avatar4.webp', 'Avatar 4'), ('images/avatar5.webp', 'Avatar 5'), ('images/avatar6.webp', 'Avatar 6'), ('images/avatar7.webp', 'Avatar 7'), ('images/avatar8.webp', 'Avatar 8'), ('images/avatar9.webp', 'Avatar 9'), ('images/avatar10.webp', 'Avatar 10'), ('images/avatar11.webp', 'Avatar 11')], upload_to='images/', verbose_name='Avatar')),
                ('customAvatar', models.FileField(blank=True, upload_to='images/', verbose_name='Custom Avatar')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='AllPosts',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, verbose_name='عنوان')),
                ('slug', models.SlugField(max_length=100, unique=True, verbose_name='آدرس')),
                ('image', models.ImageField(help_text=' WEBP & Transparent حجم عکس باید کمتر از 200 کیلوبایت باشد ترجیحا 100 کیلوبایت و در فرمت', null=True, upload_to='images/', verbose_name='تصویر تک صفحه ')),
                ('content', ckeditor_uploader.fields.RichTextUploadingField(verbose_name='محتوا')),
                ('date', models.DateField(verbose_name='تاریخ و ساعت')),
                ('isEvent', models.BooleanField(default=False, null=True)),
                ('eventStage', models.CharField(blank=True, choices=[('e3', 'e3'), ('game-awards', 'game-awards'), ('gamescom', 'gamescom'), ('tgs', 'tgs')], max_length=100, null=True, verbose_name='برگزارکننده رویداد')),
                ('isVideo', models.BooleanField(default=False, null=True)),
                ('videoType', models.CharField(blank=True, choices=[('gameplays-trailers', 'gameplays-trailers'), ('blink', 'blink')], max_length=40, null=True, verbose_name='تایپ ویدیو')),
                ('tags', django_jsonform.models.fields.ArrayField(base_field=models.CharField(max_length=100), blank=True, null=True, size=None)),
                ('ogImage', models.ImageField(help_text=' سایز عکس 1200*630', upload_to='images/', verbose_name='عکس انتشار')),
                ('postSummary', models.TextField(help_text='خلاصه شامل دو یا سه جمله باشد', verbose_name='خلاصه')),
                ('commentCount', models.IntegerField(blank=True, default=0, verbose_name='تعداد کامنت')),
                ('replyCount', models.IntegerField(blank=True, default=0, verbose_name='تعداد ریپلای')),
                ('isArticle', models.BooleanField(default=False, null=True)),
                ('isNews', models.BooleanField(default=False, null=True)),
                ('isStory', models.BooleanField(default=False, null=True)),
                ('isReportage', models.BooleanField(default=False, null=True)),
                ('memberId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myapp.bazikachoteam', verbose_name='آیدی نویسنده')),
                ('platformIds', models.ManyToManyField(to='myapp.platform', verbose_name='پلتفرم ها')),
            ],
            options={
                'verbose_name': ' پست ها',
                'verbose_name_plural': ' همه پست ها',
            },
        ),
        migrations.CreateModel(
            name='Comments',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('commentText', models.TextField(verbose_name='متن کامنت')),
                ('createdAt', models.DateTimeField(auto_now_add=True, verbose_name='زمان و تاریخ انتشار کامنت')),
                ('likeCount', models.IntegerField(default=0, verbose_name='تعداد لایک')),
                ('post', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='post', to='myapp.allposts', verbose_name='آیدی پست')),
                ('userId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user', to=settings.AUTH_USER_MODEL, verbose_name='آیدی کاربر')),
            ],
            options={
                'verbose_name': 'کامنت',
                'verbose_name_plural': 'کامنت ها',
            },
        ),
        migrations.CreateModel(
            name='CommentReport',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('commentText', models.TextField()),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='post_comment_reports', to='myapp.allposts')),
                ('userId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_comment_reports', to=settings.AUTH_USER_MODEL)),
                ('commentId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comment_reports_id', to='myapp.comments')),
            ],
            options={
                'verbose_name': 'گزارش کامنت',
                'verbose_name_plural': 'کامنت های گزارش شده',
            },
        ),
        migrations.CreateModel(
            name='CommentLikeHistory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('liked_at', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('comment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myapp.comments')),
            ],
            options={
                'verbose_name': 'لایک کامنت ها',
                'verbose_name_plural': 'لایک کامنت ها',
            },
        ),
        migrations.CreateModel(
            name='CommentLike',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('likeCount', models.IntegerField(default=0, verbose_name='تعداد لایک')),
                ('userId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='userliker', to=settings.AUTH_USER_MODEL, verbose_name='آیدی کاربر')),
                ('commentId', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='likecount', to='myapp.comments', verbose_name='آیدی کامنت')),
            ],
            options={
                'verbose_name': 'لایک کامنت ها',
                'verbose_name_plural': 'لایک کامنت ها',
            },
        ),
        migrations.CreateModel(
            name='Polls',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('expiryTimestamp', models.DateField(verbose_name=' تاریخ  اتمام نظرسنجی')),
                ('endTime', models.CharField(default='24:00:00', max_length=8)),
                ('question', models.CharField(max_length=170, verbose_name='سوال نظر سنجی')),
                ('isActive', models.BooleanField(default=False, null=True)),
                ('choices', models.ManyToManyField(to='myapp.choice', verbose_name='گزینه ها')),
            ],
            options={
                'verbose_name': 'نظرسنجی',
                'verbose_name_plural': 'نظرسنجی ها',
            },
        ),
        migrations.CreateModel(
            name='Reply',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('replyText', models.TextField(verbose_name='متن پاسخ')),
                ('createdAt', models.DateTimeField(auto_now_add=True, verbose_name='زمان و تاریخ انتشار پاسخ')),
                ('likeCount', models.IntegerField(default=0, verbose_name='تعداد لایک')),
                ('commentId', models.ManyToManyField(related_name='replies_comment', to='myapp.comments', verbose_name='کامنت')),
                ('parentReplyId', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='replies', to='myapp.reply', verbose_name='پاسخ والد')),
                ('post', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='postreply', to='myapp.allposts', verbose_name='آیدی پست')),
                ('userId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_replies', to=settings.AUTH_USER_MODEL, verbose_name='آیدی کاربر')),
            ],
            options={
                'verbose_name': 'ریپلای',
                'verbose_name_plural': 'ریپلای ها',
            },
        ),
        migrations.CreateModel(
            name='ReplyLike',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('likeCount', models.IntegerField(default=0, verbose_name='تعداد لایک')),
                ('replyId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myapp.reply', verbose_name='آیدی کامنت')),
                ('userId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='آیدی کاربر')),
            ],
            options={
                'verbose_name': 'لایک های ریپلای',
                'verbose_name_plural': 'لایک های ریپلای',
            },
        ),
        migrations.CreateModel(
            name='ReplyLikeHistory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('liked_at', models.DateTimeField(auto_now_add=True)),
                ('reply', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myapp.reply')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'لایک ریپلای',
                'verbose_name_plural': 'لایک ریپلای ها',
            },
        ),
        migrations.CreateModel(
            name='ReplyReport',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('replyText', models.TextField()),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='post_reply_reports', to='myapp.allposts')),
                ('reply', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='report_of_reply', to='myapp.reply')),
                ('userId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_reply_reports', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'گزارش ریپلای',
                'verbose_name_plural': 'ریپلای های گزارش شده',
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
