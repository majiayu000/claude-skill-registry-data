---
name: portal-frontend-components
description: Create or modify Vue 3 / Nuxt 4 components for the Portal Centralizado de Datos Financieros. Use when building pages, layouts, tool-call cards, lineage overlay, skeleton/empty/error states, the /admin/usuarios panel, the login page, or any Lazy-wrapped heavy component with Tailwind v4 design tokens.
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
---

# Portal Frontend Components Skill

## Rules — NON-NEGOTIABLE

- Nuxt 4 con estructura **`app/`**: `app/pages/`, `app/components/`, `app/layouts/`, `app/composables/`, `app/middleware/`.
- `<script setup lang="ts">` con tipos obligatorios; props y emits tipados con genéricos.
- **UI SOLO en español** — strings directos en los templates. NO hay i18n en este proyecto (descartado): prohibido `useI18n()`, `t('key')` o locales.
- Componentes pesados (ECharts, modales, overlay de linaje) con prefijo **`Lazy`** (`<LazyVChart/>`) — fuera del bundle inicial.
- TailwindCSS v4 con **tokens del sistema de diseño** (`@theme` en `app/assets/css/main.css`), **derivados de `docs/entregables/estilo/uxdoc.sty` y generados por script** (US-UX-09); nunca colores/espaciados mágicos inline.
- Estados **skeleton / vacío / error** diseñados para cada módulo, con dimensiones reservadas (sin layout shift).
- Sin lógica de negocio en componentes: consumo vía composables/stores (ver `portal-frontend-composables`).
- SSR-safe: `import.meta.client` antes de tocar `window`/`document`. Sin emojis en código ni UI.

## Mapa de componentes por dominio

```
app/
├── pages/
│   ├── login.vue                  # OAuth2 password -> cookie httpOnly
│   ├── index.vue                  # redirige al home del rol (middleware)
│   ├── catalogo.vue               # Data Catalog UI
│   ├── explorador.vue             # Analista: filtros + ECharts + export
│   ├── dashboard.vue              # Directivo: tarjetas predictivas (SWR)
│   └── admin/usuarios.vue         # solo rol admin
├── components/
│   ├── chat/
│   │   ├── ChatPanel.vue          # historial + input + boton Detener
│   │   ├── ToolCallCard.vue       # estados anuncio/ejecucion/resultado/error
│   │   └── LazyLineageOverlay.vue # linaje: tools, parametros, fuentes
│   ├── dashboard/
│   │   ├── InsightCard.vue        # tarjeta predictiva con etiqueta de metodo
│   │   └── LazyChartPanel.vue     # panel expandible con serie ECharts
│   ├── admin/
│   │   ├── UserTable.vue          # tabla + acciones editar/desactivar
│   │   └── UserFormModal.vue      # alta/edicion con confirmacion
│   └── common/
│       ├── SkeletonBlock.vue      # placeholder con altura fija
│       └── EmptyState.vue         # vacio con CTA
```

## Tarjeta de tool call (4 estados)

```vue
<!-- app/components/chat/ToolCallCard.vue -->
<template>
  <div class="rounded-lg border border-border bg-surface p-3" role="status">
    <div class="flex items-center gap-2">
      <span v-if="call.status === 'announced' || call.status === 'running'"
            class="size-4 animate-spin rounded-full border-2 border-accent border-t-transparent" />
      <span class="text-sm font-medium">{{ label }}</span>
      <span v-if="call.durationMs" class="ml-auto text-xs text-muted">{{ call.durationMs }} ms</span>
    </div>
    <div v-if="call.status === 'done' && call.result" class="mt-2 overflow-x-auto">
      <MiniResultTable :rows="call.result.rows" :source="call.result.source" />
    </div>
    <p v-else-if="call.status === 'error'" class="mt-2 text-sm text-danger">
      Fallo al consultar la fuente. La respuesta puede estar incompleta.
    </p>
  </div>
</template>

<script setup lang="ts">
import type { ToolCall } from '~/types/chat'

const props = defineProps<{ call: ToolCall }>()

const LABELS: Record<string, string> = {
  buscar_catalogo: 'Consultando el catalogo de datos',
  consultar_metricas: 'Consultando base de datos',
  solicitar_export: 'Preparando exportacion en segundo plano',
  resumir_vista: 'Resumiendo la vista actual',
}
const label = computed(() =>
  props.call.status === 'done' ? `Consulta completada: ${props.call.tool}` : LABELS[props.call.tool])
</script>
```

