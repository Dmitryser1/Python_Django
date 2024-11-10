# Python_Django

# Django Video Upload App

Это Django приложение предназначено для загрузки видеофайлов в Yandex Object Storage (объектное хранилище Яндекс Облака). В данном руководстве представлены шаги для настройки Yandex Cloud и запуска приложения.

## Основные шаги:
1. Регистрация в Yandex Cloud.
2. Настройка платёжного счёта.
3. Создание бакета (bucket) для хранения видео.
4. Настройка Python приложения с использованием Django для загрузки файлов.
5. Запуск приложения локально или в облаке.

### 1. Регистрация на Yandex Cloud
Для начала работы с Yandex Cloud необходимо создать аккаунт.

1. Перейдите на сайт [Yandex Cloud](https://cloud.yandex.ru) и нажмите "Войти".
2. Используйте ваш существующий аккаунт Yandex или создайте новый.
3. Пройдите процесс регистрации, указав ваши контактные данные.

### 2. Создание платёжного счёта
Для использования Yandex Cloud необходимо создать платёжный счёт. Без активного счёта невозможно использовать ресурсы облака.

1. После входа в консоль Yandex Cloud перейдите в раздел **Биллинг**.
2. Нажмите на кнопку "Создать платёжный аккаунт" и следуйте инструкциям.
3. Заполните платёжную информацию (платёжные данные, номер карты).
4. Завершите создание платёжного аккаунта.

### 3. Создание бакета для хранения видео
Бакет в Yandex Object Storage — это место для хранения файлов.

1. Перейдите в **Консоль управления Yandex Cloud**.
2. Выберите сервис "Object Storage".
3. Нажмите "Создать бакет".
   - Укажите уникальное имя для бакета.
   - Выберите регион (например, `ru-central1`).
   - Оставьте остальные параметры по умолчанию.
4. Сохраните настройки.

### 4. Настройка приложения

#### Шаг 1: Клонируйте репозиторий

```bash
git clone https://github.com/Dmitryser1/Python_Django.git
cd Python_Django
```

#### Шаг 2: Установка зависимостей

```bash
python -m venv venv
source venv/bin/activate  # для Windows: venv\Scripts\activate
pip install -r requirements.txt
```


#### Шаг 3: Настройка Yandex Object Store

1. Перейдите в раздел "Сервисные аккаунты" в Yandex Cloud.
2. Создайте новый сервисный аккаунт и привяжите к нему роль "storage.admin".
3. Создайте статический ключ доступа:
4. Перейдите в раздел "Сервисные аккаунты".
5. Найдите ваш аккаунт и создайте ключ доступа (Access Key ID и Secret Access Key).
6. Сохраните полученные данные.

#### Шаг 4 Настройка переменных окружения

Создайте .env файл в корне проекта и добавьте следующие параметры

```makefile
YANDEX_CLOUD_ACCESS_KEY=ваш_доступ_ключ
YANDEX_CLOUD_SECRET_KEY=ваш_секретный_ключ
YANDEX_CLOUD_BUCKET_NAME=имя_вашего_бакета
YANDEX_CLOUD_ENDPOINT=https://storage.yandexcloud.net
```

#### Шаг 5: Примените миграции и запустите сервер

```bash
python manage.py migrate
python manage.py runserver
```


#### Шаг 6: Настройка виртуального сервера (Compute Instance)
Перейдите в Yandex Cloud Compute.

Создайте новый виртуальный сервер:  

- В разделе "Compute Cloud" нажмите "Создать виртуальную машину".
- Выберите операционную систему Ubuntu 20.04 LTS.
- Настройте количество CPU и памяти (рекомендуется не менее 4 CPU и 16 ГБ RAM для YOLOv8).
- Создайте новый SSH ключ для доступа или используйте существующий.

```bash
ssh <your-username>@<your-public-ip>
```

#### Шаг 7: Установка YOLOv8 и зависимостей

1. Обновите пакеты на сервере:

```bash
sudo apt update && sudo apt upgrade -y
```
2. Установите Python и необходимые библиотеки:

```bash
sudo apt install python3-pip -y
pip3 install --upgrade pip
```
3. Установите виртуальное окружение Python:

```bash
sudo apt install python3-venv -y
python3 -m venv yolov8-env
source yolov8-env/bin/activate
```
4. Установите YOLOv8:

```bash
pip install ultralytics
```
Это установит YOLOv8 и все необходимые библиотеки для работы с ней.


5. Проверьте установку YOLOv8:

```bash
yolo
```

#### Шаг 8: Настройка доступа к Yandex Object Storage

1. Установите библиотеку boto3 для взаимодействия с Yandex Object Storage:

```bash
pip install boto3
```

#### Шаг 9: Настройка скрипта для загрузки и обработки видео

1. Разместите код загрузки видео из Object Storage и обработки YOLOv8 на VM. Создайте файл, например, process_video.py.

Пример структуры process_video.py для скачивания видео и обработки YOLOv8:

```python
import boto3
from ultralytics import YOLO
import cv2

# Настройки подключения к Object Storage
s3_client = boto3.client(
    's3',
    endpoint_url='https://storage.yandexcloud.net',
    aws_access_key_id='ВАШ_ACCESS_KEY',
    aws_secret_access_key='ВАШ_SECRET_KEY'
)

bucket_name = 'your-bucket-name'
video_key = 'path/to/video.mp4'  # Путь к видеофайлу в бакете
local_video_path = '/tmp/video.mp4'

# Скачивание видео из Object Storage
s3_client.download_file(bucket_name, video_key, local_video_path)

# Обработка видео с помощью YOLOv8
model = YOLO("yolov8n.pt")
results = model.predict(local_video_path, save=True)

print("Обработка завершена. Результаты сохранены локально.")
```

2. Запуск скрипта обработки:

Выполните скрипт на сервере:

```bash
python3 process_video.py
```
Скрипт загрузит видеофайл из Object Storage, выполнит обработку с YOLOv8 и сохранит результаты на локальной машине.

# Автоматизация запуска (опционально):

Настройте автоматический запуск скрипта с помощью Cron или других утилит для периодической обработки видео, если необходимо.