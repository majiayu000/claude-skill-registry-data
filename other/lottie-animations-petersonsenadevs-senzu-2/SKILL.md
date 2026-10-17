---
name: lottie-animations
description: "Animaciones Lottie/dotLottie (JSON de After Effects) en web, React, Vue y Svelte: lottie-web, @lottiefiles/dotlottie-*, lottie-react, iconos animados, loaders, scroll/hover. No para animaciones con estados (usa rive-interactive)."
---

# lottie-animations (índice Senzu, ES)

Documentación completa upstream (inglés): `SKILL.upstream.md` (692 líneas). **No la leas entera**: usa el mapa y lee solo la sección que necesites (Read con offset/limit o Grep).

## Cuándo usar / cuándo NO
- Usar: reproducir animaciones diseñadas en After Effects (.json / .lottie) con fidelidad: iconos animados, loaders, onboarding, marketing.
- Usar: controlar play/pause/seek/segmentos, eventos, temas y multi-animación desde código (dotLottie), o sincronizar con scroll/hover.
- Usar: optimizar tamaño y rendimiento (dotLottie, canvas, DotLottieWorker, lazy load).
- NO usar: animaciones con máquinas de estados, inputs y data binding bidireccional → rive-interactive.
- NO usar: animación de DOM/layout general o scroll complejo → gsap-scrolltrigger / motion-framer; 3D → threejs-webgl.

## Lectura mínima por tarea
| Tarea | Lee solo |
|---|---|
| Empezar un proyecto/starter | `SKILL.upstream.md` L28-109 (§Core Concepts: formatos y librerías) + `assets/starter_lottie/README.md` |
| Componente React con controles y eventos | L142-219 (§2 y §3) + `references/api_reference.md` |
| Scroll / hover / segmentos | L221-289 (§4, §5) y L373-416 (§With GSAP ScrollTrigger) |
| Vue 3 / Svelte / vanilla HTML | L112-140 (§1 HTML) y L442-481 (§Vue 3, §Svelte) |
| Exportar desde After Effects | L652-667 (§6 compatibilidad) + `references/after_effects_export.md` |
| Depurar / rendimiento | L483-570 (§Performance Optimization) + L572-667 (§Common Pitfalls) + `references/performance_guide.md` |

## Mapa de `SKILL.upstream.md`
| Líneas | Sección | Para qué |
|---|---|---|
| 8-27 | Overview | Qué es Lottie, cuándo usarlo, ventajas frente a GIF/vídeo |
| 28-109 | Core Concepts | Formatos JSON vs dotLottie (30), librerías lottie-web / dotlottie-web / dotlottie-react / lottie-react (46), fuentes de datos (93) |
| 110-369 | Common Patterns | HTML dotLottie (112), React con controles (142), eventos (177), scroll (221), hover por segmentos (259), multi-animación y temas (291), Web Worker (347) |
| 371-481 | Integration Patterns | GSAP ScrollTrigger (373), Framer Motion (418), Vue 3 (442), Svelte (459) |
| 483-570 | Performance Optimization | Tamaño de archivo y lazy load (485), renderer, workers y móvil (523) |
| 572-667 | Common Pitfalls | Fugas de memoria (574), listeners (594), archivos grandes (613), stutter (624), rutas/CORS (635), features AE no soportadas (652) |
| 669-692 | Resources / Related Skills | Índice de scripts, references, assets y skills relacionadas |

## Recursos
- `references/api_reference.md` — API completa de lottie-web, lottie-react y dotlottie-web (métodos, props, eventos).
- `references/after_effects_export.md` — Guía de exportación con Bodymovin y ajustes para reducir tamaño.
- `references/performance_guide.md` — Estrategias detalladas de rendimiento (renderer, workers, DPR, lazy load).
- `scripts/generate_lottie_component.py` — Genera componente React/Vue/Svelte: `py -3 scripts/generate_lottie_component.py --framework react --type interactive --name Loader --src /animations/x.lottie --output src/Loader.tsx`.
- `scripts/optimize_lottie.py` — Reduce el JSON (precisión numérica, metadatos): `py -3 scripts/optimize_lottie.py anim.json -o anim.min.json -p 2`.
- `assets/starter_lottie/README.md` — Descripción del starter React + Vite + DotLottieReact (solo README, sin código fuente).

## Reglas duras
- Prefiere `.lottie` (dotLottie) sobre `.json` en producción: hasta 90 % menos peso; pásalo por `optimize_lottie.py` si sigue siendo JSON.
- Destruye siempre la instancia (`dotLottie.destroy()`) y elimina cada `addEventListener` en el cleanup del componente.
- Animaciones complejas: renderer canvas (no SVG), `DotLottieWorker` para descargar el hilo principal y `devicePixelRatio: 1` en móvil.
- Carga perezosa con IntersectionObserver; en Next.js coloca los archivos en `public/` y usa rutas absolutas; URLs externas requieren CORS.
- Respeta `prefers-reduced-motion`: sin autoplay/loop, muestra el primer frame o un estático (norma del proyecto, no del upstream).

## Integración con el stack del proyecto
- Detecta el stack como indica la skill `front-activation`/`skill-router` (senzu/senzu.json → package.json).
- React → `@lottiefiles/dotlottie-react` (o `lottie-react` si necesitas `interactivity` scroll/cursor); Vue → `@lottiefiles/dotlottie-vue`; Svelte → `@lottiefiles/dotlottie-svelte`; Astro/vanilla → `@lottiefiles/dotlottie-web` sobre `<canvas>` (solo cliente, necesita `window`).
