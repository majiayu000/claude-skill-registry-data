---
name: gsap-scrolltrigger
description: "Animación web con GSAP 3 + ScrollTrigger + Lenis: entradas al hacer scroll, pin/scrub, parallax, scroll horizontal, reveals, transiciones de página, sincronía con 3D. Vue/Inertia, Next, Astro, vanilla. No para hovers CSS ni estados simples."
---

# gsap-scrolltrigger (capa Senzu, en español)

Skill upstream (inglés): `SKILL.upstream.md` (API completa, patrones, integración con Three.js y React),
`references/api_reference.md`, `references/common_patterns.md`, `references/easing_guide.md`,
`assets/starter_scroll/`, `assets/easings/easing_visualizer.html`, `scripts/generate_animation.py`, `scripts/timeline_builder.py`.
Capa Senzu (español): `references/es/` y `templates/`.

El movimiento **refuerza jerarquía y feedback**; nunca es decoración gratuita. Duraciones, easing y "qué se anima"
salen del `senzu/design-system/*/MASTER.md` del proyecto (skill `ui-ux-pro-max`); si no existe, usa 150/250/400 ms,
`power2.out` para entradas y `power1.inOut` para scrubs.

## 1. Detectar el stack e integrar
| Stack (perfil Senzu) | Referencia | Plantillas | Puntos críticos |
|---|---|---|---|
| Vue 3 (SPA o con Laravel + Inertia) | `references/es/vue.md` | `templates/useGsap.ts`, `ScrollReveal.vue`, `HorizontalScroll.vue`, `useLenis.ts` | `gsap.context` en `onMounted` + `revert()` en `onBeforeUnmount`; con Inertia: `router.on('finish')` → `ScrollTrigger.refresh()`, matar triggers al navegar, layouts persistentes, SSR-safe. |
| Next.js / React | `references/es/next.md` | `templates/useGsapReact.tsx` | `@gsap/react` `useGSAP({ scope })`, `"use client"`, `contextSafe`, refresh por `pathname`, StrictMode. |
| Astro | `references/es/astro.md` | `templates/gsap-astro.ts` | GSAP en `<script>` vanilla, SIN isla (islands React solo para Motion/R3F/estado); `astro:page-load` / `astro:before-swap` (View Transitions), scripts deduplicados. |
| Vanilla / otros | `SKILL.upstream.md` | `assets/starter_scroll/` | `gsap.matchMedia`, `ScrollTrigger.refresh()` tras cargar imágenes/fuentes. |

Detecta el stack como indica `ui-ux-pro-max/SKILL.md` §1 (`senzu/senzu.json` → `composer.json`/`package.json`).

## 1b. Lectura mínima por tarea
| Tarea | Lee solo |
|---|---|
| Reveal al hacer scroll / stagger | `references/es/scrolltrigger-patterns.md` §batch/fade-up + `templates/ScrollReveal.vue` (o React/Astro equivalente) |
| Sección pinned con scrub / scroll-story | `scrolltrigger-patterns.md` §pin + `references/es/api-cheatsheet.md` §timelines |
| Scroll horizontal | `scrolltrigger-patterns.md` §horizontal + `templates/HorizontalScroll.vue` |
| Smooth scroll (Lenis) | `references/es/vue.md`/`next.md`/`astro.md` §Lenis + `templates/useLenis.ts` |
| Transición de página | referencia de tu stack §transiciones |
| Texto que se revela (SplitText) | `api-cheatsheet.md` §plugins + patrón SplitText |
| Efecto concreto (marquee, cursor, skew, lupa, before/after, stacking, galería…) | `references/es/effects-pro.md` (sección del efecto) |
| Patrón solo documentado en inglés (stacked cards §2.4, scramble §7.2, typewriter §7.3, curtain §8.1) | `references/common_patterns.md` (Grep por el título) |
| Algo no funciona | `references/es/pitfalls.md` (busca el síntoma con Grep) |
| API concreta de GSAP | `references/api_reference.md` upstream (Grep por el método) |

