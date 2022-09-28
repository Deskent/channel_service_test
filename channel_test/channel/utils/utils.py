from datetime import datetime

import requests

from channel.utils.sheets_parser import SheetsParser
from config import settings


def update_orders(token_filepath: str):
    """Get data from Google, send messages with expired orders,
    Update DB"""

    parser = SheetsParser(
        currency='USD',
        google_token_filename=token_filepath
    )
    orders: list[dict] = parser.get_data()
    expired_orders: tuple[str] = _get_expired_orders(orders)
    _send_report(expired_orders)
    _update_database(orders)


def _update_database(orders: list[dict]):
    from channel.models import ChannelOrder

    fields: list[int] = [elem['order_number'] for elem in orders]
    orders: list[ChannelOrder] = [ChannelOrder(**elem) for elem in orders]
    ChannelOrder.objects.bulk_create(
        objs=orders,
        update_conflicts=True,
        update_fields=['usd_cost', 'rubles_cost', 'serial_number', 'transfer_date'],
        unique_fields=['order_number']
    )
    ChannelOrder.objects.exclude(order_number__in=fields).delete()


def _get_expired_orders(orders: list[dict]) -> tuple[str]:
    """Returns tuple of expired order numbers"""

    return tuple(
        str(order['order_number'])
        for order in orders
        if datetime.strptime(order['transfer_date'], '%Y-%m-%d') < datetime.now()
    )


def send_message_to_user(bot_token: str, telegram_id: int, text: str) -> None:
    """
    Sends the message to user telegram id using bot token
    """

    url: str = f"https://api.telegram.org/bot{bot_token}/sendMessage?chat_id={telegram_id}&text={text}"
    requests.get(url, timeout=5)


def _send_report(orders: tuple[str], step: int = 30) -> None:
    """Send messages divided by step parts"""

    length: int = len(orders)
    for shift in range(0, length, step):
        orders_slice: tuple[str] = orders[shift:shift + step]
        order_string: str = '\n'.join(orders_slice)
        text = f'Expired orders: \n{order_string}'
        send_message_to_user(
            bot_token=settings.TELEBOT_TOKEN,
            telegram_id=settings.ADMIN_TELEGRAM_ID,
            text=text
        )
