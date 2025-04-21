# your_app/urls.py

from django.urls import path
from .views import ListFilesView, DownloadFileView, UploadFileView, DeleteFileView

urlpatterns = [
    path('', ListFilesView.as_view(), name='list_files'),
    path('delete/<path:filename>/', DeleteFileView.as_view(), name='delete_file'),
    path('download/<path:filename>', DownloadFileView.as_view(), name='download_file'),
    path('upload/', UploadFileView.as_view(), name='upload_file'),
]
