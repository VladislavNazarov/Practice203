# Схема сетевого взаимодействия контейнеров

```mermaid
flowchart LR
    User[Пользователь / Клиент] -->|HTTP :3000| App[app container]

    subgraph docker_internal_net [Docker internal network]
        App -->|TCP 5432| DB[(PostgreSQL db)]
        App -->|TCP 6379| Cache[(Redis cache)]
    end

    DB --> DBVol[(Volume: postgres_data)]
    Cache --> CacheVol[(Volume: redis_data)]

    classDef svc fill:#eaf7ff,stroke:#2f6f9f,stroke-width:1px;
    classDef data fill:#f2fff0,stroke:#4c8a3f,stroke-width:1px;

    class App svc;
    class DB,Cache,DBVol,CacheVol data;
```

Ключевые принципы:

- Сервисы взаимодействуют по именам контейнеров (`db`, `cache`) через внутреннюю сеть.
- Наружу публикуется только порт приложения, БД и кэш изолированы.
- Данные PostgreSQL сохраняются в персистентном томе `postgres_data`.
