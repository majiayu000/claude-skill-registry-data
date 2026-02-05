---
name: Deployment & DevOps
description: Управление деплоем и Docker контейнерами
version: 2.0.0
author: Family Budget Team
tags: [deployment, docker, docker-compose, devops, nginx, ssl]
dependencies: [db-management]
---

# Deployment & DevOps Skill

Автоматизация деплоя приложения и управления Docker контейнерами для проекта Family Budget.

## Когда использовать этот скил

Используй этот скил когда нужно:
- Задеплоить приложение на production/staging
- Управлять Docker сервисами (start, stop, restart)
- Просмотреть логи сервисов
- Проверить health статус сервисов
- Сделать backup базы данных
- Применить миграции на production

Скил автоматически вызывается при запросах типа:
- "Задеплой приложение на production"
- "Перезапусти backend сервис"
- "Покажи логи postgres за последний час"
- "Проверь health всех сервисов"

## Контекст проекта

Проект использует:
- **Docker 24+** & **Docker Compose v2** для контейнеризации
- **3 deployment скрипта**: install.sh, setup.sh, deploy.sh (ТОЛЬКО из ~/familyBudget)
- **2 Docker Compose профиля**: default (postgres + backend), full (+ bot + nginx + certbot)
- **3 Phases**: Phase 1 (Backend+Web), Phase 2 (Bot+ЦФО/МВЗ), Phase 3 (Telegram Web Apps)
- **UFW firewall** + **Docker firewall rules** (DOCKER-USER chain)
- **Health checks** для всех сервисов
- **Alembic** для миграций БД
- **Single Bridge Network** (172.28.0.0/16) для всех сервисов

## Deployment workflow

### Первоначальная установка (один раз)

```bash
# Шаг 1: Установка системных зависимостей (Docker, UFW, etc.)
sudo ./install.sh

# Шаг 2: Настройка .env и конфигурации
./setup.sh

# Шаг 3: Деплой приложения
./deploy.sh --profile full
```

### Обновление кода (regular updates)

```bash
# В git репозитории (например ~/familyBudget)
cd ~/familyBudget
git pull

# Синхронизация и deploy
./deploy.sh --sync-mode mirror
```

### Режимы синхронизации кода

```bash
# mirror: rsync --delete (рекомендуется)
# Защищены: .env, backups/, data/, logs/
./deploy.sh --sync-mode mirror

# update: только обновление/добавление файлов
./deploy.sh --sync-mode update

# clean: удалить ВСЁ кроме .env и backups/, затем скопировать
./deploy.sh --sync-mode clean

# skip: деплой без синхронизации кода
./deploy.sh --sync-mode skip
```

## Команды для управления сервисами

### Просмотр статуса

```bash
# Статус всех сервисов
docker compose ps

# Детальный статус с health
docker compose ps --format "table {{.Name}}\\t{{.Status}}\\t{{.Ports}}"

# Health check конкретного сервиса
docker inspect familybudget-backend | grep -A5 Health
```

### Управление сервисами

```bash
# Перезапуск сервиса
docker compose restart backend

# Остановка сервиса
docker compose stop backend

# Запуск сервиса
docker compose start backend

# Пересборка и перезапуск
docker compose up -d --build backend

# Остановка всех сервисов
docker compose down

# Запуск всех сервисов
docker compose up -d
```

### Просмотр логов

```bash
# Все логи (follow mode)
docker compose logs -f

# Логи конкретного сервиса
docker compose logs -f backend

# Последние 100 строк
docker compose logs --tail=100 backend

# Логи за последний час
docker compose logs --since 1h backend

# Фильтрация по ERROR
docker compose logs backend | grep ERROR

# Логи с timestamp
docker compose logs -f --timestamps backend
```

## Deployment опции

### Профили

```bash
# Default profile (postgres + backend)
./deploy.sh

# Full profile (+ bot + nginx + certbot)
./deploy.sh --profile full

# Specific services
docker compose up -d postgres backend bot
```

### Дополнительные опции

```bash
# Clean deployment (удаляет все данные!)
./deploy.sh --clean

# Foreground mode (show logs)
./deploy.sh --foreground

# Skip migrations
./deploy.sh --no-migrate

# Sync modes (non-interactive)
./deploy.sh --sync-mode mirror      # Recommended: rsync --delete
./deploy.sh --sync-mode update      # rsync без удаления старых файлов
./deploy.sh --sync-mode skip        # Deploy без синхронизации кода

# Комбинация опций
./deploy.sh --profile full --sync-mode mirror
./deploy.sh --sync-mode mirror --no-migrate
```

**Примечание:** Образы Docker **всегда пересобираются** автоматически при `docker compose up --build` (встроено в deploy.sh). Отдельного флага `--build` не существует.

## Health checks

### Backend health endpoint

```bash
# Check health
curl http://localhost:8000/health

# Expected response:
# {
#   "status": "healthy",
#   "database": "connected",
#   "timestamp": "2025-10-22T12:00:00"
# }
```

### PostgreSQL health

```bash
# From host
docker compose exec postgres pg_isready -U familybudget

# Connection test
docker compose exec postgres psql -U familybudget -d familybudget -c "SELECT 1"
```

