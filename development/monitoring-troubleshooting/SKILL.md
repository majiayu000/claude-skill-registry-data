---
name: Monitoring & Troubleshooting
description: Мониторинг и диагностика проблем
version: 2.0.0
author: Family Budget Team
tags: [monitoring, logs, metrics, troubleshooting, diagnostics, health-checks]
dependencies: [deployment]
---

# Monitoring & Troubleshooting Skill

Мониторинг приложения, анализ логов и диагностика проблем для проекта Family Budget.

## Когда использовать этот скил

Используй этот скил когда нужно:
- Проверить статус сервисов
- Проанализировать логи на ошибки
- Найти причину проблемы
- Проверить производительность
- Мониторить resource usage (CPU, memory, disk)
- Диагностировать database проблемы

Скил автоматически вызывается при запросах типа:
- "Покажи статус всех сервисов"
- "Найди ошибки в логах за последний час"
- "Почему backend не работает?"
- "Проверь производительность БД"

## Контекст проекта

Проект использует:
- **Docker Compose** для сервисов (postgres, backend, bot, nginx, certbot)
- **Structured logging** в JSON формате
- **Health checks** для всех сервисов (backend /health endpoint)
- **APScheduler** для background jobs (weekly reports, budget alerts)
- **PostgreSQL slow query log** и pg_stat_statements
- **UFW firewall** + **Docker DOCKER-USER chain** для безопасности

## Проверка статуса сервисов

### Быстрая проверка

```bash
# Статус всех сервисов
docker compose ps

# Health status
docker ps --format "table {{.Names}}\\t{{.Status}}\\t{{.Ports}}"

# С фильтрацией unhealthy
docker ps --filter "health=unhealthy"
```

### Детальная проверка

```bash
# Inspect конкретного сервиса
docker inspect familybudget-backend

# Health check details
docker inspect familybudget-backend | jq '.[0].State.Health'

# Network connectivity
docker compose exec backend ping postgres

# Port availability
docker compose port backend 8000
```

### Health endpoints

```bash
# Backend health
curl -s http://localhost:8000/health | jq .

# Expected response:
# {
#   "status": "healthy",
#   "database": "connected",
#   "timestamp": "2025-10-22T12:00:00"
# }

# PostgreSQL health
docker compose exec postgres pg_isready -U familybudget
```

## Анализ логов

### Поиск ошибок

```bash
# ERROR в backend логах
docker compose logs backend | grep ERROR

# ERROR за последний час
docker compose logs --since 1h backend | grep ERROR

# Все уровни ошибок
docker compose logs backend | grep -E "ERROR|CRITICAL|FATAL"

# С контекстом (5 строк до и после)
docker compose logs backend | grep -C 5 ERROR

# Count ошибок
docker compose logs backend | grep ERROR | wc -l
```

### Фильтрация логов по паттерну

```bash
# Exception traces
docker compose logs backend | grep -A 20 "Traceback"

# Database errors
docker compose logs backend | grep -i "database\|sql"

# Authentication errors
docker compose logs backend | grep -i "unauthorized\|forbidden\|401\|403"

# Slow queries
docker compose logs backend | grep "slow query"

# User specific errors
docker compose logs backend | grep "user_id=123"
```

### Анализ логов по времени

```bash
# Последние 100 строк
docker compose logs --tail=100 backend

# За последний час
docker compose logs --since 1h backend

# За конкретный период
docker compose logs --since "2025-10-22T10:00:00" --until "2025-10-22T11:00:00" backend

# Real-time monitoring
docker compose logs -f backend | grep ERROR
```

## Performance мониторинг

### Resource usage

```bash
# Docker stats (real-time)
docker stats

# Specific container
docker stats familybudget-backend

# Memory usage
docker stats --no-stream --format "table {{.Container}}\\t{{.MemUsage}}"

# CPU usage
docker stats --no-stream --format "table {{.Container}}\\t{{.CPUPerc}}"
```

### Disk usage

```bash
# Host disk space
df -h

# Docker disk usage
docker system df

# Detailed breakdown
docker system df -v

# Large log files
find /var/lib/docker/containers -name "*.log" -exec ls -lh {} \\; | sort -k5 -h -r | head -10
```

### Network monitoring

```bash
# Network connections
docker compose exec backend netstat -tulpn

# Active connections count
docker compose exec backend netstat -an | grep ESTABLISHED | wc -l

# Network I/O
docker stats --no-stream --format "table {{.Container}}\\t{{.NetIO}}"
```

## Database мониторинг

### PostgreSQL статистика

