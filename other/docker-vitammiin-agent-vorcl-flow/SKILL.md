---
name: docker
description: Docker для Node-проектов — эталонный multistage Dockerfile (node-slim, npm ci --omit=dev, non-root, HEALTHCHECK), оптимизация слоёв и размера, безопасность (.dockerignore, секреты не в слои), docker-compose для локальной разработки (healthcheck, volumes, env), критичное правило force-recreate vs restart, типовые ошибки (ECONNREFUSED между сервисами). Use when пишешь/ревьюишь Dockerfile или docker-compose, чинишь сборку/поднятие контейнеров или применяешь env-изменения.
version: 1.0.0
---

# Навык: Docker для Node-проектов

Критерий готовности — не «Dockerfile написан», а **вывод команд**: `docker build` прошёл (размер образа показан), `docker compose ps` — все `healthy`.

## 1. Эталонный multistage Dockerfile (Node)
```dockerfile
# syntax=docker/dockerfile:1
FROM node:22-slim AS deps            # slim, версия пиненная — не latest
WORKDIR /app
COPY package*.json ./                # только манифесты — слой кэшируется,
RUN npm ci                          #   пока не меняются зависимости

FROM deps AS build
COPY . .                             # исходники — после deps: правка кода не сбрасывает кэш npm ci
RUN npm run build

FROM node:22-slim AS runner
WORKDIR /app
ENV NODE_ENV=production
COPY package*.json ./
RUN npm ci --omit=dev                # в финальном образе — только prod-зависимости
COPY --from=build /app/dist ./dist   # только артефакты, без исходников и devDeps
USER node                            # non-root: встроенный пользователь node
EXPOSE 3000
HEALTHCHECK --interval=30s --timeout=3s --retries=3 \
  CMD node -e "fetch('http://127.0.0.1:3000/health').then(r=>{if(!r.ok)process.exit(1)}).catch(()=>process.exit(1))"
CMD ["node", "dist/index.js"]
```

## 2. Оптимизация слоёв и размера
| Приём | Эффект |
|---|---|
| `COPY package*.json` до `COPY . .` | кэш `npm ci` живёт, пока не меняются зависимости |
| `node:XX-slim` вместо полного | ~5x меньше базы; `alpine` — ещё меньше, но musl-риски у нативных модулей |
| `npm ci --omit=dev` в runner | devDeps не попадают в прод-образ |
| Multistage: в runner только артефакты | нет исходников, кэшей сборки, `.git` |
| Один `RUN` на связанные шаги (`apt-get update && install && rm -rf /var/lib/apt/lists/*`) | меньше слоёв, мусор не фиксируется в слое |
| `.dockerignore` | меньше build-контекст → быстрее и чище сборка |

Проверка размера: `docker image ls <tag>` — Node-приложение на slim обычно 150–300 MB; сильно больше — ищи devDeps/исходники в финальном слое (`docker history <tag>`).

## 3. Безопасность
- **Non-root:** `USER node` (или свой uid) в финальном stage; root в контейнере — root на хосте при побеге.
- **Секреты не в слои:** `COPY .env` и `ARG SECRET=...` запрещены — слои неудаляемы и читаются `docker history`. Секреты — runtime-`env` (compose `env_file`, оркестратор) или BuildKit `--mount=type=secret` для build-time.
- **`.dockerignore` — обязательные строки:** `node_modules`, `.git`, `.env*`, `dist`, `*.md`, `.github`, `Dockerfile*`, `docker-compose*`.
- Пин версий образов (`node:22-slim`, `postgres:16`), не `latest` — воспроизводимость и локалка ≈ прод.

## 4. HEALTHCHECK-паттерны
- HTTP-сервис: `node -e "fetch(...)"` (без curl в slim) или поставь `curl` и `CMD curl -f http://127.0.0.1:3000/health || exit 1`.
- В compose у баз: `pg_isready -U $POSTGRES_USER` (postgres), `mongosh --quiet --eval "db.adminCommand('ping')"` (mongo), `redis-cli ping` (redis).
- Приложение стартует после баз: `depends_on: { postgres: { condition: service_healthy } }` — `depends_on` без condition ждёт лишь старта контейнера, не готовности.

## 5. docker compose: env-правило (критично)
```bash
docker compose up -d --force-recreate   # ПОСЛЕ изменения env/.env — пересоздаёт контейнеры с новыми переменными
docker compose restart                  # НЕ перечитывает env — переменные останутся старыми!
```
После поднятия — дождись `healthy` у всех: `docker compose ps` (колонка STATUS); проверь `docker compose logs --tail 50` на `ECONNREFUSED` и циклы перезапуска (`Restarting (1)`). Изменился только код при `build:` — достаточно `docker compose up -d --build`.

## 6. Типовые ошибки
| Симптом | Первопричина |
|---|---|
| `ECONNREFUSED` между сервисами | в строке подключения `localhost` вместо **имени сервиса** compose (`postgres`, `redis`); localhost внутри контейнера — сам контейнер |
| env-переменная «не применилась» | сделан `restart` вместо `up -d --force-recreate` |
| Приложение падает на старте: БД недоступна | нет `depends_on` + `condition: service_healthy`, база ещё не готова |
| «No open ports detected» на хостинге | слушает `127.0.0.1`/хардкод-порт — надо `0.0.0.0:$PORT` |
| Образ раздут / секрет в образе | нет multistage/`.dockerignore`, `COPY . .` в финальный слой; смотри `docker history` |
| Данные БД пропали после `down` | `docker compose down -v` удалил volumes — `-v` только осознанно |
