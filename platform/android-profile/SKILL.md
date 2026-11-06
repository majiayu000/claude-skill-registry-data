---
name: android-profile
description: Medir CPU, memoria o batería (p. ej. navegación con pantalla apagada, render del mapa, cálculo de notas) antes de optimizar y registrar métricas antes/después; no optimiza ni revisa código.
argument-hint: "[cpu|memory|battery]"
allowed-tools: Read, Grep, Glob, Bash(adb *), Bash(./gradlew *)
---

# android-profile

Mide `$ARGUMENTS` (`cpu`, `memory` o `battery`; por defecto `cpu`) con un escenario repetible. Sin medición no hay optimización.

## Cuándo usarla
- Sospecha de tirones, fugas de memoria o consumo (mapa vectorial/satélite, servicio de ubicación, TTS, cálculo de notas o rutas).
- Verificar con números que un cambio mejora o no empeora.

## Cuándo NO usarla
- La app falla o se cierra → `android-debug-failure`.
- Revisar código por rendimiento sin medir → `performance-review`.
- Aplicar la optimización → skill de implementación, tras esta medición.

## Precondiciones
- Dispositivo físico preferible; el emulador `trombito-36` solo es orientativo. `adb devices` correcto y build representativa.
- Escenario fijo: pasos, duración y datos (traza de `docs/rutas/` con `gps-replay`, nunca trazas reales del usuario en informes).
- Si no existe módulo Macrobenchmark, no inventarlo: avisar al agente principal.

## Pasos
1. Definir hipótesis y métrica objetivo antes de medir.
2. **Línea base**: ≥ 3 ejecuciones, mismo escenario y dispositivo; anotar mediana y dispersión.
3. Según `$ARGUMENTS`:

| Valor | Herramienta | Qué registrar |
|---|---|---|
| `cpu` | Profiler de Android Studio (CPU/System Trace) o `adb shell dumpsys gfxinfo <paquete> framestats` | arranque, frames lentos, hilos calientes |
| `memory` | Profiler (heap/allocations); `adb shell dumpsys meminfo <paquete>` | PSS total, heap Java/Native, crecimiento tras N repeticiones |
| `battery` | `adb shell dumpsys batterystats --reset`, escenario, `adb shell dumpsys batterystats <paquete>`; `adb shell dumpsys location` | uso por componente, wakelocks, GPS, CPU con pantalla apagada |

4. Si hay Macrobenchmark: `./gradlew <tarea del módulo>`; reporte fuera del repo.
5. Identificar el cuello de botella con evidencia (hilo, función, objeto retenido, wakelock). No adivinar.
6. Si procede optimizar, entregar hallazgos a `performance-review`; tras el cambio repetir el paso 2.
7. Registrar: `métrica | antes (mediana ± dispersión) | después | dispositivo/build | escenario`.

## Validaciones / tests
- Mismas condiciones antes/después (dispositivo, build, escenario, batería y temperatura similares).
- `./gradlew testDebugUnitTest` en verde tras cualquier optimización posterior.

## Definition of Done
- [ ] Hipótesis, escenario y métrica definidos antes de medir.
- [ ] Línea base con ≥ 3 ejecuciones registrada.
- [ ] Cuello de botella identificado con evidencia.
- [ ] Métricas antes/después en tabla (si hubo optimización).
- [ ] Informe sin datos de usuario ni tokens.

## Docs a actualizar
- Presupuestos de rendimiento en `docs/arquitectura.md` si se fijan · docs/ESTADO.md (skill `session-handoff`)
