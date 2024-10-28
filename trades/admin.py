from django.contrib import admin
from .models import Simulation

@admin.register(Simulation)
class SimulationAdmin(admin.ModelAdmin):
    list_display = ('symbol', 'start_date', 'end_date', 'html_time', 'created_at')
