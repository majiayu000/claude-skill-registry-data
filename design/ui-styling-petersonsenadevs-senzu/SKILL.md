---
name: ui-styling
description: "shadcn/ui y shadcn-vue + Tailwind: implementar componentes accesibles en Next, Vue/Inertia o Astro. Úsala DESPUÉS de ui-ux-pro-max (esta no elige estilo, paleta ni patrón: solo implementa componentes con los tokens ya decididos)."
---

# ui-styling (capa Senzu, en español)

Skill upstream (inglés): `SKILL.upstream.md` (stack, quick start, mapa de referencias, patrones),
`references/shadcn-components.md`, `shadcn-theming.md`, `shadcn-accessibility.md`, `tailwind-utilities.md`,
`tailwind-responsive.md`, `tailwind-customization.md`, `canvas-design-system.md`, `scripts/shadcn_add.py`,
`scripts/tailwind_config_gen.py`. Capa Senzu (español): `references/es/vue-shadcn.md`.

Aquí se **implementa** la UI: qué componente, cómo se instala, cómo se estiliza con tokens. La decisión de estilo,
paleta, tipografía y patrón de página la toma `ui-ux-pro-max` y vive en `senzu/design-system/<slug>/MASTER.md`; los tokens
se declaran según `ui-ux-pro-max/references/es/tokens-tailwind.md` (Tailwind 4 `@theme` + semánticos + `.dark`).

## 1. Cuándo sí / cuándo no
| Situación | Skill |
|---|---|
| Añadir/componer componentes shadcn, formularios, tablas, dialogs, layouts responsive, dark mode | **ui-styling** |
| Elegir estilo visual, paleta, tipografía, patrón de página; generar el design system | `ui-ux-pro-max` |
| Arquitectura de tokens en 3 capas, JSON de tokens, validación de hex sueltos | `design-system` |
| Animación de componentes | `motion-framer` (React) / `gsap-scrolltrigger` |
| Pósteres/diseño visual en canvas (`canvas-design-system.md`) | fuera del alcance Senzu; ignorar salvo petición explícita |

## 2. Lectura mínima por tarea
| Tarea | Archivo y líneas |
|---|---|
| Init y añadir componentes (React) | `SKILL.upstream.md` 56-112 |
| Catálogo de componentes con ejemplos (Button… Badge) | `references/shadcn-components.md` 5-424 (formularios RHF+zod: 43-81; Data Table: 383-405) |
| Dark mode con next-themes, CSS vars, variantes `cva`, radius | `references/shadcn-theming.md` 5-94, 95-152, 247-317, 348-364 |
| Teclado, foco, ARIA, formularios accesibles | `references/shadcn-accessibility.md` 16-104, 191-273, 384-431 |
| `@theme`, colores semánticos, fuentes, `@utility`, variantes, capas | `references/tailwind-customization.md` 5-85, 86-142, 143-250 |
| Responsive, container queries | `references/tailwind-responsive.md` |
| Utilidades de layout/espaciado/tipografía | `references/tailwind-utilities.md` |
| Formulario con validación (patrón completo) | `SKILL.upstream.md` 261-298 |

## 3. Integración por perfil Senzu
| Perfil | Instalación | Particularidades |
|---|---|---|
| Next.js App Router | `npx shadcn@latest init` → `npx shadcn@latest add button card dialog form` | Componentes en `components/ui/*` (código propio, se versiona); `next-themes` para dark mode con `attribute="class"`; formularios con `react-hook-form` + `zod` o server actions + `useActionState`; `cn()` en `lib/utils.ts`. |
| Vue 3 / Laravel + Inertia | `npx shadcn-vue@latest init` → `npx shadcn-vue@latest add button …` (Reka UI + `class-variance-authority`) | `components.json` con alias de Vite/Inertia; formularios con `vee-validate` + `zod` o `useForm` de Inertia; tablas con `@tanstack/vue-table`; dark mode con clase en `<html>` y script inline en `app.blade.php`. Detalle: `references/es/vue-shadcn.md`. |
| Astro | Islands: shadcn/ui en island React o shadcn-vue en island Vue (`client:visible`); si no hay interactividad, solo Tailwind 4 + HTML | Un solo framework de islands por proyecto; los componentes estáticos (Card, Badge) se replican en `.astro` con las mismas clases. |
| Vue 3 SPA (Vite) | igual que Inertia sin la parte Laravel | `vue-router` + Pinia; `<Transition>` para estados simples. |

Tokens: primitivos en `@theme` (`--color-brand-*`, `--font-*`, `--radius-*`), semánticos en `:root`/`.dark`
(`--background`, `--foreground`, `--primary`, `--muted`, `--border`, `--ring`…) expuestos con `@theme inline`,
como hace shadcn 2025 (`shadcn-theming.md` 95-152). Los valores vienen de `MASTER.md`; no se copian hex del upstream.

## 4. Reglas duras
- **Una sola librería de componentes** por proyecto (shadcn/ui o shadcn-vue); nada de MUI/Vuetify/Element/PrimeVue
  añadidos "para un componente". Si falta algo, se compone con Radix/Reka o se pide aprobación.
- Variantes con `cva` en el propio componente (`variant`, `size`); no clases condicionales sueltas repetidas en cada uso.
- No sobreescribir estilos base de `components/ui/*` a mano con `!important` ni CSS global; se ajustan los tokens o se
  añade una variante. Overrides puntuales vía `className`/`class` con `cn()`.
- La accesibilidad de Radix/Reka se respeta: no quitar `DialogTitle`, `Label`, roles ni `asChild` que cambie semántica;
  `Dialog` siempre con título (visible o `sr-only`) y descripción o `aria-describedby={undefined}`.
- Sin hex ni px sueltos repetidos: si un valor aparece dos veces, es un token (`design-system` lo valida).
- Dark mode con clase en `<html>`, script inline antes de pintar, `color-scheme` declarado; contraste verificado en ambos.
- Iconos `lucide-react` / `lucide-vue-next` con `aria-hidden` y texto accesible; nunca emojis como iconos.
- Formularios: `Label` visible, error con `aria-invalid` + `aria-describedby`, `autocomplete`, foco al primer error,
  botón con estado de envío (`disabled` + spinner + texto).
- Responsive 375–1440 sin scroll horizontal; `container` + `@container` cuando el componente vive en varios anchos.

## 5. Decisiones rápidas
| Necesidad | Solución |
|---|---|
| CRUD con tabla, filtros, paginación | Data Table (TanStack) + `Input` de búsqueda + `DropdownMenu` de acciones; server-side en Inertia/Next |
| Formulario largo | `Form` + `FormField` (React) / `Form` + `FormField` de shadcn-vue con vee-validate; secciones con `Separator` |
| Menú lateral de app | `Sidebar` de shadcn (o shadcn-vue) + `Sheet` en móvil |
| Selección múltiple / autocompletar | `Command` + `Popover` (combobox) |
| Notificaciones | `sonner` (`vue-sonner` en Vue); nunca `alert()` |
| Estados vacíos/carga | `Skeleton` durante carga; empty state con icono, texto y CTA |
| Componente que no existe en shadcn | Componer con primitivas Radix/Reka + `cva`, mismo estilo de archivo que los generados |

## 6. Salida esperada
Antes del código: perfil, componentes a instalar (comando exacto), tokens que se tocan. Después: código + comprobación
de estados (hover/focus/disabled/error/loading), teclado, dark mode y 375/768/1440.
