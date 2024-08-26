from django.urls import path
from . import views

urlpatterns = [
    # path('upload/', upload_video, name='upload_video'),
    # path('success/', success, name='success'),
    path('', views.upload_video, name='upload_video'),
]
