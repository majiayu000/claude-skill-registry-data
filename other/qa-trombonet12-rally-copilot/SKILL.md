---
name: qa
description: Ejecutar la puerta de calidad en modo fast o full e interpretar el resultado; no para escribir tests (test-write) ni probar en dispositivo (qa-scenario).
argument-hint: "[fast|full]"
allowed-tools: Read, Grep, Glob, Bash(./gradlew *), Bash(node scripts/*), Bash(bash scripts/*)
---

# qa

Ejecuta el gate del modo `$ARGUMENTS` (por defecto `fast`) y explica cada paso. No hay script único: se lanzan los comandos de la tabla en orden, sin parar en el primer fallo.

## Cuándo usarla
- Antes de declarar una tarea terminada o commitear (`fast`), o antes de cerrar un hito o pedir permiso para un push/release (`full`).

## Cuándo NO usarla
- Escribir o arreglar tests → usa `test-write` / `bugfix-flow`.
- Probar pantalla apagada, segundo plano, pérdida de GPS o actualización del APK → usa `qa-scenario`.
- Publicar → usa `release-preflight` y `release`.

## Precondiciones
- JDK 21 configurado para Gradle (`~/.gradle/gradle.properties`) y SDK Android (`local.properties` o `ANDROID_HOME`).
- Node ≥ 22 para `scripts/*.mjs`. No imprimir valores de entorno.

## Pasos
1. Resolver el modo; si no es `fast|full`, usar `fast` y decirlo.
2. Ejecutar los comandos del modo:

| Modo | Comandos |
|---|---|
| fast | `./gradlew ktlintCheck testDebugUnitTest :motor:test` · `node scripts/check-claude-assets.mjs` · `node scripts/gen-claude-index.mjs --check` · `bash scripts/test-hooks.sh` |
| full | fast + `./gradlew detekt lintDebug assembleDebug :app:minifyReleaseWithR8` · `node scripts/check-docs.mjs` |

3. Registrar `paso | OK/FAIL/SKIP | motivo`. SKIP solo si falta una herramienta o entorno (sin SDK); debe declararse.
4. Ante FAIL: re-ejecutar solo ese paso, corregir la causa y repetir el modo completo.
5. Informar: modo, conteo OK/FAIL/SKIP, causa de cada FAIL y si cada SKIP es aceptable (antes de un release no lo es).

## Validaciones / tests
- Todos los comandos del modo terminan con código 0.
- Nunca desactivar, saltar ni borrar tests, ni bajar reglas de lint o detekt, para poner un paso en verde.
- No imprimir variables de entorno ni secretos.

## Definition of Done
- [ ] El modo pedido termina con 0 FAIL.
- [ ] Todo SKIP explicado en el informe.
- [ ] Ningún test desactivado o relajado para pasar.
- [ ] Informe con tabla resumida y siguientes pasos si algo falló.

## Docs a actualizar
- docs/ESTADO.md con modo ejecutado, resultado y SKIP pendientes (skill `session-handoff`).
