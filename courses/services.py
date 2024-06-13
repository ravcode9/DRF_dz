import json
from datetime import datetime, timedelta
from django_celery_beat.models import IntervalSchedule, PeriodicTask


def set_schedule(*args, **kwargs):
    schedule, created = IntervalSchedule.objects.get_or_create(
        every=2,
        period=IntervalSchedule.HOURS,
    )
    PeriodicTask.objects.create(
        interval=schedule,
        name='Importing contacts',
        task='proj.tasks.import_contacts',
        kwargs=json.dumps({
            'be_careful': True,
        }),
        expires=datetime.utcnow() + timedelta(seconds=30)
    )
