# Проект "Фудграм"
[![Python](https://img.shields.io/badge/-Python-464646?style=flat-square&logo=Python)](https://www.python.org/)
[![Django](https://img.shields.io/badge/-Django-464646?style=flat-square&logo=Django)](https://www.djangoproject.com/)
[![Django REST Framework](https://img.shields.io/badge/-Django%20REST%20Framework-464646?style=flat-square&logo=Django%20REST%20Framework)](https://www.django-rest-framework.org/)
[![Nginx](https://img.shields.io/badge/-NGINX-464646?style=flat-square&logo=NGINX)](https://nginx.org/ru/)
[![gunicorn](https://img.shields.io/badge/-gunicorn-464646?style=flat-square&logo=gunicorn)](https://gunicorn.org/)
[![PostgreSQL](https://img.shields.io/badge/-PostgreSQL-464646?style=flat-square&logo=PostgreSQL)](https://www.postgresql.org/)
[![docker](https://img.shields.io/badge/-Docker-464646?style=flat-square&logo=docker)](https://www.docker.com/)
[![GitHub%20Actions](https://img.shields.io/badge/-GitHub%20Actions-464646?style=flat-square&logo=GitHub%20actions)](https://github.com/features/actions)

Проект доступен по адресу - https://foodgram.space
Данные для входа в админ-зону Django:
```
Email - vitaliktamilin@gmail.com
Password - 0z4DMnxJL_fa-3Z5euFAZ 
```
## Описание проекта
«Фудграм» — сайт, на котором пользователи могут публиковать свои рецепты, 
добавлять чужие рецепты в избранное и подписываться на публикации других авторов. 
Зарегистрированным пользователям доступен сервис «Список покупок», 
который позволяет создать список продуктов, 
которые необходимо купить для приготовления выбранных рецептов.

## Запуск проекта на удаленном сервере

1. Клонируйте репозиторий на локальный компьютер
```
git clone git@github.com:XxSweeperxX/foodgram.git
```
```
cd foodgram
```

2. В корне проекта создайте файл виртуального окружения ".env"
Ниже предоставлен пример заполненного файла
```.env

POSTGRES_USER= Имя пользователя БД
POSTGRES_PASSWORD= Пароль пользователя БД
POSTGRES_DB= Название БД
DB_HOST= Адрес соединения Django с БД
DB_PORT= Порт на котором работает БД
SECRET_KEY= Ключ проекта Django. Получить новый можно при помощи функции get_random_secret_key()
DEBUG= Вывод информации для отладки проекта
ALLOWED_HOSTS= Перечень хостов и доменов, на которых может работать этот проект
```
3. Создайте Docker-образы:

Для бэкенда 
```
cd backend/foodgram_backend
docker build -t {docker_username}/foodgram_backend .
```
Для фронтенда
```
cd frontend/
docker build -t {docker_username}/foodgram_frontend .
```
Для nginx
```
cd gateway/
docker build -t {docker_username}/foodgram_gateway .
```
4. Загрузите образы на DockerHub
```
docker push {username}/foodgram_backend
docker push {username}/foodgram_frontend
docker push {username}/foodgram_gateway
```
6. Подключитесь к своему удаленному серверу и установите DockerCompose
```
sudo apt update
sudo apt install curl
curl -fSL https://get.docker.com -o get-docker.sh
sudo sh ./get-docker.sh
sudo apt install docker-compose-plugin 
```
7. Создайте директорию проекта
```
mkdir foodgram
```
8. Перенесите в директорию проекта файлы с локального компьютера:
```
.env
docker-compose.release.yml
```
```
scp -i {path_to_SSH}/{SSH_name} docker-compose.release.yml {username}@{server_ip}:/home/username/foodgram/docker-compose.release.yml
scp -i {path_to_SSH}/{SSH_name} .env {username}@{server_ip}:/home/username/foodgram/.env
```
Где:
```
path_to_SSH     — путь к файлу с SSH-ключом;
SSH_name        — имя файла с SSH-ключом (без расширения);
username        — Ваше имя пользователя на сервере;
server_ip       — IP вашего сервера.
```
9. Запустите проект с помощью Docker Compose, выполните миграции, соберите статику и загрузите исходные данные в бд
```
sudo docker compose -f docker-compose.release.yml up -d
sudo docker compose -f docker-compose.yml exec backend python manage.py migrate
sudo docker compose -f docker-compose.yml exec backend python manage.py collectstatic
sudo docker compose -f docker-compose.yml exec backend cp -r /app/collected_static/. /backend_static/static/
sudo docker compose -f docker-compose.yml exec backend python manage.py load_data
```
10. Создайте суперпользователя
```
sudo docker compose -f docker-compose.yml exec backend python manage.py createsuperuser
```

## Примеры запросов API
Регистрация пользователя:

```
   POST /api/users/
```

Получение данных своей учетной записи:

```
   GET /api/users/me/ 
```

Добавление подписки:

```
   POST /api/users/id/subscribe/
```

Обновление рецепта:
  
```
   PATCH /api/recipes/id/
```

Удаление рецепта из избранного:

```
   DELETE /api/recipes/id/favorite/
```

Получение короткой ссылки на рецепт:

```
   GET /api/recipes/{id}/get-link/
```

### Полный перечень запросов API находится в документации
```
 foodgram/docs/redoc.html
```

#### Автор работы
Виталий Тамилин - [https://github.com/XxSweeperxX](https://github.com/XxSweeperxX)

