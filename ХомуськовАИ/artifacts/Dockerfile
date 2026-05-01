# ============================================
# ЭТАП 1: СБОРКА (builder)
# ============================================
FROM python:3.11-slim as builder

WORKDIR /app

# Установка системных зависимостей для сборки
RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc && \
    rm -rf /var/lib/apt/lists/*

# Копируем зависимости (для кэширования)
COPY requirements.txt .

# Установка в виртуальное окружение
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"
RUN pip install --no-cache-dir -r requirements.txt

# ============================================
# ЭТАП 2: ВЫПОЛНЕНИЕ (runtime)
# ============================================
FROM python:3.11-slim

WORKDIR /app

# Создаём непривилегированного пользователя
RUN addgroup --system app && \
    adduser --system --no-create-home --ingroup app app

# Копируем виртуальное окружение из builder
COPY --from=builder /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Копируем код приложения
COPY app/ ./app/
COPY .env.example .env

# Устанавливаем владельца
RUN chown -R app:app /app
USER app

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]