from datetime import timedelta


schedule = {
    'health_check': {
        'task': 'utils.celery_tasks.health_check',
        'schedule': timedelta(minutes=1),
    },
}
