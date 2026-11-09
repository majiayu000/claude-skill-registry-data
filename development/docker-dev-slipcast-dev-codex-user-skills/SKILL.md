---
name: docker-dev
description: "Контейнеризация и локальная разработка через Docker: Dockerfile, docker-compose, multi-stage сборка, networking"
whenToUse: "Применяй, когда нужно упаковать приложение в Docker, поднять окружение через docker compose или настроить dev-контейнер"
---

# Docker Dev

Гайд по контейнеризации и локальной разработке.

## Чек-лист

### Dockerfile
- [ ] Используй multi-stage сборку (build → runtime) для малых образов
- [ ] Фиксируй версии базовых образов (python:3.12-slim, node:20-alpine)
- [ ] Копируй только нужное (`.dockerignore`: node_modules, .git, .env)
- [ ] Non-root пользователь в контейнере (безопасность)
- [ ] Не храни секреты в образе (используй env/секреты в рантайме)

### docker-compose
- [ ] Сервисы: app, db, cache — каждый отдельно
- [ ] Healthcheck для зависимостей (`depends_on: condition: service_healthy`)
- [ ] Тома для данных и hot-reload (монтирование кода)
- [ ] Сеть между сервисами, порты наружу только нужные
- [ ] Env через `.env` (не коммить)

### Разработка
- [ ] `docker compose up -d` поднимает всё окружение
- [ ] Логи: `docker compose logs -f <service>`
- [ ] Пересборка при изменении зависимостей: `--build`
- [ ] Dev hot-reload через volume-mount кода

### Оптимизация и безопасность
- [ ] Слой кэширования: зависимости отдельно от кода
- [ ] Минимальный базовый образ (alpine/slim/distroless)
- [ ] Сканирование уязвимостей (`docker scout` / trivy)
- [ ] Multi-arch сборка при необходимости

## Правила
1. Образ должен быть минимальным и воспроизводимым.
2. Секреты — только через env/secret-manager, не в Dockerfile.
3. Один процесс на контейнер (12-factor).
4. Проверяй size: `docker images` перед пушем.
