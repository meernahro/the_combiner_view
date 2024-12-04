from django.shortcuts import render
from the_combiner_view.api_utils import ClassifierExternalApis

# Create your views here.

class ExchangeManagementView:
    def __init__(self):
        self.classifier_api = ClassifierExternalApis()
