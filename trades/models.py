from django.db import models

class Simulation(models.Model):
    symbol = models.CharField(max_length=10)
    start_date = models.DateField()
    end_date = models.DateField()
    html_time = models.CharField(max_length=20, blank=True, null=True)  # New field for html_time
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.symbol} from {self.start_date} to {self.end_date}"
