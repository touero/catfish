from django.http import Http404
from django.shortcuts import redirect
from pathlib import Path
import urllib.parse
import logging
from django.conf import settings
from django.views import View
from django.contrib import messages
from .models import File

logger = logging.getLogger(__name__)

class DeleteFileView(View):
    permission_required = 'catfish.can_delete_file'

    def post(self, request, filename):
        decoded_filename = urllib.parse.unquote(filename)
        logger.info(f"Attempting to delete file: {decoded_filename}")

        safe_base = Path(settings.MEDIA_ROOT).resolve()
        requested_path = (safe_base / decoded_filename).resolve()

        if not str(requested_path).startswith(str(safe_base)) or not requested_path.exists():
            raise Http404("Invalid file path.")

        try:
            file_record = File.objects.filter(name=decoded_filename).first()
            if file_record:
                file_record.delete()
                logger.info(f"Deleted file record from database: {decoded_filename}")
            else:
                logger.warning(f"No database record found for file: {decoded_filename}")
            
            requested_path.unlink()
            logger.info(f"Deleted file from storage: {decoded_filename}")
            
            messages.success(request, f"文件 {decoded_filename} 删除成功！")
        except Exception as e:
            logger.error(f"Error deleting file: {e}")
            messages.error(request, "文件删除失败，请稍后再试。")

        return redirect('list_files')
