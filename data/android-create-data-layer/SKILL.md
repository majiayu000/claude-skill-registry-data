---
name: android-create-data-layer
description: Crear la capa de datos Android de una entidad de Rally Copilot (entity Room, DAO, repository, mapper y tests JVM); no para migrar un esquema (android-create-room-migration).
argument-hint: "[nombre_entidad]"
allowed-tools: Read, Write, Edit, Grep, Glob, Bash(./gradlew *)
---

# android-create-data-layer

Crea la capa de datos de `$ARGUMENTS` en `:app`: entity, DAO, repository, mapper y tests.

## Cuándo usarla
- Entidad nueva que se persiste en Room y que la UI consume vía repository.

## Cuándo NO usarla
- Cambiar columnas/tablas de una entidad ya publicada → `android-create-room-migration`.
- Pantalla o ViewModel → `android-create-feature`.
- Datos de mapas, grafo de rutas y elevación: se descargan como paquetes de archivos (ver `docs/DECISIONES.md`), no como tablas Room. Aquí van los datos del usuario: tramos, trazas, sectores, tiempos, notas editadas, rutas precargadas, ajustes.

## Precondiciones
- `$ARGUMENTS` presente (singular, PascalCase; tabla en snake_case). Si falta, pedirlo y parar.
- Glob de una entidad existente para seguir paquetes y estilo. Sin dependencias nuevas sin `dependency-add`.

## Pasos
1. Modelo `<Entidad>` y `interface <Entidad>Repository` en `domain/` (Kotlin puro, sin Room ni Android): `Flow` para lecturas, `suspend` para escrituras.
2. `<Entidad>Entity` en `data/db/`: `id` clave primaria estable y columnas de dominio. Índices explícitos.
3. `<Entidad>Dao`: consultas `Flow`; `@Upsert`; multi-paso en `@Transaction`.
4. Registrar entity en el `@Database` con `exportSchema = true`, subir `version` y ejecutar `android-create-room-migration`.
5. `<Entidad>Mapper.kt`: extensiones `toDomain()`/`toEntity()` puras, sin reloj ni UUID dentro.
6. `<Entidad>RepositoryImpl` (`@Inject`, DAO + mapper + dispatcher inyectados): implementa la interfaz de `domain/`.
7. Binding `@Binds` y `@Provides` del DAO en `di/*Module.kt` (`android-create-hilt-module`).
8. Tests JVM (JUnit4, coroutines-test, Robolectric con Room in-memory, fakes a mano): mapper ida y vuelta; DAO (upsert, `Flow`); repository con fakes del DAO.

## Validaciones / tests
- `./gradlew testDebugUnitTest` (incluye Room con Robolectric).
- `./gradlew ktlintCheck detekt lintDebug assembleDebug`.

## Definition of Done
- [ ] Interfaz del repository en `domain/` sin dependencias de Room ni Android.
- [ ] Entity, DAO, mapper y repository implementados según los pasos.
- [ ] Esquema JSON exportado y migración manual si subió la versión.
- [ ] Binding Hilt registrado; mapper, DAO y repository con tests en verde.
- [ ] `./gradlew ktlintCheck detekt lintDebug testDebugUnitTest assembleDebug` en verde.

## Docs a actualizar
- `docs/arquitectura.md` (modelo local, si existe) · docs/ESTADO.md (skill `session-handoff`)
