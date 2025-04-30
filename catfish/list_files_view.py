import logging
from datetime import datetime
from django.shortcuts import render
from django.conf import settings
from pathlib import Path
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.views import View
from django.utils.decorators import method_decorator

from .models import File

logger = logging.getLogger(__name__)

@method_decorator(login_required, name='dispatch')
class ListFilesView(View):
    @staticmethod
    def get(request):
        show_dir = Path(settings.MEDIA_ROOT)
        file_dict = {}

        for path in show_dir.rglob('*'):
            if path.is_file():
                relative_path = path.relative_to(show_dir).as_posix()
                file_info = File.objects.filter(name=relative_path).first()
                mod_time = datetime.fromtimestamp(path.stat().st_mtime).strftime("%Y-%m-%d %H:%M:%S")

                if file_info:
                    local_time = timezone.localtime(file_info.uploaded_at)
                    file_dict[relative_path] = {
                        'description': file_info.description,
                        'uploaded_by': file_info.uploaded_by,
                        'uploaded_at': local_time.strftime("%Y-%m-%d %H:%M:%S"),
                    }
                else:
                    file_dict[relative_path] = {
                        'description': "description is null",
                        'uploaded_by': "MEDIA_ROOT dir",
                        'uploaded_at': mod_time,
                    }

        sorted_file_dict = dict(sorted(file_dict.items(), key=lambda item: (show_dir / item[0]).stat().st_mtime, reverse=True))

        can_delete = request.user.has_perm("catfish.can_delete_file")
        return render(request, 'index.html', {'file_dict': sorted_file_dict, 'can_delete': can_delete})
