---
name: skill-router
description: "ÚSAME PRIMERO en cualquier tarea no trivial: árbol de decisión que dice qué skill y sección leer (UI: ui-ux-pro-max; animación, 3D, calidad, arquitectura DDD, devlog) y detecta el stack. Puerta de entrada de Senzu; contexto mínimo."
---

# skill-router (Senzu)

## Protocolo de carga de contexto (obligatorio)
1. **Una skill por tarea** (dos como máximo si la tarea cruza UI + lógica). Lee su `SKILL.md`; no leas otras "por si acaso".
2. Dentro de la skill, sigue su tabla **"Lectura mínima por tarea"**: lee solo esa sección/referencia.
3. `SKILL.upstream.md` y `references/` **se leen por secciones** (Read con offset/limit o Grep sobre el mapa de líneas), nunca enteros.
4. No releas lo ya leído en la sesión; anota en tu razonamiento qué skill/sección usaste.
5. Al terminar la parte especializada, vuelve al contexto del proyecto (`CLAUDE.md`/`AGENTS.md`, `senzu/design-system/*/MASTER.md`).
6. Si una skill necesaria no está instalada, dilo y propón instalarla (`sync.ps1 -Skills …`, `-Bundle …`, `/plugin install …`); no improvises esa librería.

## 1. Detecta el stack (nunca lo asumas)
`senzu/senzu.json` (`stack`, `frontProfile`) → si no existe: `composer.json` (`laravel/framework`, `inertiajs/inertia-laravel`),
`package.json` (`next`, `astro`, `vue`, `react`), `pyproject.toml` (`fastapi`, `langgraph`). Si no está claro, pregunta.

## Árbol de decisión (empieza aquí)
Árboles completos (global, B1/B2 backend, F2 animación, F3 3D, F4 presupuesto de efectos): `references/decision-trees.md`.
1. ¿Existe `senzu/plan/PLAN.md`? → sigue la tarjeta `doing` (o primera `todo`) con `project-planner §references/task-protocol.md`.
2. ¿Proyecto o feature nueva? → `project-planner`.
3. ¿Produce UI/estilos/página? → `ui-ux-pro-max` PRIMERO; después la especialista (animación F2, 3D F3).
4. ¿Animación/scroll? → árbol F2 · ¿3D/WebGL? → árbol F3 (valida el coste con F4).
5. ¿Lógica/endpoint/tests/seguridad/rendimiento? → `code-quality` (por síntoma: árbol B2).
6. ¿Módulo con dominio rico? → árbol B1 (¿capas simples o DDD?).
7. ¿Cerrar tarea o commitear? → `devlog`.

## 2. Tabla de activación (lee el SKILL.md indicado ANTES de actuar)

<!-- BEGIN GENERATED (tools/build-routers.ps1 desde core/skills-registry.json; no editar) -->
| Si la tarea implica… | Skill | Grupo |
|---|---|---|
| Empezar cualquier tarea no trivial: decide qué skill y sección leer (tabla de activación + protocolo de carga) | `skill-router` **(por defecto: empieza aquí)** | Enrutado |
| Empezar una tarea de UI, animación o 3D: detecta el perfil de front y la lectura mínima por tarea; efectos concretos del catálogo (CSS moderno, formas y SVG, tipografía cinética, microinteracciones, WebGL avanzado, física e impacto: objetos que caen, pantalla rota, intros y loaders) | `front-activation` | Enrutado |
| Instalar o actualizar Senzu completo en el proyecto (/instalar): todo, por categorías o a medida | `instalar-proyecto` | Enrutado |
| Arrancar un proyecto o feature, planificar, "¿qué hacemos ahora?", siguiente tarea; y SIEMPRE que exista plan/PLAN.md (se sigue el plan) | `project-planner` **(por defecto: empieza aquí)** | Planificación |
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
| Algo falla o no funciona (tests en rojo, excepción, error 500, resultado incorrecto): método reproducir, test que falla, hipótesis, acotar y arreglar la causa | `depurar` | Calidad de código |
| Auditar backend y arquitectura con pruebas (herramientas por stack, evidencia por hallazgo, informe), deuda técnica, código legado, dependencias circulares y refactor seguro con tests de caracterización | `backend-audit` | Calidad de código |
| Escribir o refactorizar lógica, crear tests, manejar errores/logs, seguridad, rendimiento, diseñar endpoints/APIs, revisar o abrir un PR | `code-quality` | Calidad de código |
| Módulo con reglas de negocio ricas, varios contextos, refactor de arquitectura desde MVC, "¿cómo estructuro esto?" (empieza por su checklist "¿hace falta?") | `ddd-hexagonal` (si está instalada) | Arquitectura |
| Maquetar o arreglar emails HTML (transaccionales y newsletters): react-email/MJML/plantillas del framework, compatibilidad Gmail/Outlook, dark mode, texto plano y pruebas antes de enviar | `email-html` | Marketing y SEO |
| Posicionar y medir la web: SEO on-page y local, keywords, Search Console, GA4, Google Tag Manager (contenedor, dataLayer, Consent Mode) y MCPs de analítica para operar con agentes | `marketing-seo` | Marketing y SEO |
| Desplegar y operar en producción cualquier stack: Netlify/Vercel/Forge/VPS, Docker, CI/CD con GitHub Actions, secretos por entorno, colas y cron en prod, backups con restore probado, monitorización e incidentes | `deploy-ops` | Operaciones y despliegue |
| Terminar un paso relevante o commitear (siempre); preguntas sobre el pasado del proyecto (memoria y buscador) | `devlog` | Documentación |
<!-- END GENERATED -->
## 3. Reglas que aplican sin leer nada más
Contraste 4.5:1 y estados completos en UI · `prefers-reduced-motion` · tipado estricto · validar en el borde · tests del
comportamiento · autorización en cada acción sensible · push solo a la rama de trabajo, ni operaciones destructivas sin aprobación · devlog antes de commitear.
