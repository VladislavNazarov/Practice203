# Схема взаимодействия контейнеров

## Диаграмма

```mermaid
graph TB
    subgraph "Внешняя сеть"
        Client[Пользователь]
    end

    subgraph "Docker Network: epstein_network"
        App[App Container<br/>FastAPI<br/>:8000]
        DB[DB Container<br/>PostgreSQL 15<br/>:5432]
        Cache[Cache Container<br/>Redis 7<br/>:6379]
    end

    subgraph "Volume (персистентность)"
        Volume[postgres_data]
    end

    Client -->|HTTP запросы :8000| App
    App -->|SQL запросы :5432| DB
    App -->|Кэширование :6379| Cache
    DB -.->|Сохранение данных| Volume
```

## Описание взаимодействия

1. **Пользователь** → отправляет HTTP-запросы на порт `8000`
2. **App Container** → принимает запросы, обрабатывает бизнес-логику
3. **App** → подключается к PostgreSQL для чтения/записи данных
4. **App** → использует Redis для кэширования частых запросов
5. **PostgreSQL** → сохраняет данные в volume (персистентность)

## Изоляция

Все три сервиса находятся в одной пользовательской сети `epstein_network`:
- Внутренняя изоляция от других контейнеров
- Доступ по именам сервисов (`db`, `cache`, `app`)
- Порты БД и Redis не публикуются наружу (только внутренние)