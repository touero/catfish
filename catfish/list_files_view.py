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
        file_dict = {}

        for path in show_dir.rglob('*'):
            if path.is_file():
                relative_path = path.relative_to(show_dir).as_posix()
                mod_time = datetime.fromtimestamp(path.stat().st_mtime).strftime("%Y-%m-%d %H:%M:%S")
                file_dict[relative_path] = mod_time

        sorted_file_dict = dict(sorted(file_dict.items(), key=lambda item: (show_dir / item[0]).stat().st_mtime, reverse=True))

        return render(request, 'index.html', {'file_dict': sorted_file_dict})
