---
name: android-install-and-logcat
description: Arrancar el emulador trombito-36, instalar el APK debug de Rally Copilot, lanzar la app, leer logcat filtrado sin datos sensibles y capturar pantalla; no compila ni diagnostica.
allowed-tools: Read, Grep, Glob, Bash(adb *), Bash(emulator *), Bash(./gradlew assembleDebug), Bash(mkdir *)
---

# android-install-and-logcat

Instala el APK debug en el emulador (o dispositivo), lo arranca, captura logcat acotado y sin datos sensibles, y guarda capturas de pantalla.

## Cuándo usarla
- Probar a mano un cambio en emulador/dispositivo y ver sus logs.
- Obtener un fragmento de logcat limpio o una captura para una issue, PR o `docs/capturas/`.

## Cuándo NO usarla
- Compilar el artefacto → `android-build`.
- Analizar un build roto o un crash → `android-debug-failure`.
- Medir rendimiento → `android-profile`.

## Precondiciones
- SDK en `%LOCALAPPDATA%\Android\Sdk` (Git Bash: `$LOCALAPPDATA/Android/Sdk`); `platform-tools` y `emulator` en el `PATH` o llamados por ruta completa.
- AVD disponible: `trombito-36` (`emulator -list-avds`). Si hay varios dispositivos, `-s <serial>` en cada comando.
- APK en `app/build/outputs/apk/debug/*.apk`; si falta o es antiguo, `./gradlew assembleDebug`.
- `<paquete>` = `applicationId` de `app/build.gradle.kts` (esperado `app.trombito.rallycopilot`, con sufijo `.dev` en debug). No asumirlo.
- Para simular movimiento, ver la skill `gps-replay` (rutas reales de Mallorca en `docs/rutas/`).

## Pasos
1. Emulador: `adb devices`; si no hay ninguno, `emulator -avd trombito-36 -no-snapshot-save &` y esperar con `adb wait-for-device` y `adb shell getprop sys.boot_completed` = `1`.
2. Confirmar estado `device` (no `unauthorized`/`offline`) y que el APK es posterior al último cambio.
3. Instalar conservando datos: `adb install -r <apk>`; esperado `Success`. Ante `INSTALL_FAILED_*` reportarlo tal cual; no desinstalar por cuenta propia.
4. Arrancar: `adb shell monkey -p <paquete> -c android.intent.category.LAUNCHER 1`.
5. Limpiar buffer: `adb logcat -c`; reproducir.
6. Logs acotados (`-d`, sin streaming):
   - `adb logcat -d -v threadtime --pid=$(adb shell pidof -s <paquete>)`
   - Por tag: `adb logcat -d -v threadtime -s <Tag>:I`; solo errores: `adb logcat -d -v threadtime *:E`.
7. Captura: `mkdir -p docs/capturas` y `adb exec-out screencap -p > docs/capturas/<nombre>.png`. Revisar que no muestre datos personales (ni ubicación real del usuario) antes de versionarla.
8. Antes de pegar logs fuera de la sesión, redactar con `[REDACTED]`: tokens, `Authorization`, claves, JWT (`eyJ...`), emails y coordenadas de trazas reales del usuario. Compartir ≤ 50 líneas alrededor del evento.

## Validaciones / tests
- `adb shell pidof -s <paquete>` devuelve un PID (la app sigue viva).
- `grep -iE "authorization|bearer|apikey|api_key|eyJ|password" <fragmento>` sin coincidencias.
- La captura PNG existe y su tamaño es > 0.

## Definition of Done
- [ ] APK instalado (`Success`) y app arrancada.
- [ ] Logs filtrados y acotados; fragmento sin tokens, claves ni emails.
- [ ] Capturas en `docs/capturas/<nombre>.png` si se pidieron.
- [ ] No se ha desinstalado la app ni borrado datos sin petición explícita.
- [ ] Resultado (éxito o error literal de instalación) comunicado.

## Docs a actualizar
- Ninguno salvo capturas referenciadas desde `docs/` · docs/ESTADO.md (skill `session-handoff`)
