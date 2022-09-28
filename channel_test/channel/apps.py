from django.apps import AppConfig
from django.conf import settings

from apscheduler.schedulers.background import BackgroundScheduler

from channel.utils.utils import parse
from config import settings


class ChannelTestConfig(AppConfig):
    name = 'channel'
    verbose_name = 'Каналсервис'

    def ready(self):
        scheduler = BackgroundScheduler()
        scheduler.add_job(
            func=parse,
            args=(settings.GOOGLE_TOKEN_FILEPATH, ),
            trigger='interval',
            seconds=settings.UPDATE_INTERVAL_SECONDS)
        scheduler.start()
