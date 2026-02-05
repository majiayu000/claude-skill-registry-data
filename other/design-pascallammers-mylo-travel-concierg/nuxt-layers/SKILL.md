---
name: nuxt-layers
description: Working with Nuxt layers (base, nuxt-ui, x-ui) that provide shared functionality. Use when understanding layer architecture, importing from layers, extending layer functionality, or creating new layers.
---

# Nuxt Layers

Shared foundation layers providing composables, models, repositories, and UI components across applications.

## Layer Stack

**[layers.md](references/layers.md)** - Complete layer architecture, what each provides, how to extend

## Three-Layer Architecture

```
x-ui          → Extended UI components (XTable, XForm, XSlideover)
    ↓
nuxt-ui       → UI primitives (modals, toasts, tabs, overlays)
    ↓
base          → Core infrastructure (Model, Repository, composables, utils)
```

## Extending Layers

```typescript
// nuxt.config.ts
export default defineNuxtConfig({
  extends: [
    '../../../nuxt-layers/base',
    '../../../nuxt-layers/nuxt-ui',
    '../../../nuxt-layers/x-ui',
  ],
})
```

## Importing from Layers

```typescript
// Base layer imports
import Model from '#layers/base/app/models/Model'
import type { Castable, DataResponse } from '#layers/base/app/types'
import { BaseRepository } from '#layers/base/app/repositories/base-repository'
import { ModelHydrator } from '#layers/base/app/repositories/hydrators/model-hydrator'

// Composables auto-imported
const leadApi = useRepository('leads')
const { start, stop } = useWait()
const { can } = usePermissions()
```

## Base Layer Provides

| Category | Items |
|----------|-------|
| **Composables** | `useRepository`, `useQuery`, `useFilterQuery`, `useWait`, `usePermissions`, `useFlash`, `useForm`, `useReactiveFilters`, `useRealtime`, `useShadowCache` |
| **Classes** | `Model`, `BaseRepository`, `ApiClient`, `ModelHydrator` |
| **Errors** | `ValidationError`, `ConflictError`, `TooManyRequestsError` |
| **Utils** | 49 utility functions (array, string, object, date, async) |

## Nuxt-UI Layer Provides

| Category | Items |
|----------|-------|
| **Composables** | `useModal`, `useSlideover`, `useConfirmationToast`, `useTabs`, `useDropdown`, `useAppHeader`, `useBreadcrumbs` |
| **Components** | `Copyable`, `SearchInput`, `SearchSelect`, `Rating`, `LoadingLine` |
