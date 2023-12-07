import time
from easierdocker import log
from django.http import HttpResponseForbidden


class CatfishMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.requests = {}

    def __call__(self, request):
        user_agent = request.META.get('HTTP_USER_AGENT', '').lower()
        ip_address = request.META.get('REMOTE_ADDR')
        log(f'[{ip_address}]: {user_agent}')
        response = self.get_response(request)
        if request.method != 'GET':
            return response
        if 'mozilla' not in user_agent:
            return HttpResponseForbidden("Forbidden: Bad User-Agent")
        if ip_address in self.requests:
            last_request_time = self.requests[ip_address]
            elapsed_time = time.time() - last_request_time
            if elapsed_time < 2:
                return HttpResponseForbidden("Forbidden: Too many requests from this IP")
        self.requests[ip_address] = time.time()
        return response
