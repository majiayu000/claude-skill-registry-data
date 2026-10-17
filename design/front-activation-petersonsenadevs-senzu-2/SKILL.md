---
name: front-activation
description: "ÚSAME PRIMERO en tareas de front: detecta el stack (Laravel+Inertia+Vue, Next, Astro, Vue) y aplica el árbol de front: 1º ui-ux-pro-max (design system y patrón), luego el efecto (catálogo de efectos), animación (gsap) o 3D (three). Contexto mínimo."
---

# front-activation (Senzu)

Esta skill es el punto de entrada cuando el proyecto NO tiene el bloque "Front y diseño" generado por
`sync.ps1` (es decir, cuando Senzu se instaló como plugin o skills globales). Haz esto en orden:

## Árbol de front (empieza aquí)
1. ¿Tarea de UI (página, componente, layout, tema)? → 1º `ui-ux-pro-max` (design system + patrón + componentes).
2. ¿Efecto concreto (marquee, parallax, hover WebGL, blob, gooey, view transitions, microinteracción…)? → `references/effects-catalog.md` (las recetas propias en `references/recipes/`: CSS moderno, formas y SVG, tipografía cinética, microinteracciones, WebGL avanzado, **física e impacto**: objeto que cae, pantalla rota, intro o loader que se rompe, con demos que funcionan en `recipes/demos/`); si no está: `references/effect-sources.md` (Codrops/CodePen + protocolo para hacerlo receta).
3. ¿Animación? → árbol F2 de `skill-router/references/decision-trees.md`.
4. ¿3D? → árbol F3 del mismo archivo. Antes de implementar cualquier efecto, valida el coste con F4.

## 1. Detecta el stack de front (nunca lo asumas)
| Evidencia | Perfil | `--stack` del buscador (en orden) |
|---|---|---|
| `senzu/senzu.json` con `frontProfile` | el que indique | `frontProfile.stacks` |
| `composer.json` con `inertiajs/inertia-laravel` (+ `vue` en `package.json`) | Laravel + Inertia + Vue 3 | `laravel`, `vue`, `html-tailwind`, `shadcn` |
| `package.json` con `next` | Next.js (App Router) + React | `nextjs`, `react`, `shadcn`, `html-tailwind` |
| `package.json` con `astro` | Astro + React islands | `astro`, `react`, `shadcn`, `html-tailwind` |
| `package.json` con `vue` (sin Inertia) | Vue 3 SPA | `vue`, `html-tailwind`, `shadcn` |
| `svelte` / `nuxt` / `angular` / `react-native` / `flutter` | otros | el stack upstream con ese nombre |
| Nada concluyente | pregunta al usuario | — |

## 2. Lee la skill que corresponda ANTES de escribir código

