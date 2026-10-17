---
name: ui-ux-pro-max
description: "SKILL POR DEFECTO de front: ante cualquier landing, página, web, hero, componente, formulario, dashboard, tema o rediseño úsala PRIMERO (elige estilo, paleta, tipografía y patrón; design system por stack). Después, la especialista. No para backend."
---

# ui-ux-pro-max (capa Senzu, en español)

Esta skill es **UI UX Pro Max** (upstream, en inglés: `SKILL.upstream.md`, `references/pro-rules.md`,
`references/quick-reference.md`) más una capa propia en español con **perfiles por stack de front**,
plantillas y guías (`references/es/`). Eres el diseñador de producto del equipo: antes de escribir UI decides
estilo, paleta, tipografía y patrón, lo persistes en `senzu/design-system/<slug>/MASTER.md` y luego implementas
con las guías del stack. Nunca improvises colores, fuentes o espaciados en mitad de un componente.

## 1. Detectar el stack (obligatorio, nunca asumir)
1. `senzu/senzu.json` en la raíz → `frontProfile.stacks` (orden de prioridad para `--stack`).
2. Si no existe: `composer.json` con `inertiajs/inertia-laravel` → perfil Laravel+Inertia; `package.json` con
   `next` → Next.js; `astro` → Astro; `vue` sin Inertia → Vue 3; `svelte`/`nuxt`/`angular` → sus stacks upstream.
3. Si sigue sin estar claro, pregunta. Anota el perfil en el devlog.

| Perfil (Senzu) | `--stack` (en orden) | Particularidades que SIEMPRE aplican |
|---|---|---|
| Laravel + Inertia + Vue 3 | `laravel`, `vue`, `html-tailwind`, `shadcn` | Layouts persistentes, `<Head>`, `useForm` con `form.errors.campo` + `form.processing`, `preserveScroll`, partial reloads, flash messages, Ziggy, SSR opcional; componentes shadcn-vue/Reka UI; dark mode con clase en `app.blade.php`. |
| Next.js (App Router) + React | `nextjs`, `react`, `shadcn`, `html-tailwind` | Server/Client Components (`"use client"` solo donde haga falta), `next/image`, `next/font`, `metadata`, `loading.tsx`/`error.tsx`, forms con server actions + `useActionState`, shadcn/ui. |
| Astro (+ React islands) | `astro`, `react`, `shadcn`, `html-tailwind` | HTML primero; efectos de scroll/GSAP en `<script>` vanilla (SIN isla); UI interactiva con estado o animación declarativa (Motion, R3F, shadcn/ui) → island React con `client:visible`/`client:idle`; View Transitions, content collections, `<Image>`, SEO en `<head>`. |
| Vue 3 + TS (SPA) | `vue`, `html-tailwind`, `shadcn` | `<script setup lang="ts">`, composables, Pinia, VueUse, Reka UI/shadcn-vue, `<Transition>`, Teleport, router guards, lazy routes. |

Las filas marcadas `(es)` en las guías de stack provienen de Senzu (`data/stacks/*.extra.csv`).

## 1b. Lectura mínima por tarea (no cargues más; `SKILL.upstream.md` y referencias por secciones)
| Tarea | Lee solo |
|---|---|
| Proyecto/página nueva, rediseño o cliente dudoso | `references/es/brief-discovery.md` (entrevista, glosario) + `references/es/business-playbooks.md` (SU negocio) + `references/es/proposal-mode.md` (blueprint aprobable + maquetas A/B ANTES de construir) + `references/es/rondas.md` (más maquetas: fija lo que gustó, veta lo que no, algo nuevo; plantilla y ronda-check) |
| Fuentes, iconos, herramientas o referencias | `references/es/fonts-icons.md` · `references/es/resources-toolbox.md` · `references/es/inspiration.md` |
| Landing / marketing | §2 flujo + `references/es/page-patterns.md` + `references/es/industry-rules.md` + `references/es/copywriting.md` (titulares/CTAs) |
| Dashboard / admin / tabla | `references/es/components-spec.md` §Table, §Empty state, §Skeleton + `--stack` guías |
| Formulario | `components-spec.md` §Input, §Form (tu stack) + `references/es/accessibility.md` §Formularios |
| Componente suelto | `components-spec.md` (solo ese componente) + tokens de `senzu/design-system/*/MASTER.md` |
| Tema / tokens / dark mode | `references/es/tokens-tailwind.md` (sección de tu stack) |
| Auditoría de UI · repaso CON el usuario | `references/es/review-rubric.md` · juntos: `references/es/review-session.md` |
| "Que se vea moderna" (hero, bento, aurora, glass, glow) | `references/es/modern-look.md` (recetas + CSS moderno nativo §9) |
| Charts / presets GSAP · Entrega | `references/quick-reference.md` (sección concreta) · `references/pro-rules.md` (checklist) |

