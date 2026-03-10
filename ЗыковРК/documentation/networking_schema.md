# Схема взаимодействия контейнеров

## Диаграмма (Mermaid)

```mermaid
graph TD
    subgraph "Docker network: vrkayak_net"
        App["app (ASP.NET Core)\nпорт 80 (internal)"]
        DB["db (PostgreSQL 15)\nпорт 5432 (internal)"]
        Cache["cache (Redis 7)\nпорт 6379 (internal)"]
    end

    Client((Клиент / Тренер)) -->|HTTP :8080| App
    App -->|postgresql://| DB
    App -->|redis://| Cache

    style App fill:#e1f5fe,stroke:#01579b
    style DB fill:#fff9c4,stroke:#fbc02d
    style Cache fill:#ffccbc,stroke:#e65100