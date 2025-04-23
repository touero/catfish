import logging
import time
from django.http import HttpResponseForbidden

logger = logging.getLogger(__name__)


class CatfishMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.requests = {}

    def __call__(self, request):
        user_agent = request.META.get('HTTP_USER_AGENT', '').lower()
        ip_address = request.META.get('REMOTE_ADDR')

        logger.info(f'[{ip_address}]: {user_agent}')

        if request.method != 'GET':
            return self.get_response(request)

        if 'mozilla' not in user_agent:
            return HttpResponseForbidden("Forbidden: Bad User-Agent")

        response = self.get_response(request)
        return response