```bash
# Connection count
docker compose exec postgres psql -U familybudget -c "SELECT count(*) FROM pg_stat_activity;"

# Active queries
docker compose exec postgres psql -U familybudget -c "
SELECT pid, query_start, state, query
FROM pg_stat_activity
WHERE state != 'idle'
ORDER BY query_start;
"

# Slow queries (> 1s)
docker compose exec postgres psql -U familybudget -c "
SELECT pid, now() - query_start AS duration, query
FROM pg_stat_activity
WHERE state = 'active'
  AND now() - query_start > interval '1 second'
ORDER BY duration DESC;
"

# Database size
docker compose exec postgres psql -U familybudget -c "
SELECT pg_size_pretty(pg_database_size('familybudget'));
"

# Table sizes
docker compose exec postgres psql -U familybudget -c "
SELECT
    schemaname,
    tablename,
    pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename)) AS size
FROM pg_tables
WHERE schemaname = 'public'
ORDER BY pg_total_relation_size(schemaname||'.'||tablename) DESC
LIMIT 10;
"
```

### Database performance

```bash
# Index usage
docker compose exec postgres psql -U familybudget -c "
SELECT
    schemaname,
    tablename,
    indexname,
    idx_scan,
    idx_tup_read,
    idx_tup_fetch
FROM pg_stat_user_indexes
ORDER BY idx_scan DESC
LIMIT 20;
"

# Missing indexes (sequential scans)
docker compose exec postgres psql -U familybudget -c "
SELECT
    schemaname,
    tablename,
    seq_scan,
    seq_tup_read,
    idx_scan,
    seq_tup_read / NULLIF(seq_scan, 0) AS avg_seq_read
FROM pg_stat_user_tables
WHERE seq_scan > 0
ORDER BY seq_tup_read DESC
LIMIT 20;
"

# Cache hit ratio (should be > 99%)
docker compose exec postgres psql -U familybudget -c "
SELECT
    sum(heap_blks_read) as heap_read,
    sum(heap_blks_hit) as heap_hit,
    sum(heap_blks_hit) / (sum(heap_blks_hit) + sum(heap_blks_read)) * 100 AS cache_hit_ratio
FROM pg_statio_user_tables;
"
```

## Troubleshooting распространенных проблем

### Backend не запускается

**Симптомы:**
- `docker compose ps` показывает "Restarting" или "Exit 1"
- Health check fails

**Диагностика:**
```bash
# 1. Проверить логи
docker compose logs --tail=50 backend

# 2. Проверить .env
cat .env | grep -E "DATABASE_URL|JWT_SECRET|TELEGRAM_BOT_TOKEN"

# 3. Проверить PostgreSQL доступность
docker compose exec postgres pg_isready

# 4. Проверить migrations
docker compose exec backend alembic current
```

**Решение:**
```bash
# Fix .env если нужно
nano .env

# Restart
docker compose restart backend

# Rebuild если нужно
docker compose up -d --build backend
```

### База данных медленная

**Симптомы:**
- Запросы выполняются > 1s
- High CPU usage на postgres

**Диагностика:**
```bash
# 1. Найти slow queries
docker compose exec postgres psql -U familybudget -c "
SELECT pid, now() - query_start AS duration, query
FROM pg_stat_activity
WHERE state = 'active'
ORDER BY duration DESC;
"

# 2. Проверить missing indexes
# (см. "Database performance" выше)

# 3. Analyze table statistics
docker compose exec postgres psql -U familybudget -c "ANALYZE;"
```

**Решение:**
```bash
# Добавить indexes (через миграцию)
# Запустить VACUUM
docker compose exec postgres psql -U familybudget -c "VACUUM ANALYZE;"
```

### Disk space заполнен

**Симптомы:**
- `df -h` показывает > 90% usage
- Services failing с "no space left"

**Диагностика:**
```bash
# 1. Проверить disk usage
df -h

# 2. Найти большие файлы
find / -xdev -type f -size +100M -exec ls -lh {} \\; 2>/dev/null | sort -k5 -h -r | head -20

# 3. Docker disk usage
docker system df
```

**Решение:**
```bash
# Clean Docker
docker system prune -a

# Clean logs
docker compose exec postgres psql -U familybudget -c "
SELECT pg_ls_logdir();
"

# Rotate logs
sudo logrotate -f /etc/logrotate.conf

# Удалить old backups
find /opt/budget/backups -mtime +7 -delete
```

### Memory leak

**Симптомы:**
- Memory usage постоянно растет
- OOM Killer убивает контейнеры

