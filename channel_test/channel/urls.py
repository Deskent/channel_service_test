from django.urls import path
from channel.views import InfoView


urlpatterns = [
    path('', InfoView.as_view(), name='info'),
    path('info', InfoView.as_view(), name='info'),
]