<!-- BEGIN GENERATED (tools/build-routers.ps1 desde core/skills-registry.json; no editar) -->
| Si la tarea implica… | Skill | Grupo |
|---|---|---|
| Crear, maquetar o rediseñar páginas, vistas, layouts, componentes, formularios, dashboards, temas, colores, tipografía, iconos, responsive, accesibilidad; archivos .vue .tsx .jsx .astro .blade.php .html .css | `ui-ux-pro-max` **(por defecto: empieza aquí)** | Front y diseño |
| Tokens de diseño (primitivos → semánticos → componente), CSS variables, validación de tokens | `design-system` (si está instalada) | Front y diseño |
| Componentes shadcn/ui (React o Vue) y utilidades/tema de Tailwind | `ui-styling` (si está instalada) | Front y diseño |
| Verificar una UI terminada en navegador real: responsive 375/768/1440, dark mode, consola y accesibilidad (axe); obligatoria antes de dar una vista por hecha | `ui-verify` | Front y diseño |
| Generar imágenes IA acordes a la web: producto flotante, heros, fondos, 3D, mockups, texturas (gpt-image en Codex, Nano Banana en Antigravity, script multi-proveedor) | `image-gen` | Front y diseño |
| Tendencias y principios de diseño web moderno | `modern-web-design` (si está instalada) | Front y diseño |
| Animación declarativa en React/Next con Motion (variants, gestos, layout animations) | `motion-framer` (si está instalada) | Animación |
| Animación basada en físicas en React (react-spring) | `react-spring-physics` (si está instalada) | Animación |
| Componentes animados prehechos (Magic UI, React Bits) | `animated-component-libraries` (si está instalada) | Animación |
| Smooth scroll con Locomotive Scroll | `locomotive-scroll` (si está instalada) | Animación |
| Transiciones entre páginas con Barba.js (sitios multipágina) | `barba-js` (si está instalada) | Animación |
| Animaciones Lottie (JSON de After Effects) | `lottie-animations` (si está instalada) | Animación |
| Reveals simples al hacer scroll (AOS) en landings | `scroll-reveal-libraries` (si está instalada) | Animación |
| Animaciones JS ligeras (anime.js) de DOM/SVG | `animejs` (si está instalada) | Animación |
| Animación, scroll-driven, parallax, pin/scrub, timelines, transiciones de página, smooth scroll (Lenis) | `gsap-scrolltrigger` (si está instalada) | Animación |
| 3D declarativo en React/Next (R3F + drei) | `react-three-fiber` (si está instalada) | 3D / WebGL |
| Gráficos 2D/partículas en canvas con PixiJS | `pixijs-2d` (si está instalada) | 3D / WebGL |
| Efectos 3D decorativos ligeros (Zdog, Vanta, tilt) | `lightweight-3d-effects` (si está instalada) | 3D / WebGL |
| Exportar/optimizar modelos de Blender a glTF para web | `blender-web-pipeline` (si está instalada) | 3D / WebGL |
| Escenas hechas en Spline e integración en web | `spline-interactive` (si está instalada) | 3D / WebGL |
| Texturizado PBR con Substance 3D para web | `substance-3d-texturing` (si está instalada) | 3D / WebGL |
| Animaciones interactivas Rive (state machines) | `rive-interactive` (si está instalada) | 3D / WebGL |
| Juegos/experiencias con PlayCanvas | `playcanvas-engine` (si está instalada) | 3D / WebGL |
| Combinar Three.js + GSAP + R3F + Motion en experiencias 3D complejas | `web3d-integration-patterns` (si está instalada) | 3D / WebGL |
| 3D con Babylon.js (juegos, escenas complejas) | `babylonjs-engine` (si está instalada) | 3D / WebGL |
| VR/AR en el navegador (A-Frame, WebXR) | `aframe-webxr` (si está instalada) | 3D / WebGL |
| 3D, WebGL/WebGPU, modelos GLB/GLTF, shaders, partículas, configuradores, heros 3D | `threejs-webgl` (si está instalada) | 3D / WebGL |
| Presentaciones HTML | `slides` (si está instalada) | Diseño gráfico y marca |
| Banners para redes, ads y heros | `banner-design` (si está instalada) | Diseño gráfico y marca |
| Logos, iconos, identidad corporativa, mockups (generación con IA) | `graphic-design` (si está instalada) | Diseño gráfico y marca |
| Voz de marca, identidad visual, guías de marca | `brand` (si está instalada) | Diseño gráfico y marca |
<!-- END GENERATED -->
Si una skill necesaria no está instalada, dilo y propón instalarla (`/plugin install bundle-core-3d-animation@senzu`
o `tools/install-skills.ps1 -Bundle …`); no improvises esas librerías sin su skill.

## 2b. Lectura mínima por tarea (no cargues más)
| Tarea | Lee solo |
|---|---|
| Landing / página de marketing | `ui-ux-pro-max/SKILL.md` §2 flujo + `ui-ux-pro-max/references/es/page-patterns.md` (patrón) + `search.py --design-system` |
| Dashboard / admin / tabla | `ui-ux-pro-max/references/es/components-spec.md` §Table, §Empty state, §Skeleton + guías `--stack` |
| Formulario | `components-spec.md` §Input, §Form (tu stack) + `ui-ux-pro-max/references/es/accessibility.md` §Formularios |
| Componente suelto | `components-spec.md` (solo ese componente) + tokens de `senzu/design-system/*/MASTER.md` |
| Tema / tokens / dark mode | `ui-ux-pro-max/references/es/tokens-tailwind.md` (sección de tu stack) |
| Auditoría de UI existente | `ui-ux-pro-max/references/es/review-rubric.md` |
| Animación | `gsap-scrolltrigger/SKILL.md` §1 (tu stack) + un patrón de `gsap-scrolltrigger/references/es/scrolltrigger-patterns.md` |
| 3D | `threejs-webgl/SKILL.md` §1 (tu stack) + la referencia ES de esa integración |

Protocolo: una skill por tarea; `SKILL.upstream.md` y referencias por secciones (Read offset/limit o Grep), nunca enteras.

## 3. Design system del proyecto
Si existe `senzu/design-system/*/MASTER.md`, es la fuente de verdad (y `pages/<página>.md` prevalece para esa página).
Si no existe, genéralo con `ui-ux-pro-max`:
```bash
python3 ${CLAUDE_SKILL_DIR}/../ui-ux-pro-max/scripts/search.py "<producto industria keywords>" --design-system -p "<Proyecto>" --persist -o senzu
# Windows: py -3 ...
```
(En plugin, la skill vive en `${CLAUDE_PLUGIN_ROOT}/skills/ui-ux-pro-max/`.)

## 4. Reglas duras que aplican siempre
Contraste 4.5:1 · estados hover/focus/active/disabled/loading/empty/error · 375–1440 px sin scroll horizontal ·
`prefers-reduced-motion` · iconos SVG (nunca emojis) · tokens semánticos, no valores sueltos · formularios con label
visible y error junto al campo · un H1 por vista · imágenes con dimensiones y `alt` · copy real.
Checklist de entrega: `ui-ux-pro-max/references/pro-rules.md`.
