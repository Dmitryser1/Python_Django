#import boto3
from django.conf import settings
from django.shortcuts import render, redirect
from .forms import VideoUploadForm
from .models import Video
from django.core.files.storage import FileSystemStorage

def upload_video(request):
    if request.method == 'POST':
        form = VideoUploadForm(request.POST, request.FILES)
        if form.is_valid():
            video_file = form.cleaned_data['video_file']
            fs = FileSystemStorage()
            filename = fs.save(video_file.name, video_file)
            uploaded_file_url = fs.url(filename)
            return render(request, 'upload.html', {'form': form, 'uploaded_file_url': uploaded_file_url})
    else:
        form = VideoUploadForm()
    return render(request, 'upload.html', {'form': form})


# def upload_video(request):
#     if request.method == 'POST':
#         form = VideoUploadForm(request.POST, request.FILES)
#         if form.is_valid():
#             video = form.save()

#             # Загрузка файла на Yandex Cloud
#             session = boto3.session.Session()
#             s3 = session.client(
#                 service_name='s3',
#                 endpoint_url=settings.YANDEX_CLOUD['ENDPOINT_URL'],
#                 aws_access_key_id=settings.YANDEX_CLOUD['ACCESS_KEY'],
#                 aws_secret_access_key=settings.YANDEX_CLOUD['SECRET_KEY'],
#             )

#             s3.upload_fileobj(
#                 request.FILES['video_file'],
#                 settings.YANDEX_CLOUD['BUCKET_NAME'],
#                 video.video_file.name
#             )

#             return redirect('success')

#     else:
#         form = VideoUploadForm()

#     return render(request, 'upload_video.html', {'form': form})

def success(request):
    return render(request, 'success.html')
