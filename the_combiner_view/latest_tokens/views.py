from django.shortcuts import render
from django.http import HttpResponse
from django.template.loader import render_to_string

# Create your views here.

def get_latest_tokens(request):
    try:
        latest_tokens = request.channel_view.classifier_api.get_latest_tokens(limit=10)
    except Exception:
        latest_tokens = []

    html = render_to_string('latest_tokens/latest_tokens_partial.html', {'latest_tokens': latest_tokens})
    return HttpResponse(html)
