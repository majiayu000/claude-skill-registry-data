---
name: rls-policy-optimizer
description: Optimiza políticas RLS de Supabase usando el patrón (select auth.uid()) para mejor performance. Usa cuando trabajes con RLS policies, auth.uid() reevaluación, o tareas 1.3 y 2.1 del PLAN_MEJORAS.md.
allowed-tools: Read, Write, Edit, Bash, mcp_supabase
---

# RLS Policy Optimizer

Skill para optimizar Row Level Security policies en Supabase evitando reevaluación de `auth.uid()` por cada fila.

## Problema

```sql
-- MALO: auth.uid() se evalúa por cada fila
USING (auth.uid() = user_id)
```

## Solución

```sql
-- BUENO: (select auth.uid()) se evalúa una vez
USING ((select auth.uid()) = user_id)
```

## Tablas Afectadas en este Proyecto

- `leads` - policies: Users insert/read/update
- `cotizaciones` - policies: Users insert/read
- `items_cotizacion` - policies: Users insert/read
- `email_logs` - policies: Admins manage

## Instrucciones

1. Usar MCP Supabase para obtener policies actuales de la tabla
2. Crear migración en `database/migrations/YYYYMMDD_optimize_rls_<tabla>.sql`
3. Incluir DROP POLICY + CREATE POLICY con el fix
4. Aplicar con `mcp_supabase_apply_migration`
5. Verificar con `mcp_supabase_get_advisors` type="performance"
6. Documentar en `docs/PLAN_MEJORAS.md`

## Template de Migración

```sql
-- Optimizar RLS: usar (select auth.uid()) en lugar de auth.uid()
-- Referencia: https://supabase.com/docs/guides/database/postgres/row-level-security#call-functions-with-select

-- Backup implícito: recreamos la policy con la misma lógica optimizada

DROP POLICY IF EXISTS "Users read own <tabla>" ON public.<tabla>;

CREATE POLICY "Users read own <tabla>" ON public.<tabla>
  FOR SELECT TO authenticated
  USING ((select auth.uid()) = user_id);
```

## Verificación

Después de aplicar, ejecutar advisor de Supabase y confirmar que no hay warnings de "auth function called per row".