**Диагностика:**
```bash
# 1. Track memory usage
docker stats --no-stream

# 2. Container memory
docker inspect familybudget-backend | jq '.[0].HostConfig.Memory'

# 3. Process memory inside container
docker compose exec backend ps aux --sort=-%mem | head -10
```

**Решение:**
```bash
# Restart affected service
docker compose restart backend

# Limit memory в docker-compose.yml:
# services:
#   backend:
#     deploy:
#       resources:
#         limits:
#           memory: 512M
```

## Alerts и notifications

### Критические метрики для мониторинга

**Сервисы:**
- All containers healthy
- Backend responding on /health
- PostgreSQL accepting connections

**Performance:**
- CPU usage < 80%
- Memory usage < 90%
- Disk usage < 85%
- Database cache hit ratio > 99%

**Errors:**
- No ERROR logs in last hour
- No 5xx responses
- No slow queries (> 5s)

### Скрипт для health check

```bash
#!/bin/bash
# health_check.sh

echo "=== Family Budget Health Check ==="
echo

# Check services
echo "Services:"
docker compose ps --format "table {{.Name}}\\t{{.Status}}" | grep -v "Up" && echo "⚠️  Some services down!" || echo "✅ All services running"
echo

# Check backend
echo "Backend API:"
curl -sf http://localhost:8000/health > /dev/null && echo "✅ Backend healthy" || echo "❌ Backend unhealthy"
echo

# Check PostgreSQL
echo "Database:"
docker compose exec -T postgres pg_isready -U familybudget > /dev/null && echo "✅ PostgreSQL ready" || echo "❌ PostgreSQL not ready"
echo

# Check disk
echo "Disk usage:"
DISK_USAGE=$(df -h / | awk 'NR==2 {print $5}' | sed 's/%//')
if [ $DISK_USAGE -gt 85 ]; then
    echo "⚠️  Disk usage: ${DISK_USAGE}% (> 85%)"
else
    echo "✅ Disk usage: ${DISK_USAGE}%"
fi
echo

# Check memory
echo "Memory:"
MEM_USAGE=$(free | awk 'NR==2 {printf "%.0f", $3/$2 * 100}')
if [ $MEM_USAGE -gt 90 ]; then
    echo "⚠️  Memory usage: ${MEM_USAGE}% (> 90%)"
else
    echo "✅ Memory usage: ${MEM_USAGE}%"
fi
```

## Проверочный чеклист

При возникновении проблем проверь:

- [ ] Все сервисы running (docker compose ps)
- [ ] Health checks проходят (curl /health)
- [ ] Логи без ERROR за последний час
- [ ] CPU usage < 80%
- [ ] Memory usage < 90%
- [ ] Disk usage < 85%
- [ ] PostgreSQL accepting connections
- [ ] Database cache hit ratio > 99%
- [ ] No slow queries (> 5s)
- [ ] UFW firewall active

## Связанные скилы

- **deployment**: для управления сервисами
- **db-management**: для диагностики БД
- **testing**: для проверки работоспособности

## Примеры использования

### Пример 1: Диагностика проблемы

```
Backend перестал отвечать. Проверь:
1. Статус контейнера
2. Логи за последние 10 минут
3. Database connectivity
4. Memory usage
Найди причину и предложи решение.
```

### Пример 2: Performance анализ

```
Проанализируй производительность:
1. Найди slow queries в PostgreSQL
2. Проверь cache hit ratio
3. Найди missing indexes
4. Проверь table bloat
Предложи оптимизации.
```

### Пример 3: Еженедельный health check

```
Выполни еженедельный health check:
1. Статус всех сервисов
2. Disk/memory/CPU usage
3. Ошибки в логах за неделю
4. Database performance metrics
5. Backup status
Создай отчет.
```

## Часто задаваемые вопросы

**Q: Как настроить automated alerts?**

A: Используй monitoring tools (Prometheus, Grafana) или cron + скрипты:
```bash
# /etc/cron.d/health-check
*/5 * * * * /opt/budget/scripts/health_check.sh | grep "❌" && /opt/budget/scripts/send_alert.sh
```

**Q: Как ротировать логи?**

A: Docker автоматически ротирует логи если настроено в docker-compose.yml:
```yaml
logging:
  driver: "json-file"
  options:
    max-size: "10m"
    max-file: "3"
```

**Q: Как мониторить production 24/7?**

A: Используй:
- Uptime monitoring (UptimeRobot, Pingdom)
- APM tools (New Relic, Datadog)
- Log aggregation (ELK stack, Loki)
- Alerting (PagerDuty, OpsGenie)
