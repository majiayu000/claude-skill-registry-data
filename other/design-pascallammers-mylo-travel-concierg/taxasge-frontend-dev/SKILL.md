---
name: TaxasGE Frontend Dev
description: Patterns frontend Next.js/React/shadcn/ui, complète DEV_AGENT avec best practices frontend
version: 2.0.0
---

# TaxasGE Frontend Dev Skill

## Overview

Ce skill **complète le DEV_AGENT** avec des patterns spécifiques frontend Next.js/React. Il ne remplace PAS le workflow de développement mais fournit des références techniques et templates pour l'implémentation frontend.

**Principe fondamental** : Guide technique, pas workflow (le workflow est dans DEV_AGENT.md et DEV_WORKFLOW.md).

---

## When to Use This Skill

Claude invoquera automatiquement ce skill quand :
- DEV_AGENT implémente tâche frontend
- Besoin patterns Next.js/React
- Questions shadcn/ui composants
- Référence technique frontend

**Ne PAS utiliser pour** :
- Workflow développement (voir DEV_WORKFLOW.md)
- Validation (voir Go/No-Go Validator)
- Orchestration (voir Orchestrator)

---

## Core Responsibilities

### 1. Architecture Frontend TaxasGE

**Stack** :
```
Next.js 14 (App Router)
    ↓
React Server Components + Client Components
    ↓
shadcn/ui + Tailwind CSS
    ↓
Zod (Validation) + React Hook Form
    ↓
API Client (fetch/axios)
```

**Structure** :
```
packages/web/src/
├── app/
│   ├── (dashboard)/              ← Pages authentifiées
│   │   ├── declarations/
│   │   ├── profile/
│   │   └── layout.tsx
│   └── (auth)/                   ← Pages auth (login, register)
│       ├── login/
│       └── register/
│
├── components/
│   ├── ui/                       ← shadcn/ui (Button, Input, etc.)
│   ├── declarations/             ← Composants métier
│   └── layout/                   ← Layout (Header, Sidebar)
│
├── lib/
│   ├── api/                      ← API clients
│   ├── validations/              ← Schémas Zod
│   ├── utils.ts                  ← Utilitaires
│   └── constants.ts              ← Constantes
│
└── hooks/
    ├── useDeclarations.ts        ← Hooks métier
    └── useAuth.ts
```

### 2. Référence Documentation Frontend

**Source unique de vérité** : `.github/docs-internal/Documentations/Frontend/`

Structure :
```
.github/docs-internal/Documentations/Frontend/
├── ARCHITECTURE.md               ← Architecture Next.js
├── COMPONENTS.md                 ← Composants shadcn/ui
├── ROUTING.md                    ← Routing App Router
├── STATE_MANAGEMENT.md           ← State (Zustand/Context)
├── FORMS.md                      ← Formulaires (react-hook-form + Zod)
└── STYLING.md                    ← Tailwind CSS + Themes
```

**Important** : Toujours référencer cette documentation, ne PAS dupliquer.

### 3. Templates Code

**Templates disponibles** :
- `templates/page_template.tsx` - Page Next.js
- `templates/component_template.tsx` - Composant React
- `templates/api_client_template.ts` - Client API
- `templates/form_template.tsx` - Formulaire react-hook-form

---

## Patterns Frontend

### Pattern 1 : Page Next.js (App Router)

**Template** : `templates/page_template.tsx`

**Structure** :
```typescript
import { Suspense } from 'react'
import { DeclarationList } from '@/components/declarations/declaration-list'
import { DeclarationListSkeleton } from '@/components/declarations/declaration-list-skeleton'

/**
 * Page liste déclarations
 * 
 * @source .github/docs-internal/Documentations/Frontend/ROUTING.md
 * @route /declarations
 */
export default function DeclarationsPage() {
  return (
    <div className="container mx-auto py-8">
      <h1 className="text-3xl font-bold mb-6">Mes Déclarations</h1>
      
      <Suspense fallback={<DeclarationListSkeleton />}>
        <DeclarationList />
      </Suspense>
    </div>
  )
}
```

**Points clés** :
1. **Suspense** : Loading states automatiques
2. **Skeleton** : Composant loading dédié
3. **Tailwind** : Classes utilitaires uniquement
4. **Docstring** : Source + Route
5. **Export default** : Convention Next.js

---

### Pattern 2 : Composant Client

**Template** : `templates/component_template.tsx`

