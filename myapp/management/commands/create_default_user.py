from django.core.management.base import BaseCommand
from django.contrib.auth.models import User


class Command(BaseCommand):
    help = "Create or reset the default user"

    def handle(self, *args, **kwargs):
        user, created = User.objects.get_or_create(
            username="ragavi"
        )

        user.set_password("ragavi@123")
        user.save()

        self.stdout.write(
            self.style.SUCCESS(
                "Default user ragavi is ready."
            )
        )