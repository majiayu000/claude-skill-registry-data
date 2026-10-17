---
name: motion-framer
description: "Animación en React con Motion (ex Framer Motion): variants, gestos, layout, AnimatePresence, springs, useScroll. ÚSALA en Next.js/React y en Astro dentro de una island React. No para Vue ni scroll complejo (usa gsap)."
---

# motion-framer (capa Senzu, en español)

Skill upstream (inglés): `SKILL.upstream.md` (conceptos, patrones, hooks, integración GSAP/R3F, rendimiento, pitfalls),
`references/api_reference.md` (API completa, 1077 líneas), `assets/starter_motion/`, `assets/examples/`,
`scripts/animation_generator.py`, `scripts/variant_builder.py`. Capa Senzu (español): `references/es/next.md`.

Motion es la herramienta de **animación de estado en React**: entradas/salidas de componentes, gestos, listas que se
reordenan, modales, tabs con indicador compartido. Duraciones, easing y "qué se anima" salen del
`senzu/design-system/*/MASTER.md` (skill `ui-ux-pro-max`); sin él, 150/250/400 ms y `ease: [0.2, 0.8, 0.2, 1]`.

## 1. Cuándo sí / cuándo no
| Situación | Skill |
|---|---|
| Componentes React/Next: estados, gestos, AnimatePresence, `layout`, `layoutId`, stagger de listas | **motion-framer** |
| Scroll narrativo, pin, scrub, parallax de varias capas, SplitText, timelines largas | `gsap-scrolltrigger` |
| Vue 3 (SPA o Laravel + Inertia), Astro sin islands React | `gsap-scrolltrigger` (o `motion` vanilla: `import { animate } from "motion"`) |
| 3D: mover cámara/mesh | `react-three-fiber` (Motion solo aporta `useMotionValue` como puente, ver upstream 656-686) |
| Hover/focus trivial de un botón | CSS `transition` (no cargues Motion por esto) |

## 2. Lectura mínima por tarea (`SKILL.upstream.md`)
| Tarea | Líneas |
|---|---|
| Primer componente: `motion.*`, `animate`, `initial`, `transition` | 31-107 |
| Variants y propagación a hijos (stagger) | 108-150, 860-879 |
| Hover / tap / drag | 152-281, 506-542 |
| Modales, toasts, listas con salida (AnimatePresence) | 283-357, 790-824 |
| Layout animations y `layoutId` (tabs, expandir card) | 359-424, 767-786, 840-858 |
| Aparecer al hacer scroll (`whileInView`, `useInView`) | 426-465, 606-623 |
| Springs y presets | 467-504 |
| Control imperativo (`useAnimate`, `stagger`) | 544-604 |
| Rendimiento y reduced motion | 722-786 |
| Errores frecuentes (6 casos) | 788-902 |
| API detallada: `useScroll`/`useTransform`/`useSpring` | `references/api_reference.md` 619-718 |
| `AnimatePresence` modos (`wait`, `popLayout`) y `usePresence` | `references/api_reference.md` 779-886 |

## 3. Integración con perfiles Senzu
| Perfil | Cómo | Puntos críticos |
|---|---|---|
| Next.js App Router + React | `npm i motion` → `import { motion, AnimatePresence } from "motion/react"` (upstream aún importa `framer-motion`; equivale) | Todo componente con Motion lleva `"use client"`; el Server Component padre pasa datos como props. `useReducedMotion()` en cada patrón; `LazyMotion` + `m` + `domAnimation` para reducir bundle en páginas públicas. Detalle: `references/es/next.md`. |
| Vue 3 / Laravel + Inertia | No uses Motion for React | `gsap-scrolltrigger` (`gsap-scrolltrigger/references/es/vue.md`) o `motion` vanilla (`animate()`, `inView()`, `scroll()`) para casos puntuales. |
| Astro | Solo dentro de islands React (`client:visible`) | Si la página no tiene React, `gsap-scrolltrigger/references/es/astro.md`. |
| shadcn/ui | Envolver: `<motion.div>` alrededor del componente o `asChild` + `motion.button` | No reescribas los componentes de `components/ui/*`; anima contenedores. |

## 4. Reglas duras
- `useReducedMotion()` en todo patrón con desplazamiento, escala o stagger: con `reduce`, solo opacidad o `duration: 0`;
  el estado final siempre visible (nunca contenido oculto por `initial` en SSR/sin JS: usa `initial={false}` o
  `whileInView` con `viewport={{ once: true }}`).
- Animar solo `x/y/scale/rotate/opacity/clipPath`; nada de `width/height/top/left/boxShadow` animados (upstream 724-746).
- `layout` / `layoutId` solo donde el cambio de layout sea visible y en pocos elementos (< 20); en listas largas,
  `opacity` + `exit` sin `layout`. `layout="position"` cuando el tamaño no cambia.
- Toda salida requiere `AnimatePresence` con `key` estable (id, no índice) y el `motion.*` como hijo directo.
- Transiciones de gesto van dentro del propio `whileHover`/`whileTap` (upstream 881-902).
- Limpieza: `useAnimate`/`animate()` se cancelan en el cleanup del efecto; `useScroll` con `target` referenciado
  a un elemento montado; sin listeners de scroll manuales.
- Duraciones: micro ≤ 200 ms, entradas ≤ 500 ms, page transitions ≤ 400 ms; sin intros bloqueantes.
- Un solo sistema por interacción: no mezclar GSAP y Motion sobre el mismo nodo/propiedad.

## 5. Decisiones rápidas
| Necesidad | Patrón |
|---|---|
| Lista que aparece escalonada | variants contenedor `staggerChildren: 0.06` + hijos `hidden/visible` (upstream 127-150) |
| Modal / drawer con salida | `AnimatePresence` + `motion.div` overlay y panel, `key` fijo; foco gestionado por Radix/shadcn |
| Tabs con subrayado que se desliza | `motion.span layoutId="tab-indicator"` dentro del tab activo (upstream 395-408) |
| Card que se expande a detalle | `layoutId` compartido + `AnimatePresence`; en Next, misma ruta (no entre páginas) |
| Botón con feedback | `whileHover={{ scale: 1.03 }} whileTap={{ scale: 0.97 }}`, transición 150 ms |
| Sección que aparece al scroll | `whileInView` + `viewport={{ once: true, amount: 0.3 }}` |
| Progreso de lectura / parallax suave | `useScroll` + `useTransform` + `useSpring` (`references/es/next.md` §5) |
| Transición entre rutas Next | `template.tsx` con `motion.div` de entrada; salida solo si compensa (`references/es/next.md` §2) |

## 6. Salida esperada
Antes del código: patrón elegido, dónde va `"use client"`, comportamiento con reduced-motion, qué se limpia.
Después: código + verificación en navegador (375 y 1440, consola limpia, sin parpadeo de hidratación).
