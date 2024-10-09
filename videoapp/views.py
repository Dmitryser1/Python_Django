import boto3
from django.shortcuts import render, redirect
from .forms import VideoUploadForm
from django.core.files.storage import default_storage
from django.conf import settings


def upload_video(request):
    if request.method == 'POST':
        form = VideoUploadForm(request.POST, request.FILES)
        if form.is_valid():
            video_file = request.FILES['video_file']

            # Загрузка файла на Yandex Cloud
            session = boto3.session.Session()
            s3 = session.client(
                service_name='s3',
                endpoint_url=settings.YANDEX_CLOUD['ENDPOINT_URL'],
                aws_access_key_id=settings.YANDEX_CLOUD['ACCESS_KEY'],
                aws_secret_access_key=settings.YANDEX_CLOUD['SECRET_KEY'],
            )

            s3.upload_fileobj(
                request.FILES['video_file'],  # Файл, загружаемый пользователем
                settings.YANDEX_CLOUD['BUCKET_NAME'],  # Имя бакета
                request.FILES['video_file'].name  # Имя файла в бакете
            )   


            return redirect('success')

    else:
        form = VideoUploadForm()

    return render(request, 'upload.html', {'form': form})

def success(request):
    return render(request, 'success.html')
