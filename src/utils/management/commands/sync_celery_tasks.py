from django.core.management import BaseCommand

from utils.celery import sync_django_celery_beat, collect_celery_beat_schedules


class Command(BaseCommand):
    def handle(self, *args, **options):
        related_name = "celery_beat"
        packages = (
            "utils",
        )
        beat_schedule = collect_celery_beat_schedules(related_name=related_name, packages=packages)
        sync_django_celery_beat(beat_schedule=beat_schedule)