**Structure** :
```typescript
'use client'

import { useState } from 'react'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { useDeclarations } from '@/hooks/useDeclarations'

/**
 * Liste déclarations avec actions
 * 
 * @source .github/docs-internal/Documentations/Frontend/COMPONENTS.md
 */
export function DeclarationList() {
  const { declarations, isLoading, error, deleteDeclaration } = useDeclarations()
  const [deletingId, setDeletingId] = useState<string | null>(null)

  const handleDelete = async (id: string) => {
    setDeletingId(id)
    try {
      await deleteDeclaration(id)
    } finally {
      setDeletingId(null)
    }
  }

  if (isLoading) return <DeclarationListSkeleton />
  if (error) return <ErrorMessage error={error} />
  if (!declarations.length) return <EmptyState />

  return (
    <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
      {declarations.map((declaration) => (
        <Card key={declaration.id}>
          <CardHeader>
            <CardTitle>{declaration.title}</CardTitle>
          </CardHeader>
          <CardContent>
            <p className="text-sm text-muted-foreground">
              {declaration.description}
            </p>
            <div className="mt-4 flex gap-2">
              <Button variant="outline" size="sm">
                Voir
              </Button>
              <Button 
                variant="destructive" 
                size="sm"
                disabled={deletingId === declaration.id}
                onClick={() => handleDelete(declaration.id)}
              >
                {deletingId === declaration.id ? 'Suppression...' : 'Supprimer'}
              </Button>
            </div>
          </CardContent>
        </Card>
      ))}
    </div>
  )
}
```

**Points clés** :
1. **'use client'** : Directive obligatoire pour interactivité
2. **shadcn/ui** : Composants UI (Button, Card)
3. **Custom hook** : `useDeclarations()` pour logique
4. **Loading states** : Gestion isLoading + disabled
5. **Responsive** : `md:grid-cols-2 lg:grid-cols-3`

---

### Pattern 3 : Formulaire (react-hook-form + Zod)

**Template** : `templates/form_template.tsx`

**Structure** :
```typescript
'use client'

import { zodResolver } from '@hookform/resolvers/zod'
import { useForm } from 'react-hook-form'
import * as z from 'zod'
import { Button } from '@/components/ui/button'
import {
  Form,
  FormControl,
  FormDescription,
  FormField,
  FormItem,
  FormLabel,
  FormMessage,
} from '@/components/ui/form'
import { Input } from '@/components/ui/input'
import { Textarea } from '@/components/ui/textarea'

/**
 * Schéma validation déclaration
 * 
 * @source .github/docs-internal/Documentations/Frontend/FORMS.md
 */
const declarationSchema = z.object({
  title: z.string()
    .min(3, 'Titre minimum 3 caractères')
    .max(100, 'Titre maximum 100 caractères'),
  description: z.string()
    .min(10, 'Description minimum 10 caractères')
    .max(500, 'Description maximum 500 caractères'),
  amount: z.number()
    .positive('Montant doit être positif')
    .max(1000000, 'Montant maximum 1 000 000'),
})

type DeclarationFormData = z.infer<typeof declarationSchema>

interface DeclarationFormProps {
  onSubmit: (data: DeclarationFormData) => Promise<void>
  defaultValues?: Partial<DeclarationFormData>
}

/**
 * Formulaire création/édition déclaration
 * 
 * @source .github/docs-internal/Documentations/Frontend/FORMS.md
 */
export function DeclarationForm({ onSubmit, defaultValues }: DeclarationFormProps) {
  const form = useForm<DeclarationFormData>({
    resolver: zodResolver(declarationSchema),
    defaultValues: {
      title: '',
      description: '',
      amount: 0,
      ...defaultValues,
    },
  })

  const handleSubmit = async (data: DeclarationFormData) => {
    try {
      await onSubmit(data)
      form.reset()
    } catch (error) {
      form.setError('root', {
        message: error instanceof Error ? error.message : 'Erreur inconnue',
      })
    }
  }

  return (
    <Form {...form}>
      <form onSubmit={form.handleSubmit(handleSubmit)} className="space-y-6">
        <FormField
          control={form.control}
          name="title"
          render={({ field }) => (
            <FormItem>
              <FormLabel>Titre</FormLabel>
              <FormControl>
                <Input placeholder="Titre de la déclaration" {...field} />
              </FormControl>
              <FormDescription>
                Titre court et descriptif
              </FormDescription>
              <FormMessage />
            </FormItem>
          )}
        />

        <FormField
          control={form.control}
          name="description"
          render={({ field }) => (
            <FormItem>
              <FormLabel>Description</FormLabel>
              <FormControl>
                <Textarea 
                  placeholder="Description détaillée" 
                  rows={4}
                  {...field} 
                />
              </FormControl>
              <FormMessage />
            </FormItem>
          )}
        />

        <FormField
          control={form.control}
          name="amount"
          render={({ field }) => (
            <FormItem>
              <FormLabel>Montant (FCFA)</FormLabel>
              <FormControl>
                <Input 
                  type="number" 
                  placeholder="0"
                  {...field}
                  onChange={(e) => field.onChange(parseFloat(e.target.value))}
                />
              </FormControl>
              <FormMessage />
            </FormItem>
          )}
        />

        {form.formState.errors.root && (
          <div className="rounded-md bg-destructive/10 p-4 text-sm text-destructive">
            {form.formState.errors.root.message}
          </div>
        )}

        <Button 
          type="submit" 
          disabled={form.formState.isSubmitting}
          className="w-full"
        >
          {form.formState.isSubmitting ? 'Envoi...' : 'Créer déclaration'}
        </Button>
      </form>
    </Form>
  )
}
```

