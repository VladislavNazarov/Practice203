# Practice203 — Голов Денис

## Сервисы

- `app` — Spring Boot приложение (SanatoriumProject)
- `db` — PostgreSQL 17 для хранения данных
- `cache` — Redis 7 для кэширования

## Образ

- GHCR: `ghcr.io/dengoan969/naumenpracticesanatoriumproject/sanatorium-project:latest`

## Запуск одной командой

```bash
docker compose -f artifacts/docker-compose.yml up -d --build
```

После запуска:
- Приложение: `http://localhost:8080`
- Swagger UI: `http://localhost:8080/swagger-ui.html`
- API Docs: `http://localhost:8080/api-docs`

## Документация

- [Стратегия контейнеризации](documentation/containerization_strategy.md)
- [Схема сети](documentation/networking_schema.md)
