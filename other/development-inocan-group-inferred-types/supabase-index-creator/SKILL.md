---
name: supabase-index-creator
description: Crea índices para foreign keys sin cobertura en Supabase. Usa cuando veas warnings de FK sin índice, performance de JOINs, o tarea 1.2 del PLAN_MEJORAS.md.
allowed-tools: Read, Write, Edit, Bash, mcp_supabase
---

# Supabase Index Creator

Skill para crear índices de cobertura para foreign keys en Supabase.

## Problema Detectado

FK `email_logs_quote_id_fkey` sin índice de cobertura.

## Instrucciones

1. Verificar que el índice no existe con MCP Supabase
2. Crear migración en `database/migrations/YYYYMMDD_add_<tabla>_<columna>_index.sql`
3. Aplicar migración
4. Verificar con advisor de Supabase

## Template de Migración

```sql
-- Añadir índice para FK <fk_name>
-- Mejora performance de consultas que usen esta relación

CREATE INDEX IF NOT EXISTS idx_<tabla>_<columna> 
ON public.<tabla>(<columna>);
```

## Caso Específico: email_logs

```sql
-- Añadir índice para FK email_logs_quote_id_fkey
CREATE INDEX IF NOT EXISTS idx_email_logs_quote_id 
ON public.email_logs(quote_id);
```

## Verificación

Ejecutar `mcp_supabase_get_advisors` con type="performance" y confirmar que el warning de FK sin índice desaparece.
