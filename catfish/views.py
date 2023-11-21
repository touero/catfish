import os
import urllib.parse

from django.core.cache import cache
from django.http import FileResponse, HttpResponse
from django.views import View
from django.shortcuts import render, redirect
from django.conf import settings
from django.http import Http404


class ListFilesView(View):
    @staticmethod
    def get(request):
        media_path = os.path.join(settings.BASE_DIR, 'media')
        file_list = sorted(
            [f for f in os.listdir(media_path) if os.path.isfile(os.path.join(media_path, f))],
            key=lambda f: os.path.getmtime(os.path.join(media_path, f)),
            reverse=True
        )

        print("File List:", file_list)  # 添加这一行来打印文件列表

        return render(request, 'download.html', {'file_list': file_list})



class DownloadFileView(View):
    @staticmethod
    def get(request, filename):
        file_path = os.path.join(settings.BASE_DIR, 'media', filename)

        # Define a cache key for this user and file using IP address
        client_ip = request.META.get('REMOTE_ADDR')
        cache_key = f'download_limit:{client_ip}:{filename}'

        # Get the current download count from cache, default to 0
        download_count = cache.get(cache_key, 0)

        # Check if the user has exceeded the download limit
        if download_count >= 3:
            ...

        # Increment the download count and update the cache
        cache.set(cache_key, download_count + 1, 60)  # Cache expires in 60 seconds

        # Serve the file
        if os.path.exists(file_path):
            response = FileResponse(open(file_path, 'rb'))
            response['Content-Disposition'] = f'attachment; filename="{filename}"'
            response['Content-Type'] = 'application/octet-stream'
            return response
        else:
            raise Http404
