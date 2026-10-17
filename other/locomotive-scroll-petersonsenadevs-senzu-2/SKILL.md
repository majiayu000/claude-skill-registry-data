---
name: locomotive-scroll
description: "Scroll suave y parallax con Locomotive Scroll: data-scroll-*, sticky, scroll horizontal, eventos scroll/call, sync con GSAP ScrollTrigger (scrollerProxy). No para reveals simples (scroll-reveal-libraries) ni scroll sin smooth (gsap)."
---

# locomotive-scroll (índice Senzu, ES)

Documentación completa upstream (inglés): `SKILL.upstream.md` (480 líneas). **No la leas entera**: usa el mapa y lee solo la sección que necesites (Read con offset/limit o Grep).

## Cuándo usar / cuándo NO
- Usar: landings inmersivas tipo Apple con scroll suavizado (lerp), capas parallax por velocidad y elementos sticky dentro de secciones.
- Usar: scroll horizontal o storytelling largo que necesita progreso por elemento (`data-scroll-id`) o disparadores `data-scroll-call`.
- NO usar: solo fade-in al entrar en viewport → scroll-reveal-libraries (AOS) o IntersectionObserver.
- NO usar: animaciones scrubbed/pin sin smooth scroll → gsap-scrolltrigger (ScrollSmoother si se quiere suavizado); en React → motion-framer.

## Lectura mínima por tarea
| Tarea | Lee solo |
|---|---|
| Empezar un proyecto/starter | `SKILL.upstream.md` L33-116 (§Installation + §Core Concepts) + `assets/starter_locomotive/` |
| Parallax, sticky, scroll horizontal | L139-161 (§2. Parallax), L193-209 (§4. Sticky), L236-254 (§6. Horizontal) |
| Eventos, progreso y scrollTo | L163-191 (§3. Viewport Detection) + L211-234 (§5. Programmatic Scrolling) + L333-353 (§Instance Methods) |
| Combinar con GSAP ScrollTrigger | L277-331 (§Integration with GSAP ScrollTrigger) + `references/gsap_integration.md` |
| Depurar / rendimiento | L355-383 (§Performance Optimization) + L385-466 (§Common Pitfalls) |

## Mapa de `SKILL.upstream.md`
| Líneas | Sección | Para qué |
|---|---|---|
| 10-32 | Overview | Capacidades y trade-offs (accesibilidad, móviles, position fixed) |
| 33-47 | Installation | npm + CSS obligatorio, o CDN |
| 49-116 | Core Concepts | Estructura `data-scroll-container`/`-section`, opciones de `new LocomotiveScroll`, tabla de atributos |
| 118-275 | Common Patterns | Smooth básico, parallax, eventos, sticky, scrollTo, horizontal, breakpoints tablet/smartphone |
| 277-331 | Integration with GSAP ScrollTrigger | `scrollerProxy`, `scroller`, refresh/update mutuos |
| 333-353 | Instance Methods | init/update/destroy/start/stop, scrollTo, on/off |
| 355-383 | Performance Optimization | Secciones, limitar parallax, desactivar en móvil, update en resize, destroy |
| 385-466 | Common Pitfalls | Fixed roto, lazy images, posiciones desactualizadas, accesibilidad, fugas de memoria, z-index |
| 468-480 | Related Skills / Resources | Skills relacionadas e índice de scripts, references y assets |

## Recursos
- `references/api_reference.md` — API completa: opciones, atributos, métodos, eventos.
- `references/gsap_integration.md` — Patrones de ScrollTrigger + Locomotive (scrollerProxy, pin, scrub).
- `scripts/generate_config.py` — Genera la configuración inicial: `py -3 scripts/generate_config.py --smooth` / `--horizontal` (o `python3 …`).
- `scripts/integration_helper.py` — Genera código de integración GSAP por patrón/framework: `py -3 scripts/integration_helper.py --pattern fade-in --framework react`.
- `assets/starter_locomotive/` — Starter completo (index.html, main.js, style.css, package.json, README.md).

## Reglas duras
- Importa siempre `locomotive-scroll/dist/locomotive-scroll.css`; envuelve el contenido en `data-scroll-container` y segmenta con `data-scroll-section`.
- Respeta `prefers-reduced-motion`: `smooth: !matchMedia('(prefers-reduced-motion: reduce)').matches`; considera `smartphone: { smooth: false }`.
- Llama a `scroll.update()` tras insertar contenido dinámico, cargar imágenes o en resize; llama a `scroll.destroy()` al desmontar o cambiar de ruta.
- Los elementos `position: fixed` van fuera del contenedor (o usa `data-scroll-sticky`); las capas parallax necesitan z-index explícito.
- Con GSAP: registra `scrollerProxy`, pasa `scroller: '[data-scroll-container]'` a cada ScrollTrigger y encadena `ScrollTrigger.refresh()` → `locoScroll.update()`.
- SSR-safe: instancia solo en cliente (`useEffect`/`onMounted`/`client:only`), nunca en el nivel superior del módulo.

## Integración con el stack del proyecto
- Detecta el stack como indica la skill `front-activation`/`skill-router` (senzu/senzu.json → package.json). Es vanilla JS y sirve en HTML estático, Astro, Vue (instancia en `onMounted`, destruye en `onUnmounted`) y React (`useEffect` con cleanup). En proyectos React con GSAP, valora ScrollSmoother (gsap-scrolltrigger) para evitar dos sistemas de scroll; con barba-js, destruye y recrea la instancia en cada transición.
