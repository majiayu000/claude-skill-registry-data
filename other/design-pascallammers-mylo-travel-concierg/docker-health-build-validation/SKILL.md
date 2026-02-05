---
name: "Docker Health & Build Validation"
description: "Valida la configuración de Docker, construye imágenes y verifica que todos los servicios arranquen correctamente. Chequea health endpoints del backend, frontend y bases de datos."
trigger-phrases: ["test docker", "validate docker", "docker health check", "test build", "docker-compose check"]
allowed-tools: ["bash", "read"]
---

# 🐳 Docker Health & Build Validation

Valida que la configuración de Docker sea correcta y que todos los servicios funcionen localmente antes de desplegar.

## Proceso de Validación

### 1️⃣ Validar Configuración de docker-compose.yml

```bash
# Verificar sintaxis YAML
docker-compose config > /dev/null

# Listar servicios
docker-compose config --services
```

**Servicios esperados:**
- postgres (Puerto 5432)
- redis (Puerto 6379)
- qdrant (Puerto 6333)
- backend (Puerto 3001)
- frontend (Puerto 3000/3011)

### 2️⃣ Construir Imágenes Docker

```bash
# Backend
cd backend
docker build -t bip2-backend:latest .

# Frontend
cd frontend
docker build -t bip2-frontend:latest .
```

**Validaciones:**
- ✓ Builds completados sin errores
- ✓ Imágenes creadas correctamente
- ✓ Tamaños razonables (no tienen megabytes innecesarios)

### 3️⃣ Iniciar Servicios

```bash
docker-compose up -d
```

**Esperar a que se estabilicen (15-30 segundos)**

### 4️⃣ Verificar Servicios Corriendo

```bash
docker-compose ps
```

Todos deben estar en estado `running` (no `exited` o `restarting`)

### 5️⃣ Chequear Health Endpoints

**Backend - Health Check General:**
```bash
curl -s http://localhost:3001/api/health | jq .
```

Respuesta esperada:
```json
{
  "status": "healthy",
  "timestamp": "...",
  "services": {
    "database": {"healthy": true},
    "qdrant": {"healthy": true},
    "redis": {"healthy": true}
  }
}
```

**Backend - Health Database:**
```bash
curl -s http://localhost:3001/api/health/database | jq .
```

**Backend - Health Redis:**
```bash
curl -s http://localhost:3001/api/health/redis | jq .
```

**Backend - Health Qdrant:**
```bash
curl -s http://localhost:3001/api/health/qdrant | jq .
```

**Frontend - Page Load:**
```bash
curl -s http://localhost:3011 | grep -q "title" && echo "✓ Frontend respondiendo"
```

### 6️⃣ Verificar Logs

```bash
# Últimas líneas de cada servicio
docker-compose logs backend --tail=20
docker-compose logs frontend --tail=20
docker-compose logs postgres --tail=10
docker-compose logs redis --tail=10
docker-compose logs qdrant --tail=10
```

**Buscar errores críticos:**
- ❌ Connection refused
- ❌ FATAL
- ❌ Error: Cannot find module
- ❌ Segmentation fault

### 7️⃣ Validar Volúmenes

```bash
# Verificar que los datos persisten
ls -la data/postgres/
ls -la data/redis/
ls -la data/qdrant/
```

### 8️⃣ Chequear Conectividad Inter-Servicios

```bash
# Backend puede conectar a DB desde dentro del container
docker-compose exec backend npm run typeorm -- query "SELECT 1"

# Backend puede contactar Redis
docker-compose exec backend redis-cli -h redis ping

# Backend puede contactar Qdrant
docker-compose exec backend curl -s http://qdrant:6333/health | jq .
```

### 9️⃣ Validar Variables de Entorno

```bash
docker-compose exec backend env | grep -E "GEMINI|QDRANT|DATABASE|REDIS|JWT"
```

Verificar que:
- ✓ Todas las vars necesarias están presentes
- ✓ Los valores son los esperados (no vacíos)
- ✓ Las URLs internas usan nombres de container (qdrant, postgres, redis)

### 🔟 Cleanup

Si todo pasó:
```bash
docker-compose down
```

Si hay errores, dejar containers corriendo para inspeccionar.

## Salida Esperada

```
✅ DOCKER BUILD & HEALTH CHECK REPORT
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📋 Configuración:
✓ docker-compose.yml sintaxis válida
✓ 5 servicios configurados correctamente

🏗️  Build:
✓ Backend image construida (125MB)
✓ Frontend image construida (850MB)

🚀 Servicios:
✓ postgres running
✓ redis running
✓ qdrant running
✓ backend running
✓ frontend running

❤️  Health Checks:
✓ Backend health: HEALTHY
  - Database: ✓
  - Qdrant: ✓
  - Redis: ✓
✓ Frontend respondiendo
✓ PostgreSQL: conectado
✓ Redis: ping OK
✓ Qdrant: health OK

💾 Volúmenes:
✓ data/postgres: 15MB
✓ data/redis: 2MB
✓ data/qdrant: 5MB

🌍 Conectividad:
✓ Backend↔Database OK
✓ Backend↔Redis OK
✓ Backend↔Qdrant OK

✅ TODO OK - LISTO PARA PRODUCCIÓN
```

O en caso de problemas:

```
❌ DOCKER VALIDATION FAILED
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🔴 Backend build FALLÓ
   Error: Cannot find module '@nestjs/common'
   → Solución: Ejecutar npm install en backend/

🔴 postgres no inicia
   Error: FATAL: password authentication failed
   → Verificar DATABASE_PASSWORD en .env

⚠️  Frontend tardó mucho en cargar
   Consejo: Verificar memoria disponible

🔧 PRÓXIMOS PASOS:
1. Revisa los errores arriba
2. Ejecuta: docker-compose down -v
3. Soluciona los issues
4. Vuelve a ejecutar este check
```

## Uso

Invoca este skill cuando quieras validar tu setup local:

```
"Valida que Docker funcione bien"
"Test docker build and health"
"¿Está todo correcto en Docker?"
"Antes de hacer push, validación de Docker"
```

Claude automáticamente ejecutará todas las validaciones y te reportará el estado.