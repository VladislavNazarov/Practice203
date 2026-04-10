# Схема взаимодействия контейнеров

## Сетевая диаграмма

```mermaid
flowchart TB
	subgraph DockerNetwork["weather-net (bridge)"]
		App["weather-api\nFastAPI\nPort: 8000"]
		DB["postgres\nPostgreSQL 16\nPort: 5432"]
		Cache["redis\nRedis 7\nPort: 6379"]
	end

	Client["Client"] -->|"8080 -> 8000"| App
	App -->|"TCP 5432"| DB
	App -->|"TCP 6379"| Cache
	DB --- PgData["pg-data\n(named volume)"]

	style DockerNetwork fill:#e8f4f8,stroke:#333
	style App fill:#4CAF50,color:#fff
	style DB fill:#336791,color:#fff
	style Cache fill:#DC382D,color:#fff
```

## Описание

Все сервисы объединены в изолированную Docker-сеть `weather-net` (bridge driver).

| Сервис | Внутренний порт | Внешний порт | Описание |
|--------|----------------|--------------|----------|
| weather-api | 8000 | 8080 | REST API - единственный сервис с внешним доступом |
| postgres | 5432 | - | БД - доступна только внутри сети |
| redis | 6379 | - | Кэш - доступен только внутри сети |

### Volumes

- `pg-data` - named volume для persistent storage данных PostgreSQL

### Безопасность сети

- PostgreSQL и Redis не имеют пробросов на хост
- Доступ к БД и кэшу возможен только из контейнеров внутри `weather-net`
- Пароли передаются через переменные окружения, не хранятся в образе
