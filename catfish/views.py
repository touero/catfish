import os

from easierdocker import log
from django.core.cache import cache
from django.core.files.storage import FileSystemStorage
from django.http import FileResponse, HttpResponse, HttpResponseForbidden
from django.views import View
from django.shortcuts import render, redirect
from django.conf import settings
from django.http import Http404
from datetime import datetime


class ListFilesView(View):
    @staticmethod
    def get(request):
        media_path = os.path.join(settings.BASE_DIR, 'media')
        files = [f for f in os.listdir(media_path) if os.path.isfile(os.path.join(media_path, f))]
        sorted_files = sorted(files, key=lambda f: os.path.getmtime(os.path.join(media_path, f)), reverse=True)
        file_dict: dict = {}
        for file in sorted_files:
            file_dict[file] = datetime.fromtimestamp(os.path.getmtime(os.path.join(media_path, file))).strftime(
                "%Y-%m-%d %H:%M:%S")
        return render(request, 'download.html', {'file_dict': file_dict})


class DownloadFileView(View):
    @staticmethod
    def get(request, filename):
        file_path = os.path.join(settings.BASE_DIR, 'media', filename)

        client_ip = request.META.get('REMOTE_ADDR')
        cache_key = f'download_limit:{client_ip}:{filename}'

        download_count = cache.get(cache_key, 0)

        if download_count >= 3:
            error_message = "You have reached the file download limit and are unable to download this file."
            return HttpResponse(error_message, status=403)

        cache.set(cache_key, download_count + 1, 60)

        if os.path.exists(file_path):
            response = FileResponse(open(file_path, 'rb'))
            response['Content-Disposition'] = f'attachment; filename="{filename}"'
            response['Content-Type'] = 'application/octet-stream'
            return response
        else:
            raise Http404


class UploadFileView(View):
    AUTHORIZATION_CODE = ['223366']

    @staticmethod
    def post(request):
        if request.POST.get('authorization_code') not in UploadFileView.AUTHORIZATION_CODE:
            return HttpResponseForbidden("Forbidden: Invalid Authorization Code")

        if not request.FILES.get('file'):
            return HttpResponseForbidden("Forbidden: Invalid file")

        if request.FILES['file']:
            uploaded_file = request.FILES['file']
            fs = FileSystemStorage()
            log(uploaded_file.name)
            fs.save(uploaded_file.name, uploaded_file)
            return redirect('list_files')

        return render(request, 'download.html')
