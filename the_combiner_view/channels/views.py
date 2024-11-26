from django.shortcuts import render, redirect
from django.contrib import messages
from django.views import View
from the_combiner_view.api_utils import ClassifierExternalApis

class ChannelManagementView(View):
    def __init__(self):
        self.classifier_api = ClassifierExternalApis()

    def get(self, request):
        try:
            channels = self.classifier_api.get_all_channels()
            return render(request, 'channels/channel_list.html', {'channels': channels})
        except Exception as e:
            messages.error(request, f"Error fetching channels: {str(e)}")
            return render(request, 'channels/channel_list.html', {'channels': []})

    def post(self, request):
        action = request.POST.get('action')
        
        if action == 'add':
            channel_data = {
                'name': request.POST.get('channel_name'),
            }
            try:
                self.classifier_api.add_channel(channel_data)
                messages.success(request, "Channel added successfully!")
            except Exception as e:
                messages.error(request, f"Error adding channel: {str(e)}")

        elif action == 'delete':
            channel_id = request.POST.get('channel_id')
            try:
                self.classifier_api.delete_channel(int(channel_id))
                messages.success(request, "Channel unfollowed successfully!")
            except Exception as e:
                messages.error(request, f"Error unfollowing channel: {str(e)}")

        return redirect('channel-management')
