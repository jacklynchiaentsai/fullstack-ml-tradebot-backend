from django.urls import path
from .views import RunTradeBotView

urlpatterns = [
    path('run-trade-bot/', RunTradeBotView.as_view(), name='run-trade-bot'),
]
