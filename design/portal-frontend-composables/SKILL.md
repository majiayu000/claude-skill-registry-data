---
name: portal-frontend-composables
description: Create composables, Pinia stores, and route middleware for the Portal Nuxt 4 frontend. Use when implementing useChatStream, useSession (httpOnly JWT cookie, role guards, module visibility by scope), the shared dashboard-chat Pinia store (TwinBI pattern), or useFetch consumers of massive payloads.
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
---

# Portal Frontend Composables Skill

## Rules — NON-NEGOTIABLE

- Composables retornan estado reactivo + acciones; jamás exportar `ref`/`reactive` sueltos entre archivos. Estado cross-component SIEMPRE en Pinia.
- Sesión vía **cookie httpOnly con el JWT**: el JS del cliente nunca lee el token; el rol/scope llega de `/api/auth/me` (o del payload SSR). Nada de `localStorage` para tokens.
- Middleware de rutas Nuxt para autenticación y **guardas por rol**; los módulos se ocultan según scope (un Operativo no ve el enlace de export ni /admin).
- `useFetch` aprovecha el **`shallowRef` por defecto de Nuxt 4**: payloads masivos (series de 1M puntos) SIN reactividad profunda; jamás envolverlos en `reactive()`.
- Patrón **TwinBI** (paper 06): los filtros activos del dashboard viajan como contexto del agente en cada consulta del chat; acción "Resumir vista actual" serializa el estado del store.
- `useChatStream` es la única vía de consumo de `/api/chat` (contrato de eventos en `portal-sse-streaming`); incluye `stop()` real vía `AbortController`.
- TypeScript estricto; tipos compartidos en `app/types/`. `import.meta.client` antes de browser APIs.

## useSession — cookie httpOnly + guardas

```typescript
// app/composables/useSession.ts
import type { SessionUser, Role } from '~/types/auth'

export function useSession() {
  // El token vive en cookie httpOnly: el server la reenvia; el cliente solo ve el perfil.
  const user = useState<SessionUser | null>('session-user', () => null)

  async function fetchProfile() {
    user.value = await $fetch<SessionUser>('/api/auth/me')  // cookie viaja sola
  }

  async function login(username: string, password: string) {
    await $fetch('/api/auth/token', {
      method: 'POST',
      body: new URLSearchParams({ username, password }),  // OAuth2 password form
    })  // el backend setea Set-Cookie httpOnly
    await fetchProfile()
    return navigateTo(HOME_BY_ROLE[user.value!.role])
  }

  function hasScope(required: Role): boolean {
    const order: Role[] = ['operativo', 'analista', 'directivo', 'admin']
    return !!user.value && order.indexOf(user.value.role) >= order.indexOf(required)
  }

  return { user, fetchProfile, login, hasScope }
}

export const HOME_BY_ROLE: Record<Role, string> = {
  operativo: '/catalogo',       // default: buscador arriba
  analista: '/explorador',      // default: explorador + exportaciones
  directivo: '/dashboard',      // default: tarjetas + resumen del agente
  admin: '/admin/usuarios',
}
```

```typescript
// app/middleware/auth.global.ts
export default defineNuxtRouteMiddleware(async (to) => {
  const { user, fetchProfile, hasScope } = useSession()
  if (to.path === '/login') return
  if (!user.value) {
    try { await fetchProfile() } catch { return navigateTo('/login') }
  }
  const required = to.meta.requiredRole as Role | undefined  // definePageMeta({ requiredRole: 'admin' })
  if (required && !hasScope(required)) return navigateTo('/')  // 403 visual: ni siquiera monta
})
```

Ocultamiento de módulos: la navegación itera módulos declarados con su scope y filtra con `hasScope` — el usuario sin permiso no ve el enlace (y el backend igualmente responde 403 si fuerza la URL).

## Store compartido dashboard↔chat (TwinBI)

```typescript
// app/stores/workspace.ts
import { defineStore } from 'pinia'
import type { DashboardFilters } from '~/types/dashboard'

export const useWorkspaceStore = defineStore('workspace', {
  state: () => ({
    filters: { silo: null, producto: null, rangoFechas: null } as DashboardFilters,
    activeChart: null as string | null,   // grafica enfocada por drill-down
  }),
  getters: {
    // Contexto que viaja con CADA consulta del chat (paper 06: TwinBI)
    agentContext(state): Record<string, unknown> {
      return { filters: state.filters, active_chart: state.activeChart }
    },
  },
  actions: {
    applyDrillDown(dimension: string, value: string) {
      this.filters = { ...this.filters, [dimension]: value }  // ECharts emite -> store
    },
    async resumirVistaActual() {
      const { send } = useChatStream()
      await send('Resume la vista actual del dashboard', this.agentContext)
    },
  },
})
```

En el envío del chat: `send(query, workspaceStore.agentContext)` — el backend inyecta ese contexto al agente (tool `resumir_vista`).

## useFetch con payloads masivos

```typescript
// app/composables/useSerieLiquidez.ts
export function useSerieLiquidez(filters: Ref<DashboardFilters>) {
  // Nuxt 4: data es shallowRef por defecto -> sin proxies profundos sobre 1M puntos
  const { data, pending, error, refresh } = useFetch('/api/liquidez', {
    query: computed(() => ({ metric: 'posicion_diaria', ...filters.value })),
    watch: [filters],
  })
  // PROHIBIDO: reactive(data.value) o deep:true sobre este payload
  return { serie: data, pending, error, refresh }
}
```

## Tabla de piezas

| Pieza | Archivo | Responsabilidad |
|-------|---------|-----------------|
| `useChatStream` | `app/composables/useChatStream.ts` | SSE + Stop + Reintentar (ver `portal-sse-streaming`) |
| `useSession` | `app/composables/useSession.ts` | login, perfil, `hasScope`, homes por rol |
| `auth.global` | `app/middleware/auth.global.ts` | redirect a login + guarda `requiredRole` |
| `workspace` store | `app/stores/workspace.ts` | filtros compartidos, drill-down, contexto del agente |
| `useSerieLiquidez` y afines | `app/composables/` | useFetch shallowRef por endpoint semántico |

## QA Checklist

- [ ] Token solo en cookie httpOnly; cero acceso al JWT desde JS
- [ ] Middleware global: sin sesión -> /login; sin scope -> home del rol
- [ ] Módulos ocultos por scope en navegación (y backend devuelve 403 igual)
- [ ] Filtros del dashboard viajan como contexto en cada consulta del chat
- [ ] "Resumir vista actual" disponible desde el dashboard directivo
- [ ] Ningún payload masivo envuelto en reactividad profunda
- [ ] Tests Vitest de hasScope, middleware y acciones del store
