---
name: hito
description: Gestionar un hito Hn de ROADMAP.md (start = arranque | plan = lotes | split = sub-hitos | complete = gates y cierre); nunca empieza un hito no pedido; no es session-start/handoff.
argument-hint: "[start|plan|split|complete] [Hn]"
allowed-tools: Read, Grep, Glob, Edit, Write, Bash(./gradlew *), Bash(node scripts/*), Bash(bash scripts/*), Bash(git status *), Bash(git log *)
---

# hito

Operación `$0` sobre el hito `$1` (sección `## Hn` de `ROADMAP.md`, estructura de `docs/_templates/HITO.template.md`). Sin `$0`: pedirlo y parar. Sin `$1`: usar el hito activo de `docs/ESTADO.md`; si no consta, parar y preguntar.

## Cuándo usarla
- Arrancar, planificar en lotes, dividir o cerrar un hito.

## Cuándo NO usarla
- Retomar o cerrar una sesión sin cambiar de hito → usa `session-start` / `session-handoff`.
- Editar docs técnicos → usa `docs-update`. Registrar decisiones → usa `registrar-decision`.
- Diseñar una funcionalidad concreta dentro del hito → usa `design-feature`.

## Precondiciones
- Modo desatendido: los hitos se encadenan (MEMORIA 2026-11-01). Se para solo si hay dudas de producto, al principio o al final del hito; sin dudas, el cierre publica la versión y arranca el siguiente.
- `ROADMAP.md` leído entero, junto a `docs/ESTADO.md`, `QUESTIONS.md` y las secciones citadas de `docs/DECISIONES.md`.
- `docs/ESTADO.md` es reservado: esta skill redacta el texto a añadir y lo entrega al agente principal (`session-handoff`).

## Pasos
### start
1. Leer `### Estado` (`Depende de`) y comprobar: hitos previos `completado`, dudas bloqueantes de `QUESTIONS.md` respondidas, pasos manuales del usuario hechos (`docs/pasos-manuales.md`), entorno, `git status` limpio.
2. Si falta algo: parar e informar; no cambiar el estado. Lo que no dependa del bloqueo puede avanzar.
3. Listar los `VERIFICAR` y dudas de producto abiertas antes de seguir.
4. Cambiar el Estado a `en curso` y redactar la fila de `ESTADO.md` (hito, siguiente paso).
5. Si no hay plan de lotes, encadenar `plan`.

### plan
1. Convertir el Alcance en lotes (tabla en `ESTADO.md` o bajo el hito): Lote · Agente [modelo] · Archivos (propiedad exclusiva) · Validación · Paralelo con.
2. Cada lote cumple CLAUDE.md § Delegación: 1 objetivo, brief ≤ 40 líneas, ≤ 5 archivos, 1 comando de validación, respuesta ≤ 15 líneas.
3. Modelo explícito (`haiku` mecánico · `sonnet` ingeniería · `opus` seguridad/arquitectura/revisión de notas). Si un script puede hacerlo, ningún modelo.
4. Paralelo solo con archivos disjuntos y **presupuesto simultáneo ≤ 1 punto** (opus 1 · sonnet 0,5 · haiku 0,25). `gradle/libs.versions.toml` y `settings.gradle.kts` son del agente principal.
5. Cambios sensibles (ubicación, permisos, CI, firma) → revisión de seguridad [opus] en un lote propio.

### split
1. Estimar: > 5 lotes secuenciales, > 15 archivos o varios dominios (motor + Android + datos) indican que no cabe en una sesión.
2. Dividir en sub-hitos `HnA`, `HnB`… cortando por contrato: cada uno deja el repo en verde, con criterios propios y `Depende de`.
3. Cada sub-hito con la estructura de `HITO.template.md`, sin duplicar tareas ni tests.

### complete
1. Recorrer `### Criterios de aceptación`; marcar `[x]` solo lo comprobado con evidencia (comando, test, captura del emulador).
2. Gates: `./gradlew ktlintCheck detekt lintDebug testDebugUnitTest :motor:test assembleDebug :app:minifyReleaseWithR8`, `node scripts/check-claude-assets.mjs`, `bash scripts/test-hooks.sh`, `node scripts/check-docs.mjs`.
3. Si algo falla o queda abierto: no cerrar; listarlo en el Estado del hito con destino (otro hito o TODO en ESTADO.md).
4. Si todo pasa: Estado `completado (AAAA-MM-DD)` con qué se hizo y qué quedó pendiente; entregar el texto de ESTADO.md al agente principal.
5. Subir la menor en `version.properties` + whatsnew, push con todo en verde y comprobar la release. Si hay dudas abiertas en `QUESTIONS.md`, **parar** y presentarlas juntas (de 4 en 4); con las respuestas, o si no había dudas, arrancar el siguiente hito.

## Validaciones / tests
- `start`/`plan`/`split`: `node scripts/check-docs.mjs`. `complete`: los gates de arriba, todos en verde.

## Definition of Done
- [ ] Solo se operó sobre el hito pedido; Estado coherente con la operación.
- [ ] `plan`: todos los lotes con agente, modelo, archivos y validación, dentro del presupuesto de subagentes.
- [ ] `split`: cada sub-hito cabe en una sesión y es verificable por separado.
- [ ] `complete`: gates en verde, criterios marcados con evidencia y dudas presentadas al usuario.

## Docs a actualizar
- `ROADMAP.md` · docs/ESTADO.md (skill `session-handoff`) · `docs/DECISIONES.md` si cambia una decisión (`registrar-decision`) · `QUESTIONS.md`
