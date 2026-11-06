---
name: android-static-analysis
description: Pasar ktlintCheck, detekt y Android Lint (lintDebug) sobre Rally Copilot y resumir hallazgos; no ejecuta tests (android-run-tests) ni revisa diseño (android-review).
allowed-tools: Read, Grep, Glob, Bash(./gradlew *), Bash(ls *)
---

# android-static-analysis

Ejecuta el análisis estático y devuelve los hallazgos agrupados por herramienta.

## Cuándo usarla
- Antes de cerrar una tarea o de pedir permiso para un push (el gate de CLAUDE.md incluye ktlint y detekt).
- Tras tocar Gradle, manifest o recursos, que Lint revisa.

## Cuándo NO usarla
- Ejecutar tests → `android-run-tests`; compilar artefactos → `android-build`.
- Revisión de lifecycle, background, permisos, ubicación o audio → `android-review`.
- Revisión de seguridad → `security-review`.

## Precondiciones
- Gradle desde la raíz, JDK 21 y Android SDK (CLAUDE.md § Comandos).
- Reglas de ktlint, detekt y Lint son las del repo; no relajarlas para pasar.

## Pasos
1. Ejecutar `./gradlew ktlintCheck detekt lintDebug`. Aislar una herramienta: `./gradlew ktlintCheck` (o `detekt`, `lintDebug`). Formato auto-corregible: `./gradlew ktlintFormat`.
2. Leer los reportes en `**/build/reports/` (ktlint, detekt y `lint-results-debug` en HTML/XML; usar `Glob` si la ruta difiere).
3. Presentar cada hallazgo como `SEVERIDAD | archivo:línea | regla: problema | corrección propuesta`.
4. Corregir en el código lo evidente (formato, imports, nombres) sin cambiar lógica por estilo. Lo no trivial, delegarlo con archivo y regla.
5. Baseline (detekt o Lint) **solo** como último recurso:
   - Prohibida para código nuevo; solo deuda preexistente demostrada.
   - Debe justificarse y registrarse en `docs/ESTADO.md` (regla, alcance, plan de retirada); ese archivo es del agente principal: pedirle el registro.
   - Nunca regenerar una baseline para limpiar una ejecución en rojo.
6. Ningún `@Suppress` ni entrada nueva en `lint.xml` sin comentario justificativo; ninguna regla desactivada globalmente.
7. Repetir hasta 0 errores.

## Validaciones / tests
- `./gradlew ktlintCheck detekt lintDebug` termina en `BUILD SUCCESSFUL`.
- `git diff` sin baselines nuevas o ampliadas sin su registro.
- Los avisos restantes están listados con su justificación.

## Definition of Done
- [ ] `ktlintCheck`, `detekt` y `lintDebug` sin errores.
- [ ] Hallazgos corregidos en código; supresiones o baseline justificadas y registradas.
- [ ] Ninguna regla desactivada globalmente.
- [ ] Gate completo `./gradlew ktlintCheck detekt lintDebug testDebugUnitTest assembleDebug` en verde si cierra una tarea.

## Docs a actualizar
- docs/ESTADO.md si se añadió o cambió una baseline (skill `session-handoff`).
