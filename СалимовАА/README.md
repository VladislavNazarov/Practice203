# Practice 3 (203) — Контейнеризация и воспроизводимость окружения

## Сервисы

- `app`: backend `SincSlot` на FastAPI, собирается через multi-stage Docker build
- `db`: PostgreSQL 17 для основного хранилища данных
- `cache`: Redis 7 как отдельный контейнер кэширования

## Публичный образ

- GHCR image: `ghcr.io/al-dozor/sincslot-backend:latest`
- GHCR package: `https://github.com/users/Al-DozoR/packages/container/package/sincslot-backend`
- Проверенный immutable tag: `ghcr.io/al-dozor/sincslot-backend:sha-0ae912a`

## Запуск

```bash
docker compose -f Practice203/СалимовАА/artifacts/docker-compose.yml up -d
```

## Локальная проверка
-swagger: `http://127.0.0.1:10004/docs`

## Что приложено

- стратегия контейнеризации: [containerization_strategy.md](documentation/containerization_strategy.md)
- схема сети: [networking_schema.md](documentation/networking_schema.md)
- Dockerfile: [Dockerfile](artifacts/Dockerfile)
- orchestration: [docker-compose.yml](artifacts/docker-compose.yml)
- пример лога успешного push из CI: [registry_push_log.txt](artifacts/registry_push_log.txt)


