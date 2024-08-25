from django.urls import path
from .views import upload_video, success

urlpatterns = [
    path('upload/', upload_video, name='upload_video'),
    path('success/', success, name='success'),
]
