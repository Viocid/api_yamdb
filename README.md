# api_yamdb
api_yamdb

# Project Name

## Описание проекта

Этот проект представляет собой API для работы с постами, группами и комментариями. Он позволяет создавать, читать, обновлять и удалять посты и комментарии, а также просматривать группы.

## Как развернуть проект

Клонировать репозиторий и перейти в него в командной строке:
```
git clone https://github.com/LunarBirdMYT/api_yamdb.git
```

```
cd api_yamdb
```

Cоздать и активировать виртуальное окружение:

```
python -m venv env
```

```
source env/bin/activate
```

```
python -m pip install --upgrade pip
```

Установить зависимости из файла requirements.txt:

```
pip install -r requirements.txt
```

Перейти в папку с файлом manage.py и выполнить миграции:

```
python manage.py makemigrations users
python manage.py migrate
```

Запустить проект:

```
python manage.py runserver
```

Документация по работе с проектом доступна по адресу /redoc:
```
http://127.0.0.1:8000/redoc/ (по умолчанию)

