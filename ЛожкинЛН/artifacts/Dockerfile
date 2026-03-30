# syntax=docker/dockerfile:1

# --- Stage 1: Base ---
FROM oven/bun:1 AS base
WORKDIR /app

# --- Stage 2: Dependencies ---
FROM base AS deps

COPY package.json bun.lock ./
COPY api/package.json ./api/
COPY bot/package.json ./bot/
COPY alert-relay/package.json ./alert-relay/
COPY web/package.json ./web/
COPY packages/db/package.json ./packages/db/
COPY packages/db/prisma ./packages/db/prisma/
COPY packages/logger/package.json ./packages/logger/
COPY packages/types/package.json ./packages/types/
COPY packages/shared/package.json ./packages/shared/

RUN bun install --filter '@projectlpn/api' --frozen-lockfile

# --- Stage 3: Builder ---
FROM base AS builder
WORKDIR /app

COPY --from=deps /app/node_modules ./node_modules

COPY package.json bun.lock ./
COPY api ./api
COPY packages/db ./packages/db
COPY packages/logger ./packages/logger
COPY packages/shared ./packages/shared
COPY bot/package.json ./bot/package.json
COPY alert-relay/package.json ./alert-relay/package.json
COPY web/package.json ./web/package.json
COPY packages/types ./packages/types

RUN bun install --filter '@projectlpn/api' --frozen-lockfile
RUN cd packages/db && bunx prisma generate

WORKDIR /app/api
RUN bun run build

# --- Stage 4: Runner ---
FROM oven/bun:1-slim AS runner
WORKDIR /app

RUN apt-get update && \
    apt-get install -y --no-install-recommends openssh-client ca-certificates && \
    rm -rf /var/lib/apt/lists/*

RUN groupadd --gid 1001 appuser && \
    useradd --uid 1001 --gid appuser --shell /bin/bash --create-home appuser && \
    mkdir -p /home/appuser/.ssh && \
    chown -R appuser:appuser /home/appuser/.ssh

ENV NODE_ENV=production

COPY --from=builder --chown=appuser:appuser /app/node_modules ./node_modules
COPY --from=builder --chown=appuser:appuser /app/api/dist/index.js ./index.js

USER appuser

EXPOSE 3000
CMD ["bun", "index.js"]
