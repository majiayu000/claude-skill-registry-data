---
name: modern-web-design
description: "Tendencias y principios de diseño web 2024-25 (bento, glassmorphism, neobrutalism) como inspiración puntual. Úsala DESPUÉS de ui-ux-pro-max y solo para explorar estilos; el design system y el patrón los decide ui-ux-pro-max. No para codificar."
---

# modern-web-design (índice Senzu, ES)

Documentación completa upstream (inglés): `SKILL.upstream.md` (990 líneas). **No la leas entera**: usa el mapa y lee solo la sección que necesites (Read con offset/limit o Grep).

## Cuándo usar / cuándo NO
- Usar: decidir la dirección visual/interactiva de una landing o portfolio (hero inmersivo, galería horizontal, reveals, cursor personalizado, glass).
- Usar: definir tokens de diseño (OKLCH, tipografía fluida con clamp, elevaciones, timing) o auditar accesibilidad y rendimiento de una página.
- Usar: elegir qué skill de animación/3D aplicar a cada patrón (esta skill es el enrutador).
- NO usar: para escribir el código de una librería concreta → `gsap-scrolltrigger`, `motion-framer`, `react-three-fiber`, `barba-js`, etc.
- NO usar: para componentes UI/estilado de sistema → `ui-styling`, `design-system`, `animated-component-libraries`.

## Lectura mínima por tarea
| Tarea | Lee solo |
|---|---|
| Empezar un proyecto/starter | `SKILL.upstream.md` L14-33 (§Performance-First) + L903-946 (§Design System Architecture); no hay starter en `assets/` (solo README) |
| Elegir patrón de sección (hero, galería, visor 3D, transiciones) | L252-510 (§Common Design Patterns) y la skill que cite cada patrón |
| Micro-interacciones, cursor, glass | L67-222 (§3, §5, §6) + `references/interaction_patterns.md` |
| Accesibilidad | L586-687 (§Accessibility Best Practices) + `references/accessibility_guide.md` |
| Depurar / rendimiento | L689-790 (§Performance Optimization) + L791-901 (§Common Pitfalls) + `references/performance_checklist.md` |

## Mapa de `SKILL.upstream.md`
| Líneas | Sección | Para qué |
|---|---|---|
| 8-13 | Overview | Qué cubre la meta-skill |
| 14-251 | Core Design Principles (2024-2025) | 7 principios: Performance-First (16), Bold Minimalism (34), Micro-Interactions (67), Scrollytelling (105), Cursor UX (145), Glassmorphism & Depth (194), AI Personalization (224) |
| 252-511 | Common Design Patterns | 7 patrones con código: Hero (254), Horizontal Gallery (290), 3D Product Viewer (316), Data Viz (349), Page Transitions (402), Cursor Effects (434), Staggered Reveals (470) |
| 512-585 | Integration with Other Skills | Qué skill usar para animación (514), 3D (546) y componentes (572) |
| 586-688 | Accessibility Best Practices | reduced-motion (588), contraste (615), teclado (634), lector de pantalla (657), touch targets (673) |
| 689-790 | Performance Optimization | Animación 60 FPS (691), carga (713), imágenes (733), 3D (759), bundle (775) |
| 791-902 | Common Pitfalls | Sobreanimación, móvil, fallbacks, a11y, loading states, scroll hijacking |
| 903-947 | Design System Architecture | Tokens CSS (905) y arquitectura atómica (937) |
| 948-990 | Resources | Lista de skills relacionadas, references, scripts, assets |

## Recursos
- `references/design_trends_2024.md` — tendencias y previsiones de diseño 2024-25.
- `references/interaction_patterns.md` — catálogo de micro-interacciones.
- `references/accessibility_guide.md` — patrones WCAG AAA y cómo testearlos.
- `references/performance_checklist.md` — checklist de optimización y métricas.
- `scripts/pattern_generator.py` — genera boilerplate HTML de un patrón: `py -3 scripts/pattern_generator.py --pattern hero --output hero.html`.
- `scripts/design_audit.py` — audita un HTML (a11y, rendimiento, patrones): `py -3 scripts/design_audit.py --file index.html --report audit.txt`.
- `assets/README.md` — solo describe tokens/plantillas previstas; no hay archivos de starter reales.

## Reglas duras
- Respeta `prefers-reduced-motion` siempre (CSS L592-601 y JS L606-612); la animación debe poder desactivarse.
- Anima solo `transform` y `opacity`; nunca top/left/width/height; `will-change` solo durante la animación.
- Objetivos Core Web Vitals: LCP < 2,5 s, CLS < 0,1, INP < 200 ms; difiere animaciones no críticas y lazy-load de imágenes/3D.
- Contraste AAA 7:1 (4,5:1 texto grande); `:focus-visible` visible; touch targets ≥ 44x44 px.
- Nunca secuestres el scroll nativo ni desactives el scroll; mejora, no reemplaza (L890-901).
- Mejora progresiva: el contenido esencial debe verse sin JS; detecta features antes de usarlas.

## Integración con el stack del proyecto
- Detecta el stack como indica la skill `front-activation`/`skill-router` (senzu/senzu.json → package.json). Esta skill es agnóstica de framework: los principios y tokens CSS valen para vanilla, Vue, Astro y React.
- Los ejemplos con `motion`/Framer y R3F son React-only; en Vue/vanilla/Astro usa `gsap-scrolltrigger`, `animejs`, `scroll-reveal-libraries` o `barba-js` según el patrón.
