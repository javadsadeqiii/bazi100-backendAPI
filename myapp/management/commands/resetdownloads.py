from django.core.management.base import BaseCommand
from django.utils import timezone
from myapp.models import CustomUser



#class Command(BaseCommand):

  #  def handle(self, *args, **options):
    #    thirty_days_ago = timezone.now() - timezone.timedelta(days=30)
    #    users_to_reset = CustomUser.objects.filter(last_download_date__lte=thirty_days_ago)

    #    for user in users_to_reset:
    #        user.downloads = 5  
    #        user.save()

   #     self.stdout.write(self.style.SUCCESS('تعداد دانلودهای مجاز با موفقیت بروزرسانی شد'))
        