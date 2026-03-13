# Практика 3 (203): Контейнеризация и воспроизводимость

## Статус

- Основной образ приложения (GHCR): `ghcr.io/boussaidms/practice203-app:latest`
- Compose-оркестрация включает 3 сервиса: `app`, `db` (PostgreSQL), `cache` (Redis)

## Запуск одной командой

```bash
docker compose -f БуссаидМС/artifacts/docker-compose.yml up -d --build
```

## Сервисы

- `app`: основное приложение (multi-stage Docker build, минимальный runtime)
- `db`: PostgreSQL 16 с персистентным томом
- `cache`: Redis 7 во внутренней сети

## CI/CD

- Пайплайн расширен этапом сборки и публикации контейнера после успешных тестов
- Workflow: `.github/workflows/ci.yml`
- Push выполняется только при `push` в `main`

## Быстрая проверка

```bash
docker compose -f БуссаидМС/artifacts/docker-compose.yml ps
docker compose -f БуссаидМС/artifacts/docker-compose.yml logs app --tail=100
```
