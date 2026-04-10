graph TB
    User[Пользователь] -->|HTTP :8000| API[FastAPI App]

    subgraph Docker Network
        API -->|Чтение/запись| DB[(PostgreSQL)]
        API -->|Кэширование| Cache[(Redis)]
    end

    DB -->|Хранение| VolumeDB[💾 persistent volume]
    Cache -->|Хранение| VolumeCache[💾 persistent volume]