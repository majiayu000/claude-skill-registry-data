---
name: test-debug-flaky
description: Diagnosticar y corregir un test intermitente (aislar, repetir, hallar causa raíz); no para un fallo reproducible siempre (bugfix-flow) ni para crear dobles (test-create-double).
allowed-tools: Read, Grep, Glob, Edit, Bash(./gradlew *)
---

# test-debug-flaky

Procedimiento para un test que unas veces pasa y otras falla. Objetivo: corregir la causa raíz, nunca ocultarla.

## Cuándo usarla
- Un test falla de forma intermitente en local o en CI.
- Pasa solo o en un orden y falla dentro de la suite completa.

## Cuándo NO usarla
- Falla siempre y de forma determinista → usa `bugfix-flow`.
- Falta un doble reutilizable (reloj, fake) para arreglarlo → usa `test-create-double`.

## Precondiciones
- Nombre del test y fallo observado (log de CI o salida local). Si no hay, pedirlos.
- Árbol de trabajo limpio de cambios no relacionados.

## Pasos
1. Aislar: ejecutar solo ese test.
   - Motor: `./gradlew :motor:test --tests "<clase>.<método>"`.
   - Android: `./gradlew testDebugUnitTest --tests "<clase>.<método>"`.
2. Repetir N veces (p. ej. 20) para reproducir: bucle de shell, con `--rerun-tasks` para que Gradle no reutilice resultados en caché.
3. Si solo falla en la suite completa, ejecutar la clase junto a sus vecinas y bisecar el orden hasta encontrar el test que contamina el estado.
4. Clasificar la causa típica:
   - Tiempo: reloj real, zonas horarias, `delay`, posiciones GPS reales → `Clock` inyectado o `TestDispatcher` con tiempo virtual.
   - Orden: dependencia entre tests → cada test crea su propio estado.
   - Concurrencia: carreras, corrutinas sin esperar → esperar el evento o la finalización explícita, no dormir.
   - Red: llamadas reales → fake del cliente (ver `test-create-double`).
   - Estado compartido: singletons, base en memoria, `object` mutables → reiniciar en `@Before`.
   - Azar/ids: generadores no deterministas → semilla o generador inyectado.
5. Corregir la causa raíz en el test o en el código; confirmar reproduciendo antes (falla en N) y después (N/N verde).
6. Prohibido: `@Ignore`, `Thread.sleep`/`delay` arbitrarios, subir timeouts o añadir reintentos para tapar el fallo.
7. Si no se resuelve en esta sesión: dejar el test activo, registrar causa sospechosa, comando de repetición y frecuencia en `docs/ESTADO.md` (skill `session-handoff`).

## Validaciones / tests
- Test aislado N/N veces en verde (N ≥ 20) y también dentro de su suite.
- Gate qa fast (skill `qa`).

## Definition of Done
- [ ] Causa raíz identificada y descrita en el mensaje de commit.
- [ ] Sin tests desactivados, sin sleeps ni timeouts ampliados.
- [ ] Repetición N/N en verde antes de cerrar.
- [ ] Si queda abierto: entrada en `docs/ESTADO.md` con cómo reproducirlo.
- [ ] Gate qa fast en verde.

## Docs a actualizar
- docs/ESTADO.md (skill `session-handoff`), obligatorio si el flaky sigue abierto.
