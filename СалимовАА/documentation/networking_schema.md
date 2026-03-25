# Схема взаимодействия контейнеров

```mermaid
flowchart LR
    User["Пользователь / Host"] -->|"HTTP :10004"| App["app<br/>FastAPI + Uvicorn"]
    App -->|"SQLAlchemy / asyncpg<br/>5432"| DB["db<br/>PostgreSQL 17"]
    App -->|"Redis protocol<br/>6379"| Cache["cache<br/>Redis 7"]

    subgraph DockerNet["Docker network: sincslot_internal"]
        App
        DB
        Cache
    end

    DB -->|"volume: postgres_data"| Storage["Персистентное хранилище БД"]
```

## Пояснение

- `app` доступен с хост-машины по порту `10004`;
- `db` и `cache` находятся во внутренней bridge-сети и общаются по сервисным DNS-именам `db` и `cache`;
- наружу публикуются только необходимые порты;
- данные PostgreSQL сохраняются в именованном volume `postgres_data`.
