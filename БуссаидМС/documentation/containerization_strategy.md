# Стратегия контейнеризации

## 1. Выбор базового образа

Для сборки используется `node:22-alpine`, для рантайма - `gcr.io/distroless/nodejs22-debian12:nonroot`.

Почему так:

- `node:22-alpine` удобен для этапов `deps/build`: быстрый, небольшой, есть пакетный менеджер.
- Distroless runtime не содержит shell и лишних утилит, что уменьшает поверхность атаки.
- `nonroot`-вариант запускает приложение без root-прав по умолчанию.

Итог: меньше финальный образ и выше безопасность по сравнению с single-stage образом на full Node.

## 2. Управление ENV

Используются переменные окружения:

| Переменная | Назначение | Где задается |
|---|---|---|
| `NODE_ENV` | Режим работы Node.js (`production`) | Dockerfile / app |
| `PORT` | Порт приложения внутри контейнера | Dockerfile / compose |
| `DB_HOST` | Хост БД | compose (`db`) |
| `DB_PORT` | Порт БД | compose |
| `DB_NAME` | Имя БД | compose |
| `DB_USER` | Пользователь БД | compose |
| `DB_PASSWORD` | Пароль БД | compose / secrets |
| `REDIS_HOST` | Хост Redis | compose (`cache`) |
| `REDIS_PORT` | Порт Redis | compose |
| `POSTGRES_DB` | Инициализация базы в postgres-контейнере | compose |
| `POSTGRES_USER` | Инициализация пользователя postgres | compose |
| `POSTGRES_PASSWORD` | Инициализация пароля postgres | compose / secrets |

Для CI/CD учетные данные реестра берутся из секретов GitHub Actions (для GHCR можно использовать `GITHUB_TOKEN` с `packages: write`).

## 3. Оптимизация размера

Сравнение подходов:

- До оптимизации (single-stage, `node:22`, с dev-зависимостями и исходниками): ~420 MB
- После оптимизации (multi-stage + distroless runtime + prod dependencies): ~95 MB

Экономия: около 4.4x по размеру.

Достигнуто за счет:

- разделения build/runtime;
- исключения dev-зависимостей в финальном образе;
- отсутствия компиляторов, package cache и исходников в runtime-слое.
