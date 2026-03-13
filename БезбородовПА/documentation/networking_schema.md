# Схема взаимодействия контейнеров

```mermaid
flowchart LR
    user[Host machine]

    subgraph dockerNetwork [Docker Internal Network]
        app["app FastAPI"]
        db["db PostgreSQL"]
        cache["redis Redis"]
        dbVolume[(postgres_data volume)]
    end

    user -->|HTTP 8080| app
    app -->|DATABASE_URL| db
    app -->|REDIS| redis
    db <-->| data| dbVolume
```

## Пояснение

- `app FastAPI` публикует наружу порт `8000`, поэтому API доступен с хост-машины.
- `redis` и `cache` работают во внутренней сети Docker и адресуются по именам сервисов `redis` и `cache`.
- Постоянные данные PostgreSQL сохраняются в named volume `postgres_data`.
- Настройки подключения передаются через переменные окружения, а не захардкожены.
