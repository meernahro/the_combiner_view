from django.views import View
from django.shortcuts import render, redirect
from django.contrib import messages
from channels.views import ChannelManagementView
from exchanges.views import ExchangeManagementView

class DashboardView(View):
    def __init__(self):
        self.channel_view = ChannelManagementView()
        self.exchange_view = ExchangeManagementView()

    def get(self, request):
        context = {}
        
        # Get channels
        try:
            channels = self.channel_view.classifier_api.get_all_channels()
        except Exception:
            channels = []
        
        # Get exchanges
        try:
            exchanges = self.exchange_view.classifier_api.get_all_exchanges()
        except Exception:
            exchanges = []
        
        # Get latest tokens
        try:
            latest_tokens = self.channel_view.classifier_api.get_latest_tokens(limit=10)
        except Exception:
            latest_tokens = []
        
        context.update({
            'channels': channels,
            'exchanges': exchanges,
            'latest_tokens': latest_tokens
        })
        
        return render(request, 'dashboard/dashboard.html', context)

    def post(self, request):
        action = request.POST.get('action')
        
        if action == 'add':
            channel_data = {
                'name': request.POST.get('channel_name'),
            }
            try:
                self.channel_view.classifier_api.add_channel(channel_data)
                messages.success(request, "Channel added successfully!")
            except Exception as e:
                messages.error(request, f"Error adding channel: {str(e)}")

        elif action == 'delete':
            channel_id = request.POST.get('channel_id')
            try:
                self.channel_view.classifier_api.delete_channel(int(channel_id))
                messages.success(request, "Channel unfollowed successfully!")
            except Exception as e:
                messages.error(request, f"Error unfollowing channel: {str(e)}")

        elif action == 'add_exchange':
            exchange_data = {
                'name': request.POST.get('exchange_name'),
            }
            try:
                self.exchange_view.classifier_api.add_exchange(exchange_data)
                messages.success(request, "Exchange added successfully!")
            except Exception as e:
                messages.error(request, f"Error adding exchange: {str(e)}")

        elif action == 'delete_exchange':
            exchange_id = request.POST.get('exchange_id')
            try:
                self.exchange_view.classifier_api.delete_exchange(int(exchange_id))
                messages.success(request, "Exchange deleted successfully!")
            except Exception as e:
                messages.error(request, f"Error deleting exchange: {str(e)}")

        return redirect('dashboard')
