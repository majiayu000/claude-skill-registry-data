---
name: barba-js
description: "Transiciones de página con Barba.js (@barba/core, router, prefetch, head) en webs multipágina: wrapper/container/namespace, hooks, views, animación con GSAP. No para routers React/Vue ni Astro View Transitions ni animación DOM general."
---

# barba-js (índice Senzu, ES)

Documentación completa upstream (inglés): `SKILL.upstream.md` (871 líneas). **No la leas entera**: usa el mapa y lee solo la sección que necesites (Read con offset/limit o Grep).

## Cuándo usar / cuándo NO
- Usar: web multipágina (HTML estático, Astro sin View Transitions, WordPress, Eleventy) que necesita transiciones fluidas entre páginas sin recarga completa.
- Usar: transiciones condicionales por namespace/ruta, indicador de carga, re-inicializar scripts o analítica tras cada navegación.
- NO usar: apps React/Next con router propio → motion-framer (AnimatePresence); Astro con View Transitions nativas.
- NO usar: animaciones dentro de una misma página o por scroll → gsap-scrolltrigger.

## Lectura mínima por tarea
| Tarea | Lee solo |
|---|---|
| Empezar un proyecto/starter | `SKILL.upstream.md` L25-67 (§Wrapper, Container, and Namespace) + L151-183 (§Basic Setup) o `scripts/project_setup.py` |
| Crear una transición (fade/slide/crossfade) | L185-274 (§2-4 Common Patterns) + `references/transition_patterns.md` |
| Transiciones distintas según página o ruta | L276-387 (§Transition Rules + §Router Plugin) |
| Lógica por página / re-init de scripts | L121-147 (§Views) + L490-565 (§View-Specific… §Third-Party…) |
| Depurar / rendimiento | L567-669 (§Performance Optimization) + L671-844 (§Common Pitfalls) |

## Mapa de `SKILL.upstream.md`
| Líneas | Sección | Para qué |
|---|---|---|
| 10-22 | Overview | Qué es Barba (7 kb, agnóstico de framework) |
| 23-147 | Core Concepts | Estructura DOM, ciclo async/sync, los 11 hooks, views |
| 25-67 | 1. Wrapper, Container, and Namespace | Atributos `data-barba` obligatorios |
| 69-93 | 2. Transition Lifecycle | Orden de pasos en modo async vs `sync: true` |
| 94-120 | 3. Hooks | Orden de ejecución y uso típico de cada hook |
| 149-422 | Common Patterns | Setup mínimo, fade, crossfade, slide, reglas, router, loader |
| 424-565 | Integration Patterns | Timelines GSAP, init por vista, analítica, widgets de terceros |
| 567-669 | Performance Optimization | Prefetch, evitar layout shift, propiedades GPU, limpiar listeners, lazy images |
| 671-844 | Common Pitfalls | Promesas no devueltas, enlaces externos, CSS entre páginas, title/meta, flicker, sync sin position absolute |
| 846-871 | Resources / Related Skills | Índice de scripts, references y skills relacionadas |

## Recursos
- `references/api_reference.md` — API completa: init, hooks, transitions, views, router.
- `references/hooks_guide.md` — Los 11 hooks con orden de ejecución y casos de uso.
- `references/gsap_integration.md` — Patrones de animación GSAP para leave/enter.
- `references/transition_patterns.md` — Implementaciones de transiciones listas para copiar.
- `scripts/transition_generator.py` — Genera el código de una transición: `py -3 scripts/transition_generator.py --type slide --sync` (o `python3 …`).
- `scripts/project_setup.py` — Crea estructura de proyecto Barba + GSAP: `py -3 scripts/project_setup.py --name mi-proyecto --transition fade`.
- `assets/README.md` — Solo describe starters; el upstream cita `starter_barba/` y `examples/` pero NO existen en el paquete.

## Reglas duras
- Los hooks `leave`/`enter` deben devolver una promesa (return del tween o `async/await`); si no, la transición termina al instante.
- Con `sync: true`, posiciona los contenedores en `position: absolute` (wrapper `relative`) para evitar saltos de layout.
- Anima solo `opacity`/`transform` (x, scale, rotation); nunca width/height/top.
- Limpia listeners e instancias (sliders, lightbox, Locomotive) en `beforeLeave`; reinicia scroll y estado global en `beforeEnter`.
- Actualiza `<title>` y meta con `@barba/head` o manualmente en `barba.hooks.after`; usa `prevent` para dejar pasar enlaces externos.
- Respeta `prefers-reduced-motion`: si está activo, usa transiciones instantáneas o de opacidad muy corta.

## Integración con el stack del proyecto
- Detecta el stack como indica la skill `front-activation`/`skill-router` (senzu/senzu.json → package.json). Barba es vanilla JS: encaja en HTML estático, Astro (sin View Transitions), Vue/Nuxt solo en modo MPA. Para React/Next usa motion-framer; combina con locomotive-scroll (destruir/recrear la instancia en cada transición) y gsap-scrolltrigger (`ScrollTrigger.refresh()` en `afterEnter`).
