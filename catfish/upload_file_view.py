import logging
from django.shortcuts import redirect
from django.http import Http404, HttpResponseNotAllowed
from django.contrib import messages
from django.views import View
from django.conf import settings
from django.core.files.storage import default_storage
from pathlib import Path

from .models import File


logger = logging.getLogger(__name__)

class UploadFileView(View):
    def post(self, request):
        upload_file = request.FILES.get('file')
        description = request.POST.get('description', '').strip()

        if not upload_file:
            messages.error(request, "请选择要上传的文件")
            raise Http404("文件不存在")

        save_dir = Path(settings.MEDIA_ROOT).resolve()
        save_dir.mkdir(parents=True, exist_ok=True)
        save_path = save_dir / upload_file.name
        if not str(save_path).startswith(str(save_dir)):
            logger.error(f"文件路径超出预期范围: {save_path}")
            messages.error(request, "文件路径无效，上传失败")
            raise Http404("文件路径无效，上传失败")

        try:
            with default_storage.open(str(save_path), 'wb+') as destination:
                for chunk in upload_file.chunks():
                    destination.write(chunk)
            
            file_record = File(name=upload_file.name, uploaded_by=request.user, description=description)
            file_record.save()
            
            logger.info(f"用户 {request.user.username} 上传文件: {upload_file.name}，描述: {description}")
            messages.success(request, f"文件 {upload_file.name} 上传成功！")
        except Exception as e:
            logger.error(f"上传文件失败: {e}")
            messages.error(request, "文件上传失败，请稍后再试。")

        return redirect('list_files')

