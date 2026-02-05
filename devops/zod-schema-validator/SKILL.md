---
name: zod-schema-validator
description: Implementa validación de esquemas con Zod en servicios y API routes. Usa cuando necesites validar inputs, crear schemas, o tarea 3.1 del PLAN_MEJORAS.md.
allowed-tools: Read, Write, Edit, Bash
---

# Zod Schema Validator

Skill para implementar validación de datos con Zod.

## Instalación

```bash
npm install zod
```

## Ubicación de Schemas

Crear schemas en `src/schemas/`:

```
src/schemas/
├── lead.ts
├── quote.ts
├── product.ts
└── index.ts
```

## Schemas para este Proyecto

### Lead Schema

```typescript
// src/schemas/lead.ts
import { z } from 'zod'

export const LeadSchema = z.object({
  nombre: z.string().min(1, 'Nombre requerido').max(255),
  email: z.string().email('Email inválido'),
  telefono: z.string().optional(),
  empresa: z.string().optional(),
  ruc_cedula: z.string().optional(),
  ciudad: z.string().optional(),
  notas: z.string().optional(),
})

export type LeadInput = z.infer<typeof LeadSchema>

// Para updates parciales
export const LeadUpdateSchema = LeadSchema.partial()
export type LeadUpdateInput = z.infer<typeof LeadUpdateSchema>
```

### Quote Schema

```typescript
// src/schemas/quote.ts
import { z } from 'zod'

export const QuoteItemSchema = z.object({
  producto_id: z.number().int().positive('ID de producto inválido'),
  cantidad: z.number().int().positive('Cantidad debe ser mayor a 0'),
  precio_unitario: z.number().positive('Precio debe ser mayor a 0'),
  subtotal: z.number().positive(),
})

export const CreateQuoteSchema = z.object({
  lead_id: z.number().int().positive().optional(),
  items: z.array(QuoteItemSchema).min(1, 'Al menos un item requerido'),
  notas: z.string().max(1000).optional(),
})

export type CreateQuoteInput = z.infer<typeof CreateQuoteSchema>
```

## Uso en Servicios

```typescript
// src/services/leads.ts
import { LeadSchema, type LeadInput } from '@/src/schemas/lead'

export async function createLead(data: unknown): Promise<Lead> {
  // Validar input
  const validatedData = LeadSchema.parse(data)
  
  // Si llega aquí, data es válido
  const { data: lead, error } = await supabase
    .from('leads')
    .insert(validatedData)
    .select()
    .single()
    
  if (error) throw error
  return lead
}
```

## Uso en API Routes

```typescript
// app/api/leads/route.ts
import { NextResponse } from 'next/server'
import { LeadSchema } from '@/src/schemas/lead'
import { ZodError } from 'zod'

export async function POST(request: Request) {
  try {
    const body = await request.json()
    const validatedData = LeadSchema.parse(body)
    
    // Procesar datos validados...
    
    return NextResponse.json({ success: true })
  } catch (error) {
    if (error instanceof ZodError) {
      return NextResponse.json(
        { error: 'Validation failed', details: error.errors },
        { status: 400 }
      )
    }
    return NextResponse.json(
      { error: 'Internal server error' },
      { status: 500 }
    )
  }
}
```

## Uso en Server Actions

```typescript
// app/admin/actions/leads.ts
'use server'

import { LeadSchema } from '@/src/schemas/lead'

export async function createLeadAction(formData: FormData) {
  const rawData = Object.fromEntries(formData)
  
  const result = LeadSchema.safeParse(rawData)
  
  if (!result.success) {
    return { error: result.error.flatten() }
  }
  
  // Procesar result.data...
  return { success: true }
}
```

## Instrucciones

1. Instalar Zod: `npm install zod`
2. Crear carpeta `src/schemas/`
3. Crear schemas para cada entidad
4. Integrar en servicios/API routes
5. Manejar errores de validación en UI

## Verificación

```bash
npm run build
npm run test
```
