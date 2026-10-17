---
name: pixijs-2d
description: "PixiJS v8: render 2D WebGL/WebGPU para sprites, sprite sheets, partículas (ParticleContainer), Graphics vectorial, filtros/shaders, BitmapText, juegos 2D y HUD sobre Three.js. No para 3D (threejs-webgl) ni DOM (gsap-scrolltrigger)."
---

# pixijs-2d (índice Senzu, ES)

Documentación completa upstream (inglés): `SKILL.upstream.md` (935 líneas). **No la leas entera**: usa el mapa y lee solo la sección que necesites (Read con offset/limit o Grep).

## Cuándo usar / cuándo NO
- Usar: canvas 2D interactivo de alto rendimiento (miles de sprites a 60 FPS), sistemas de partículas, juegos 2D, animación por sprite sheet.
- Usar: dibujo vectorial programático (Graphics), filtros por píxel (blur, displacement, shaders custom) o capa HUD 2D sobre una escena 3D.
- NO usar: gráficos 3D → `threejs-webgl` / `react-three-fiber`; animación de elementos DOM/UI → `gsap-scrolltrigger`, `motion-framer`, `animejs`.
- NO usar: efectos de fondo ligeros sin canvas propio → `lightweight-3d-effects`.

## Lectura mínima por tarea
| Tarea | Lee solo |
|---|---|
| Empezar un proyecto/starter | `SKILL.upstream.md` L32-58 (§Application & Renderer) + L221-263 (§Pattern 1) + `assets/starter_pixijs/` |
| Partículas | L122-156 (§ParticleContainer) + L319-388 (§Pattern 3) o `scripts/particle_builder.py` |
| Filtros y shaders custom | L158-187 (§Filters) + L390-494 (§Pattern 4-5) + `references/filters_effects.md` |
| Sprite sheet / AnimatedSprite | L496-530 (§Pattern 6) + `references/api_reference.md` |
| Integrar en React o sobre Three.js | L603-689 (§Integration Patterns) |
| Depurar / rendimiento | L691-797 (§Performance Best Practices) + L798-903 (§Common Pitfalls) + `references/performance_guide.md` |

## Mapa de `SKILL.upstream.md`
| Líneas | Sección | Para qué |
|---|---|---|
| 12-28 | When to Use This Skill | Disparadores y cuándo no usar Pixi |
| 30-217 | Core Concepts | Application (32), Sprites & Textures (60), Graphics API (89), ParticleContainer (122), Filters (158), Text/BitmapText (189) |
| 219-601 | Common Patterns | Sprite interactivo (221), Graphics (265), partículas (319), filtros (390), shader custom (431), sprite sheet (496), object pooling (532) |
| 603-689 | Integration Patterns | Componente React con destroy (605); overlay 2D sobre Three.js (647) |
| 691-797 | Performance Best Practices | ParticleContainer, filterArea, memoria de texturas, culling, cacheAsBitmap, ajustes de renderer, BitmapText |
| 798-903 | Common Pitfalls | No destruir objetos, dynamicProperties estáticos, exceso de filtros, Text dinámico, clear() sin redibujar, Sprite.from sin Assets |
| 905-935 | Resources / Related Skills / Summary | Enlaces oficiales y skills relacionadas |

## Recursos
- `references/api_reference.md` — referencia de clases y métodos de PixiJS v8.
- `references/filters_effects.md` — guía de filtros integrados y shaders propios.
- `references/performance_guide.md` — optimización detallada para 60 FPS.
- `scripts/particle_builder.py` — genera un sistema de partículas JS: `py -3 scripts/particle_builder.py --type fountain --count 5000 --output ./` (interactivo sin args).
- `scripts/sprite_generator.py` — genera código de sprite básico/interactivo/animado: `py -3 scripts/sprite_generator.py --type interactive --output ./`.
- `assets/starter_pixijs/` — starter vanilla (index.html, main.js, styles.css, README.md).
- `assets/examples/README.md` — catálogo de ejemplos (juegos, UI, partículas, shaders).

## Reglas duras
- API v8: `await app.init({...})` y `app.canvas`; carga texturas con `await Assets.load()`, nunca `Sprite.from(url)` sin precarga.
- Limpieza obligatoria: `app.destroy(true, { children: true })` al desmontar (React useEffect cleanup) y `sprite.destroy({ texture: true })` para liberar GPU.
- Miles de sprites → `ParticleContainer` con `dynamicProperties` solo en lo que cambia; usa object pooling para spawn/despawn.
- Filtros: máximo 1-2 por objeto, define `filterArea`, hornea filtros en texturas cuando sea estático; `BitmapText` para texto que cambia cada frame.
- En móvil/gama baja: `antialias: false`, `resolution: 1`, `cullable = true`; el canvas debe crearse solo en cliente (SSR-safe: `useEffect`/`onMounted`).

## Integración con el stack del proyecto
- Detecta el stack como indica la skill `front-activation`/`skill-router` (senzu/senzu.json → package.json). PixiJS es agnóstico: en vanilla/Astro instancia en un `<script>` cliente; en React sigue L605-643; en Vue replica el mismo patrón en `onMounted`/`onBeforeUnmount`.
- Para animar propiedades de Pixi con scroll usa `gsap-scrolltrigger`; para combinarlo con 3D, `threejs-webgl` (overlay L647-687).
