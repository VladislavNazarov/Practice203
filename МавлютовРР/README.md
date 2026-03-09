# Practice203 - Мавлютов Р. Р.

## Сервисы

- `app` - FastAPI приложение `python-videohosting`
- `db` - PostgreSQL 16 для постоянного хранилища
- `cache` - Redis 7 для кэша и инфраструктурной готовности окружения

## Образ

- GHCR: [ghcr.io/stirk1337/python-videohosting:latest](https://ghcr.io/stirk1337/python-videohosting)

## Запуск одной командой

```bash
docker compose -f artifacts/docker-compose.yml up -d --build
```

После запуска приложение доступно на `http://localhost:8000`, проверка состояния - `http://localhost:8000/health`.

## Документация

- [Стратегия контейнеризации](documentation/containerization_strategy.md)
- [Схема сети контейнеров](documentation/networking_schema.md)
