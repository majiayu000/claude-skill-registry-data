---
name: design-system
description: "Tokens de diseño en 3 capas (primitivo, semántico, componente) con scripts de generación y validación. Úsala DESPUÉS de ui-ux-pro-max para formalizar los tokens del design system ya decidido; en proyectos pequeños basta @theme. No elige paleta."
---

# design-system (capa Senzu, en español)

Skill upstream (inglés): `SKILL.upstream.md` (arquitectura, scripts, specs, sistema de slides),
`references/token-architecture.md`, `primitive-tokens.md`, `semantic-tokens.md`, `component-tokens.md`,
`component-specs.md`, `states-and-variants.md`, `tailwind-integration.md`, `templates/design-tokens-starter.json`,
`scripts/generate-tokens.cjs`, `scripts/validate-tokens.cjs`. Capa Senzu (español): `references/es/tokens-por-stack.md`.
El sistema de slides upstream (`search-slides.py`, `data/slide-*.csv`, Chart.js) queda **fuera** del alcance Senzu.

Aquí se **formaliza** lo que `ui-ux-pro-max` decidió: el `senzu/design-system/<slug>/MASTER.md` (estilo, paleta, tipografía)
se convierte en un JSON de tokens versionado, CSS generado y reglas verificables. `ui-styling` consume los tokens.

## 1. Cuándo sí / cuándo no
| Situación | Qué hacer |
|---|---|
| Producto con varias apps/temas, marca blanca, dark mode + alto contraste, equipo > 3 front | **design-system**: JSON en 3 capas + generación + validación en CI |
| Landing o app pequeña con un tema | Basta `@theme` + semánticos en `app.css` según `ui-ux-pro-max/references/es/tokens-tailwind.md`; no montes pipeline |
| Elegir colores/fuentes/estilo | `ui-ux-pro-max` (`search.py --design-system`) |
| Implementar componentes | `ui-styling` |
| Presentaciones/slides | fuera de alcance; ignorar la sección upstream 108-235 |

## 2. Lectura mínima por tarea
| Tarea | Archivo y líneas |
|---|---|
| Entender las 3 capas y el naming | `SKILL.upstream.md` 25-49; `references/token-architecture.md` 5-27, 137-159 |
| Definir primitivos (escalas de color, spacing, tipografía, radius, sombra, motion, z-index) | `references/primitive-tokens.md` 5-203 |
| Definir semánticos (background/foreground, primary, muted, status, border/ring) y dark | `references/semantic-tokens.md` 5-101, 162-188 |
| Tokens por componente (button, input, card, badge, alert, dialog, table) | `references/component-tokens.md` |
| Specs de estados (hover/focus/disabled/loading/error) y variantes | `references/states-and-variants.md` 5-47, 48-161, 209-241 |
| Anatomía y medidas de componentes base | `references/component-specs.md` |
| Integración con Tailwind (CSS vars, HSL/oklch, shadcn) | `references/tailwind-integration.md` 5-58, 115-127, 232-251 |
| Migrar tokens planos y alineación W3C DTCG | `references/token-architecture.md` 186-224 |

## 3. Las 3 capas (regla de dependencia)
```
primitive  --color-blue-600: #2563eb          valores crudos; nunca se usan en componentes
semantic   --color-primary: var(--color-blue-600)   propósito; cambia con el tema (light/dark/brand)
component  --button-bg: var(--color-primary)        solo si el componente necesita desviarse o ser configurable
```
Un componente consume semánticos (o sus propios tokens); un semántico referencia primitivos; un primitivo no
referencia nada. Dark mode y temas solo redefinen la capa semántica.

## 4. Scripts upstream (ejecutar con node, sin dependencias)
```bash
SK=<skills-dir>/design-system            # .claude/skills · .agents/skills · .cursor/skills
cp $SK/templates/design-tokens-starter.json senzu/design-system/tokens.json    # punto de partida DTCG ($value/$type)
node $SK/scripts/generate-tokens.cjs --config senzu/design-system/tokens.json -o resources/css/tokens.css   # CSS vars
node $SK/scripts/generate-tokens.cjs --config senzu/design-system/tokens.json --format tailwind             # bloque para @theme
node $SK/scripts/validate-tokens.cjs --dir resources/js --ignore vendor   # hex/px/rem sueltos; --fix solo sugiere
```
- Referencias en JSON con llaves: `"$value": "{primitive.color.blue.600}"`; el generador las resuelve.
- El validador ignora `node_modules`, `.git`, `dist`, `build`, `.next`; añade `vendor`, `public/build`, `storage`.
- Añade ambos comandos a `package.json` (`tokens:build`, `tokens:check`) y el check al CI.

## 5. Integración con Tailwind 4 y ui-ux-pro-max
1. `MASTER.md` (secciones color, tipografía, espaciado, radios, sombras, movimiento) → `tokens.json` capa primitiva.
2. Semánticos con los nombres que `ui-ux-pro-max` exige (`background/surface/border/text/text-muted/primary/accent/
   success/warning/danger`) y los de shadcn si el proyecto los usa (`--background`, `--foreground`, `--muted`…).
3. `tokens.css` generado se importa en `app.css`; los primitivos entran en `@theme`, los semánticos en `:root`/`.dark`
   y se exponen con `@theme inline` (utilidades `bg-surface`, `text-text-muted`). Detalle: `references/es/tokens-por-stack.md`.
4. Cambios de marca: se edita `tokens.json`, se regenera, nunca se tocan componentes.

## 6. Reglas duras
- Sin hex, `rgb()`, px o rem sueltos en componentes: todo valor visual pasa por un token (validado por script/CI).
- Naming `--<categoría>-<concepto>-<variante>-<estado>` en kebab-case; sin nombres de color en semánticos (`--color-primary`, no `--color-blue`).
- Colores en oklch (o HSL) para permitir `color-mix()` y alpha; contraste 4.5:1 / 3:1 comprobado en cada tema.
- Toda escala tiene pasos finitos (spacing 4 px base, tipografía modular, radius 3-4 pasos); no se añaden valores intermedios ad hoc.
- Un token = un propósito documentado (`$description`); tokens huérfanos se eliminan.
- Motion tokens (`--duration-fast/normal/slow`, `--ease-*`) compartidos con `gsap-scrolltrigger`/`motion-framer`.
- `tokens.json` es la fuente; `tokens.css` es artefacto generado (no se edita a mano, se versiona igualmente).

## 7. Salida esperada
Antes: qué capas hacen falta, nombres de semánticos, temas previstos, dónde vive el JSON. Después: `tokens.json`,
CSS generado, `app.css` integrado, resultado de `validate-tokens.cjs` y lista de valores migrados.
