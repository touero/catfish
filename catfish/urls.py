# your_app/urls.py

from django.urls import path
from .views import ListFilesView, DownloadFileView, UploadFileView

urlpatterns = [
    path('', ListFilesView.as_view(), name='list_files'),
    path('download/<str:filename>/', DownloadFileView.as_view(), name='download_file'),
    path('upload/', UploadFileView.as_view(), name='upload_file'),
]
