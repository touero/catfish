import logging
import urllib.parse

from pathlib import Path

from django.core.files.storage import FileSystemStorage
from django.http import FileResponse, HttpResponseForbidden
from django.views import View
from django.shortcuts import render, redirect
from django.conf import settings
from django.http import Http404
from datetime import datetime


logger = logging.getLogger(__name__)


class ListFilesView(View):
    @staticmethod
    def get(request):
        show_dir = Path(settings.SHOW_DIR)
        file_dict = {}

        for path in show_dir.rglob('*'):
            if path.is_file():
                relative_path = path.relative_to(show_dir).as_posix()
                mod_time = datetime.fromtimestamp(path.stat().st_mtime).strftime("%Y-%m-%d %H:%M:%S")
                file_dict[relative_path] = mod_time

        sorted_file_dict = dict(sorted(file_dict.items(), key=lambda item: (show_dir / item[0]).stat().st_mtime, reverse=True))

        return render(request, 'index.html', {'file_dict': sorted_file_dict})


class DownloadFileView(View):
    @staticmethod
    def get(request, filename):
        filename = filename.rstrip('/')
        decoded_filename = urllib.parse.unquote(filename)
        logger.info(f"will download file: {decoded_filename}")

        safe_base = Path(settings.SHOW_DIR).resolve()
        requested_path = (safe_base / decoded_filename).resolve()

        if not str(requested_path).startswith(str(safe_base)):
            raise Http404("Invalid file path.")

        if requested_path.exists() and requested_path.is_file():
            response = FileResponse(open(requested_path, 'rb'))
            response['Content-Disposition'] = f'attachment; filename="{requested_path.name}"'
            response['Content-Type'] = 'application/octet-stream'
            return response
        else:
            raise Http404("File not found.")


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
            logger.info(uploaded_file.name)
            fs.save(uploaded_file.name, uploaded_file)
            return redirect('list_files')

        return render(request, 'index.html')
