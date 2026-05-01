## Казанцев Владислав Дмитриевич. Практика 3 (203): Контейнеризация и воспроизводимость


## Сервисы

- `reviewParsers`: сервис для парсинга.
- `db`: PostgreSQL 15 как основное хранилище
- `cache`: Redis 7.2 для кэширования

- GHCR image: `ghcr.io/gmerl1n/reviewparsers:latest `

### Команда для запуска всего проекта одной строкой
```bash
docker-compose up -d
```

## Документация 

- стратегия контейнеризации: [containerization_strategy.md](documentation/containerization_strategy.md)
- схема сети: [networking_schema.md](documentation/networking_schema.md)
- Dockerfile: [Dockerfile](artifacts/Dockerfile)
- orchestration: [docker-compose.yml](artifacts/docker-compose.yml)
- пример лога успешного: [registry_push_log.txt](artifacts/registry_push_log.txt)
