import importlib
from datetime import timedelta
from typing import Any, Sequence

from celery.schedules import crontab
from django_celery_beat.models import (
    PeriodicTask,
    IntervalSchedule,
    CrontabSchedule,
)

related_name = 'celery_beat'
packages = (
    'utils',
)


def collect_celery_beat_schedules(related_name: str, packages: Sequence[str]) -> dict[str, dict[str, Any]]:
    beat_schedules = {}
    for package in packages:
        module_to_import = f'{package}.{related_name}'
        try:
            module = importlib.import_module(module_to_import)
        except ModuleNotFoundError as e:
            continue

        schedule = getattr(module, 'schedule')
        for task_name, task_info in schedule.items():
            task_name = f'{package}-{task_name}'
            beat_schedules[task_name] = task_info
    return beat_schedules


def sync_django_celery_beat(beat_schedule: dict):
    PeriodicTask.objects.all().delete()

    for task_name, task_info in beat_schedule.items():
        task = task_info['task']
        schedule = task_info['schedule']

        crontab_schedule = None
        interval_schedule = None

        if isinstance(schedule, timedelta):
            seconds = schedule.total_seconds()
            if seconds % 60 == 0:
                minutes = seconds / 60
                interval_schedule, _ = (
                    IntervalSchedule.objects.get_or_create(
                        every=int(minutes),
                        period=IntervalSchedule.MINUTES,
                    )
                )
            else:
                interval_schedule, _ = (
                    IntervalSchedule.objects.get_or_create(
                        every=int(seconds),
                        period=IntervalSchedule.SECONDS,
                    )
                )
        elif isinstance(schedule, crontab):
            crontab_schedule, _ = CrontabSchedule.objects.get_or_create(
                minute=schedule.minute,
                hour=schedule.hour,
                day_of_week=schedule.day_of_week,
                day_of_month=schedule.day_of_month,
                month_of_year=schedule.month_of_year,
            )
        else:
            raise NotImplementedError(type(schedule))

        PeriodicTask.objects.create(
            name=task_name,
            task=task,
            interval=interval_schedule,
            crontab=crontab_schedule,
            enabled=True,
        )
