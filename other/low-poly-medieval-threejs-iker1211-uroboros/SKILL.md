---
name: low-poly-medieval-threejs
description: >
  Configuración de escena Three.js optimizada para assets low-poly medievales
  de KayKit. Cubre iluminación sin normal maps, tone mapping, fog, color space,
  calibración de cámara para el hex grid, y decisiones estéticas específicas
  al estilo low-poly de KayKit (atlas de texturas compartido, ausencia de PBR
  complejo, paleta de colores plana). Activa este skill antes de configurar
  cualquier escena Three.js con assets KayKit medievales.
---

# low-poly-medieval-threejs

## Por qué low-poly cambia la configuración de escena

Los assets low-poly no tienen normal maps ni roughness/metalness maps complejos.
Esto cambia radicalmente qué configuraciones de render valen la pena y cuáles son desperdicio:

- **Sombras suaves (PCFSoft):** visualmente impactantes en low-poly, barato de calcular
- **Point lights / spot lights:** caros, y en low-poly la facetación rompe el efecto
- **HDRI environment maps:** overkill — un AmbientLight + DirectionalLight es suficiente
- **Normal maps:** los assets no los tienen — activarlos no cambia nada
- **Tone mapping ACES:** mejora mucho la temperatura de color calientre de los assets KayKit

---

## Setup de escena mínimo y correcto

```js
// ── Renderer ──────────────────────────────────────────
const renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
renderer.setPixelRatio(Math.min(devicePixelRatio, 2));
renderer.setSize(innerWidth, innerHeight);

// Obligatorio para que los colores de KayKit se vean como en Blender
renderer.outputColorSpace = THREE.SRGBColorSpace;

// ACESFilmic da calidez mediterránea/épica — idóneo para medieval
renderer.toneMapping         = THREE.ACESFilmicToneMapping;
renderer.toneMappingExposure = 1.0; // Ajustar entre 0.8-1.2 según paleta

// Sombras suaves — visualmente importantes en low-poly
renderer.shadowMap.enabled = true;
renderer.shadowMap.type    = THREE.PCFSoftShadowMap;

document.body.appendChild(renderer.domElement);
```

---

## Iluminación: la configuración que funciona con KayKit

### Luz principal (sol)

```js
const sun = new THREE.DirectionalLight(0xffe5b0, 1.6);
// 0xffe5b0 = blanco cálido ligeramente amarillo → paleta medieval
// intensidad 1.6 con ACESFilmic → apariencia natural sin quemar
sun.position.set(10, 20, 12); // ángulo de mediodía ligeramente lateral

sun.castShadow = true;
sun.shadow.mapSize.width  = 1024; // 2048 para tier 3, 512 para tier 1
sun.shadow.mapSize.height = 1024;

// Shadow camera calibrada para un grid hex 5x5 (ajustar al tamaño real del mundo)
sun.shadow.camera.left   = -22;
sun.shadow.camera.right  =  22;
sun.shadow.camera.top    =  22;
sun.shadow.camera.bottom = -22;
sun.shadow.camera.near   =  1;
sun.shadow.camera.far    =  60;
sun.shadow.camera.updateProjectionMatrix(); // Obligatorio después de cambiar propiedades

scene.add(sun);
```

### Luz de relleno (fill)

```js
const fill = new THREE.DirectionalLight(0x5580a0, 0.35);
// Azul frío → simula luz de cielo/ambiente en el lado de sombra
// Intensidad baja: solo suaviza las sombras, no compite con el sol
fill.position.set(-6, 6, -10);
scene.add(fill);
```

### Luz ambiente (base)

```js
const ambient = new THREE.AmbientLight(0x8fb0d0, 0.9);
// Azul grisáceo → temperatura de ambiente exterior de día nublado
// Sin ambient, las sombras de KayKit son negro puro — demasiado duro
scene.add(ambient);
```

### Por qué no usar PointLight ni SpotLight con low-poly

Los assets low-poly tienen polígonos grandes. Una PointLight crea gradientes
de color visibles por cara, rompiendo la estética flat. DirectionalLight
ilumina uniformemente y respeta la paleta plana de KayKit.

---

## Niebla

```js
// FogExp2 → densidad exponencial, más natural que la lineal para exteriores
scene.fog = new THREE.FogExp2(
  0x1a252c,  // color de fondo/cielo — debe coincidir con scene.background
  0.022      // densidad: 0.015 = poca niebla, 0.035 = muy cerrada
);
scene.background = new THREE.Color(0x1a252c);

// Para tier 1 (gama baja): scene.fog = null → ahorra cálculo por fragmento
```

---

## Cámara para hex grid medieval

