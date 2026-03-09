# Схема взаимодействия контейнеров

```mermaid
flowchart LR
    user[UserHost]
    subgraph dockerNet [DockerInternalNetwork]
        app["app FastAPI"]
        db["db PostgreSQL"]
        cache["cache Redis"]
        dbVolume[(db_data volume)]
    end

    user -->|HTTP 8000| app
    app -->|DATABASE_URL| db
    app -->|REDIS_URL| cache
    db -->|persist data| dbVolume
```

## Пояснение

- `app` публикует наружу порт `8000`, поэтому API доступен с хост-машины.
- `db` и `cache` работают во внутренней сети Docker и адресуются по именам сервисов `db` и `cache`.
- Постоянные данные PostgreSQL сохраняются в named volume `db_data`.
- Настройки подключения передаются через переменные окружения, а не захардкожены в коде.
