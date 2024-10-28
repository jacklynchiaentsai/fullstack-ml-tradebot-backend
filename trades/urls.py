from django.urls import path
from .views import RunTradeBotView, SimulationListView, GetSimulationDataView

urlpatterns = [
    path('run-trade-bot/', RunTradeBotView.as_view(), name='run-trade-bot'),
    path('simulations/', SimulationListView.as_view(), name='simulation-list'),
    path('get-simulation-data/', GetSimulationDataView.as_view(), name='get-simulation-data'), 
]
