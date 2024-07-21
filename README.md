## Установка и запуск

### Склонируйте репозиторий:

```bash
git clone https://github.com/Kirill8769/authorization_service.git
```

### Перейдите в папку с проектом

```bash
cd authorization_service
```

### Установите зависимости:

Сначала активируем poetry
```bash
poetry shell
```

Затем установим все зависимости из pyproject.toml
```bash
poetry install
```

Для определения необходимых переменных окружения воспользуйтесь шаблоном
```bash
.env.sample
```

Сделайте миграции
```bash
python manage.py makemigrations
python manage.py migrate
```

Создайте суперпользователя
```bash
python manage.py csu
```

## Запуск программы

### Сервер сайта
Для запуска сервера сайта выполните команду:
```bash
python manage.py runserver
```

## Лицензия

Проект распространяется под лицензией MIT.

---

Этот README файл предоставляет основную информацию о проекте, его установке и использовании.