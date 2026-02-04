---
name: rls-policy-consolidator
description: Consolida múltiples políticas RLS permisivas redundantes en Supabase. Usa cuando hay varias policies del mismo rol/acción, warnings de múltiples permissive policies, o tarea 2.1 del PLAN_MEJORAS.md.
allowed-tools: Read, Write, Edit, Bash, mcp_supabase
---

# RLS Policy Consolidator

Skill para consolidar políticas RLS redundantes que degradan performance.

## Problema

Múltiples políticas permisivas para el mismo rol y acción se ejecutan secuencialmente:

```sql
-- Policy 1: Users can insert
-- Policy 2: Admins can insert  
-- Ambas se evalúan para cada INSERT de authenticated
```

## Solución

Consolidar en una sola política con OR:

```sql
CREATE POLICY "Authenticated can insert <tabla>" ON public.<tabla>
  FOR INSERT TO authenticated
  WITH CHECK (
    (select auth.uid()) = user_id
    OR EXISTS (
      SELECT 1 FROM public.profiles
      WHERE id = (select auth.uid()) AND role = 'admin'
    )
  );
```

## Tablas Afectadas en este Proyecto

- `cotizaciones` (INSERT, SELECT para authenticated)
- `items_cotizacion` (INSERT, SELECT para authenticated)
- `lead_actividades` (INSERT para authenticated)
- `leads` (INSERT, SELECT, UPDATE para authenticated)
- `precios_escalonados` (múltiples roles/acciones)
- `productos` (múltiples roles/acciones)
- `profiles` (SELECT, UPDATE para authenticated)

## Instrucciones

1. Listar policies actuales por tabla con MCP Supabase
2. Identificar policies redundantes (mismo rol + misma acción)
3. Crear migración que:
   - DROP de policies redundantes
   - CREATE de policy unificada con lógica OR
4. Aplicar y verificar permisos

## Template de Migración

```sql
-- Consolidar policies permisivas para <tabla>
-- Referencia: PERF-002 en PLAN_MEJORAS.md

BEGIN;

-- Eliminar policies redundantes
DROP POLICY IF EXISTS "Policy A" ON public.<tabla>;
DROP POLICY IF EXISTS "Policy B" ON public.<tabla>;

-- Crear policy unificada
CREATE POLICY "Unified policy for <action>" ON public.<tabla>
  FOR <action> TO authenticated
  USING/WITH CHECK (
    -- Condición usuario normal
    (select auth.uid()) = user_id
    OR
    -- Condición admin
    EXISTS (
      SELECT 1 FROM public.profiles
      WHERE id = (select auth.uid()) AND role = 'admin'
    )
  );

COMMIT;
```

## Importante

- Probar SIEMPRE en desarrollo antes de producción
- Verificar que los permisos funcionan para usuarios normales Y admins
- Documentar en PLAN_MEJORAS.md
