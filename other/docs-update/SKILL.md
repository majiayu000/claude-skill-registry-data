---
name: docs-update
description: Actualizar el doc afectado (architecture|data-model|testing|ci|voz|runbook) según DOC.template.md; no para ESTADO/DECISIONES/ROADMAP ni enlaces (docs-check).
argument-hint: "[architecture|data-model|testing|ci|voz|runbook]"
allowed-tools: Read, Grep, Glob, Edit, Write, Bash(git diff *), Bash(git log *), Bash(node scripts/*)
---

# docs-update

Actualiza el documento que corresponde a `$ARGUMENTS` para que refleje el estado real del código.

## Cuándo usarla
- Un cambio de código, esquema, datos, pipeline de voz o CI deja desfasado un doc de `docs/`.
- Hay que crear un doc nuevo del tema (runbook, contrato) con la estructura de `docs/_templates/DOC.template.md`.

## Cuándo NO usarla
- Registrar una decisión técnica → usa `registrar-decision`; `docs/DECISIONES.md` es reservado.
- Actualizar `docs/ESTADO.md` → usa `session-handoff` (reservado al agente principal).
- Comprobar enlaces o coherencia sin reescribir → usa `docs-check`.

## Precondiciones
- `$ARGUMENTS` es uno de los valores; si falta, deducirlo de `git diff --stat` y confirmarlo; si es ambiguo, preguntar.
- Conocer el cambio fuente (diff, commit o hito). Reservados que NO se editan aquí: `docs/DECISIONES.md`, `docs/ESTADO.md`, `docs/MEMORIA.md`, `docs/_templates/**`, `CLAUDE.md`, `ROADMAP.md`, `QUESTIONS.md`. Si hay que tocarlos, pedirlo al agente principal.

## Pasos
1. Localizar el doc destino con la tabla; si no existe, crearlo desde `DOC.template.md` (cabecera `Propósito · Audiencia · Actualizado`, Resumen, secciones del tema, Decisiones y fuentes, Pendiente).

| Valor | Doc destino |
|---|---|
| architecture | `docs/arquitectura.md` (diagramas Mermaid) |
| data-model | doc del modelo de datos en `docs/` (tablas Room, índices, formato de paquetes de mapas; localizar con Glob) |
| testing | `docs/testing.md` |
| ci | `docs/ci-cd.md` (workflows, release y Play; ver también `docs/play.md`) |
| voz | `docs/VOZ.md` (pipeline de voice-lab: transcripción, glosario, entrenamiento, pregeneración) |
| runbook | `docs/runbooks/<tema>.md` (pasos operativos, comprobaciones, vuelta atrás) |

2. Leer el doc entero y el cambio fuente (`git diff`, código, migración, workflow); contrastar cada afirmación con el código real, no con la memoria.
3. Editar solo las secciones afectadas; mantener estilo, tablas y diagramas. No duplicar `docs/DECISIONES.md`: referenciarlo por sección.
4. Datos no verificados (límites, versiones) → marcar `VERIFICAR`. Nunca inventar cifras.
5. Seguridad: nunca valores de secretos; solo nombres de variables.
6. Actualizar `Actualizado: AAAA-MM-DD` de la cabecera y mover a `## Pendiente` lo abierto.
7. Si se añade un doc nuevo, enlazarlo desde el doc relacionado.
8. Ejecutar la skill `docs-check links` sobre los archivos tocados.

## Validaciones / tests
- `node scripts/check-docs.mjs` sin errores en los archivos tocados.
- `git diff --stat` solo muestra docs permitidos, ninguno reservado.

## Definition of Done
- [ ] El doc refleja el código actual; cada dato verificable contrastado o marcado `VERIFICAR`.
- [ ] Estructura de `DOC.template.md` respetada y fecha `Actualizado` al día.
- [ ] Ningún doc reservado editado; peticiones sobre ellos listadas para el agente principal.
- [ ] Sin secretos ni valores sensibles.
- [ ] `node scripts/check-docs.mjs` en verde.

## Docs a actualizar
- Doc destino de la tabla · enlaces cruzados en docs relacionados · docs/ESTADO.md (skill `session-handoff`, agente principal)
