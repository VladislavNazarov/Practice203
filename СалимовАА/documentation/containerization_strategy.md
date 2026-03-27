# Стратегия контейнеризации SincSlot

## Выбор базового образа

Для сборки и запуска backend выбран `python:3.12-slim`.

Причины выбора:

- образ официальный и стабильно поддерживается;
- `slim` заметно меньше полного `python`-образа;
- по сравнению с `alpine` проще работать с зависимостями `asyncpg`, `cryptography` и `psycopg/libpq`-совместимыми библиотекам без лишних проблем со сборкой;
- финальный runtime-образ не содержит компиляторы и dev-пакеты, так как они остаются только на этапе `builder`.

Для зависимостей выбраны:

- `postgres:17-alpine` для БД;
- `redis:7-alpine` для кэша.

Оба образа компактные, официальные и хорошо подходят для локального окружения и CI.

## Управление переменными окружения

В `docker-compose.yml` используются следующие переменные:

| Переменная | Назначение | Пример |
|---|---|---|
| `APP_IMAGE` | Имя итогового образа приложения | `ghcr.io/al-dozor/sincslot-backend:latest` |
| `APP_PORT` | Порт backend на хосте | `10004` |
| `POSTGRES_DB` | Имя основной БД | `syncslot_db` |
| `POSTGRES_USER` | Пользователь PostgreSQL | `pguser` |
| `POSTGRES_PASSWORD` | Пароль PostgreSQL | `pgpassword` |
| `POSTGRES_PORT` | Порт PostgreSQL на хосте | `5432` |
| `REDIS_PORT` | Порт Redis на хосте | `6379` |
| `SYNC_SLOT__DB__URL` | URL подключения backend к PostgreSQL | `postgresql+asyncpg://pguser:pgpassword@db:5432/syncslot_db` |
| `SYNC_SLOT__DB__ECHO` | Логирование SQL | `0` |
| `SYNC_SLOT__DB__ECHO_POOL` | Логирование пула соединений | `0` |
| `SYNC_SLOT__DB__POOL_SIZE` | Размер пула БД | `5` |
| `SYNC_SLOT__DB__MAX_OVERFLOW` | Дополнительные соединения сверх пула | `10` |
| `SYNC_SLOT__PASSWORD__SALT` | Соль для хеширования паролей | `Tom&Jerry` |
| `SYNC_SLOT__JWT__SECRET_KEY` | Секрет для JWT | `secret_key` |
| `SYNC_SLOT__JWT__ALGORITHM` | Алгоритм подписи JWT | `HS256` |
| `SYNC_SLOT__JWT__ACCESS_TOKEN_EXPIRE_MINUTES` | Время жизни access-token | `30` |
| `SYNC_SLOT__CACHE__URL` | Адрес Redis внутри docker-сети | `redis://cache:6379/0` |

Чувствительные значения в CI выносятся в GitHub Secrets. Для публикации образа используются:

- `GITHUB_TOKEN` для push в GHCR;
- при необходимости альтернативного реестра могли бы использоваться `DOCKERHUB_USERNAME` и `DOCKERHUB_TOKEN`.

## Multi-stage build и оптимизация

Использована двухэтапная сборка:

### 1. `builder`

- устанавливаются только необходимые системные пакеты для сборки Python-зависимостей;
- создаётся отдельное виртуальное окружение `/opt/venv`;
- сначала копируется только `requirements.txt`, чтобы Docker мог переиспользовать кэш слоя с зависимостями;
- после этого устанавливаются Python-пакеты.

### 2. `runtime`

- используется отдельный чистый `python:3.12-slim`;
- в runtime попадает только готовое virtualenv и исходники backend;
- отсутствуют `build-essential`, `libpq-dev` и кэш `pip`;
- контейнер запускается от непривилегированного пользователя `appuser`.

Дополнительно:

- `.dockerignore` исключает frontend, git-метаданные, локальные кэши и временные файлы;
- контейнер стартует с миграциями `alembic upgrade head`, после чего поднимает `uvicorn`;
- удалён dev-режим `--reload`, чтобы runtime был ближе к production-сценарию.
- публикация в GHCR выполняется с тегами `latest` и `sha-<commit>`, что позволяет использовать и удобный плавающий тег, и воспроизводимый immutable tag.

## Сравнение размера образа

Сравнение выполнено по ожидаемой структуре слоёв:

- до оптимизации, при одноэтапной сборке с компиляторами и dev-пакетами, образ был бы порядка `900-1100 MB`;
- после перехода на multi-stage и очистки runtime ожидаемый размер составляет примерно `220-300 MB`.
