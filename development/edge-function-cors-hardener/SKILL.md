---
name: edge-function-cors-hardener
description: Implementa CORS restrictivo en Edge Functions de Supabase. Usa cuando veas Access-Control-Allow-Origin con *, seguridad de CORS, o tarea 2.2 del PLAN_MEJORAS.md.
allowed-tools: Read, Write, Edit, Bash, mcp_supabase
---

# Edge Function CORS Hardener

Skill para asegurar Edge Functions de Supabase con CORS restrictivo.

## Problema

```typescript
// INSEGURO: permite cualquier origen
'Access-Control-Allow-Origin': '*'
```

## Solución

Crear módulo compartido con orígenes permitidos.

## Archivos a Crear/Modificar

### 1. Crear `supabase/functions/_shared/cors.ts`

```typescript
const ALLOWED_ORIGINS = [
  'https://fullcolor.com.ec',
  'https://www.fullcolor.com.ec',
  'https://cotizador.fullcolor.com.ec',
  Deno.env.get('ALLOWED_ORIGIN'),
].filter(Boolean) as string[]

export function getCorsHeaders(req: Request): HeadersInit {
  const origin = req.headers.get('origin')
  const allowedOrigin = ALLOWED_ORIGINS.includes(origin ?? '') 
    ? origin 
    : ALLOWED_ORIGINS[0]
  
  return {
    'Access-Control-Allow-Origin': allowedOrigin ?? ALLOWED_ORIGINS[0],
    'Access-Control-Allow-Headers': 'authorization, x-client-info, apikey, content-type',
    'Access-Control-Allow-Methods': 'POST, OPTIONS',
  }
}

export function corsResponse(req: Request): Response {
  return new Response(null, {
    status: 204,
    headers: getCorsHeaders(req)
  })
}
```

### 2. Actualizar Edge Functions

```typescript
import { getCorsHeaders, corsResponse } from '../_shared/cors.ts'

Deno.serve(async (req) => {
  // Manejar preflight
  if (req.method === 'OPTIONS') {
    return corsResponse(req)
  }

  // ... lógica de la función ...

  return new Response(JSON.stringify(data), {
    headers: { ...getCorsHeaders(req), 'Content-Type': 'application/json' }
  })
})
```

## Edge Functions a Actualizar

- `supabase/functions/generate-pdf/index.ts`
- `supabase/functions/send-email/index.ts`
- `supabase/functions/upsert-lead/index.ts`

## Instrucciones

1. Crear `_shared/cors.ts`
2. Actualizar cada Edge Function
3. Configurar variable `ALLOWED_ORIGIN` en Supabase para desarrollo
4. Desplegar con `mcp_supabase_deploy_edge_function`
5. Probar desde frontend

## Verificación

1. Abrir DevTools > Network
2. Verificar que requests tienen el header correcto
3. Intentar desde origen no permitido (debe fallar)
