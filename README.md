# WhatsApp parser

## Описание

Приложение для отслеживания статуса онлайна контактов в WhatsApp

## Установка и запуск

Перед запуском убедитесь, что вы авторизованы в WhatsApp в браузере Chrome

1. Склонируйте репозиторий:
 ```ssh
 git@github.com:ionov-nikita/whatsapp_parser
 ```
2. Скачайте драйвер для работы с браузером и поместите файл в директорию
4. Создайте и активируйте виртуальное окружение:
 ```sh
  python3 -m venv venv
  source venv/bin/activate
  ```
4. Установите зависимости:
 ```sh
  pip install -r requirements.txt
 ```
5. Запустите проект и подготовить камеру телефона для считывания QR-кода из браузера:
 ```sh
  python3 app.py
 ```

## Полезные ссылки

* Скачивание браузера - https://chromedriver.storage.googleapis.com/index.html
* Список опций Chromium - https://peter.sh/experiments/chromium-command-line-switches/