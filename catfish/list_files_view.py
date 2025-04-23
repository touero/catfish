import logging

from pathlib import Path

from django.views import View
from django.shortcuts import render
from django.conf import settings
from datetime import datetime


logger = logging.getLogger(__name__)


class ListFilesView(View):
    @staticmethod
    def get(request):
        show_dir = Path(settings.SHOW_DIR)
        file_data = []

        for path in show_dir.rglob('*'):
            if path.is_file():
                relative_path = path.relative_to(show_dir).as_posix()
                file_stat = path.stat()
                file_mtime = file_stat.st_mtime
                mod_time_str = datetime.fromtimestamp(file_mtime).strftime("%Y-%m-%d %H:%M:%S")
                file_data.append((relative_path, mod_time_str, file_mtime))

        sorted_file_dict = {
            rel: mod for rel, mod, _ in sorted(file_data, key=lambda item: item[2], reverse=True)
        }

        return render(request, 'index.html', {'file_dict': sorted_file_dict})
