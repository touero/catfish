import logging
import urllib.parse
from pathlib import Path

from django.conf import settings
from django.views import View
from django.http import Http404, FileResponse

logger = logging.getLogger(__name__)

class DownloadFileView(View):
    @staticmethod
    def get(request, filename):
        filename = filename.rstrip('/')
        decoded_filename = urllib.parse.unquote(filename)
        logger.info(f"will download file: {decoded_filename}")

        safe_base = Path(settings.MEDIA_ROOT).resolve()
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