```js
// PerspectiveCamera con FOV bajo → compresión épica/isométrica
// FOV 45-52: isométrico evocador
// FOV >60: demasiado "FPS", pierde la sensación de mapa de estrategia
const camera = new THREE.PerspectiveCamera(
  52,                          // fov
  innerWidth / innerHeight,    // aspect
  0.1,                         // near
  100                          // far — suficiente para un grid de 10×10
);

// Posición para ver un grid 5×5 de hexágonos KayKit (HEX_W=1.82, HEX_H=1.575)
// El grid ocupa ~11 unidades de ancho y ~6 de alto
camera.position.set(0, 12, 16);
// camera.lookAt(0, 0, 0) — OrbitControls lo maneja automáticamente

const controls = new OrbitControls(camera, renderer.domElement);
controls.enableDamping   = true;
controls.dampingFactor   = 0.05;
controls.maxPolarAngle   = Math.PI / 2.1; // No bajar de la línea del suelo
controls.target.set(0, 0, 0);
```

### Escalado de posición de cámara según tamaño de grid

| Grid      | Celdas | Posición cámara sugerida |
|-----------|--------|--------------------------|
| 5×5       | 25     | (0, 12, 16)              |
| 10×10     | 100    | (0, 22, 30)              |
| 20×20     | 400    | (0, 40, 55)              |

---

## Propiedades específicas de KayKit

### Atlas de texturas compartido

Todos los assets del mismo pack comparten una o dos texturas (atlas PNG).
Esto significa que `MeshStandardMaterial` ya apunta al mismo texture object
en GPU si se carga desde el mismo GLTF. No forzar clones de material.

```js
// ✔ CORRECTO — compartir material de los sub-meshes del GLTF
const inst = new THREE.InstancedMesh(src.geometry, src.material, count);

// ✗ INCORRECTO — clonar el material duplica la textura en GPU
const inst = new THREE.InstancedMesh(src.geometry, src.material.clone(), count);
```

### Sub-meshes por tipo de asset (calibrado con el PoC)

| Tipo              | Sub-meshes típicos | Estrategia          |
|-------------------|--------------------|---------------------|
| Hex tile          | 1                  | 1 InstancedMesh     |
| Prop ambiente     | 1-3                | 1 InstancedMesh/sub |
| Building          | 2-6                | Mesh clone          |
| Character         | 3-8                | Mesh clone          |

### Coordenadas de elevación recomendadas

KayKit hex tiles tienen su base en Y=0 y top en Y≈0.14.
Los assets que se colocan encima (L1, L2) deben iniciar en Y=0 —
la mayoría ya tienen su propia base. Solo ajustar si hay interpenetración visual.

```js
// L1 props: colocar en Y=0, el asset lleva su propia base
obj.position.y = 0;

// Si hay interpenetración visual del prop con el tile:
obj.position.y = 0.05; // offset mínimo
```

---

## Checklist antes de render

```
☐ renderer.outputColorSpace = THREE.SRGBColorSpace
☐ renderer.toneMapping = THREE.ACESFilmicToneMapping
☐ AmbientLight (0x8fb0d0, 0.9) añadida
☐ DirectionalLight principal (0xffe5b0, 1.6) con sombras
☐ DirectionalLight fill (0x5580a0, 0.35) en lado opuesto
☐ scene.background y scene.fog con el mismo color
☐ sun.shadow.camera.updateProjectionMatrix() llamado
☐ OrbitControls.maxPolarAngle ≤ Math.PI/2 (no girar bajo el suelo)
☐ Materiales de InstancedMesh NO clonados
☐ instanceMatrix.needsUpdate = true en cada InstancedMesh
```

---

## Pitfalls específicos de KayKit + Three.js

**1. Sin `outputColorSpace = SRGBColorSpace`, los colores se ven saturados/incorrectos.**
KayKit exporta texturas en sRGB. Sin este flag, Three.js las interpreta en linear.

**2. `Object.assign` falla en propiedades de Object3D.**
`position`, `rotation`, `scale` son getters. Usar `.set()`, `.copy()`, o asignación directa.
```js
// ✗ sun.shadow.camera = { left: -22, ... }  → ERROR
// ✔ sun.shadow.camera.left = -22;            → CORRECTO
```

**3. Sin `updateProjectionMatrix()` en la shadow camera, las sombras no actualizan.**
Llamarlo siempre después de cambiar left/right/top/bottom/near/far de la shadow camera.

**4. `FogExp2` con densidad >0.04 tapa todo el grid en grids grandes.**
Calibrar densidad según el radio del grid: `densidad ≈ 0.5 / (radio_en_unidades * 10)`.
