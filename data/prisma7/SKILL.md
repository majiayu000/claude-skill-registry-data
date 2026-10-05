---
name: prisma7
description: Patrones de Prisma 7 para schema, migraciones y queries. Usa cuando trabajes con modelos de datos, consultas a la DB, o migraciones.
---

# Prisma 7 - Patrones PROSEGUIT

Cuando trabajes con la base de datos de PROSEGUIT, usa Prisma 7:

## Schema patterns
```prisma
generator client {
  provider = "prisma-client-js"
}

datasource db {
  provider = "postgresql"
  url      = env("DATABASE_URL")
}

model Equipo {
  id            Int            @id @default(autoincrement())
  serie         Int            @unique
  modelo        String?        @db.VarChar(100)
  tipoEquipo    TipoEquipo     @relation(fields: [tipoEquipoId], references: [id])
  tipoEquipoId  Int
  oficina       Oficina        @relation(fields: [oficinaId], references: [id])
  oficinaId     Int
  estado        EstadoEquipo   @default(ACTIVO)
  historial     Historial[]
  createdAt     DateTime       @default(now())
  updatedAt     DateTime       @updatedAt

  @@map("equipo")
}

enum EstadoEquipo {
  ACTIVO
  EN_REPARACION
  DADO_DE_BAJA
  EN_DEPOSITO
  PRESTADO
  EN_SERVICIO_EXTERNO

  @@map("estado_equipo")
}
```

## Query patterns
```typescript
// Buscar con relaciones incluidas
const equipo = await prisma.equipo.findUnique({
  where: { id },
  include: {
    tipoEquipo: true,
    oficina: { include: { seccion: { include: { ciudad: true } } } },
    historial: { orderBy: { fecha: 'desc' }, take: 20 }
  }
});

// Listado con filtros y paginacion
const equipos = await prisma.equipo.findMany({
  where: {
    ...(tipo && { tipoEquipoId: tipo }),
    ...(estado && { estado }),
    ...(search && {
      OR: [
        { modelo: { contains: search, mode: 'insensitive' } },
        { observacion: { contains: search, mode: 'insensitive' } }
      ]
    })
  },
  skip: (page - 1) * limit,
  take: limit,
  orderBy: { serie: 'desc' }
});

// Transaccion para acciones atomicas
await prisma.$transaction(async (tx) => {
  await tx.equipo.update({ where: { id }, data: { estado: 'EN_REPARACION', oficinaId: soporteId } });
  await tx.historial.create({ data: { equipoId: id, accion: 'ENVIO_SOPORTE', motivo, usuarioId } });
});
```

## Reglas
- Siempre usar transacciones cuando una accion modifica mas de una tabla
- Usar `include` para relaciones, no queries separadas
- Mapear modelos a nombres de tabla en espaniol con `@@map`
- Usar enums para valores fijos (estados, roles, tipos de accion)
