from django.contrib import admin
from .models import AutomationRule

@admin.register(AutomationRule)
class AutomationRuleAdmin(admin.ModelAdmin):
    list_display = ('id', 'status', 'market_type', 'account', 'amount_usdt', 'created_at', 'updated_at')
    list_filter = ('status', 'market_type')
    search_fields = ('account',)
