---
name: docker
description: Docker для Node — эталонный multistage Dockerfile (node-slim, npm ci --omit=dev, non-root, HEALTHCHECK), оптимизация слоёв/размера, безопасность (.dockerignore, секреты не в слои), compose (healthcheck, force-recreate vs restart), типовые ошибки (ECONNREFUSED). Use для написания/ревью Dockerfile и docker-compose, починки сборки/поднятия.
---

# Навык: Docker для Node-проектов

Критерий готовности — вывод команд: `docker build` прошёл (размер показан), `docker compose ps` — все `healthy`.

## Multistage-эталон
`deps` (`COPY package*.json` → `npm ci` — слой кэшируется) → `build` (`COPY . .` после deps → `npm run build`) → `runner`: `node:22-slim` (пин, не `latest`), `NODE_ENV=production`, `npm ci --omit=dev`, `COPY --from=build /app/dist ./dist`, `USER node`, `EXPOSE`, `HEALTHCHECK ... CMD node -e "fetch('http://127.0.0.1:3000/health')..."`, `CMD ["node","dist/index.js"]`.

## Оптимизация
Манифесты до исходников (кэш `npm ci`); slim-база (~5x меньше; alpine — musl-риски у нативных модулей); в runner только артефакты; связанные `RUN` одним слоем с очисткой (`rm -rf /var/lib/apt/lists/*`); `.dockerignore` уменьшает контекст. Slim-Node обычно 150–300 MB; раздуто — смотри `docker history`.

## Безопасность
Non-root `USER node` в финальном stage. Секреты НЕ в слои: `COPY .env` и `ARG SECRET` запрещены (слои читаются `docker history`); runtime-`env` или BuildKit `--mount=type=secret`. `.dockerignore` обязательные строки: `node_modules`, `.git`, `.env*`, `dist`, `*.md`, `.github`. Пин версий всех образов.

## Compose и env-правило (критично)
- После изменения env/`.env`: `docker compose up -d --force-recreate`; `docker compose restart` НЕ перечитывает env.
- Healthcheck баз: `pg_isready` / `mongosh --eval "db.adminCommand('ping')"` / `redis-cli ping`; приложение — `depends_on: { db: { condition: service_healthy } }` (без condition — ждёт лишь старта).
- После поднятия: `compose ps` до `healthy` у всех + `logs --tail 50` без `ECONNREFUSED`/рестарт-циклов.

## Типовые ошибки
`ECONNREFUSED` между сервисами → `localhost` вместо **имени сервиса** compose; env «не применилась» → `restart` вместо `force-recreate`; падение на старте → нет `service_healthy`; «No open ports» на хостинге → слушать `0.0.0.0:$PORT`; данные пропали → `down -v` удалил volumes.
