---
name: animated-component-libraries
description: "Componentes React animados prefabricados: Magic UI (Tailwind + Motion + shadcn/ui) y React Bits (BlurText, CountUp, Dock, Particles, Aurora). Para landings, hero, marquee, stats, fondos. No para animación a medida, Vue/vanilla ni 3D."
---

# animated-component-libraries (índice Senzu, ES)

Documentación completa upstream (inglés): `SKILL.upstream.md` (824 líneas). **No la leas entera**: usa el mapa y lee solo la sección que necesites (Read con offset/limit o Grep).

## Cuándo usar / cuándo NO
- Usar: landing/marketing en React o Next.js que necesita hero con fondo animado, texto revelado, contadores, marquee de testimonios, botones con shimmer/border beam, dock estilo macOS.
- Usar: el proyecto ya tiene shadcn/ui + Tailwind y quiere añadir componentes animados vía `npx shadcn@latest add https://magicui.design/r/<comp>`.
- Usar: elegir entre Magic UI y React Bits o combinarlos en una misma página.
- NO usar: animación DOM a medida, scroll-driven o timelines → `gsap-scrolltrigger` / `motion-framer`; física de muelles → `react-spring-physics`.
- NO usar: proyectos Vue, Astro sin islas React o vanilla (ambas librerías son solo React); fondos 3D reales → `threejs-webgl`.

## Lectura mínima por tarea
| Tarea | Lee solo |
|---|---|
| Empezar un proyecto/starter | `SKILL.upstream.md` L18-91 (§Core Concepts: instalación y estructura) + `assets/README.md` |
| Hero con fondo animado (grid, particles, plasma, aurora) | L94-136 (§1 Magic UI backgrounds) y L358-427 (§7 React Bits WebGL) |
| Texto animado, contadores, dock, marquee | L137-171, L212-311, L312-357 |
| Integrar con shadcn/ui, Framer Motion, React Router | L429-567 (§Integration Patterns) |
| Depurar / rendimiento | L568-642 (§Performance) y L643-797 (§Common Pitfalls) |

## Mapa de `SKILL.upstream.md`
| Líneas | Sección | Para qué |
|---|---|---|
| 8-17 | Overview | Qué es cada librería (150+ Magic UI, 90+ React Bits) |
| 18-91 | Core Concepts | Arquitectura, instalación y categorías de componentes |
| 92-428 | Common Patterns | 7 patrones: GridPattern, BlurText, ShimmerButton/BorderBeam, Dock, CountUp, Marquee, Particles/Plasma/Aurora |
| 429-567 | Integration Patterns | shadcn/ui (`cn()`), Framer Motion, React Router, combinar ambas librerías |
| 568-642 | Performance Optimization | Masks CSS, menos partículas en móvil, lazy load, reduced motion |
| 643-797 | Common Pitfalls | Dependencias, keyframes CSS en globals.css, z-index, tipos TS, content paths de Tailwind |
| 798-818 | Resources | Enlaces oficiales, scripts, references y assets |
| 819-824 | Related Skills | Skills alternativas |

## Recursos
- `references/magic_ui_components.md` — catálogo Magic UI con props y ejemplos de uso.
- `references/react_bits_components.md` — catálogo React Bits (texto, interactivos, fondos, layouts).
- `references/customization_guide.md` — personalización por props, estilos y composición en ambas librerías.
- `scripts/component_importer.py` — importa y adapta un componente: `py -3 scripts/component_importer.py --library magicui --component grid-pattern` (o `--library reactbits`).
- `scripts/props_generator.py` — genera configuración de props: `py -3 scripts/props_generator.py --component shimmer-button --format typescript`.
- `assets/README.md` — plantillas de arranque (Next.js + shadcn + Magic UI; Vite + React Bits) y ejemplos de secciones.

## Reglas duras
- Instala las dependencias reales: Magic UI requiere `motion clsx tailwind-merge` y el helper `cn()` en `lib/utils.ts`; los componentes WebGL de React Bits requieren `ogl`.
- Tras instalación manual de Magic UI, añade los `@keyframes` (ripple, shimmer-slide, marquee) a `globals.css` o las animaciones no se aplican.
- Respeta `prefers-reduced-motion`: desactiva reveals y reduce partículas; en móviles/low-end baja `numSquares`/`particleCount` o sustituye por un fondo estático.
- Fondos siempre `absolute inset-0 -z-10` y contenido `relative z-10`; no apiles varios efectos WebGL en la misma vista.
- Carga componentes pesados con `React.lazy` y cliente-only (`"use client"` / `dynamic(..., { ssr: false })` en Next.js): usan `window` y WebGL.

## Integración con el stack del proyecto
- Detecta el stack como indica la skill `front-activation`/`skill-router` (senzu/senzu.json → package.json). Solo aplica a React/Next.js con Tailwind (Magic UI exige además shadcn/ui).
- Si el stack es Vue, Astro sin React o vanilla, no uses esta skill: recurre a `gsap-scrolltrigger`, `scroll-reveal-libraries` o `lightweight-3d-effects` para lograr efectos equivalentes.
