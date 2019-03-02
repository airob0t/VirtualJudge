from django.core.management.base import BaseCommand
from django.db import connection
from django.db.utils import OperationalError
from user.models import User


class Command(BaseCommand):
    def handle(self, *args, **options):
        try:
            connection.cursor()
        except OperationalError:
            self.stdout.write(self.style.WARNING('waiting database connect'))
            exit(1)
        username = 'root'
        email = 'root@vjudge.top'
        password = 'rootroot'
        if User.objects.filter(username=username).exists():
            self.stdout.write(self.style.WARNING('Due to the existence of this account, no new account was created'))
        else:
            user = User.objects.create_superuser(username=username, email=email, password=password)
            user.save()