## 2. Flujo obligatorio
1. **Brief** (`references/es/brief-discovery.md`): checklist de lo que hay que saber (marca/guideline, objetivo,
   audiencia, contenido real, restricciones) + entrevista en lenguaje llano con glosario cliente→técnico;
   pide SIEMPRE 2-3 webs de referencia (protocolo en `references/es/inspiration.md`). Manual de marca →
   `senzu/design-system/<slug>/BRAND.md`. Proyecto nuevo/rediseño → **modo propuesta** (`references/es/proposal-mode.md`):
   blueprint aprobado + 2 maquetas A/B que se VEN, y solo después construir.
2. **Design system del proyecto**: si existe `senzu/design-system/*/MASTER.md`, es la fuente de verdad (y `pages/<página>.md`
   prevalece para esa página). Si no existe, genéralo y persístelo desde la raíz del proyecto:
   ```bash
   python3 <skills-dir>/ui-ux-pro-max/scripts/search.py "<producto industria keywords>" --design-system -p "<Proyecto>" --persist -o senzu
   # Windows:  py -3 <skills-dir>/ui-ux-pro-max/scripts/search.py "..." --design-system -p "<Proyecto>" --persist -o senzu
   # Página concreta:  ... --design-system --page checkout -p "<Proyecto>" --persist -o senzu
   # Dials opcionales: --variance 1-10  --motion 1-10  --density 1-10
   ```
   `<skills-dir>` = `.claude/skills` (Claude Code) · `.agents/skills` (Codex/Antigravity/Cursor) · `.cursor/skills` · `.windsurf/skills` · `${CLAUDE_PLUGIN_ROOT}/skills` (instalada como plugin).
   Wrappers: `scripts/search.ps1` (Windows) y `scripts/search.sh` (bash) buscan el intérprete por ti.
3. **Búsquedas puntuales** (2-5 términos): `--domain style|color|typography|ux|product|chart|gsap|accessibility|icons`.
4. **Guías del stack**: `search.py "<tema>" --stack <primero del perfil>`; repite con el resto del perfil si aporta
   (p. ej. `laravel` y luego `vue`). Si 0 resultados, reformula una vez; nunca inventes resultados.
5. **Tokens antes que markup**: convierte el design system en tokens (`references/es/tokens-tailwind.md`, Tailwind 4
   `@theme` + semánticos + dark). Nada de hex sueltos repetidos.
6. **Implementa** siguiendo el patrón de página, `references/es/components-spec.md` (anatomía/estados por stack) y las
   guías del stack. Animación/3D → skills `gsap-scrolltrigger` / `threejs-webgl` si están instaladas, respetando estos tokens.
7. **Antes de entregar (bloqueante)**: checklist de `references/pro-rules.md` + `references/es/accessibility.md`.
   Comprueba 375 (con `ui-verify`: mide y anota la captura) / 768 / 1440 px y dark mode; documenta en devlog lo verificado y lo pendiente.

