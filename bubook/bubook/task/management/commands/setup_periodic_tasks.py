from django.core.management.base import BaseCommand
from django.utils.timezone import get_default_timezone_name

from django_celery_beat.models import IntervalSchedule, CrontabSchedule, PeriodicTask

from bubook.users.tasks import backup_otps_to_db_task


class Command(BaseCommand):
    help = '''
    help
    '''

    def handle(self, *args, **options):
        print('deleting all periodic tasks and schedules...\n')
        IntervalSchedule.objects.all().delete()
        CrontabSchedule.objects.all().delete()
        PeriodicTask.objects.all().delete()

        periodic_tasks = [
            {
                'task': backup_otps_to_db_task,
                'name': 'backup_otps_to_db_task',
                'cron': {
                    'minute': '*',
                    'hour': '*',
                    'day_of_week': '*',
                    'day_of_month': '*',
                    'month_of_year': '*',
                },
                'enabled': True,
            },
        ]

        timezone = get_default_timezone_name()

        for periodic_task in periodic_tasks:
            print(f'setting up {periodic_task["task"].name}')
            cron = CrontabSchedule.objects.create(timezone=timezone, **periodic_task['cron'])
            PeriodicTask.objects.create(
                name=periodic_task['name'],
                task=periodic_task['task'].name,
                crontab=cron,
                enabled=periodic_task['enabled'],
            )
