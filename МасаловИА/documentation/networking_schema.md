# Networking Schema

## Описание взаимодействия сервисов

В системе используются три контейнера:
- **app** — основное приложение (Go-сервер)
- **db** — база данных PostgreSQL
- **cache** — кэш Redis

Контейнеры объединены в одну внутреннюю сеть Docker (`backend`), что позволяет им взаимодействовать по именам сервисов.

---

## Схема взаимодействия

```mermaid
graph TD
    User[Пользователь] -->|HTTP :8080| App[app container]
    App -->|DB_HOST=db<br/>:5432| DB[(PostgreSQL)]
    App -->|REDIS_HOST=cache<br/>:6379| Cache[(Redis)]

    subgraph Docker Network: backend
        App
        DB
        Cache
    end
```