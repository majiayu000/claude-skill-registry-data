---
name: design-feature
description: Diseñar una feature antes de implementarla (contratos, flujo de datos, impacto, plan de lotes); no registra decisiones (registrar-decision) ni revisa código (architecture-review).
allowed-tools: Read, Grep, Glob
---

# design-feature

Produce un diseño previo para la feature descrita en `$ARGUMENTS`, sin escribir código. Entrega: contratos, flujo de datos, impacto y plan de lotes delegables.

## Cuándo usarla
- Antes de implementar una feature que toca `app/` y `motor/`, el esquema Room, el servicio de ubicación, la voz o los datos offline.
- Antes de repartir trabajo en subagentes: el plan de lotes sale de aquí.

## Cuándo NO usarla
- Decisión técnica puntual que hay que registrar → usa `registrar-decision` (se invoca desde el paso 6).
- Revisar código ya escrito → usa `architecture-review`.
- Bugfix o cambio local sin contratos nuevos → impleméntalo directamente (`bugfix-flow`).

## Precondiciones
- `$ARGUMENTS` con la descripción de la feature; si falta, pedirla y parar.
- Haber leído `docs/ESTADO.md`, el hito activo de `ROADMAP.md`, `QUESTIONS.md`, `docs/arquitectura.md` (si existe) y `docs/DECISIONES.md`. La feature debe caber en el hito activo; si no, parar y avisar.

## Pasos
1. Acotar: objetivo, fuera de alcance, criterios de aceptación comprobables. Lo que sea **decisión de producto** (UI, comportamiento, alcance) no se inventa: va a `QUESTIONS.md` con opciones y recomendación.
2. Localizar código y contratos existentes (Grep/Glob) en `app/` y `motor/`. No suponer: citar archivo.
3. Contratos: modelos y funciones de `motor/` (geometría, notas, cronometraje, sectores, deltas, GPX/KML), entidades Room, interfaces de dominio. Indicar dueño y consumidores de cada uno.
4. Flujo de datos: offline por defecto; Room como persistencia de usuario; datos de mapas descargados desde la app; red solo para mapas e incidencias. Para la conducción: estado que sobrevive a pantalla apagada, segundo plano y muerte del proceso (foreground service de ubicación).
5. Impacto: hitos afectados, decisiones que contradice o que faltan, migraciones Room, tests críticos (TDD en notas, cronometraje, detección de tramos, deltas, parsing), permisos Android, batería y privacidad.
6. Si hay decisión estructural nueva, delegar en `registrar-decision`. Si el riesgo es alto, pedir `architecture-review` con un revisor [opus].
7. Plan de lotes con los límites de CLAUDE.md § Delegación: 1 objetivo, ≤ 5 archivos, 1 comando de validación, respuesta ≤ 15 líneas, modelo explícito. Paralelo solo con archivos disjuntos y **presupuesto simultáneo ≤ 1 punto** (opus 1 · sonnet 0,5 · haiku 0,25). Los archivos reservados quedan para el agente principal.
8. Redactar cada lote con `docs/_templates/BRIEF.template.md` (skill `delegate-task`).

## Validaciones / tests
- Cada contrato tiene dueño, consumidor y test asociado.
- Ningún lote supera 5 archivos ni tiene dos comandos de validación.
- Los lotes paralelos no comparten archivos y respetan el presupuesto.

## Definition of Done
- [ ] Diseño con objetivo, contratos, flujo de datos, impacto y plan de lotes.
- [ ] Encaja en el hito activo y no contradice `docs/DECISIONES.md` (o propone registro).
- [ ] Dudas de producto apuntadas en `QUESTIONS.md`, no decididas.
- [ ] Riesgos listados; lo no verificable marcado `VERIFICAR`.
- [ ] Entregado en la respuesta (no se modifican archivos salvo petición).

## Docs a actualizar
- Hito en `ROADMAP.md` (si el diseño lo amplía) · `docs/DECISIONES.md` vía `registrar-decision` · `QUESTIONS.md` · docs/ESTADO.md (skill `session-handoff`)
