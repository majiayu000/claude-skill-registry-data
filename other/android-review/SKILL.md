---
name: android-review
description: Revisar Android de Rally Copilot sin modificar (lifecycle, background, permissions, location, audio) con findings por severidad; no arquitectura (architecture-review) ni implementar.
argument-hint: "[lifecycle|background|permissions|location|audio]"
allowed-tools: Read, Grep, Glob, Bash(git diff *), Bash(git log *), Bash(git show *), Bash(./gradlew *)
---

# android-review

Revisión de solo lectura de `:app` según `$ARGUMENTS`. Devuelve findings; no modifica código. Sin argumento, recorrer los cinco ámbitos en orden: lifecycle, background, permissions, location, audio.

## Cuándo usarla
- El diff toca ViewModels, pantallas Compose, el servicio de ubicación, la voz, `AndroidManifest.xml` o receivers.
- Antes de cerrar una tarea Android.

## Cuándo NO usarla
- Fronteras de módulos, capas o flujo de datos → `architecture-review`.
- Implementar o corregir lo hallado → agente de ingeniería correspondiente o `bugfix-flow`.

## Precondiciones
- Rama con cambios respecto a `main` o commits locales; sin diff, revisar el estado actual de `:app`.
- Decisiones aplicables: `docs/DECISIONES.md` (ubicación sin Google Play Services, offline por defecto, TTS on-device).
- Concurrencia o lifecycle complejos (Flow compartidos, scopes manuales) → escalar a revisión de arquitectura.

## Pasos
1. Delimitar: `git diff main...HEAD --stat` (o `git diff HEAD~N`) sobre `app/`; leer los archivos del ámbito.
2. Aplicar la lista del valor de `$ARGUMENTS`:

| Valor | Comprobar |
|---|---|
| `lifecycle` | Estado en ViewModel (`StateFlow` con `stateIn(WhileSubscribed(5000))`), sin `Context`/`Activity` retenidos; `collectAsStateWithLifecycle`; eventos por `Channel` sin pérdida; `LaunchedEffect`/`DisposableEffect` con claves y `onDispose`; sin `GlobalScope`; dispatchers inyectados; navegación y cronómetro sobreviven a rotación y muerte de proceso (estado en Room/servicio, no solo en la UI) |
| `background` | Foreground service tipo `location` iniciado desde la UI; notificación persistente; sin hilos/`Timer` ad hoc; trabajo pesado (cálculo de notas, rutas) fuera del hilo principal; parada ordenada |
| `permissions` | Mínimo en el manifest, sin huérfanos; ubicación precisa pedida en contexto con rationale, aproximada y denegación permanente tratadas; `POST_NOTIFICATIONS`; `FOREGROUND_SERVICE_LOCATION`; sin `ACCESS_BACKGROUND_LOCATION` no decidido; componentes `exported` justificados; sin coordenadas en logs |
| `location` | `LocationManager` sin Google Play Services; frecuencia y precisión acordes; detección de pérdida de señal y saltos; filtrado de fixes malos; batería; trazas guardadas solo en el dispositivo |
| `audio` | TTS on-device; audio focus con ducking (`AUDIOFOCUS_GAIN_TRANSIENT_MAY_DUCK`) y liberación al terminar; cola de frases sin solapes; modo silencio respetado; `AudioAttributes` de navegación (`USAGE_ASSISTANCE_NAVIGATION_GUIDANCE`) |

3. Cada hallazgo con `archivo:línea` exacto y una corrección concreta. Lo no verificable en el código se pide confirmar, no se afirma.
4. Contrastar con las herramientas: ejecutar la validación y atribuir fallos al cambio.
5. Emitir findings por severidad (CRITICA, ALTA, MEDIA, BAJA) y veredicto: limpio / con avisos / bloquea. Navegación o voz que se detienen con la pantalla apagada, o coordenadas filtradas: mínimo ALTA.

## Validaciones / tests
- `./gradlew lintDebug testDebugUnitTest` y `./gradlew ktlintCheck detekt`.
- Comportamiento revisado sin test: finding MEDIA.

## Definition of Done
- [ ] Ámbito de `$ARGUMENTS` (o los cinco) recorrido por completo.
- [ ] Findings `SEVERIDAD | archivo:línea | problema | corrección propuesta`, ordenados por severidad.
- [ ] Ningún archivo modificado; veredicto emitido.
- [ ] Escalado a revisión de arquitectura si hay concurrencia/lifecycle complejo.
- [ ] Gate `./gradlew ktlintCheck detekt lintDebug testDebugUnitTest` ejecutado (o fallo atribuido).

## Docs a actualizar
- Ninguno si el veredicto es limpio; `registrar-decision` si se acuerda un cambio de enfoque · docs/ESTADO.md (skill `session-handoff`)
