from django.views import View
from django.shortcuts import render, redirect
from django.contrib import messages
from channel_management.views import ChannelManagementView
from exchanges.views import ExchangeManagementView
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.http import HttpResponse
from django.template.context_processors import csrf
from django.template.context import RequestContext

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
        is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
        
        try:
            if action == 'add':
                channel_data = {
                    'name': request.POST.get('channel_name'),
                }
                self.channel_view.classifier_api.add_channel(channel_data)
                if is_ajax:
                    return JsonResponse({'success': True})
                messages.success(request, "Channel added successfully!")

            elif action == 'delete':
                channel_id = request.POST.get('channel_id')
                self.channel_view.classifier_api.delete_channel(int(channel_id))
                if is_ajax:
                    return JsonResponse({'success': True})
                messages.success(request, "Channel deleted successfully!")

            elif action == 'add_exchange':
                exchange_data = {
                    'name': request.POST.get('exchange_name'),
                }
                self.exchange_view.classifier_api.add_exchange(exchange_data)
                if is_ajax:
                    return JsonResponse({'success': True})
                messages.success(request, "Exchange added successfully!")

            elif action == 'delete_exchange':
                exchange_id = request.POST.get('exchange_id')
                self.exchange_view.classifier_api.delete_exchange(int(exchange_id))
                if is_ajax:
                    return JsonResponse({'success': True})
                messages.success(request, "Exchange deleted successfully!")

        except Exception as e:
            if is_ajax:
                return JsonResponse({'success': False, 'error': str(e)})
            messages.error(request, f"Error: {str(e)}")

        if is_ajax:
            return JsonResponse({'success': False})
        return redirect('dashboard')

def get_exchanges(request):
    exchange_view = ExchangeManagementView()
    try:
        exchanges = exchange_view.classifier_api.get_all_exchanges()
    except Exception:
        exchanges = []
    
    context = {'exchanges': exchanges}
    context.update(csrf(request))
    
    html = render_to_string('exchanges/exchange_list_content.html', 
                          context,
                          request=request)
    return HttpResponse(html)

def get_channels(request):
    channel_view = ChannelManagementView()
    try:
        channels = channel_view.classifier_api.get_all_channels()
    except Exception:
        channels = []
    
    context = {'channels': channels}
    context.update(csrf(request))
    
    html = render_to_string('channel_management/channel_list_content.html', 
                          context,
                          request=request)
    return HttpResponse(html)
