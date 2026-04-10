# WeatherAPI - Контейнеризация

## Публичный образ

```
ghcr.io/akulov-da/weather-api:latest
```

## Запуск проекта

```powershell
cd artifacts
docker-compose up -d
```

Сервисы после запуска:

| Сервис | URL | Назначение |
|--------|-----|-----------|
| WeatherAPI | http://localhost:8080 | REST API |
| PostgreSQL | localhost:5432 | База данных (внутренний доступ) |
| Redis | localhost:6379 | Кэш (внутренний доступ) |

## Проверка

```powershell
Invoke-WebRequest http://localhost:8080/health -UseBasicParsing
Invoke-WebRequest http://localhost:8080/api/v1/weather?city=Moscow -UseBasicParsing
```

## Документация

- [Стратегия контейнеризации](documentation/containerization_strategy.md)
- [Схема сети](documentation/networking_schema.md)
