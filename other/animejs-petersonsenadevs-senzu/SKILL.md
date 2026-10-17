---
name: animejs
description: "Animaciones DOM/CSS/SVG con Anime.js: timelines con offsets, stagger (grid, from center), dibujo y morphing de paths SVG, keyframes, easings spring/steps. No para scroll-driven complejo (gsap-scrolltrigger) ni React (motion-framer)."
---

# animejs (índice Senzu, ES)

Documentación completa upstream (inglés): `SKILL.upstream.md` (525 líneas). **No la leas entera**: usa el mapa y lee solo la sección que necesites (Read con offset/limit o Grep).

## Cuándo usar / cuándo NO
- Usar: secuencias coreografiadas con `anime.timeline()`, reveals escalonados con `anime.stagger()`, animación de paths SVG (line drawing, morphing, motion path).
- Usar: proyectos vanilla/Vue/Astro donde importa el bundle (~9 KB) y no se quiere dependencia de React.
- NO usar: experiencias scroll-driven, pin, scrub → `gsap-scrolltrigger`; animación declarativa con gestos en React → `motion-framer`; física de muelles en React → `react-spring-physics`.

## Lectura mínima por tarea
| Tarea | Lee solo |
|---|---|
| Empezar un proyecto/starter | `SKILL.upstream.md` L30-135 (§Core Concepts) + `assets/README.md` (Vite vanilla + `npm i animejs`) |
| Stagger / reveal en grid | L138-165 (§1-2) + `references/stagger_guide.md` |
| SVG (línea, morph, seguir path) | L166-193, L293-308 + `scripts/animation_generator.py --type svg-morph` |
| Timeline de hero/modal/menú | L194-218, L111-135 + `references/timeline_guide.md` o `scripts/timeline_builder.py --preset hero` |
| Easings avanzados y control de reproducción | L309-371 (§Advanced Techniques) |
| Integrar en React/Vue | L253-292 (§Integration Patterns) |
| Depurar / rendimiento | L372-424 (§Performance) + L425-500 (§Common Pitfalls) |

## Mapa de `SKILL.upstream.md`
| Líneas | Sección | Para qué |
|---|---|---|
| 10-29 | Overview | Cuándo usar y features clave |
| 30-135 | Core Concepts | `anime()` básico (32), targets (48), propiedades animables CSS/SVG/objetos (67), timeline (111) |
| 136-252 | Common Patterns | Stagger (138), stagger from center (151), SVG line (166), morph (178), timeline (194), keyframes (219), scroll manual (236) |
| 253-308 | Integration Patterns | React con cleanup (255), Vue `mounted` (279), motion path (293) |
| 309-371 | Advanced Techniques | Easing spring/steps/bezier, direction/loop, play/pause/seek |
| 372-424 | Performance Optimization | Solo transform/opacity, batch de targets, `will-change`, `autoplay:false` |
| 425-500 | Common Pitfalls | Unidades, `transform` como string, cleanup, demasiados elementos, offsets de timeline, loops infinitos |
| 501-525 | Resources / Related Skills | Scripts, referencias y comparativa con GSAP/Framer |

## Recursos
- `references/api_reference.md` — API completa Anime.js v3 (parámetros, callbacks, helpers).
- `references/stagger_guide.md` — `anime.stagger()`: grid, from, axis, easing, rangos.
- `references/timeline_guide.md` — secuencias, offsets relativos/absolutos, control de timeline.
- `scripts/animation_generator.py` — boilerplate de 8 tipos (basic, stagger, grid-stagger, svg-line, svg-morph, timeline, keyframe, scroll): `py -3 scripts/animation_generator.py --type stagger` (Linux/mac: `python3 …`).
- `scripts/timeline_builder.py` — presets hero/modal/cards/loader/page/toast/menu: `py -3 scripts/timeline_builder.py --preset modal`.
- `assets/README.md` — solo instrucciones de starter con Vite y enlaces a ejemplos oficiales (no hay carpeta `starter_animejs/` real pese a lo que dice el upstream).

## Reglas duras
- Anima únicamente `translateX/Y`, `scale`, `rotate`, `opacity`; nunca `left/top/width` ni el string `transform`.
- Una llamada `anime()` con varios targets, no un bucle de llamadas; para más de 200 elementos usa CSS animations.
- En React/Vue guarda la instancia y haz `pause()` en el cleanup del efecto/`unmounted`.
- Offsets de timeline siempre con `'-=500'`/`'+=200'`; un número sin operador es tiempo absoluto.
- Sin `loop: true` infinitos por defecto; respeta `prefers-reduced-motion` (salta al estado final con `seek(duration)` o no animes).

## Integración con el stack del proyecto
- Detecta el stack como indica la skill `front-activation`/`skill-router` (senzu/senzu.json → package.json). Es framework-agnóstica: vanilla y Astro (en `<script>` cliente o `client:*`), Vue (`onMounted`/`onUnmounted`), React (`useEffect` con cleanup, L255-278).
- SSR-safe solo si se importa y ejecuta en cliente; en Next/Nuxt/Astro no invoques `anime()` en módulos de servidor.
