---
name: maplibre-layers
description: >-
  Use when adding map layers, managing GeoJSON sources, styling markers, or
  handling layer interactions. Load for layer registration patterns, markRaw
  usage, MglGeoJsonSource components, data-driven styling, and layer event
  handling. Covers the mapLayers store and dynamic layer composition.
---

# MapLibre Layers

Layer management patterns for map visualization.

> **Announce:** "I'm using maplibre-layers to implement map layers correctly."

## Layer Registration Pattern

Views register layers via the `mapLayers` store:

```typescript
// src/stores/mapLayers.ts
import { markRaw } from 'vue'

export const useMapLayersStore = defineStore('mapLayers', () => {
  const layers = ref<MapLayer[]>([])

  function setLayers(newLayers: MapLayer[]) {
    // CRITICAL: markRaw prevents Vue from making components reactive
    layers.value = newLayers.map(l => ({
      ...l,
      component: markRaw(l.component)
    }))
  }

  function clearLayers() {
    layers.value = []
  }

  return { layers, setLayers, clearLayers }
})
```

**In a view:**

```typescript
// GameView.vue
import CandidatesLayer from '@/components/map/CandidatesLayer.vue'
import { MAP_KEY } from '@/composables/map/useMapCamera'

const mapLayersStore = useMapLayersStore()

onMounted(() => {
  mapLayersStore.setLayers([{
    key: 'candidates',
    component: CandidatesLayer,
    props: { 
      candidates: candidates,
      mapKey: MAP_KEY
    }
  }])
})

onUnmounted(() => {
  mapLayersStore.clearLayers()
})
```

**In BaseMap.vue:**

```vue
<template>
  <MglMap ...>
    <component
      v-for="layer in layers"
      :key="layer.key"
      :is="layer.component"
      v-bind="layer.props"
    />
  </MglMap>
</template>
```

## GeoJSON Layer Pattern

Use `MglGeoJsonSource` with layer components:

```vue
<!-- CandidatesLayer.vue -->
<template>
  <MglGeoJsonSource 
    source-id="candidates" 
    :data="candidatesGeoJson"
  >
    <!-- Circle markers -->
    <MglCircleLayer
      layer-id="candidates-circles"
      :paint="{
        'circle-radius': ['get', 'radius'],
        'circle-color': ['get', 'color'],
        'circle-opacity': 0.8
      }"
    />
  </MglGeoJsonSource>
</template>

<script setup lang="ts">
const props = defineProps<{
  candidates: Candidate[]
}>()

const candidatesGeoJson = computed(() => ({
  type: 'FeatureCollection' as const,
  features: props.candidates.map(c => ({
    type: 'Feature' as const,
    geometry: {
      type: 'Point' as const,
      coordinates: [c.lng, c.lat]
    },
    properties: {
      id: c.id,
      name: c.name,
      radius: Math.max(5, c.confidence * 20),
      color: getColorForConfidence(c.confidence)
    }
  }))
}))
</script>
```

## Data-Driven Styling

Use MapLibre expressions for dynamic styling:

```typescript
// Interpolate color based on confidence
const paintConfig = {
  'circle-color': [
    'interpolate',
    ['linear'],
    ['get', 'confidence'],
    0, '#gray',
    0.5, '#yellow', 
    1.0, '#green'
  ],
  'circle-radius': [
    'interpolate',
    ['linear'],
    ['zoom'],
    2, 3,   // At zoom 2, radius 3
    10, 15  // At zoom 10, radius 15
  ]
}
```

## Layer Event Handling

Handle clicks and hovers on layers:

```vue
<script setup lang="ts">
import { inject, onMounted, onUnmounted } from 'vue'
import type { Map as MapLibreMap } from 'maplibre-gl'

const props = defineProps<{ mapKey: symbol }>()
const map = inject<MapLibreMap>(props.mapKey)

function handleClick(e: any) {
  const feature = e.features?.[0]
  if (feature) {
    emit('placeClick', feature.properties.id)
  }
}

function handleMouseEnter() {
  if (map) map.getCanvas().style.cursor = 'pointer'
}

function handleMouseLeave() {
  if (map) map.getCanvas().style.cursor = ''
}

onMounted(() => {
  if (!map) return
  map.on('click', 'candidates-circles', handleClick)
  map.on('mouseenter', 'candidates-circles', handleMouseEnter)
  map.on('mouseleave', 'candidates-circles', handleMouseLeave)
})

onUnmounted(() => {
  if (!map) return
  map.off('click', 'candidates-circles', handleClick)
  map.off('mouseenter', 'candidates-circles', handleMouseEnter)
  map.off('mouseleave', 'candidates-circles', handleMouseLeave)
})
</script>
```

## HTML Markers for Labels

Use HTML markers for complex labels (Vue components):

```vue
<template>
  <!-- Native layer for performance -->
  <MglGeoJsonSource ...>
    <MglCircleLayer ... />
  </MglGeoJsonSource>
  
  <!-- HTML markers for labels -->
  <MglMarker
    v-for="candidate in topCandidates"
    :key="candidate.id"
    :lng-lat="[candidate.lng, candidate.lat]"
    :offset="[0, -20]"
  >
    <div class="candidate-label">
      {{ candidate.name }}
    </div>
  </MglMarker>
</template>
```

**When to use what:**
- **Native layers** (MglCircleLayer, MglFillLayer): Thousands of points, GPU-accelerated
- **HTML markers** (MglMarker): Complex styling, Vue components, limited count

## Anti-Patterns

### DON'T: Skip markRaw

```typescript
// WRONG: Vue makes component reactive (bad performance)
layers.value = [{ component: MyLayer }]

// CORRECT: markRaw prevents reactivity
layers.value = [{ component: markRaw(MyLayer) }]
```

### DON'T: Forget Cleanup

```typescript
// WRONG: Event listeners leak
onMounted(() => {
  map.on('click', 'layer', handler)
})

// CORRECT: Clean up on unmount
onUnmounted(() => {
  map.off('click', 'layer', handler)
})
```

### DON'T: Mutate GeoJSON Directly

```typescript
// WRONG: Mutating doesn't trigger reactivity
candidatesGeoJson.value.features.push(newFeature)

// CORRECT: Create new object
candidatesGeoJson.value = {
  ...candidatesGeoJson.value,
  features: [...candidatesGeoJson.value.features, newFeature]
}
```

## Layer Ordering

Layers render in order added. Control z-order with `beforeId`:

```vue
<MglFillLayer
  layer-id="regions"
  :beforeId="'candidates-circles'"  <!-- Render below circles -->
/>
```

## References

See `references/layer-examples.md` for more patterns.