**Points clés** :
1. **Zod schema** : Validation côté client
2. **react-hook-form** : Gestion formulaire
3. **shadcn/ui Form** : Composants formulaire
4. **Error handling** : `form.setError('root')`
5. **Type-safety** : `z.infer<typeof schema>`

---

### Pattern 4 : API Client

**Template** : `templates/api_client_template.ts`

**Structure** :
```typescript
/**
 * Client API Déclarations
 * 
 * @source .github/docs-internal/Documentations/Frontend/*.md
 */

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api/v1'

export interface Declaration {
  id: string
  title: string
  description: string
  amount: number
  status: 'draft' | 'submitted' | 'approved' | 'rejected'
  created_at: string
  updated_at: string
}

export interface CreateDeclarationDTO {
  title: string
  description: string
  amount: number
}

export interface UpdateDeclarationDTO extends Partial<CreateDeclarationDTO> {}

/**
 * Récupérer toutes déclarations
 */
export async function getDeclarations(): Promise<Declaration[]> {
  const response = await fetch(`${API_BASE_URL}/declarations/`, {
    headers: {
      'Authorization': `Bearer ${getToken()}`,
    },
  })

  if (!response.ok) {
    throw new Error('Erreur récupération déclarations')
  }

  return response.json()
}

/**
 * Créer déclaration
 */
export async function createDeclaration(
  data: CreateDeclarationDTO
): Promise<Declaration> {
  const response = await fetch(`${API_BASE_URL}/declarations/`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${getToken()}`,
    },
    body: JSON.stringify(data),
  })

  if (!response.ok) {
    const error = await response.json()
    throw new Error(error.detail || 'Erreur création déclaration')
  }

  return response.json()
}

/**
 * Mettre à jour déclaration
 */
