# Стратегия контейнеризации

## Выбор базового образа

| Этап | Образ | Обоснование |
|------|-------|-------------|
| **base / deps / builder** | `oven/bun:1` | Полный Bun-образ с инструментами сборки, необходим для `bun install` и компиляции TypeScript |
| **runner** | `oven/bun:1-slim` | Минимальный образ с Bun runtime без лишних пакетов, ~150 МБ |

Альтернативы:
- `alpine` — не подходит, Bun пока не имеет стабильной alpine-сборки
- `distroless` — не подходит, нужен shell для health check и SSH-клиент для API
- `node:20-slim` — подходит, но Bun даёт лучшую производительность при старте и потреблении памяти

## Multi-stage сборка

Сборка API-сервиса проходит через 4 этапа:

```
┌─────────────────────────────────────────────────┐
│ Stage 1: base                                   │
│   oven/bun:1, WORKDIR /app                      │
├─────────────────────────────────────────────────┤
│ Stage 2: deps                                   │
│   Копирование package.json всех workspace'ов    │
│   bun install --filter '@projectlpn/api'        │
│   (только зависимости целевого пакета)          │
├─────────────────────────────────────────────────┤
│ Stage 3: builder                                │
│   Копирование исходников                        │
│   prisma generate + bun run build               │
│   Результат: dist/index.js (один файл)          │
├─────────────────────────────────────────────────┤
│ Stage 4: runner                                 │
│   oven/bun:1-slim, non-root user (appuser)      │
│   Копируется только node_modules + index.js     │
│   CMD ["bun", "index.js"]                       │
└─────────────────────────────────────────────────┘
```

### Сравнение размера образа

| Вариант | Размер |
|---------|--------|
| Без multi-stage (весь monorepo + node_modules + исходники) | ~1.2 ГБ |
| Multi-stage (runtime + node_modules + dist/index.js) | ~200 МБ |
| **Сокращение** | **~83%** |

### Оптимизация кэширования слоёв

1. Сначала копируются только `package.json` и `bun.lock` — слой зависимостей пересобирается только при изменении lockfile
2. `--filter` устанавливает только нужные workspace-зависимости
3. `--frozen-lockfile` гарантирует воспроизводимость
4. Исходники копируются последним слоем — при изменении кода зависимости берутся из кэша

## Безопасность

- **Non-root user:** создаётся `appuser` (UID 1001), процесс запускается от его имени
- **Минимальная поверхность атаки:** в runner-образе только runtime и скомпилированный файл
- **`--no-install-recommends`:** при установке системных пакетов в API (openssh-client, ca-certificates)
- **Очистка кэша:** `rm -rf /var/lib/apt/lists/*` после apt-get

## Управление переменными окружения (ENV)

### Приложение

| Переменная | Назначение | Пример |
|------------|------------|--------|
| `NODE_ENV` | Режим работы | `production` |
| `PORT` | Порт API-сервера | `3000` |
| `DATABASE_URL` | Строка подключения к PostgreSQL | `postgresql://user:pass@postgres:5432/db` |
| `BOT_TOKEN` | Токен Telegram-бота | `123456:ABC...` |
| `API_BASE_URL` | URL API для бота | `http://api:3000` |
| `API_ADMIN_TOKEN` | Токен админ-доступа к API | `secret-token` |

### Хранилище (MinIO / S3)

| Переменная | Назначение | Пример |
|------------|------------|--------|
| `S3_ENDPOINT` | URL MinIO | `http://minio:9000` |
| `S3_ACCESS_KEY_ID` | Ключ доступа | `minioadmin` |
| `S3_SECRET_ACCESS_KEY` | Секретный ключ | `minioadmin` |
| `S3_BUCKET_RECEIPTS` | Бакет для чеков | `receipts` |

### База данных

| Переменная | Назначение | Пример |
|------------|------------|--------|
| `POSTGRES_USER` | Пользователь БД | `lpn` |
| `POSTGRES_PASSWORD` | Пароль БД | `secret` |
| `POSTGRES_DB` | Имя базы | `projectlpn` |

### Мониторинг

| Переменная | Назначение | Пример |
|------------|------------|--------|
| `GRAFANA_ADMIN_PASSWORD` | Пароль админа Grafana | `admin123` |
| `BOT_SUPPORT_CHAT_ID` | Chat ID для алертов | `-100123456` |

Все секреты хранятся в `.env` файле (не коммитится) и передаются через `env_file` в docker-compose.

## CI/CD: Сборка и Push

Workflow `docker.yml` собирает и пушит 5 образов в GHCR при создании тега `v*.*.*` или push в `staging`:

- Используется **matrix strategy** для параллельной сборки
- **Docker Buildx** с GitHub Actions Cache (`cache-from: type=gha`)
- Теги: semver (`v1.2.3`), `sha-<commit>`, `latest`
- При push в `staging` автоматически деплоится на staging-сервер
