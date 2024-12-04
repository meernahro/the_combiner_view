from django.shortcuts import render
from django.http import HttpResponse
from django.template.loader import render_to_string
from the_combiner_view.views import ChannelManagementView

# Create your views here.

def get_latest_tokens(request):
    channel_view = ChannelManagementView()
    try:
        latest_tokens = channel_view.classifier_api.get_latest_tokens(limit=10)
       
    except Exception as e:
        print(f"Error getting latest tokens: {e}")
        latest_tokens = []

    html = render_to_string('latest_tokens/latest_tokens_content.html', 
                          {'latest_tokens': latest_tokens})
    return HttpResponse(html)
