import os

import requests as requests
from django.core.files.storage.base import Storage


# Создаем класс YandexDiskStorage, который наследует от базового класса Storage
class YandexDiskStorage(Storage):
    # Инициализируем класс с параметрами токена и пути к папке на Yandex Disk
    def __init__(self, token, folder):
        self.token = token
        self.folder = folder

    # Определяем метод _get_full_path, который возвращает полный путь к файлу на Yandex Disk
    def _get_full_path(self, name):
        return f"{self.folder}/{name}"

    # Определяем метод _open, который возвращает файловый объект для чтения файла с Yandex Disk
    def _open(self, name, mode="rb"):
        # Проверяем, что режим открытия файла поддерживается
        if mode not in ("r", "rb"):
            raise ValueError("Unsupported mode: %s" % mode)
        # Формируем URL для запроса к API Yandex Disk
        url = "https://cloud-api.yandex.net/v1/disk/resources/download"
        params = {"path": self._get_full_path(name)}
        headers = {"Authorization": f"OAuth {self.token}"}
        # Отправляем GET-запрос и получаем ответ с ссылкой для скачивания файла
        response = requests.get(url, params=params, headers=headers)
        response.raise_for_status()
        download_url = response.json()["href"]
        # Отправляем GET-запрос по ссылке для скачивания файла и получаем файловый объект
        file_response = requests.get(download_url, stream=True)
        file_response.raise_for_status()
        return file_response.raw

    # Определяем метод _save, который сохраняет файл на Yandex Disk
    def _save(self, name, content):
        # Формируем URL для запроса к API Yandex Disk
        url = "https://cloud-api.yandex.net/v1/disk/resources/upload"
        params = {"path": self._get_full_path(name), "overwrite": True}
        headers = {"Authorization": "OAuth %s" % self.token}
        # Отправляем GET-запрос и получаем ответ с ссылкой для загрузки файла
        response = requests.get(url, params=params, headers=headers)
        response.raise_for_status()
        upload_url = response.json()["href"]
        # Отправляем PUT-запрос по ссылке для загрузки файла и передаем файловый объект
        upload_response = requests.put(upload_url, data=content)
        upload_response.raise_for_status()
        # Возвращаем имя сохраненного файла
        return name

    # Определяем метод exists, который проверяет, существует ли файл на Yandex Disk
    def exists(self, name):
        # Формируем URL для запроса к API Yandex Disk
        url = "https://cloud-api.yandex.net/v1/disk/resources"
        params = {"path": self._get_full_path(name)}
        headers = {"Authorization": "OAuth %s" % self.token}
        # Отправляем GET-запрос и проверяем статус ответа
        response = requests.get(url, params=params, headers=headers)
        return response.status_code == 200

    # Определяем метод url, который возвращает URL для доступа к файлу на Yandex Disk
    def url(self, name):
        # Формируем URL для запроса к API Yandex Disk
        url = "https://cloud-api.yandex.net/v1/disk/resources/download"
        params = {"path": self._get_full_path(name)}
        headers = {"Authorization": "OAuth %s" % self.token}
        # Отправляем GET-запрос и получаем ответ с ссылкой для скачивания файла
        response = requests.get(url, params=params, headers=headers)
        response.raise_for_status()
        download_url = response.json()["href"]
        # Возвращаем ссылку для скачивания файла
        return download_url


yandex_disk_storage = YandexDiskStorage(
    token="", folder="/test"
)