export async function updateDeclaration(
  id: string,
  data: UpdateDeclarationDTO
): Promise<Declaration> {
  const response = await fetch(`${API_BASE_URL}/declarations/${id}`, {
    method: 'PUT',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${getToken()}`,
    },
    body: JSON.stringify(data),
  })

  if (!response.ok) {
    throw new Error('Erreur mise à jour déclaration')
  }

  return response.json()
}

/**
 * Supprimer déclaration
 */
export async function deleteDeclaration(id: string): Promise<void> {
  const response = await fetch(`${API_BASE_URL}/declarations/${id}`, {
    method: 'DELETE',
    headers: {
      'Authorization': `Bearer ${getToken()}`,
    },
  })

  if (!response.ok) {
    throw new Error('Erreur suppression déclaration')
  }
}

/**
 * Récupérer token JWT depuis localStorage
 */
function getToken(): string | null {
  if (typeof window === 'undefined') return null
  return localStorage.getItem('access_token')
}
```

**Points clés** :
1. **Types TypeScript** : Interfaces pour types retour
2. **Environment variables** : `NEXT_PUBLIC_API_URL`
3. **Error handling** : Throw errors explicites
4. **Authorization** : Header Bearer token
5. **SSR-safe** : Check `typeof window`

---

### Pattern 5 : Custom Hook

**Structure** :
```typescript
'use client'

import { useState, useEffect } from 'react'
import * as api from '@/lib/api/declarations'
import type { Declaration, CreateDeclarationDTO } from '@/lib/api/declarations'

/**
 * Hook déclarations
 * 
 * @source .github/docs-internal/Documentations/Frontend/STATE_MANAGEMENT.md
 */
export function useDeclarations() {
  const [declarations, setDeclarations] = useState<Declaration[]>([])
  const [isLoading, setIsLoading] = useState(true)
  const [error, setError] = useState<Error | null>(null)

  // Charger déclarations
  useEffect(() => {
    const loadDeclarations = async () => {
      try {
        setIsLoading(true)
        const data = await api.getDeclarations()
        setDeclarations(data)
        setError(null)
      } catch (err) {
        setError(err instanceof Error ? err : new Error('Erreur inconnue'))
      } finally {
        setIsLoading(false)
      }
    }

    loadDeclarations()
  }, [])

  // Créer déclaration
  const createDeclaration = async (data: CreateDeclarationDTO) => {
    const newDeclaration = await api.createDeclaration(data)
    setDeclarations((prev) => [newDeclaration, ...prev])
    return newDeclaration
  }

  // Supprimer déclaration
  const deleteDeclaration = async (id: string) => {
    await api.deleteDeclaration(id)
    setDeclarations((prev) => prev.filter((d) => d.id !== id))
  }

  return {
    declarations,
    isLoading,
    error,
    createDeclaration,
    deleteDeclaration,
  }
}
```

**Points clés** :
1. **State local** : `useState` pour données
2. **Side effects** : `useEffect` pour chargement
3. **Mutations** : Fonctions async retournées
4. **Optimistic updates** : Mise à jour state avant API

---

## Checklist Implémentation Frontend

Avant de considérer tâche frontend terminée :

### Code
- [ ] **Pages** : Structure App Router respectée
- [ ] **Composants** : shadcn/ui utilisés
- [ ] **Formulaires** : react-hook-form + Zod
- [ ] **API Client** : Type-safe avec interfaces
- [ ] **Hooks** : Custom hooks pour logique réutilisable

### Styling
- [ ] **Tailwind** : Classes utilitaires uniquement
- [ ] **Responsive** : Mobile/Tablet/Desktop
- [ ] **Dark mode** : Support thème sombre
- [ ] **Accessibilité** : ARIA labels, keyboard navigation

### Tests
- [ ] **Tests unitaires** : Jest (composants) >75%
- [ ] **Tests E2E** : Playwright (flows) >80%
- [ ] **Tests passent** : 100%

### Qualité
- [ ] **ESLint** : 0 erreurs
- [ ] **TypeScript** : 0 erreurs (strict mode)
- [ ] **Build** : `npm run build` réussi

### Performance
- [ ] **Lighthouse** : Score >90
- [ ] **Bundle size** : Optimisé
- [ ] **Images** : Next.js Image optimisé

---

## Integration avec DEV_AGENT

### Workflow Complet

```
1. DEV_AGENT reçoit tâche frontend (ex: TASK-P2-015)
   ↓
2. DEV_AGENT lit DEV_WORKFLOW.md
   ↓
3. DEV_AGENT invoque Frontend Dev Skill (ce skill)
   ↓
4. Frontend Dev Skill fournit :
   - Patterns Next.js
   - Templates composants
   - Références documentation
   ↓
5. DEV_AGENT implémente selon patterns
   ↓
6. DEV_AGENT génère rapport
   ↓
7. Go/No-Go Validator valide
```

**Ce skill ne fait PAS** :
- ❌ Workflow développement
- ❌ Git operations
- ❌ Génération rapports
- ❌ Validation

**Ce skill fait** :
- ✅ Fournit patterns techniques
- ✅ Référence documentation
- ✅ Templates code
- ✅ Best practices frontend

---

## References

### Agents & Workflows
- `.claude/.agent/Tasks/DEV_AGENT.md`
- `.claude/.agent/SOP/DEV_WORKFLOW.md`
- `.claude/.agent/SOP/CODE_STANDARDS.md`
- `.claude/.agent/SOP/TEST_WORKFLOW.md`

### Documentation Frontend
- `.github/docs-internal/Documentations/Frontend/ARCHITECTURE.md`
   → Architecture Next.js App Router
- `.github/docs-internal/Documentations/Frontend/COMPONENTS.md`
   → Composants shadcn/ui disponibles
- `.github/docs-internal/Documentations/Frontend/ROUTING.md`
   → Patterns routing Next.js
- `.github/docs-internal/Documentations/Frontend/STYLING.md`
   → Design system et charte graphique
- `.github/docs-internal/Documentations/Frontend/FORMS.md`
   → Patterns formulaires
- `.github/docs-internal/Documentations/Frontend/STATE_MANAGEMENT.md`
  → Gestion état

### Templates
- `templates/page_template.tsx`
- `templates/component_template.tsx`
- `templates/api_client_template.ts`
- `templates/form_template.tsx`

---

## Success Criteria

Une implémentation frontend est réussie si :
- ✅ Pages Next.js App Router
- ✅ shadcn/ui composants
- ✅ Formulaires react-hook-form + Zod
- ✅ Tests coverage >75%
- ✅ Lighthouse >90
- ✅ 0 erreurs ESLint/TypeScript
- ✅ Build réussi

---

**Skill created by:** TaxasGE Frontend Team  
**Date:** 2025-10-31  
**Version:** 2.0.0  
**Status:** ✅ READY FOR USE
