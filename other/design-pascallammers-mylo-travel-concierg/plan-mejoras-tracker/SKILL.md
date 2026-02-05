---
name: plan-mejoras-tracker
description: Documenta progreso y marca tareas completadas en PLAN_MEJORAS.md. Usa SIEMPRE después de completar cualquier tarea del plan de mejoras.
allowed-tools: Read, Write, Edit
---

# Plan Mejoras Tracker

Skill para documentar progreso en el plan de mejoras del proyecto.

## Archivo Objetivo

`docs/PLAN_MEJORAS.md`

## Formato de Nota de Progreso

Al completar CUALQUIER tarea, agregar al final de la sección de esa tarea:

```markdown
**[NOTA DE PROGRESO - YYYY-MM-DD HH:MM]**
- Resultado: Completado ✓ / Parcial / Bloqueado
- Cambios: [Archivos modificados, migraciones aplicadas]
- Novedades: [Hallazgos inesperados, decisiones tomadas]
- Verificación: [Cómo se confirmó que funciona]
```

## Actualizar Estado de Tarea

Cambiar el checkbox de la tarea:

```markdown
# De:
#### [ ] Tarea X.Y: Descripción

# A:
#### [✓] 2025-11-27 - Tarea X.Y: Descripción
```

## Actualizar Tabla de Estado

Actualizar la tabla "Estado de Implementación":

```markdown
| Fase | Estado | Progreso | Última actualización |
|------|--------|----------|---------------------|
| Fase 1 - CRÍTICO | ✅ Completada | 3/3 tareas | 2025-11-27 |
| Fase 2 - ALTA PRIORIDAD | 🔄 En progreso | 2/4 tareas | 2025-11-27 |
| Fase 3 - MEJORAS | ⏳ No iniciada | 0/5 tareas | - |

**Progreso General:** 42% (5/12 tareas completadas)
```

## Instrucciones

1. Leer la tarea completada en PLAN_MEJORAS.md
2. Agregar nota de progreso con fecha/hora actual
3. Marcar checkbox como completado
4. Actualizar tabla de estado
5. Calcular y actualizar progreso general

## Ejemplo Completo

```markdown
#### [✓] 2025-11-27 - Tarea 1.2: Crear Índice para FK en email_logs
- **Archivos afectados:** Nueva migración SQL
- **Esfuerzo estimado:** 30 minutos
- **Pasos específicos:**
  1. Crear archivo `database/migrations/...`
  ...

---
**[NOTA DE PROGRESO - 2025-11-27 15:30]**
- Resultado: Completado ✓
- Cambios: Creada migración `20251127_add_email_logs_quote_id_index.sql`, aplicada via MCP Supabase
- Novedades: El índice se creó correctamente, advisor ya no muestra warning
- Verificación: `mcp_supabase_get_advisors` type="performance" sin warnings de FK
---
```

## Regla Crítica

**SIEMPRE** documentar después de completar una tarea. Esto permite continuidad entre sesiones y agentes.
