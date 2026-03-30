# LPN-сервис — Практика 203

## Описание

LPN-сервис — monorepo на Bun для управления приватными сетевыми туннелями. Полностью контейнеризировано: 14 сервисов в Docker Compose, multi-stage сборка, автоматический push в GHCR через GitHub Actions.

## Образы в реестре (GHCR)

| Сервис | Образ |
|--------|-------|
| API | `ghcr.io/oglenyaboss/projectlpn-api:latest` |
| Bot | `ghcr.io/oglenyaboss/projectlpn-bot:latest` |
| Alert Relay | `ghcr.io/oglenyaboss/projectlpn-alert-relay:latest` |
| Migrate | `ghcr.io/oglenyaboss/projectlpn-migrate:latest` |
| Blackbox Exporter | `ghcr.io/oglenyaboss/projectlpn-blackbox:latest` |

## Запуск проекта

```bash
# Клонировать и настроить переменные
git clone <repo-url>
cd projectlpn
cp .env.example .env  # заполнить переменные

# Запустить всю инфраструктуру
docker compose up -d
```

Сервисы будут доступны:
- API: `http://localhost:3000`
- Grafana: `http://localhost:3001`
- Prometheus: `http://localhost:9090`
- MinIO Console: `http://localhost:9001`

## Сервисы

| Сервис | Образ / Сборка | Порт | Сеть |
|--------|----------------|------|------|
| **api** | multi-stage build (Bun) | 3000 | frontend, backend |
| **bot** | multi-stage build (Bun) | — | frontend, backend |
| **alert-relay** | multi-stage build (Bun) | — | monitoring |
| **postgres** | postgres:16.4-alpine | 5432 | backend |
| **minio** | minio/minio:latest | 9000, 9001 | backend |
| **migrate** | Dockerfile.migrate | — | backend |
| **prometheus** | prom/prometheus:v2.54.0 | 9090 | monitoring, frontend |
| **grafana** | grafana/grafana:11.2.0 | 3001 | monitoring |
| **alertmanager** | prom/alertmanager:v0.27.0 | 9093 | monitoring |
| **node_exporter** | prom/node-exporter:v1.8.2 | — | monitoring |
| **postgres_exporter** | prometheuscommunity/postgres-exporter:v0.15.0 | — | monitoring, backend |
| **cadvisor** | gcr.io/cadvisor/cadvisor:v0.49.1 | — | monitoring |
| **blackbox_exporter** | custom build | — | monitoring, frontend |
| **minio_init** | minio/mc:latest | — | backend |

## Документация

- [Стратегия контейнеризации](documentation/containerization_strategy.md)
- [Схема сетевого взаимодействия](documentation/networking_schema.md)
