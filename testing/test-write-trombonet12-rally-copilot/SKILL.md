---
name: test-write
description: Escribir tests por tipo (motor, unit, db, android-ui) con TDD en lógica crítica (notas, cronometraje, tramos, deltas, parsing); no ejecuta QA (qa) ni escenarios en dispositivo (qa-scenario).
argument-hint: "[motor|unit|db|android-ui]"
allowed-tools: Read, Grep, Glob, Write, Edit, Bash(./gradlew *)
---

# test-write

Escribe tests del tipo `$ARGUMENTS` para el código indicado. Sin argumento, deducirlo del archivo a probar (`motor/` → `motor`, `app/` → `unit`/`android-ui`, DAO/migración → `db`).

## Cuándo usarla
- Añadir cobertura a código nuevo o existente, o fijar un bug con un test de regresión antes de arreglarlo.
- TDD obligatorio (CLAUDE.md) en lógica crítica: generación de notas, cronometraje, detección de tramos, cálculo de deltas, parsing GPX/KML y de datos, migraciones Room. Orden: test rojo, código mínimo, verde, refactor.

## Cuándo NO usarla
- Solo ejecutar la validación global → usa `qa`.
- Probar pantalla apagada, segundo plano o pérdida de GPS en dispositivo → usa `qa-scenario`.
- Test intermitente → usa `test-debug-flaky`. Crear el doble reutilizable → `test-create-double`.

## Precondiciones
- Conocer el comportamiento esperado (criterio de aceptación del hito, `docs/DECISIONES.md`); si es ambiguo y es de producto, apuntarlo en `QUESTIONS.md` antes de fijarlo en un test.
- Librería de test nueva → skill `dependency-add`, no instalar a mano.

## Pasos
1. Resolver el tipo desde `$ARGUMENTS`; localizar el test vecino más parecido y copiar su estilo (nombres en frase con backticks, en español).
2. Lógica crítica: escribir primero el test, ejecutarlo y comprobar que falla por la razón correcta; solo entonces implementar.
3. Escribir el test según la tabla.
4. Reglas comunes: nombre que describe el comportamiento; Arrange-Act-Assert; un motivo de fallo por test; deterministas (sin reloj, red, GPS ni azar reales: reloj, ids y fuentes de posición inyectados, ver `test-create-double`).
5. Geometría y notas: usar trazas pequeñas sintéticas (círculo de radio conocido, recta, horquilla) y fragmentos de rutas reales de `docs/rutas/` como fixtures; tolerancias explícitas en distancias y radios.
6. Mutar mentalmente el código: si cambiar una condición no rompe ningún test, falta una aserción.
7. Ejecutar el comando del tipo y luego el gate qa fast.

| Tipo | Dónde y con qué | Comando |
|---|---|---|
| motor | `motor/src/test`: JUnit4 + kotlin-test; geometría, curvatura, notas 1–6 y modificadores, cronometraje, sectores, deltas, GPX/KML; casos válidos, inválidos y bordes | `./gradlew :motor:test` |
| unit | `app/src/test`: JUnit4; corrutinas con `runTest` y `StandardTestDispatcher`/`Dispatchers.setMain`; ViewModels con fakes a mano | `./gradlew testDebugUnitTest` |
| db | Room en memoria con Robolectric + DAO real; migraciones con `MigrationTestHelper` y schemas exportados | `./gradlew testDebugUnitTest` |
| android-ui | Robolectric + harness `BancoCompose`/`LimpiezaCompose` (sin `createComposeRule`), `@Config(qualifiers = "w411dp-h891dp-xxhdpi")`; semántica antes que `testTag`; estados vacío/error, tema oscuro y claro, horizontal | `./gradlew testDebugUnitTest` |

- Sin Turbine ni tests instrumentados (`androidTest`): la batería end-to-end en emulador llega en H12.

## Validaciones / tests
- El test nuevo falla sin el cambio (rojo verificado) y pasa con él.
- Tres ejecuciones seguidas con el mismo resultado (sin flakiness).
- Gate qa fast en verde; en cambios de BD o Android, también qa full.

## Definition of Done
- [ ] Test del tipo correcto, en la ruta convencional y con estilo del vecino.
- [ ] Casos: camino feliz, bordes (vacío, nulo, límites) y error.
- [ ] Ningún test desactivado (`@Ignore`, `assumeTrue` espurio); sin datos personales en fixtures.
- [ ] En lógica crítica, evidencia de que el test falló antes de implementar.
- [ ] Gate qa fast en verde.

## Docs a actualizar
- `docs/testing.md` si existe y cambia la estrategia · docs/ESTADO.md (skill `session-handoff`)
