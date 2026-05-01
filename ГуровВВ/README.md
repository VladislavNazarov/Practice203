# Практика 203 — Git4CodeSys: Контейнеризация и оркестрация

**Студент:** Гуров Владислав  
**Проект:** Git4CodeSys – инструмент интеграции Git и Codesys

## Статус
Приложение и его зависимости (PostgreSQL, Redis) упакованы в Docker-контейнеры.  
Настроена автоматическая сборка и публикация образа в GitHub Container Registry (GHCR).

## Публичный образ
Образ доступен в GHCR: `ghcr.io/vladislavnazarov/git4codesys:latest`

## Запуск всей системы
```bash
docker-compose up -d
