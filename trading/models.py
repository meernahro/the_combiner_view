# models.py in the trading app

from django.db import models

class AutomationRule(models.Model):
    STATUS_CHOICES = [
        ('enabled', 'Enabled'),
        ('disabled', 'Disabled'),
    ]

    
    exchanges = models.JSONField()  # List of exchanges
    market_type = models.CharField(max_length=10, choices=[('spot', 'Spot'), ('future', 'Future'), ('both', 'Both')])
    account = models.CharField(max_length=255)  # Account ID or details
    amount_usdt = models.FloatField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='enabled')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Rule {self.id} - {self.status}"

