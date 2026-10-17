---
name: scroll-reveal-libraries
description: "Reveals al hacer scroll con AOS (Animate On Scroll): data-aos, fade/slide/zoom/flip en landings, marketing y blogs, con React/Vue/Next. No para timelines, scrub o parallax (gsap-scrolltrigger, locomotive-scroll) ni física."
---

# scroll-reveal-libraries (índice Senzu, ES)

Documentación completa upstream (inglés): `SKILL.upstream.md` (820 líneas). **No la leas entera**: usa el mapa y lee solo la sección que necesites (Read con offset/limit o Grep).

## Cuándo usar / cuándo NO
- Usar: landings, páginas de marketing o sitios de contenido que solo necesitan aparecer/deslizar/zoom al entrar en viewport.
- Usar: cuando se pide "AOS", "data-aos", "animate on scroll", "reveal al hacer scroll" o un prototipo rápido sin JS de animación.
- Usar: grids de cards, testimonios o secciones alternas con retardo escalonado vía `data-aos-delay`.
- NO usar: timelines, pin, scrub o animación sincronizada con el scroll → `gsap-scrolltrigger`; smooth scroll y parallax → `locomotive-scroll`.
- NO usar: animación con física o gestos en React → `motion-framer` / `react-spring-physics`; componentes React ya animados → `animated-component-libraries`.

## Lectura mínima por tarea
| Tarea | Lee solo |
|---|---|
| Empezar un proyecto/starter | `SKILL.upstream.md` L31-120 (§Core Concepts) + `assets/README.md` (plantillas CDN/React/Next/Vue) |
| Maquetar hero, cards, secciones alternas, galería | L122-348 (§Common Patterns) + L697-732 (§Built-in Animations) |
| Integrar en React, Vue o Next.js | L350-529 (§Integration Patterns) |
| Crear una animación propia | L734-768 (§Custom Animations) |
| Depurar / rendimiento | L531-591 (§Performance Optimization) + L593-695 (§Common Pitfalls) |

## Mapa de `SKILL.upstream.md`
| Líneas | Sección | Para qué |
|---|---|---|
| 8-30 | Overview | Qué es AOS, cuándo sí y cuándo no |
| 31-120 | Core Concepts | Instalación CDN/npm, `data-aos`, `AOS.init` y overrides por elemento |
| 122-348 | Common Patterns | Hero, grid de features, secciones alternas, testimonios, anchor, cadena, galería |
| 350-529 | Integration Patterns | React (init, refresh en rutas, wrapper), Vue (`mounted`/`updated`), Next.js `_app` |
| 531-591 | Performance Optimization | `disable` en móvil, `once`, throttle/debounce, MutationObserver, `requestIdleCallback` |
| 593-695 | Common Pitfalls | `refresh()` tras cambios de DOM, React, jank, conflictos CSS, anchor placement, límite 3000 ms |
| 697-732 | Built-in Animations | Lista de fade, slide, zoom y flip |
| 734-768 | Custom Animations | Definir `[data-aos="x"]` y `.aos-animate` en CSS |
| 770-794 | Comparison with Alternatives | Tabla AOS vs GSAP ScrollTrigger |
| 796-820 | Resources / Related Skills | Enlaces oficiales y skills relacionadas |

## Recursos
- `references/aos_api.md` — Referencia completa: opciones de `AOS.init`, métodos (`refresh`, `refreshHard`), atributos `data-aos-*` y eventos.
- `references/animation_catalog.md` — Catálogo de las 50+ animaciones integradas con descripción de cada una.
- `scripts/aos_generator.py` — Genera HTML boilerplate con AOS: `py -3 scripts/aos_generator.py --list` / `--template <nombre> --output out.html` (o `python3`).
- `scripts/config_builder.py` — Genera la configuración `AOS.init`: `py -3 scripts/config_builder.py --list-presets` / `--preset <p> --format modern|cdn|react [--once true ...]`.
- `assets/README.md` — Plantillas listas (CDN mínimo, React, Next.js, Vue), patrones, rendimiento y accesibilidad. No existen `assets/starter_aos/` ni `references/integration_patterns.md` aunque el upstream los cite.

## Reglas duras
- Llama a `AOS.refresh()` (o `refreshHard()`) tras añadir elementos al DOM o cambiar de ruta; en React inicializa en `useEffect`, nunca en render.
- Usa `once: true` y `disable` en móvil (`< 768px`) en páginas con muchos elementos; evita `mirror` salvo necesidad real.
- Respeta `prefers-reduced-motion`: usa `disable: () => matchMedia('(prefers-reduced-motion: reduce)').matches` (ver `assets/README.md`, sección accesibilidad).
- No pongas `opacity`/`transform` con `!important` sobre elementos `[data-aos]`; rompe la animación.
- `duration`/`delay` máximos de 3000 ms; para más, CSS propio (L678-695). Prefiere fades a flips por rendimiento.

## Integración con el stack del proyecto
- Detecta el stack como indica la skill `front-activation`/`skill-router` (senzu/senzu.json → package.json). Librería agnóstica: vanilla (CDN o npm), React/Next (init en `useEffect`, L352-455 y L497-529), Vue (`mounted` + `updated`, L457-495), Astro (script cliente o `client:load`). Toca `window`, así que inicializa solo en cliente (SSR-safe).