## 3. Reglas duras (upstream + Senzu)
1. Iconos SVG (Phosphor/Lucide/Heroicons) con `aria-hidden` y texto accesible — **nunca emojis como iconos**.
2. Contraste 4.5:1 texto normal, 3:1 texto grande/iconos/bordes; verificado en claro y oscuro.
3. Responsive 375–1440 px sin scroll horizontal; zoom no bloqueado. **Móvil PENSADO, no encogido**: cada sección y efecto se decide para táctil (`references/es/movil.md`: efectos, burger/barra inferior, tamaños, hover).
4. Todos los estados: hover, focus-visible (anillo 2 px), active, disabled, loading, empty, error, success.
5. `prefers-reduced-motion` respetado; micro-interacciones 150–300 ms; nada bloquea la interacción.
6. Tokens semánticos (`background/surface/border/text/text-muted/primary/accent/success/warning/danger`) en claro y oscuro.
7. Texto resiliente: labels cortos, elipsis/`line-clamp` de fallback, botones que no rompen en 2 líneas.
8. Formularios: label visible, error junto al campo con `aria-invalid`/`aria-describedby`, `autocomplete`, foco al primer error, botón con estado de envío.
9. Un H1 por vista, landmarks semánticos, navegación por teclado completa, modales con foco atrapado y `Esc`.
10. Imágenes con dimensiones/`aspect-ratio`, `alt`, lazy bajo el fold, WebP/AVIF.
11. Copy real (sin lorem ipsum), CTAs con verbo, errores que dicen cómo resolverse.
12. Sin segunda librería de componentes ni fuentes nuevas sin aprobación; se reutiliza lo que ya hay en el proyecto.

## 4. Prioridad de fuentes de verdad
`senzu/design-system/<slug>/BRAND.md` (manual de marca) → `gustos.md` (vetos y preferencias acumulados: léelo SIEMPRE; un veto no se re-propone) → `pages/<página>.md` → `MASTER.md` → la skill de marca del cliente o de la agencia, si el proyecto la tiene → tokens existentes en el proyecto →
resultados de `search.py` → tu criterio (documentado en MASTER.md si te desvías).

## 5. Recursos
- `SKILL.upstream.md` — documentación completa upstream (dominios, dials, formato de salida, reglas de prioridad 1-10).
- `references/pro-rules.md` — checklist canónico de entrega. `references/quick-reference.md` — iconos, charts, GSAP.
- ES (todas en `references/es/`): `brief-discovery.md` · `business-playbooks.md` · `proposal-mode.md` (blueprint+maquetas+gustos) · `rondas.md` + `plantilla-maqueta.html` (rondas con piezas votables) · `movil.md` (versión móvil pensada: plan por sección, efectos en táctil, menú, tamaños, hover) ·
  `fonts-icons.md` · `resources-toolbox.md` · `inspiration.md` · `modern-look.md` · `copywriting.md` · `measurement.md` · `review-session.md` · `workflow.md` · `tokens-tailwind.md` · `forms-ux.md` (formularios que la gente TERMINA: campos, validación, multi-step — léela al maquetar cualquier formulario) · `anti-ia.md` (lista NEGRA de patrones que delatan web hecha con IA + rotación de referencias: léela ANTES de proponer o maquetar) · `composiciones.md` (las maneras de ordenar la página —bento, editorial, rejilla rota, pantalla dividida, storytelling— por tipo de negocio: elige composición ANTES que efectos).
- `references/es/components-spec.md` — anatomía, estados y a11y de los componentes base (formularios por stack).
- `references/es/accessibility.md` — WCAG 2.2 AA práctico. `references/es/review-rubric.md` — auditar UI existente.
- `data/` — CSV buscables (upstream) + filas `(es)` de Senzu en `data/stacks/`.

## 6. Salida esperada cuando diseñas
Primero un bloque corto: **Perfil/stack**, **Patrón**, **Estilo**, **Paleta (tokens)**, **Tipografía**, **Efectos**,
**Evitar** — y cada decisión JUSTIFICADA en el idioma del usuario contra su brief o sus gustos.md
("serif porque pediste premium"; lo que sea criterio propio, dilo). Después el código y el checklist final.
