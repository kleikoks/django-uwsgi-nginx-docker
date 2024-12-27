from core.celery import app
from utils.utils import get_system_stats


@app.task
def health_check():
    system_stats = get_system_stats()
    return system_stats
