---
name: threejs-webgl
description: "3D/WebGL con Three.js: modelos GLB, heros 3D, configuradores, partículas, shaders, scroll 3D. TresJS (Vue/Inertia), R3F (Next), vanilla (Astro); assets, rendimiento móvil, dispose, fallback. No para charts, 2D ni animación DOM (gsap)."
---

# threejs-webgl (capa Senzu, en español)

Skill upstream (inglés): `SKILL.upstream.md` (fundamentos, WebGPU, materiales, postprocesado, patrones),
`references/api_reference.md`, `references/materials_guide.md`, `references/optimization_checklist.md`,
`assets/starter_scene/`, `scripts/setup_scene.py`. Capa Senzu (español): `references/es/` y `templates/`.
Para React declarativo existe además la skill `react-three-fiber`; para combinar 3D + GSAP + Motion, `web3d-integration-patterns`.

Construyes 3D **útil y rápido**: refuerza el producto, carga en < 2 s, no rompe el LCP, funciona en móvil y desaparece
con elegancia sin WebGL o con `prefers-reduced-motion`. Estética y tono salen del `senzu/design-system/*/MASTER.md`
(skill `ui-ux-pro-max`); el movimiento ligado al scroll se coordina con `gsap-scrolltrigger`.

## 1. Detectar el stack e integrar
| Stack (perfil Senzu) | Integración | Referencia | Plantillas |
|---|---|---|---|
| Vue 3 (SPA o Laravel + Inertia) | TresJS (`@tresjs/core` + `@tresjs/cientos`) | `references/es/tresjs-vue.md` | `templates/HeroScene.vue`, `HeroContent.vue`, `useWebGLSupport.ts` |
| Next.js / React | React Three Fiber + drei, `next/dynamic` `ssr:false` | `references/es/r3f-next.md` (+ skill `react-three-fiber`) | `templates/HeroScene.tsx` |
| Astro | clase vanilla + `<script>` con View Transitions | `references/es/vanilla-astro.md` | `templates/scene.ts`, `scene-astro.ts`, `loading-overlay.html` |
| Vanilla / otros | clase `Scene` (init/resize/loop/dispose) | `SKILL.upstream.md`, `references/es/fundamentals.md` | `templates/scene.ts` |

Comprueba versiones instaladas (`@tresjs/cientos` cambió la API de `useGLTF`; nombres de `@tresjs/post-processing`
dependen del release): lee `node_modules/@tresjs/*/dist/*.d.ts` si dudas. No inventes APIs.

## 1b. Lectura mínima por tarea
| Tarea | Lee solo |
|---|---|
| Hero 3D con modelo GLB | referencia ES de tu stack (§setup + §GLTF) + plantilla `HeroScene.*` + `references/es/assets-loaders.md` §optimizar |
| Configurador de producto | referencia ES de tu stack + `references/es/fundamentals.md` §materiales/luces |
| Partículas / shader / distorsión de imagen | `references/es/shaders-basics.md` (sección del efecto) |
| Scroll-driven 3D | `references/es/gsap-three.md` |
| Va lento / consume memoria | `references/es/performance.md` §presupuesto + §dispose |
| Se ve lavado, negro o no aparece | `references/es/pitfalls.md` (Grep por el síntoma) |
| API concreta de Three.js | `references/api_reference.md` upstream (Grep) o `SKILL.upstream.md` por sección |

## 2. Flujo
1. **Objetivo y presupuesto**: qué aporta el 3D, dispositivo objetivo, peso del asset (hero ≤ 2 MB, texturas ≤ 2048 px,
   draw calls < 100 en móvil), tiempo de carga aceptable.
2. **Asset** (`references/es/assets-loaders.md`): GLB con transforms aplicados, `gltf-transform optimize in.glb out.glb
   --texture-compress webp` (+ Draco/Meshopt), verificado en un visor; en `public/models/`.
3. **Renderer correcto**: `outputColorSpace = SRGBColorSpace`, `toneMapping = ACESFilmicToneMapping`,
   `setPixelRatio(Math.min(devicePixelRatio, 2))`, sombras solo si aportan.
4. **Carga progresiva**: canvas lazy (`defineAsyncComponent` / `next/dynamic` / `client:visible`), overlay de progreso
   accesible, placeholder estático que mantiene el LCP.
5. **Interacción**: `Raycaster` o eventos de TresJS/R3F; `OrbitControls` con damping y límites; sin zoom por rueda en heros.
6. **Rendimiento y limpieza** (`references/es/performance.md`): pausar fuera del viewport y con pestaña oculta;
   `dispose()` de geometrías/materiales/texturas/renderer al desmontar (las SPA navegan sin recargar).
7. **Fallbacks**: sin WebGL → imagen/vídeo; reduced-motion → escena estática; `webglcontextlost` gestionado.
8. **Verificar**: FPS ≥ 50 en móvil medio (CPU 4x), memoria estable tras navegar 5 veces, consola limpia, Lighthouse ≥ 85.

## 3. Reglas duras
- Nada de Three.js en SSR: importar solo en cliente. Un solo `WebGLRenderer` por página.
- Siempre `dispose` al desmontar. Pixel ratio ≤ 2 (1,5 en móvil si hace falta).
- Color space correcto (`texture.colorSpace = SRGBColorSpace` solo en mapas de color).
- Sin modelos > 5 MB sin aprobación; texturas KTX2/WebP, geometría Draco/Meshopt.
- El 3D no bloquea el contenido: texto y CTA son HTML accesible encima del canvas.
- Sin `Stats`, Leva, helpers ni `markers` en producción.
- Errores frecuentes y solución: `references/es/pitfalls.md` (40 casos).

## 4. Decisiones rápidas
| Necesidad | Solución |
|---|---|
| Hero con modelo que gira y sigue al ratón | TresJS/R3F + `useGLTF` + loop con lerp hacia el puntero |
| Producto configurable | Un GLB, `material.color.set(token)`, `Environment` HDRI, `ContactShadows` |
| Scroll-driven 3D (cámara por secciones) | GSAP timeline con labels + ScrollTrigger `scrub` (`references/es/gsap-three.md`) |
| Fondo de partículas ligero | `Points` + shader (`references/es/shaders-basics.md`), ≤ 20k puntos en móvil |
| Distorsión de imagen al hover | plane + `ShaderMaterial` con `uHover`/`uTime` |
| Escena hecha en Spline | exportar GLB e integrarlo aquí (evita el runtime de Spline) — ver skill `spline-interactive` |
| Muchas copias del mismo objeto | `InstancedMesh` |
| Vidrio/reflejos realistas | `MeshPhysicalMaterial` + `transmission` + `Environment` (solo desktop) |

## 5. Salida esperada
Antes del código: objetivo, presupuesto, integración elegida, fallback y limpieza. Después: código + pasos de
optimización del asset + verificación (FPS, memoria, consola).
