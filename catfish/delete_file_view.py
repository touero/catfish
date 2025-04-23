import logging
import urllib.parse
from pathlib import Path

from django.conf import settings
from django.views import View
from django.http import Http404
from django.shortcuts import redirect


logger = logging.getLogger(__name__)


class DeleteFileView(View):
    def post(self, request, filename):
        decoded_filename = urllib.parse.unquote(filename)
        logger.info(f"will delete file: {decoded_filename}")

        safe_base = Path(settings.SHOW_DIR).resolve()
        requested_path = (safe_base / decoded_filename).resolve()

        if not str(requested_path).startswith(str(safe_base)) or not requested_path.exists():
            raise Http404("Invalid file path.")
        try:
            requested_path.unlink()
            return redirect('list_files')
        except OSError as error:
            logger.exception("删除文件失败: %s", requested_path, exc_info=error)
            raise Http404("Invalid file path.")

