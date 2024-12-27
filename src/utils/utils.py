import os
from datetime import datetime

import psutil
import time


def bytes_to_gigabytes(bytes, decimals=2):
    """Convert bytes to gigabytes and round to specified decimals."""
    gigabytes = bytes / 1024 / 1024 / 1024
    return round(gigabytes, decimals)


def seconds_to_hours(seconds, decimals=2):
    hours = round(seconds / 3600, decimals)
    return hours


def hours_to_days(hours, decimals=2):
    days = round(hours / 24, decimals)
    return days


def get_system_stats():

    boot_time_epoch = psutil.boot_time()
    boot_datetime = datetime.fromtimestamp(boot_time_epoch)
    system_uptime_seconds = round(time.time() - boot_time_epoch, 2)
    system_uptime_hours = seconds_to_hours(system_uptime_seconds, 2)
    system_uptime_days = hours_to_days(system_uptime_hours, 2)

    cpu_usage = psutil.cpu_percent(interval=1)
    cpu_frequency = psutil.cpu_freq()
    cpu_times = psutil.cpu_times()

    # Memory metrics
    memory = psutil.virtual_memory()
    swap = psutil.swap_memory()

    # Disk metrics
    disk_usage = psutil.disk_usage('/')
    disk_io = psutil.disk_io_counters()

    # Network metrics
    net_io = psutil.net_io_counters()
    # net_connections = len(psutil.net_connections())

    return {
        'cpu': {
        'usage_percent': cpu_usage,
        'frequency_current': getattr(cpu_frequency, 'current', None),
        'system_time': cpu_times.system,
        'user_time': cpu_times.user,
        'idle_time': cpu_times.idle,
        'cores_physical': psutil.cpu_count(logical=False),
        'cores_logical': psutil.cpu_count(logical=True),
        },
        'memory': {
            'total_gb': bytes_to_gigabytes(memory.total),
            'used_gb': bytes_to_gigabytes(memory.used),
            'free_gb': bytes_to_gigabytes(memory.free),
            'percent_used': memory.percent,
        },
        'swap': {
            'total_gb': bytes_to_gigabytes(swap.total),
            'used_gb': bytes_to_gigabytes(swap.used),
            'free_gb': bytes_to_gigabytes(swap.free),
            'percent_used': swap.percent,
        },
        'disk': {
            'total_gb': bytes_to_gigabytes(disk_usage.total),
            'used_gb': bytes_to_gigabytes(disk_usage.used),
            'free_gb': bytes_to_gigabytes(disk_usage.free),
            'percent_used': disk_usage.percent,
            'read_count': disk_io.read_count,
            'write_count': disk_io.write_count,
        },
        'network': {
            'bytes_sent': net_io.bytes_sent,
            'bytes_received': net_io.bytes_recv,
            # 'current_connections': net_connections

            'gb_sent': bytes_to_gigabytes(net_io.bytes_sent),
            'gb_received': bytes_to_gigabytes(net_io.bytes_recv),
        },
        'os_info': {
            'boot_datetime': str(boot_datetime),
            'platform': os.name,
            'system_uptime_days': system_uptime_days,
            'system_uptime_hours': system_uptime_hours,
            'system_uptime_seconds': system_uptime_seconds,
            'system': os.uname().sysname,
            'release': os.uname().release,
        },
    }
