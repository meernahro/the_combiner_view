from django.views.generic import TemplateView
from channels.views import ChannelManagementView

class DashboardView(TemplateView):
    template_name = 'dashboard/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Get channel data
        channel_view = ChannelManagementView()
        try:
            channels = channel_view.classifier_api.get_all_channels()
        except Exception:
            channels = []
        
        context['channels'] = channels
        return context
