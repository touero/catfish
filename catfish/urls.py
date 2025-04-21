# your_app/urls.py

from django.urls import path
from .list_files_view import ListFilesView
from .delete_file_view import DeleteFileView
from .download_file_view import DownloadFileView

urlpatterns = [
    path('', ListFilesView.as_view(), name='list_files'),
    path('delete/<path:filename>/', DeleteFileView.as_view(), name='delete_file'),
    path('download/<path:filename>', DownloadFileView.as_view(), name='download_file'),
]
