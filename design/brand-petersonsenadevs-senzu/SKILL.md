---
name: brand
description: "Identidad de marca: voz y tono, identidad visual, mensajes, paleta, tipografía, logo, validación de assets; sincroniza brand-guidelines.md a design tokens. Disparadores: marca, tono, guía de estilo, compliance. No para UI/CSS."
---

# brand (índice Senzu, ES)

Documentación completa upstream (inglés): `SKILL.upstream.md` (97 líneas). **No la leas entera**: usa el mapa y lee solo la sección que necesites (Read con offset/limit o Grep).

## Cuándo usar / cuándo NO
- Usar: definir o actualizar voz, mensajes y guía de estilo de marca (`senzu/design-system/<slug>/brand-guidelines.md`).
- Usar: auditar consistencia, validar naming/tamaño/formato de assets, comparar colores de una imagen con la paleta.
- Usar: inyectar contexto de marca en prompts de otras skills (banners, slides, social) o sincronizar la guía a tokens.
- NO usar: tokens semánticos y CSS vars de un design system → `design-system`; componentes Tailwind/shadcn → `ui-styling`.
- NO usar: generar logos o mockups con IA → `design` (Logo/CIP).

## Lectura mínima por tarea
| Tarea | Lee solo |
|---|---|
| Empezar una marca nueva | `SKILL.upstream.md` L23-40 (§Quick Start) + `templates/brand-guidelines-starter.md` |
| Actualizar marca y sincronizar tokens | `SKILL.upstream.md` L42-61 (§Brand Sync Workflow, §Subcommands) + `references/update.md` |
| Definir voz o mensajes | `references/voice-framework.md` + `references/messaging-framework.md` |
| Revisar consistencia / aprobar assets | `references/consistency-checklist.md` + `references/approval-checklist.md` |
| Depurar un script | `SKILL.upstream.md` L78-85 (§Scripts) y el `.cjs` correspondiente |

## Mapa de `SKILL.upstream.md`
| Líneas | Sección | Para qué |
|---|---|---|
| 14-21 | When to Use | Casos de uso del skill |
| 23-40 | Quick Start | Comandos `node` para inyectar contexto, validar assets y extraer colores |
| 42-55 | Brand Sync Workflow | Flujo guía → `design-tokens.json`/`.css` y archivos implicados |
| 57-61 | Subcommands | Subcomando `update` → `references/update.md` |
| 63-76 | References | Tabla tema → archivo de referencia |
| 78-85 | Scripts | Propósito de cada script |
| 87-91 | Templates | Plantilla de arranque |
| 93-97 | Routing | Cómo se resuelve el subcomando desde `$ARGUMENTS` |

## Recursos
- `references/voice-framework.md` — voz y tono. `references/messaging-framework.md` — pilares de mensaje.
- `references/visual-identity.md` — identidad visual. `references/logo-usage-rules.md` — uso correcto del logo.
- `references/color-palette-management.md` — paleta. `references/typography-specifications.md` — tipografía.
- `references/asset-organization.md` — naming y carpetas. `references/approval-checklist.md` y `references/consistency-checklist.md` — auditoría.
- `references/brand-guideline-template.md` — estructura de la guía. `references/update.md` — flujo del subcomando `update`.
- `scripts/inject-brand-context.cjs` — extrae contexto de marca para prompts (`node scripts/inject-brand-context.cjs senzu/design-system/<slug>/brand-guidelines.md [--json]`).
- **`scripts/sync-senzu.mjs` (Senzu)** — guía → `design-tokens.json` y `.css` **junto a la guía**, en Claude y en Codex (`node <skills-dir>/brand/scripts/sync-senzu.mjs [--slug x] [--dry-run]`). Úsalo SIEMPRE en lugar de `sync-brand-to-tokens.cjs`: el original tiene rutas fijas (`docs/`, `assets/`, `.claude/skills`) y en Codex no genera el CSS.
- `scripts/validate-asset.cjs` — valida naming, tamaño y formato (`node scripts/validate-asset.cjs <ruta>`).
- `scripts/extract-colors.cjs` — extrae/compara colores (`node scripts/extract-colors.cjs --brand-file senzu/design-system/<slug>/brand-guidelines.md --palette | <imagen>`); `scripts/tests/` — test de regresión (`py -3 -m pytest`).
- `templates/brand-guidelines-starter.md` — plantilla completa para marcas nuevas. No hay `assets/`.

## Reglas duras
- `senzu/design-system/<slug>/brand-guidelines.md` (junto a MASTER.md y gustos.md) es la única fuente de verdad; los tokens se regeneran con `sync-senzu.mjs`, nunca a mano. Proyecto con la guía en `docs/` (ubicación antigua de la skill): funciona, pero muévela.
- Logo ya elegido (`senzu/design-system/<slug>/logos/final/`): la guía lo cita por su ruta; no se proponen logos nuevos sin que el usuario lo pida.
- Tras editar la guía, ejecutar `sync-brand-to-tokens.cjs` y verificar con `inject-brand-context.cjs --json`.
- Todo asset nuevo pasa por `validate-asset.cjs` antes de aprobarse; colores fuera de paleta se detectan con `extract-colors.cjs`.
- Cualquier pieza creativa de otra skill (banner, slides, social) debe inyectar contexto de marca antes de diseñar.

## Integración con el stack del proyecto
- Detecta el stack como indica la skill `front-activation`/`skill-router` (senzu/senzu.json → package.json). Skill agnóstica de framework (scripts Node); los tokens CSS generados se consumen igual en React, Vue, Astro o vanilla. Requiere Node en el entorno.