## Skeleton sin layout shift

```vue
<!-- app/components/common/SkeletonBlock.vue -->
<template>
  <div :style="{ height }" class="animate-pulse rounded-lg bg-surface-muted" aria-hidden="true" />
</template>

<script setup lang="ts">
defineProps<{ height: string }>()  // misma altura que el contenido real: sin CLS
</script>
```

Patrón de consumo en módulos: `<SkeletonBlock v-if="pending" height="16rem" />` → `<EmptyState v-else-if="!data?.rows.length" />` → contenido; el error muestra mensaje + botón de reintento del módulo.

## Tokens Tailwind v4 (fuente única, derivados de `uxdoc.sty`)

**No inventar colores ni fuentes aquí.** El bloque lo emite `generar_tokens_a4.py` a partir de
`docs/entregables/estilo/uxdoc.sty`, de modo que los documentos del curso y la interfaz sean el
mismo producto. La derivación va en un solo sentido: `uxdoc.sty` → `@theme` → interfaz → capturas
→ PDF. Nada fluye hacia atrás.

```css
/* app/assets/css/main.css — generado, no editar a mano */
@import "tailwindcss";

@theme {
  /* Marca — anclas versionadas en uxdoc.sty */
  --color-primary: #2563EB;        /* uxblue  · accion primaria, enlaces, foco */
  --color-primary-dark: #1F4D78;   /* uxnavy  · barra lateral, cabecera de tabla, titulares */
  --color-secondary: #3B82F6;      /* uxsky   · serie primaria de grafica */
  --color-secondary-soft: #B8CCE4; /* uxpale  · relleno suave, area bajo curva */
  --color-accent: #F97316;         /* uxamber · uso escaso; NUNCA con texto blanco (2.6:1) */
  --color-accent-text: #C2540A;    /* texto de aviso sobre fondo claro */

  /* Neutros — sin negro ni blanco puros */
  --color-surface: #F8FAFC;        /* uxsurface */
  --color-surface-alt: #EEF3FA;    /* uxrow · fila alterna de tabla */
  --color-line: #CBD5E1;           /* uxline */
  --color-muted: #64748B;          /* uxmuted · solo texto secundario de 14px o mas */
  --color-ink: #1E293B;            /* uxink */

  /* Semanticos */
  --color-success: #166534;        /* uxgreen */
  --color-danger: #B91C1C;
  --color-warning: #C2540A;

  /* Tipografia */
  --font-display: "Lexend Deca", sans-serif;  /* solo peso Regular: jerarquia por tamano y color */
  --font-sans: "Fira Sans", sans-serif;

  /* Densidad — ficha Data-Dense Dashboard de ui-ux-pro-max */
  --sidebar-width: 240px;
  --header-height: 56px;
  --grid-gap: 8px;
  --card-padding: 12px;
  --table-row-height: 36px;

  /* Radios — una sola escala; --radius-full es la unica excepcion documentada */
  --radius-sm: 4px;
  --radius-md: 6px;
  --radius-lg: 10px;
}
```

## Panel /admin/usuarios

- `UserTable.vue`: columnas username, nombre, email, rol, estado; badge "Desactivado"; acciones editar y desactivar (soft delete) con modal de confirmación explícita.
- `UserFormModal.vue`: alta con contraseña temporal, edición de datos/rol; errores 409 (duplicado) mostrados junto al campo; jamás renderizar ni loguear contraseñas.
- La página valida rol admin vía middleware (ver `portal-frontend-composables`); usuarios sin scope no ven el enlace del módulo.

## Login

- `login.vue` con layout mínimo sin navegación; form POST a `/api/auth/token` (username + password), errores 401 con mensaje neutro ("Credenciales incorrectas"); al éxito la cookie httpOnly queda establecida y se redirige al home del rol.

## QA Checklist

- [ ] Estructura `app/` respetada; componentes pesados con prefijo `Lazy`
- [ ] Cero strings en inglés en la UI; cero `useI18n`
- [ ] Tokens `@theme` idénticos a los `\definecolor` de `uxdoc.sty`; ningún color escrito a mano
- [ ] Skeleton/vacío/error en cada módulo, sin layout shift
- [ ] ToolCallCard cubre los 4 estados y renderiza resultado antes del texto
- [ ] Panel admin con confirmación de desactivación y manejo de 409
