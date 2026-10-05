---
name: db-query
description: Consultar la base de datos PostgreSQL de PROSEGUIT, explorar schema, correr migraciones Prisma, y verificar datos. Usa para cualquier operacion de base de datos.
allowed-tools: Bash(npx prisma *), Bash(docker exec *)
argument-hint: "[consulta SQL o comando prisma]"
---

# DB Query - PROSEGUIT

Interactua con la base de datos PostgreSQL del proyecto.

## Conexion
- **Host**: localhost:5432
- **Database**: proseguit
- **User**: proseguit
- **Password**: proseguit

## Consultas SQL directas
```bash
docker exec -i proseguit-postgres psql -U proseguit -d proseguit -c "$ARGUMENTS"
```

## Explorar schema actual
```bash
cd backend && npx prisma db pull && npx prisma format
```

## Ver schema Prisma
Lee el archivo `backend/prisma/schema.prisma`

## Crear migracion
```bash
cd backend && npx prisma migrate dev --name "$ARGUMENTS"
```

## Resetear base de datos (CUIDADO)
```bash
cd backend && npx prisma migrate reset --force
```

## Generar Prisma Client despues de cambios al schema
```bash
cd backend && npx prisma generate
```

## Abrir Prisma Studio (UI visual de la DB)
```bash
cd backend && npx prisma studio
```

## Ver estado de migraciones
```bash
cd backend && npx prisma migrate status
```

## Contar registros por tabla
```bash
docker exec -i proseguit-postgres psql -U proseguit -d proseguit -c "
SELECT schemaname, relname AS table, n_live_tup AS row_count
FROM pg_stat_user_tables ORDER BY n_live_tup DESC;
"
```

## Reglas
- Siempre usar LIMIT en consultas de exploracion
- Nunca hacer DROP o DELETE sin confirmacion del usuario
- Preferir Prisma para migraciones, SQL directo solo para consultas
