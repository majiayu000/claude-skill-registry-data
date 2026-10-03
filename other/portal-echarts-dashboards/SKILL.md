---
name: portal-echarts-dashboards
description: Build high-performance Apache ECharts dashboards for the Portal with vue-echarts LazyVChart, one-million-point series via server-side Polars aggregation plus ECharts sampling/large, SWR routeRules on the executive dashboard, drill-down events into the Pinia store, and frame-drop measurement. Use when creating or tuning charts, dashboard routes, or the 1M-point demo view.
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
---

# Portal ECharts Dashboards Skill

## Rules — NON-NEGOTIABLE

- Todo chart via `vue-echarts` envuelto como **`<LazyVChart/>`** — fuera del bundle inicial (Time to Interactive). Imports modulares de `echarts/core` (tree-shaking), nunca `import * as echarts`.
- La vista demo debe sostener una serie de **≥1M puntos** con pan/zoom fluido: agregación **server-side con Polars** (el endpoint semántico devuelve puntos ya reducidos por bucket) + `sampling: 'lttb'` y `large: true` en la serie. **Degradación acordada**: 500K pre-agregados si el gate de rendimiento falla (§10.2) — decisión de equipo, no silenciosa.
- **SWR vía `routeRules`** en las rutas del dashboard directivo: carga percibida instantánea + revalidación en segundo plano.
- Interacciones de drill-down (click en barra, brush en serie) **emiten eventos al store Pinia** `workspace` — base del estado compartido dashboard↔chat (ver `portal-frontend-composables`).
- Datos con `useFetch` (shallowRef default de Nuxt 4); jamás reactividad profunda sobre las series.
- Fluidez medida: contador de frame drops durante pan/zoom en la vista demo, registrado antes de cerrar la US.
- Textos de ejes, tooltips y leyendas en español; sin emojis.

## routeRules SWR

```typescript
// nuxt.config.ts
export default defineNuxtConfig({
  routeRules: {
    '/dashboard': { swr: 60 },          // directivo: instantaneo + revalida cada 60 s
    '/dashboard/**': { swr: 60 },
    '/explorador': { ssr: true },       // analista: datos frescos por filtros
  },
})
```

## Serie temporal de liquidez — 1M puntos

```vue
<!-- app/components/dashboard/LiquidityTimeSeries.vue -->
<template>
  <div class="h-80">
    <SkeletonBlock v-if="pending" height="20rem" />
    <LazyVChart v-else :option="option" autoresize @datazoom="onZoom" />
  </div>
</template>

<script setup lang="ts">
import { use } from 'echarts/core'
import { CanvasRenderer } from 'echarts/renderers'
import { LineChart } from 'echarts/charts'
import { GridComponent, TooltipComponent, DataZoomComponent } from 'echarts/components'

use([CanvasRenderer, LineChart, GridComponent, TooltipComponent, DataZoomComponent])

const workspace = useWorkspaceStore()
const { serie, pending } = useSerieLiquidez(toRef(workspace, 'filters'))

const option = computed(() => ({
  tooltip: { trigger: 'axis' },
  xAxis: { type: 'time' },
  yAxis: { type: 'value', name: 'Posicion de liquidez (MXN)' },
  dataZoom: [{ type: 'inside' }, { type: 'slider' }],
  series: [{
    type: 'line',
    showSymbol: false,
    sampling: 'lttb',        // downsampling perceptual en cliente
    large: true,             // pipeline optimizado para volumen
    largeThreshold: 2000,
    data: serie.value?.points ?? [],   // [[ts, valor], ...] ya agregados por Polars
  }],
}))

function onZoom(params: unknown) {
  workspace.applyDrillDown('rangoFechas', extractRange(params))  // drill-down -> Pinia
}
</script>
```

## Endpoint de agregación server-side (contrato)

El componente NUNCA pide filas crudas: pide la métrica con un bucket objetivo y el compilador semántico genera el `group_by_dynamic` de Polars.

```python
# backend: /api/liquidez  body -> {"metric": "posicion_diaria", "bucket": "1h", "max_points": 20000}
# Polars: df.group_by_dynamic("ts", every=bucket).agg(pl.col("valor").mean())
# Respuesta: {"points": [[ts, valor], ...], "source": {"tabla": "liquidez", "campo": "pos_dia"}, "row_count_raw": 1_000_000}
```

## Tipos de gráfica del proyecto

| Gráfica | Tipo ECharts | Vista | Drill-down emitido |
|---------|-------------|-------|--------------------|
| Serie temporal de liquidez | `line` + `sampling`/`large` + dataZoom | dashboard directivo, explorador | `rangoFechas` |
| Mora por producto | `bar` (click en barra) | dashboard, explorador | `producto` |
| Heatmap (p. ej. mora x bucket de vencimiento) | `heatmap` + `visualMap` | explorador | `producto` + `bucket` |

Cada tipo vive en su componente con props tipadas (`points`, `loading`); registrar en `echarts/core` SOLO los módulos que usa.

## Medición de fluidez

```typescript
// app/composables/useFrameDropMeter.ts — solo en la vista demo, detras de ?perf=1
export function useFrameDropMeter() {
  const drops = ref(0)
  let last = 0
  function loop(ts: number) {
    if (last && ts - last > 34) drops.value++   // >2 frames a 60 fps
    last = ts
    requestAnimationFrame(loop)
  }
  onMounted(() => { if (import.meta.client) requestAnimationFrame(loop) })
  return { drops }
}
```

Gate de la US: pan/zoom sobre la serie de 1M sin jank perceptible y drops estables; si falla en hardware del equipo, activar la degradación de 500K pre-agregados y documentar la decisión.

## QA Checklist

- [ ] Todos los charts como `LazyVChart` con imports modulares de echarts/core
- [ ] Serie demo >=1M: Polars agrega server-side, `sampling: 'lttb'` + `large: true`
- [ ] `routeRules` SWR activo en `/dashboard`
- [ ] Drill-down (click/zoom) actualiza el store `workspace`
- [ ] Sin reactividad profunda sobre puntos (shallowRef de useFetch)
- [ ] Frame drops medidos y registrados; degradación 500K solo con acuerdo de equipo
