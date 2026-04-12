## Выбор базового образа

`mcr.microsoft.com/dotnet/sdk:8.0-alpine`

Образ обеспечивает готовые зависимости с минимальным весом образа.

## Список используемых пересенных

| Переменная | Описание |
|----------|-------------|
| `BUILD_CONFIGURATION` | конфигурация сборки |
| `DB_HOST` | хост БД |
| `TOURNAMENT_DB_USER` | имя пользователя для подключения к PostgreSQL |
| `TOURNAMENT_DB_PASSWORD` | пароль для подключения к PostgreSQL |
| `REDIS_PASSWORD` | пароль для Redis |
| `ASPNETCORE_ENVIRONMENT` | окружение ASP.NetCore |
| `ASPNETCORE_URLS` | по какому адресу доступно приложение |