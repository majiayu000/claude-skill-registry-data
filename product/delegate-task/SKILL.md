---
name: delegate-task
description: Generar un brief para un subagente con BRIEF.template.md y comprobar límites de tamaño, validación y presupuesto de subagentes (≤ 1 punto); si no cumple, dividir. No ejecuta la delegación.
allowed-tools: Read, Grep, Glob, Bash(wc *)
---

# delegate-task

Redacta el brief de un subagente con `docs/_templates/BRIEF.template.md`, comprueba los límites de CLAUDE.md § Delegación y devuelve el texto listo para pasar al agente.

## Cuándo usarla
- Antes de lanzar cualquier subagente (`Agent`) o lote de subagentes en paralelo.

## Cuándo NO usarla
- Si un script puede hacerlo (`node scripts/…`, Gradle), no hace falta ningún modelo.
- Cerrar sesión → usa `session-handoff`.
- Diseñar el reparto de una feature entera → usa `design-feature` (genera el plan de lotes).

## Precondiciones
- Objetivo único formulable en una frase. Si lleva "y", son dos briefs.
- Conocer: rutas de lectura y de escritura, comando de validación y modelo.

## Pasos
1. Elegir agente: especialista de `.claude/agents/` (índice `docs/agentes.md`) o, si no está cargado, `general-purpose` + "Actúa según .claude/agents/<x>.md" con el modelo de su frontmatter.
2. Elegir modelo **explícito** (nunca omitirlo, también en Explore/Plan): haiku = mecánico · sonnet = ingeniería · opus = seguridad/arquitectura/revisión de notas de rally.
3. Copiar `docs/_templates/BRIEF.template.md` y rellenar cada línea: ROL/AGENTE · MODELO · OBJETIVO · LEER PRIMERO · ARCHIVOS PERMITIDOS · ARCHIVOS PROHIBIDOS · PROHIBIDO · INSTRUCCIONES · VALIDACIÓN · SI ALGO FALLA · DEVOLVER. Quitar el comentario inicial.
4. Comprobar límites (todos obligatorios):
   - Brief ≤ 40 líneas (`wc -l`).
   - Lote: ≤ 5 archivos (o un directorio propio), o ≤ 3 skills, ≤ 4 agentes, ≤ 3 docs largos.
   - Exactamente **1** comando de validación, real (`./gradlew :motor:test`, `./gradlew testDebugUnitTest`, `node scripts/check-claude-assets.mjs`…).
   - Respuesta pedida ≤ 15 líneas.
   - Modelo explícito.
5. **Presupuesto de subagentes simultáneos ≤ 1 punto**: opus = 1 · sonnet = 0,5 · haiku = 0,25. Sumar los que ya están corriendo más los nuevos; si pasa de 1, encadenar en vez de paralelizar. Válidos: 1 opus · 2 sonnet · 4 haiku · 1 sonnet + 2 haiku.
6. En paralelo con otros: archivos permitidos **disjuntos**. Dos lotes no tocan a la vez `gradle/libs.versions.toml`.
7. Archivos reservados (CLAUDE.md, `.claude/settings.json`, `.claude/hooks/**`, `docs/_templates/**`, `docs/ESTADO.md`, `docs/DECISIONES.md`, `docs/MEMORIA.md`, `ROADMAP.md`, `QUESTIONS.md`, `gradle/libs.versions.toml`, `settings.gradle.kts`) nunca en ARCHIVOS PERMITIDOS; el subagente pide el cambio en su respuesta.
8. Las dudas de producto que encuentre el subagente vuelven en su respuesta; el agente principal las apunta en `QUESTIONS.md`.
9. Si algo incumple, **dividir** en briefs secuenciales o paralelos disjuntos y repetir la comprobación en cada uno.
10. Entregar el brief en un bloque de código con una línea de resumen: agente · modelo · puntos · nº de archivos · validación.

## Validaciones / tests
- `wc -l` del brief ≤ 40.
- Suma de puntos de los subagentes simultáneos ≤ 1.
- Cada ruta de LEER PRIMERO existe (`Glob`); el comando de VALIDACIÓN existe en `scripts/` o Gradle.

## Definition of Done
- [ ] Brief con todas las líneas de la plantilla y ≤ 40 líneas.
- [ ] Un objetivo, un comando de validación, respuesta ≤ 15 líneas, modelo explícito.
- [ ] Presupuesto simultáneo ≤ 1 punto comprobado.
- [ ] Archivos permitidos dentro del límite, disjuntos en paralelo y sin reservados.
- [ ] Prohibido git commit/push declarado en el brief (solo el agente principal commitea; el push, con permiso del usuario).

## Docs a actualizar
- Ninguno · docs/ESTADO.md (skill `session-handoff`) con lo delegado y el resultado
