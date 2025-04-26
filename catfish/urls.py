from django.urls import path
from django.contrib.auth.views import LogoutView
from django.contrib import admin


from .list_files_view import ListFilesView
from .delete_file_view import DeleteFileView
from .download_file_view import DownloadFileView
from .login_view import LoginView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('', ListFilesView.as_view(), name='list_files'),
    path('delete/<path:filename>/', DeleteFileView.as_view(), name='delete_file'),
    path('download/<path:filename>', DownloadFileView.as_view(), name='download_file'),
]
