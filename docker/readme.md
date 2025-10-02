[Ссылка с архивом docker-image ](https://drive.google.com/drive/folders/1omUVlQfz_ke1Q_rbKf3UsTZ8c2gYqxhH?usp=sharing).
-----

## README: Использование Docker Образа из Архива

Этот архив (`my_simon_ner_app.tar`) содержит готовый Docker образ вашего приложения.

### 1\. Требования

Для использования образа на целевом компьютере должен быть установлен **Docker Desktop** (или Docker Engine).

### 2\. Загрузка Образа

Загрузите образ из архива в локальное хранилище Docker. Выполните команду в терминале (PowerShell/CMD), находясь в той же папке, что и файл `.tar`:

```bash
docker load -i my_simon_ner_app.tar
```

**Проверка:** Убедитесь, что образ `my_simon_ner_app:latest` появился в списке: `docker images`

-----

### 3\. Запуск Контейнера

Запустите приложение как контейнер, пробросив порт **8080** на хосте (вашем компьютере) на порт **8000** внутри контейнера.

```bash
docker run -d -p 8080:8000 --name ner_server_instance my_simon_ner_app:latest
```

  * `ner_server_instance` – это имя для вашего запущенного контейнера.

-----

### 4\. Проверка Работы

После запуска приложение будет доступно по адресу:

```
http://localhost:8080
```

-----

### Полезные Команды

| Команда | Действие |
| :--- | :--- |
| `docker ps` | Показать запущенные контейнеры. |
| `docker logs ner_server_instance` | Посмотреть логи контейнера для отладки. |
| `docker stop ner_server_instance` | Остановить контейнер. |
