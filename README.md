Описание.
**API_FINAL** - учебный проект из курса **"Backend developer"** [Яндекс.Практикума](https://praktikum.yandex.ru/backend-developer/).
Цель работы над проектом - получить навыки работы с **Django REST framework**.
Задание представляет из себя  по заданным правилам поведения АПИ и нескольким достаточно простым моделям со связанными отношениями реализовать логику работы АПИ.

Установка.
Клонировать репозиторий и перейти в его папку в командной строке:

```
git clone https://github.com/coherentus/api_final_yatube
```

```
cd api_final_yatube
```

Cоздать и активировать виртуальное окружение:

```
python3 -m venv venv
```

Для *nix-систем:

```
source venv/bin/activate
```

Для windows-систем:

```
source venv/Scripts/activate
```

Установить зависимости из файла requirements.txt:

```
python3 -m pip install --upgrade pip
```

```
pip install -r requirements.txt
```

Выполнить миграции:

```
cd yatube_api
python3 manage.py migrate
```

Запустить проект:

```
python3 manage.py runserver
```


Некоторые примеры запросов к API.

**Получение списка сообществ:**

эндпойнт:

```
/api/api/v1/groups/
```

разрешённые HTTP-методы:

```
GET
```

в ответе:

```python
[
  {
    "id": 0,
    "title": "string",
    "slug": "string",
    "description": "string"
  }
]
response status code 200
```

**Создание подписки**

эндпойнт:
```
/api/v1/follow/
```

http-метод:
```
POST
```

Payload:
```python
{
  "following": "string"
}
```

Варианты ответов:
* удачное выполнение - статус 201 и созданный экземпляр подписки
```python
{
  "user": "string",
  "following": "string"
}
```

* отклонение запроса - статус 400 - пропущен обязательный параметр
```python
{
  "following": [
    "Обязательное поле."
  ]
}
```

* отклонение запроса - статус 401 - запрос от неаутенфицированного пользователя
```python
{
  "detail": "Учетные данные не были предоставлены."
}
```


Полный перечень запросов АПИ есть в ReDoc по адресу "/redoc/"