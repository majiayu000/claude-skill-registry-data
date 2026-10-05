---
name: dev-setup
description: Levantar el entorno de desarrollo completo de PROSEGUIT. Usa cuando necesites iniciar Docker, instalar dependencias, correr migraciones o arrancar los servidores de desarrollo.
allowed-tools: Bash(docker *), Bash(npm *), Bash(npx prisma *)
argument-hint: "[db|backend|frontend|all]"
---

# Dev Setup - PROSEGUIT

Levanta el entorno de desarrollo del proyecto.

## Sin argumentos o "all": entorno completo

1. **Verificar Docker** esta corriendo
   ```bash
   docker info > /dev/null 2>&1 || echo "ERROR: Docker no esta corriendo"
   ```

2. **Levantar PostgreSQL**
   ```bash
   docker compose up -d postgres
   ```

3. **Instalar dependencias**
   ```bash
   npm install
   ```

4. **Correr migraciones**
   ```bash
   cd backend && npx prisma migrate dev && cd ..
   ```

5. **Generar Prisma Client**
   ```bash
   cd backend && npx prisma generate && cd ..
   ```

6. **Arrancar servidores**
   ```bash
   # En terminales separadas:
   cd backend && npm run dev
   cd frontend && npm run dev
   ```

## Argumento "db": solo base de datos
```bash
docker compose up -d postgres
cd backend && npx prisma migrate dev && cd ..
```

## Argumento "backend": solo backend
```bash
cd backend && npm install && npm run dev
```

## Argumento "frontend": solo frontend
```bash
cd frontend && npm install && npm run dev
```

## Migración de datos desde seguit v1

Cuando se trae un dump SQL de seguit v1 (`db_seguit1.sql`):

1. Colocar `db_seguit1.sql` en la raíz del proyecto (`PROSEGUIT/`)
2. Asegurarse de que la DB esté corriendo: `docker compose up -d postgres`
3. Correr el comando único de migración:
   ```bash
   npm run migrate:v1
   ```

El comando encadena automáticamente:
- `node extract_data.js` — extrae datos del SQL a JSON
- Pre-flight checks: verifica conexión, detecta y repara migraciones incompletas (`estado_equipo_old`)
- `prisma migrate deploy` — aplica migraciones pendientes
- `prisma generate` — regenera el cliente
- Importación completa de datos (ubicaciones, tipos, usuarios, equipos, historial, préstamos)

## Verificar que todo funciona
- PostgreSQL: `docker compose ps` (debe mostrar postgres healthy)
- Backend: http://localhost:3001/api/v1/health
- Frontend: http://localhost:5173

## Troubleshooting
- Si el puerto 5433 esta ocupado: `docker compose down && docker compose up -d postgres`
- Si Prisma falla: `cd backend && npx prisma migrate reset --force`
- Si npm falla: borrar `node_modules` y reinstalar
- Si migrate:v1 falla con "export_datos_v1.json no encontrado": verificar que `db_seguit1.sql` está en la raíz
- Si migrate:v1 falla con "No se puede conectar": correr `npm run db:up` primero
