from django.db import models


class ChannelOrder(models.Model):
    serial_number = models.IntegerField(verbose_name='Порядковый номер')
    order_number = models.IntegerField(verbose_name='Номер заказа', unique=True)
    usd_cost = models.DecimalField(max_digits=100, decimal_places=2, verbose_name='Стоимость,$')
    rubles_cost = models.DecimalField(max_digits=100, decimal_places=2, verbose_name='Стоимость,руб')
    transfer_date = models.DateField(verbose_name='Дата поставки')

    class Meta:
        db_table = 'channel_orders'
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'
