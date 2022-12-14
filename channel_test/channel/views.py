from django.views import generic
from channel.models import ChannelOrder


class InfoView(generic.ListView):
    queryset = ChannelOrder.objects.order_by('serial_number')
    template_name = 'channel_test/info.html'
    context_object_name = 'data'
    extra_context = {'title': 'Информация'}
