# Стратегия контейнеризации

## 1. Выбор базового образа

### Backend — `eclipse-temurin:21-jre-alpine`

Для runtime-слоя выбран минимальный JRE-образ на базе Alpine Linux.

Причины:
- **Размер:** `eclipse-temurin:21-jre-alpine` весит ~60 MB, тогда как полноценный `eclipse-temurin:21-jdk` — ~400 MB. Для production нужен только JRE, компилятор не требуется.
- **Alpine:** минимальная attack surface — меньше пакетов → меньше потенциальных уязвимостей.
- **Temurin:** официальная сборка Eclipse Adoptium, совместимая с Spring Boot 3.4.
- **Container support:** образ поддерживает `-XX:+UseContainerSupport` и `-XX:MaxRAMPercentage`, что важно для корректной работы JVM внутри контейнера с ограничениями памяти.

### Frontend (build stage) — `node:20-alpine`

Используется только на этапе сборки. В итоговый образ попадает только статика (`build/`), Node.js в runtime не нужен.

### Database — `postgres:17-alpine`
### Cache — `redis:7-alpine`

Оба сервиса используют Alpine-варианты для экономии места.

## 2. Управление ENV

| Переменная | Назначение | Пример значения |
|-----------|-----------|----------------|
| `SPRING_PROFILES_ACTIVE` | Профиль Spring Boot | `production` |
| `SERVER_PORT` | Порт приложения внутри контейнера | `8080` |
| `JAVA_OPTS` | JVM-флаги (контейнерная поддержка, % RAM) | `-XX:+UseContainerSupport -XX:MaxRAMPercentage=75.0` |
| `SPRING_DATASOURCE_URL` | JDBC-строка подключения к PostgreSQL | `jdbc:postgresql://db:5432/sanatorium_db` |
| `SPRING_DATASOURCE_USERNAME` | Пользователь PostgreSQL | `sanatorium` |
| `SPRING_DATASOURCE_PASSWORD` | Пароль PostgreSQL | `sanatorium_secret` |
| `SPRING_JPA_HIBERNATE_DDL_AUTO` | Стратегия обновления схемы БД | `update` |
| `POLYTECHNIK_APP_JWTSECRET` | Секретный ключ для подписи JWT | (выносится в secrets) |
| `POLYTECHNIK_APP_JWTEXPIRATIONMS` | Время жизни токена (мс) | `86400000` (24 ч) |
| `POLYTECHNIK_APP_CORS_ALLOWEDORIGINS` | Разрешённые CORS-источники | `http://localhost:3000` |
| `NEWS_UPLOAD_DIR` | Путь для загрузки изображений новостей | `/app/uploads/news` |
| `POSTGRES_DB` | Имя базы данных | `sanatorium_db` |
| `POSTGRES_USER` | Пользователь PostgreSQL | `sanatorium` |
| `POSTGRES_PASSWORD` | Пароль PostgreSQL | `sanatorium_secret` |

## 3. Оптимизация

Применённые методы:

- **Multi-stage build (3 этапа):**
  1. `frontend-build` — компиляция React-приложения (Node.js, удаляется после копирования статики)
  2. `backend-build` — сборка Maven (JDK, удаляется после копирования JAR)
  3. `runtime` — только JRE + JAR + статика

- **Порядок слоёв:** зависимости копируются раньше кода, чтобы Docker кэшировал тяжёлый `mvn dependency:go-offline`.

- **Исключение dev-зависимостей:** в runtime-слой не попадают тесты, исходники, `.git`, IDE-файлы.

- **Непривилегированный пользователь:** приложение запускается от `appuser`, а не от `root`.

- **Контейнерная JVM:** `UseContainerSupport` + `MaxRAMPercentage=75.0` — JVM корректно определяет лимиты памяти контейнера.

## 4. Вывод

Контейнеризация обеспечивает:
- воспроизводимость — одинаковый образ локально, в CI и на продакшене
- изоляцию — БД и Redis в отдельных контейнерах во внутренней сети
- минимальный runtime — Alpine JRE без компиляторов и dev-инструментов
