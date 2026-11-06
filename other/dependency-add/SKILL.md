---
name: dependency-add
description: Evaluar y añadir una dependencia nueva (Gradle/Version Catalog) con versión exacta; no para actualizar o quitar (dependency-maintenance).
allowed-tools: Read, Grep, Glob, Edit, Bash(./gradlew *)
---

# dependency-add

Decide si una dependencia merece entrar y, solo entonces, la añade con versión exacta y decisión registrada. Sin esta skill no se añade ninguna dependencia (CLAUDE.md § Reglas de trabajo).

## Cuándo usarla
- Se propone una librería o plugin nuevo para `app/` o `motor/` (o para un script del repo).

## Cuándo NO usarla
- Actualizar, quitar o inventariar licencias de lo existente → usa `dependency-maintenance`.
- Herramienta ya fijada en `docs/DECISIONES.md` (versiones): usar esa versión, sin repetir la evaluación completa.

## Precondiciones
- Nombre de la librería y módulo destino claros (`app`, `motor`). Si faltan, pedirlos y parar.
- `gradle/libs.versions.toml` es reservado del agente principal: un subagente propone el cambio en su respuesta.
- Hito activo compatible con la dependencia (no implementar fuera del hito).

## Pasos
1. **Necesidad**: ¿lo resuelve la plataforma, la librería estándar de Kotlin o algo ya presente (`Grep` en `gradle/libs.versions.toml` y `*.gradle.kts`)? Si sí, no añadir.
2. **Licencia**: compatible con una app publicada en Play (MIT, Apache-2.0, BSD, ISC). Copyleft (GPL/AGPL) o sin licencia → parar, apuntar en `QUESTIONS.md` y consultar. Datos y modelos (mapas, voces) con su licencia y atribución.
3. **Mantenimiento**: último release, frecuencia, issues críticos. Datos no verificables → marcar `VERIFICAR`, no afirmarlos.
4. **Tamaño**: impacto en el APK (librerías nativas por ABI) y en el arranque; evitar transitivas pesadas. `motor/` debe seguir siendo Kotlin/JVM puro (sin dependencias Android).
5. **Seguridad y offline**: sin telemetría ni dependencia de servicios en línea (la app es offline por defecto, sin backend); sin Google Play Services; permisos nuevos en el manifest justificados.
6. **Versión exacta publicada hace ≥ 2 semanas**; compatible con Kotlin, AGP y las versiones fijadas en `docs/DECISIONES.md`.
7. **Instalar**: versión y alias en `gradle/libs.versions.toml` (`[versions]` y `[libraries]`/`[plugins]`) y usarlo vía `libs.*`; nunca coordenadas con versión en `build.gradle.kts`. Sin rangos ni `+`.
8. **Registrar la decisión** con `registrar-decision`: investigación en `docs/investigacion/` si es estructural (mapas, enrutado, TTS, persistencia, red); si no, una línea en `docs/DECISIONES.md` vía agente principal.

## Validaciones / tests
- `./gradlew assembleDebug testDebugUnitTest :motor:test` (la build resuelve la dependencia).
- `./gradlew ktlintCheck detekt lintDebug`.

## Definition of Done
- [ ] Necesidad, licencia, mantenimiento, tamaño y seguridad evaluados y anotados.
- [ ] Versión exacta con ≥ 2 semanas de antigüedad y compatible con las versiones fijadas.
- [ ] Declarada en el Version Catalog y consumida por `libs.*`.
- [ ] Decisión registrada en `docs/DECISIONES.md`.
- [ ] Gate qa fast en verde.

## Docs a actualizar
- `docs/investigacion/` (si estructural) · `docs/DECISIONES.md` (vía agente principal, reservado) · docs/ESTADO.md (skill `session-handoff`)