### Docker health status

```bash
# Check all containers health
docker ps --filter "health=unhealthy"

# Show health status
docker inspect familybudget-backend --format='{{.State.Health.Status}}'
```

## Миграции на production

```bash
# Проверить текущую revision
docker compose exec backend alembic current

# Показать pending миграции
docker compose exec backend alembic heads

# Применить миграции
docker compose exec backend alembic upgrade head

# Откатить последнюю миграцию
docker compose exec backend alembic downgrade -1

# Откатить на конкретную revision
docker compose exec backend alembic downgrade abc123def456
```

## Backup и restore

### Backup базы данных

```bash
# Automatic backup (через скрипт)
./scripts/backup.sh

# Manual backup
docker compose exec postgres pg_dump -U familybudget familybudget > backup_$(date +%Y%m%d_%H%M%S).sql

# Backup с сжатием
docker compose exec postgres pg_dump -U familybudget familybudget | gzip > backup.sql.gz

# Backup в S3 (если настроено)
./scripts/backup.sh --destination s3
```

### Restore базы данных

```bash
# Stop services
docker compose down

# Restore from backup
cat backup.sql | docker compose exec -T postgres psql -U familybudget familybudget

# From compressed backup
gunzip -c backup.sql.gz | docker compose exec -T postgres psql -U familybudget familybudget

# Start services
docker compose up -d
```

## Troubleshooting

### Сервис не запускается

```bash
# 1. Проверить логи
docker compose logs backend

# 2. Проверить .env
grep DATABASE_URL .env

# 3. Проверить health
docker compose ps

# 4. Restart сервиса
docker compose restart backend

# 5. Пересборка если нужно
docker compose up -d --build backend
```

### База данных недоступна

```bash
# 1. Check PostgreSQL health
docker compose exec postgres pg_isready -U familybudget

# 2. Check logs
docker compose logs postgres

# 3. Restart PostgreSQL
docker compose restart postgres

# 4. Check connection string
echo $DATABASE_URL
```

### Порт занят

```bash
# Найти процесс
sudo lsof -i :8000

# Убить процесс
sudo kill -9 <PID>

# Или изменить порт в .env
nano .env
# BACKEND_PORT=8001

# Restart
docker compose down && docker compose up -d
```

### Полная перезагрузка

```bash
# Stop all
docker compose down

# Remove volumes (УДАЛЯЕТ ДАННЫЕ!)
docker compose down -v

# Clean deploy (automatically rebuilds images)
./deploy.sh --clean
```

## Monitoring

### Resource usage

```bash
# Docker stats
docker stats

# Disk usage
df -h

# Docker disk usage
docker system df

# Clean unused images/containers
docker system prune -a
```

### Network

```bash
# List networks
docker network ls

# Inspect network
docker network inspect familybudget

# Check connectivity
docker compose exec backend ping postgres
```

## Security checklist

Перед production deploy проверь:

- [ ] `.env` файл имеет permissions 600
- [ ] POSTGRES_PASSWORD сгенерирован (32+ символов)
- [ ] JWT_SECRET сгенерирован (64 hex символов)
- [ ] UFW firewall настроен (только 22, 80, 443)
- [ ] PostgreSQL external access отключен (или ограничен IP)
- [ ] SSL сертификаты настроены (для --profile full)
- [ ] Backup cronjob работает
- [ ] Health checks проходят
- [ ] Логирование настроено

## Проверочный чеклист после деплоя

- [ ] Все сервисы running (docker compose ps)
- [ ] Health checks проходят (curl /health)
- [ ] Backend доступен (curl http://localhost:8000/docs)
- [ ] PostgreSQL доступна (pg_isready)
- [ ] Миграции применены (alembic current)
- [ ] Bot отвечает в Telegram (если full profile)
- [ ] Логи без ERROR
- [ ] UFW firewall active
- [ ] Disk space достаточно (df -h)

## Связанные скилы

- **db-management**: для применения миграций
- **monitoring**: для мониторинга сервисов
- **testing**: для запуска тестов перед деплоем

## Примеры использования

### Пример 1: Production deploy

```
Задеплой приложение на production:
1. Синхронизируй код из репозитория (mirror mode)
2. Примени миграции
3. Restart всех сервисов
4. Проверь health checks
```

### Пример 2: Hotfix deploy

```
Сделай hotfix deploy:
1. Только backend сервис
2. Без миграций
3. Zero downtime (rolling update)
```

### Пример 3: Rollback

```
Откати последний deploy:
1. Откати миграции (-1)
2. Восстанови предыдущую версию кода
3. Restart сервисов
```

## Часто задаваемые вопросы

**Q: Как сделать zero-downtime deploy?**

A: Используй rolling update:
```bash
docker compose up -d --no-deps --build backend
```

**Q: Как проверить что миграции безопасны?**

A: Запусти на staging, проверь:
1. Migrations apply successfully
2. No data loss
3. Downgrade works
4. Performance не ухудшилась

**Q: Когда использовать --clean?**

A: ТОЛЬКО при критических проблемах или первоначальной установке. --clean УДАЛЯЕТ ВСЕ ДАННЫЕ кроме .env и backups/!
