from django.http.response import HttpResponse
from django.views.decorators.cache import cache_page

from core.config import project_config

@cache_page(1)
def index(request):
    from django.conf import settings

    return HttpResponse("noise")