FROM python:3.12-slim AS builder

ENV VENV_PATH=/opt/venv \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_NO_CACHE_DIR=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

RUN apt-get update \
    && apt-get install -y --no-install-recommends build-essential libpq-dev \
    && python -m venv "${VENV_PATH}" \
    && "${VENV_PATH}/bin/pip" install --upgrade pip \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /build

COPY sincslot/backend/requirements.txt ./requirements.txt
RUN "${VENV_PATH}/bin/pip" install -r requirements.txt


FROM python:3.12-slim AS runtime

ENV VENV_PATH=/opt/venv \
    PATH="/opt/venv/bin:${PATH}" \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app/sincslot \
    SYNC_SLOT__RUN__HOST=0.0.0.0

RUN apt-get update \
    && apt-get install -y --no-install-recommends libpq5 \
    && useradd --create-home --home-dir /home/appuser --shell /usr/sbin/nologin appuser \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app/sincslot/backend

COPY --from=builder /opt/venv /opt/venv
COPY --chown=appuser:appuser sincslot/backend /app/sincslot/backend

RUN mkdir -p /app/sincslot/backend/storage \
    && chown -R appuser:appuser /app/sincslot/backend

USER appuser

EXPOSE 10004

CMD ["sh", "-c", "alembic upgrade head && uvicorn main:app --host 0.0.0.0 --port 10004"]
