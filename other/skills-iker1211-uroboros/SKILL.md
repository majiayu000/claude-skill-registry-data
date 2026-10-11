---
name: adaptive-quality
description: >
  Implementa un sistema de calidad adaptativa para escenas Three.js
  que deban funcionar bien en desktop de gama alta y mobile de gama baja.
  Usa @pmndrs/detect-gpu para clasificar la GPU real del usuario en un
  tier 0-3 basado en benchmark, y aplica un objeto de configuración
  diferenciado antes de crear el renderer. Activa este skill antes de
  escribir cualquier THREE.WebGLRenderer o THREE.WebGPURenderer.
---

# adaptive-quality

## Principio fundamental

La calidad no se elige a mano — se detecta y se asigna automáticamente.
El usuario nunca ve una app degradada: ve lo mejor que su hardware puede dar.
El renderer se crea UNA SOLA VEZ con la config del tier. No se cambia en runtime.

---

## Paso 1 — Detección con @pmndrs/detect-gpu

`@pmndrs/detect-gpu` es asíncrono y debe completarse ANTES de crear el renderer.
Usa un benchmark real de GPU (gfxbench.com), no heurísticas de RAM o cores.
Devuelve un objeto con `{ tier: 0|1|2|3, isMobile, gpu, fps }`.

```js
// Importar desde CDN (ESM)
import { getGPUTier } from 'https://cdn.jsdelivr.net/npm/@pmndrs/detect-gpu@5.0.1/dist/detect-gpu.esm.js';

async function detectTier() {
  try {
    const result = await getGPUTier();
    // tier 0 → GPU desconocida o muy limitada
    // tier 1 → gama baja  (<15fps en benchmark)
    // tier 2 → gama media (<30fps en benchmark)
    // tier 3 → gama alta  (60fps en benchmark)
    return result.tier;
  } catch (_) {
    // Fallback síncrono si detect-gpu falla
    return fallbackTier();
  }
}

function fallbackTier() {
  // Heurística mínima como seguro de falla
  // navigator.deviceMemory no disponible en Firefox → usa 4 como neutro
  const mem   = navigator.deviceMemory     ?? 4;
  const cores = navigator.hardwareConcurrency ?? 4;
  if (mem <= 2 || cores <= 2) return 1;
  if (mem <= 4 || cores <= 4) return 2;
  return 3;
}
```

---

## Paso 2 — Objeto de configuración por tier

Define el objeto de config ANTES de crear cualquier objeto Three.js.
Nunca hardcodees valores de calidad directamente en el código de escena.

```js
const QUALITY_CONFIG = {
  1: {
    dpr:           1.0,
    antialias:     false,
    shadows:       false,
    fog:           false,
    maxInstances:  50,
    toneMapping:   THREE.NoToneMapping,
    pixelRatio:    1.0,
  },
  2: {
    dpr:           1.5,
    antialias:     false,
    shadows:       false,
    fog:           true,
    maxInstances:  200,
    toneMapping:   THREE.ACESFilmicToneMapping,
    pixelRatio:    1.5,
  },
  3: {
    dpr:           2.0,
    antialias:     true,
    shadows:       true,
    fog:           true,
    maxInstances:  1000,
    toneMapping:   THREE.ACESFilmicToneMapping,
    pixelRatio:    2.0,
  },
};

// Tier 0 se trata igual que tier 1
const Q = QUALITY_CONFIG[Math.max(tier, 1)];
```

---

## Paso 3 — Aplicar en la inicialización

```js
async function initScene() {
  const tier = await detectTier();
  const Q    = QUALITY_CONFIG[Math.max(tier, 1)];

  // ── Renderer ──────────────────────────────────────
  const renderer = new THREE.WebGLRenderer({ antialias: Q.antialias });
  renderer.setPixelRatio(Math.min(devicePixelRatio, Q.dpr));
  renderer.setSize(innerWidth, innerHeight);
  renderer.toneMapping      = Q.toneMapping;
  renderer.outputColorSpace = THREE.SRGBColorSpace;
  renderer.shadowMap.enabled = Q.shadows;

  // ── Escena ────────────────────────────────────────
  if (Q.fog) {
    scene.fog = new THREE.FogExp2(0x0d0f1a, 0.022);
  }

  // ── Iluminación ───────────────────────────────────
  const sun = new THREE.DirectionalLight(0xffe5b0, 1.6);
  sun.position.set(10, 20, 12);
  if (Q.shadows) {
    sun.castShadow = true;
    sun.shadow.mapSize.width  = 1024;
    sun.shadow.mapSize.height = 1024;
  }
  scene.add(sun);

  // ── Instancias: respetar maxInstances ─────────────
  // Pasar Q.maxInstances al sistema de world compositor
  buildWorld(Q.maxInstances);
}
```

---

## Parámetros escalables por tier

| Parámetro              | Tier 1 (gama baja) | Tier 2 (media) | Tier 3 (alta) |
|------------------------|-------------------|----------------|---------------|
| `devicePixelRatio` cap | 1.0               | 1.5            | 2.0           |
| `antialias`            | false             | false          | true          |
| Sombras                | off               | off            | on (1024px)   |
| Fog                    | off               | on             | on            |
| Max instancias/tipo    | 50                | 200            | 1000          |
| `toneMapping`          | NoToneMapping     | ACESFilmic     | ACESFilmic    |

---

## Pitfalls críticos

**1. Nunca crear el renderer antes de detectar el tier.**
`getGPUTier()` es async. Si creas el renderer antes, los parámetros ya están fijos.

**2. `devicePixelRatio` en Android puede ser 3.0 o más.**
Sin cap, un Samsung gama baja renderiza a resolución 3x → muerte de FPS.
Siempre: `Math.min(devicePixelRatio, Q.dpr)`.

**3. Antialias no existe en WebGL en muchos Android.**
El fallback software es peor que no tener antialias.
Para gama baja: false siempre.

**4. `navigator.deviceMemory` no existe en Firefox.**
Por eso el fallback usa `?? 4` (neutro) y no falla.

**5. Tier 0 = GPU desconocida, no GPU mala.**
Una GPU enterprise sin benchmark puede ser tier 0.
Tratar tier 0 igual que tier 1 (conservador) es lo correcto.

---

## Integración con el mundo hex

`maxInstances` del tier se pasa al HexGridContext como límite de instancias por tipo de tile.
Si el mundo tiene más celdas que `maxInstances`, se recorta o se agrupan tiles fuera de cámara.
El tier también puede controlar el radio del grid visible (frustum culling manual por distancia).
