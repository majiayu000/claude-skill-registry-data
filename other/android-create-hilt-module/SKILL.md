---
name: android-create-hilt-module
description: Crear un módulo Hilt en di/*Module.kt con scopes y bindings de interfaces de dominio, y su reemplazo con fakes en tests; no para la capa de datos completa.
allowed-tools: Read, Write, Edit, Grep, Glob, Bash(./gradlew *)
---

# android-create-hilt-module

Crea un módulo Hilt que enlaza interfaces de dominio con implementaciones de datos o plataforma (`di/<Nombre>Module.kt`, en la raíz del paquete).

## Cuándo usarla
- Una interfaz de dominio (repositorio, reloj, fuente de posiciones, motor de voz…) necesita implementación inyectable.
- Hay que proveer objetos de terceros (Room, `LocationManager`, motor TTS) o sustituir dependencias en tests.

## Cuándo NO usarla
- Entity, DAO y repositorio completos → `android-create-data-layer` (que puede invocar esta skill).
- Clase propia con constructor simple → `@Inject constructor` basta, sin módulo.

## Precondiciones
- `@HiltAndroidApp` presente en la `Application` de `:app`; si no, parar y avisar al agente principal.
- La interfaz de dominio ya existe; el dominio y `:motor` no dependen de Android ni de Hilt.
- Decidir el scope: `SingletonComponent` (Room, clientes, estado compartido), `ViewModelComponent` (por ViewModel).

## Pasos
1. Crear `di/<Nombre>Module.kt` (paquete `app.trombito.rallycopilot.di`); nunca en `domain/`.
2. Interfaz con implementación propia: `@Module @InstallIn(<Componente>::class) abstract class` con `@Binds`; la impl lleva `@Inject constructor`.
3. Objetos sin `@Inject` (builders, librerías): `@Module @InstallIn(...) object` con `@Provides`. No mezclar `@Binds` y `@Provides` en la misma clase abstracta.
4. `@Singleton` solo con estado compartido o construcción cara; el resto sin scope.
5. Varias implementaciones del mismo tipo (dispatchers, reloj): `@Qualifier` propio, no `@Named` con strings.
6. Tests JVM (JUnit4): construir las clases a mano con fakes, sin Hilt. Si se necesita grafo (Robolectric + `@HiltAndroidTest`), módulo de test con `@TestInstallIn(components = [...], replaces = [<Nombre>Module::class])`.
7. Compilar: `MissingBinding` o `DuplicateBindings` se corrigen en el módulo, no con `@Provides` redundantes.

## Validaciones / tests
- `./gradlew assembleDebug` (valida el grafo Hilt en compilación).
- `./gradlew testDebugUnitTest ktlintCheck detekt lintDebug`.

## Definition of Done
- [ ] Cada interfaz de dominio tiene un único binding de producción (y otro de test si el grafo se usa en tests).
- [ ] Scope mínimo justificado; sin `@Singleton` gratuitos.
- [ ] Reemplazo en tests con `@TestInstallIn` (sin `@UninstallModules` salvo excepción comentada).
- [ ] El dominio no importa `dagger`/`hilt`.
- [ ] Build sin `MissingBinding`/`DuplicateBindings`.
- [ ] `./gradlew ktlintCheck detekt lintDebug testDebugUnitTest assembleDebug` en verde.

## Docs a actualizar
- `docs/arquitectura.md` si se añade un módulo o scope nuevo · docs/ESTADO.md (skill `session-handoff`)
