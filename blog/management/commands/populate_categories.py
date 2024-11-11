from typing import Any
from blog.models import category
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    def handle(self, *args: Any, **options: Any):
        category.objects.all().delete()
        categories=["sports","health","education","transport","cinema"]
        for categoryy in categories:
            category.objects.create(category_title = categoryy)
        

        self.stdout.write(self.style.SUCCESS("Completed inserting Data!"))