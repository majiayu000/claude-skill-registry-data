---
name: typescript-any-eliminator
description: Elimina uso de `any` en TypeScript creando tipos específicos. Usa cuando veas any en código, errores de tipado, o tarea 2.3 del PLAN_MEJORAS.md.
allowed-tools: Read, Write, Edit, Bash
---

# TypeScript Any Eliminator

Skill para eliminar `any` y fortalecer el tipado estricto.

## Archivos Prioritarios en este Proyecto

- `src/services/quotes.ts` (líneas 155, 195, 230, 231, 298, 316)
- `src/services/pdfQuoteService.ts` (líneas 93, 114, 146, 175, 256-264)
- `src/hooks/useQuoteBuilder.ts` (líneas 45, 46, 215, 246, 373, 441, 587, 661)
- `lib/admin-services.ts` (líneas 88, 100, 122, 165, 560, 639)
- `middleware.ts` (línea 96)

## Estrategias de Reemplazo

### 1. Datos de Supabase → Usar tipos generados

```typescript
import type { Database } from '@/src/types/database.types'
type Tables = Database['public']['Tables']

type Cotizacion = Tables['cotizaciones']['Row']
type Lead = Tables['leads']['Row']
```

### 2. Tipo desconocido → Usar `unknown` + type guard

```typescript
// En lugar de: any
function processData(data: unknown) {
  if (isValidData(data)) {
    // TypeScript sabe que data es ValidData aquí
  }
}

function isValidData(data: unknown): data is ValidData {
  return typeof data === 'object' && data !== null && 'id' in data
}
```

### 3. Callbacks de terceros → Tipar el callback

```typescript
// En lugar de: (error: any) => void
(error: Error | null) => void
```

### 4. Objetos dinámicos → Record o tipos específicos

```typescript
// En lugar de: any
Record<string, unknown>
// O mejor, un tipo específico:
interface FormData {
  [key: string]: string | number | boolean
}
```

## Tipos Sugeridos para este Proyecto

```typescript
// src/types/quotes.ts
export interface ItemWithProduct {
  id: number
  cotizacion_id: number
  producto_id: number
  cantidad: number
  precio_unitario: number
  subtotal: number
  producto: {
    id: number
    nombre: string
    categoria: string
    imagen_url?: string
  }
}

export interface QuoteWithItems {
  id: number
  codigo: string
  estado: 'borrador' | 'enviada' | 'aceptada' | 'rechazada' | 'expirada'
  total: number
  items_cotizacion: ItemWithProduct[]
  lead?: {
    nombre: string
    email: string
    telefono?: string
  }
}
```

## Instrucciones

1. Buscar todos los `any` en el archivo
2. Entender el contexto de cada uso
3. Crear tipo específico o usar existente
4. Reemplazar `any`
5. Ejecutar `npm run lint && npm run build`
6. Repetir para siguiente archivo

## Verificación

```bash
# Buscar any restantes
grep -r "any" --include="*.ts" --include="*.tsx" src/ lib/ | grep -v node_modules

# Verificar build
npm run build
```

## Regla de Oro

Si REALMENTE necesitas `any` (raro), documéntalo:

```typescript
// eslint-disable-next-line @typescript-eslint/no-explicit-any
const value: any = externalLib.unknownMethod() // TODO: tipar cuando lib actualice tipos
```
