---
name: sdd-lifecycle
description:
  'Trigger: SDD, docs/sdd, PRD, spec, diseño, tasks, apply-progress, verify-report, archive.
  Gobierna lifecycle de artefactos SDD y disciplina de cleanup.'
license: Apache-2.0
metadata:
  author: AutanaSoft
  organization: AutanaSoft
  version: '1.1.0'
  date: 'May 2026'
---

# AutanaSoft SDD Lifecycle

Prácticas de lifecycle para artefactos Spec-Driven Development en proyectos AutanaSoft.

Principio rector: esta skill define reglas reutilizables para mantener los artefactos SDD como
fuente de verdad, evitar regeneración destructiva y asegurar que implementación/verificación no deje
deuda obsoleta.

## Cuándo Usarla

Usa esta skill cuando trabajes con artefactos SDD en `docs/sdd/**`, especialmente para:

- Crear o actualizar PRDs, specs, designs, tasks, apply-progress o verify reports.
- Re-ejecutar una fase SDD cuando ya existen artefactos.
- Decidir si crear un artefacto nuevo o actualizar incrementalmente uno existente.
- Gestionar status, versión, frontmatter y changelogs de artefactos.
- Reiniciar un ciclo SDD de componente/página por aprendizaje o cleanup de lifecycle.
- Implementar cambios desde SDD tasks y reemplazar paths de código existentes.
- Verificar trabajo completado contra specs, tasks y expectativas de cleanup.
- Archivar un cambio SDD completo o sincronizar deltas hacia documentos baseline.

## Referencia Rápida

- `references/lifecycle-living-artifacts.md`: tratar artefactos existentes como documentos vivos;
  actualizar sin regeneración ciega.
- `references/lifecycle-versioning-status.md`: statuses, versionado, frontmatter y changelogs.
- `references/phase-approval-and-evidence.md`: approval gates, guía de fases y evidencia TDD.
- `references/apply-cleanup-replaced-code.md`: remover código obsoleto cuando la implementación
  reemplaza comportamiento existente.
- `references/language-and-validation.md`: política de idioma y comandos de validación.

## Categorías Por Prioridad

| Prioridad | Categoría        | Impacto | Prefijo      |
| --------- | ---------------- | ------- | ------------ |
| 1         | Lifecycle        | HIGH    | `lifecycle-` |
| 2         | Phase Gates      | HIGH    | `phase-`     |
| 3         | Apply Discipline | HIGH    | `apply-`     |
| 4         | Validation       | MEDIUM  | `language-`  |

## Estructura De La Skill

- `references/` - Reglas fuente modulares, una regla por archivo.
- `references/_sections.md` - Orden de secciones, impacto y prefijos de archivo.
- `references/_template.md` - Plantilla para reglas nuevas.

## Cómo Usarla

Lee la regla individual antes de aplicar una convención. Si una regla pertenece a TypeScript,
Next.js, NestJS o Drizzle, muévela a la skill correspondiente en lugar de duplicarla aquí.

## Regla Crítica Transversal

Cuando un cambio SDD reemplaza comportamiento, UI, data flow o componentes existentes, la
implementación debe **reemplazar y limpiar**, no solo agregar. El código reemplazado debe removerse,
no ocultarse.

Detalle: `references/apply-cleanup-replaced-code.md`.

## Recursos

- **Índice de reglas**: ver [references/agent-context.md](references/agent-context.md).