Catálogo completo de efectos con punteros: `front-activation/references/effects-catalog.md`.

## 2. Flujo
1. Lee el design system (§7 movimiento) y elige el patrón en `references/es/scrolltrigger-patterns.md` (15 patrones
   completos) o `references/common_patterns.md`; no inventes desde cero.
2. Registra plugins **una vez** en un módulo compartido (`lib/gsap.ts`): `gsap.registerPlugin(ScrollTrigger, …)`.
3. Integra según la tabla del §1 (limpieza garantizada al desmontar/navegar).
4. Envuelve en `gsap.matchMedia()` con `(prefers-reduced-motion: no-preference)`; en `reduce` deja el estado final visible.
5. Rendimiento (`references/es/performance-a11y.md`): solo `transform`/`opacity`/`clip-path`; `will-change` con criterio;
   nada de `height:auto`, `top/left`, `box-shadow` animados; `markers` solo en dev.
6. Verifica en navegador (375 y 1440): sin saltos al refrescar, sin scroll bloqueado en móvil, sin elementos invisibles
   tras navegar, consola limpia. Documenta en devlog.

## 3. Reglas duras
- Todo lo creado en un componente se **revierte** al desmontar (`ctx.revert()`); en SPA/Inertia/Next/Astro se limpian
  los ScrollTriggers al cambiar de página.
- `from({ opacity: 0 })` → usa `autoAlpha` y CSS `visibility:hidden` inicial (sin parpadeo de primer render).
- `ScrollTrigger.refresh()` tras imágenes (`decode()`), fuentes (`document.fonts.ready`) y cambios de layout.
- Sin `overflow:hidden` en `html/body` con ScrollTrigger sin `scroller` explícito.
- Sin scroll-jacking (Lenis, snap) en formularios, checkout o dashboards; solo en landings narrativas y desactivado con reduced-motion.
- Entradas ≤ 800 ms; intros > 1,2 s deben ser saltables. GSAP solo en cliente (SSR-safe).
- Errores frecuentes y su solución: `references/es/pitfalls.md` (27 casos).

## 4. Patrones más usados
| Necesidad | Patrón | Notas |
|---|---|---|
| Elementos aparecen al scroll | `ScrollTrigger.batch` + fade-up 16-24 px, stagger 0.06-0.1 | `once: true`, `start: 'top 85%'` |
| Sección fija que cuenta una historia | pin + timeline `scrub: 1` | `end: '+=200%'`, `anticipatePin: 1` |
| Carrusel horizontal con scroll vertical | pin + `xPercent: -100 * (n-1)` | `invalidateOnRefresh`, snap opcional |
| Profundidad | parallax por capas `yPercent` + `scrub` | máx. 3 capas; desactivar en móvil |
| Titular que se revela | SplitText por líneas + `yPercent: 100` + `mask: 'lines'` | esperar `document.fonts.ready` |
| Números que suben | `gsap.to(obj, { val, snap: { val: 1 }, onUpdate })` | `once`; `Intl.NumberFormat` |
| Transición entre páginas | timeline en mount + overlay en inicio de navegación | ≤ 600 ms; no en formularios |
| Header que se oculta al bajar | `ScrollTrigger.create({ onUpdate: self => self.direction })` | `yPercent: -100`, 300 ms |
| Marquee infinito | tween `xPercent: -50` + `repeat: -1`, pausa/dirección con `timeScale` | `effects-pro.md` §Marquee infinito |
| Skew según velocidad de scroll | `getVelocity()` + `quickTo` con clamp ±8 | `effects-pro.md` §Scroll velocity skew |
| Cards que se apilan al hacer scroll | sticky + escala/rotación/blur de las anteriores | `effects-pro.md` §Stacking cards completo |
| Cursor que sigue al puntero | `quickTo` x/y + estados por `data-cursor` | `effects-pro.md` §Cursor personalizado |

## 5. Salida esperada
Antes del código: patrón, dónde se registran los plugins, cómo se limpia, comportamiento con reduced-motion.
Después: código + verificación real en navegador.
