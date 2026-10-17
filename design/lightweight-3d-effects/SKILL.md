---
name: lightweight-3d-effects
description: "Efectos 3D ligeros y decorativos con Zdog (pseudo-3D), Vanta.js (fondos animados WebGL) y Vanilla-Tilt (tilt parallax en tarjetas). Para heros, landings, iconos 3D, tilt cards. No para escenas 3D reales, modelos glTF ni WebXR."
---

# lightweight-3d-effects (índice Senzu, ES)

Documentación completa upstream (inglés): `SKILL.upstream.md` (1091 líneas). **No la leas entera**: usa el mapa y lee solo la sección que necesites (Read con offset/limit o Grep).

## Cuándo usar / cuándo NO
- Usar: fondo animado de hero/sección (Vanta WAVES, NET, FOG, CLOUDS, BIRDS...) sin montar Three.js a mano.
- Usar: ilustraciones o iconos pseudo-3D vectoriales con Zdog (canvas/SVG, ~28 kB, dragRotate).
- Usar: tarjetas con tilt parallax, glare y capas `translateZ` con Vanilla-Tilt (data-attributes o API).
- NO usar: escenas 3D con modelos, luces o físicas → threejs-webgl / react-three-fiber; escenas Spline → spline-interactive.
- NO usar: animación DOM general o scroll → gsap-scrolltrigger; animaciones React declarativas → motion-framer.

## Lectura mínima por tarea
| Tarea | Lee solo |
|---|---|
| Empezar un proyecto/starter | `SKILL.upstream.md` L716-926 (§Common Patterns) + `assets/starter_lightweight/` |
| Fondo animado Vanta (elegir efecto, opciones, React) | L270-516 (§Vanta.js) + `references/vantajs_effects.md` |
| Ilustración/icono Zdog (formas, grupos, animación) | L22-268 (§Zdog) + `references/zdog_api.md` |
| Tilt en tarjetas (opciones, glare, capas, React) | L518-714 (§Vanilla-Tilt.js) + `references/tilt_patterns.md` |
| Depurar / rendimiento | L928-1068 (§Performance Best Practices + §Common Pitfalls) |

## Mapa de `SKILL.upstream.md`
| Líneas | Sección | Para qué |
|---|---|---|
| 8-21 | Overview / When to Use This Skill | Qué cubre cada librería y casos de uso |
| 22-268 | Zdog - Pseudo-3D Illustrations | Setup (35), Shapes (96), Groups (170), Animation (229) |
| 270-516 | Vanta.js - Animated 3D Backgrounds | Setup (283), Available Effects (338), Config (429), Methods destroy/setOptions (454), React (476) |
| 518-714 | Vanilla-Tilt.js - Parallax Tilt Effects | Setup (531), Config Options (567), Advanced glare/capas/API (607), React (676) |
| 716-926 | Common Patterns | Hero Vanta (718), grid iconos Zdog (761), galería tilt (826), Vanta + tilt combinados (877) |
| 928-971 | Performance Best Practices | Límites por librería, fallback móvil, `will-change` |
| 973-1068 | Common Pitfalls | Múltiples Vanta (975), fugas en SPA (997), Zdog en blanco (1014), tilt móvil (1040), colores Vanta (1054) |
| 1070-1091 | Resources / Related Skills | Enlaces oficiales y skills relacionadas |

## Recursos
- `references/zdog_api.md` — API completa de Zdog: Illustration, Anchor, formas, propiedades, animación.
- `references/vantajs_effects.md` — Catálogo de efectos Vanta con todas sus opciones y dependencias (Three.js / p5.js).
- `references/tilt_patterns.md` — Patrones y opciones avanzadas de Vanilla-Tilt (gyroscope, glare, capas).
- `scripts/generate_zdog.py` — Genera ilustraciones Zdog por tipo: `py -3 scripts/generate_zdog.py --type cube` (`--list` para ver tipos; sin args = interactivo).
- `scripts/setup_vanta.py` — Genera el HTML/JS de un fondo Vanta: `py -3 scripts/setup_vanta.py --effect waves` (`--list` para efectos).
- `assets/starter_lightweight/` — Starter vanilla (index.html, main.js, style.css, README) con las tres librerías.
- `assets/examples/README.md` — Ejemplos de producción: heros, product cards, portfolios, dashboards.

## Reglas duras
- Máximo 1-2 instancias Vanta por página; carga perezosa con IntersectionObserver y fallback a gradiente estático en móvil.
- En SPA/React llama siempre a `vantaEffect.destroy()` y `element.vanillaTilt.destroy()` en el cleanup del efecto.
- Vanta usa colores como número hex (`0x23153c`), nunca strings `"#23153c"`.
- Zdog: llama `illo.updateRenderGraph()` tras cada cambio; canvas con width/height explícitos; < 100 formas para 60 fps; canvas para animación, SVG para estático.
- Respeta `prefers-reduced-motion`: desactiva fondos animados y tilt (no lo cubre el upstream; es norma del proyecto).

## Integración con el stack del proyecto
- Detecta el stack como indica la skill `front-activation`/`skill-router` (senzu/senzu.json → package.json).
- Las tres librerías son vanilla (funcionan en Vue, Astro, HTML plano); el upstream incluye wrappers React para Vanta (L476) y Tilt (L676). En SSR (Next/Astro) inicializa solo en cliente (`useEffect` / `client:only`), Vanta necesita `window`.
