from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView


@api_view(["GET"])
def hello_world(request):
    return Response({"message": "Hello, world!", "app": "UNITECA"})


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'core/dashboard.html'