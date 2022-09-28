from pathlib import Path

from django.apps import AppConfig

from apscheduler.schedulers.background import BackgroundScheduler

from channel.utils.utils import update_orders
from config import settings


class ChannelTestConfig(AppConfig):
    name = 'channel'
    verbose_name = 'Каналсервис'

    def ready(self) -> None:
        """Run scheduler for updating data from Google sheet.
        Interval set in .env file"""

        scheduler = BackgroundScheduler()
        google_token_filepath: str = settings.GOOGLE_TOKEN_FILENAME
        if not Path(google_token_filepath).exists():
            google_token_filepath: str = Path().cwd().parent / settings.GOOGLE_TOKEN_FILENAME
        scheduler.add_job(
            func=update_orders,
            args=(google_token_filepath, ),
            trigger='interval',
            seconds=settings.UPDATE_INTERVAL_SECONDS)
        scheduler.start()
