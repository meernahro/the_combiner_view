from django.views import View
from django.shortcuts import render, redirect
from django.contrib import messages
from channels.views import ChannelManagementView

class DashboardView(View):
    def __init__(self):
        self.channel_view = ChannelManagementView()

    def get(self, request):
        try:
            channels = self.channel_view.classifier_api.get_all_channels()
        except Exception:
            channels = []
        
        context = {
            'channels': channels
        }
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

        return redirect('dashboard')
