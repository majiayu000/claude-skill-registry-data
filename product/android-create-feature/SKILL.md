---
name: android-create-feature
description: Crear una feature Android de UI en Rally Copilot (screen Compose, ViewModel con UiState/StateFlow, ruta type-safe en AppNavHost, tests JVM); no capa de datos (android-create-data-layer) ni sistema.
argument-hint: "[nombre_feature]"
allowed-tools: Read, Write, Edit, Grep, Glob, Bash(./gradlew *)
---

# android-create-feature

Crea la feature `$ARGUMENTS` en `:app` (paquete `app.trombito.rallycopilot.ui.<feature>`, con lo que necesite en `domain/` y `data/`).

## Cuándo usarla
- Pantalla o flujo nuevo con estado propio y navegación.

## Cuándo NO usarla
- Entity, DAO o repository → `android-create-data-layer`.
- Módulo Hilt, permiso o componente de sistema → `android-create-hilt-module`, `android-add-permission`, `android-create-system-component`.
- Cambios menores en una pantalla existente: editar directamente.
- Lógica pura (geometría, notas, cronometraje, sectores, deltas, GPX/KML) → va en `:motor` (Kotlin JVM, sin Android), no aquí.

## Precondiciones
- `$ARGUMENTS` presente; derivar `<Feature>` (PascalCase) y `<feature>` (minúsculas). Si falta, pedirlo y parar.
- Leer `docs/ESTADO.md` y el hito activo de `ROADMAP.md`. Glob de una feature existente para copiar su estructura; no inventar otra.
- Textos, flujo y diseño de pantalla son producto: si no están definidos en el hito, apuntar la duda en `QUESTIONS.md` y seguir con lo que no dependa.
- Si lee o escribe datos, el repository (interfaz en `domain/`) debe existir; si no, `android-create-data-layer` antes. La UI observa Room.
- Sin dependencias nuevas sin la skill `dependency-add`.

## Pasos
1. `<Feature>UiState.kt`: `data class` inmutable (solo `val`) con estados de carga/vacío/error explícitos.
2. `<Feature>ViewModel.kt` con `@HiltViewModel`: depende de casos de uso o interfaces de dominio (clases simples en `domain/`). Expone `val uiState: StateFlow<<Feature>UiState>` vía `combine(...).stateIn(viewModelScope, SharingStarted.WhileSubscribed(5000), inicial)` y `fun onXxx(...)` por acción. Eventos de una sola vez (navegar, snackbar) por `Channel` expuesto como `receiveAsFlow()`. Dispatchers inyectados.
3. `<Feature>Screen.kt` en dos niveles: `<Feature>Route` (`hiltViewModel()`, `collectAsStateWithLifecycle()`, recoge el Channel) y `<Feature>Screen(state, ...)` sin lógica de negocio ni acceso a repositories.
4. `@Preview` con estados de ejemplo (cargando, contenido, error), Material 3 y el tema del proyecto (oscuro por defecto, estética WRC). Textos en `strings_<feature>.xml` (solo español).
5. Registrar la ruta **type-safe** en `ui/AppNavHost.kt`: `@Serializable data object|data class <Feature>Ruta` y `composable<<Feature>Ruta> { … }` (Navigation Compose 2.9); argumentos con `savedStateHandle.toRoute<<Feature>Ruta>()` en el ViewModel. Nada de rutas en string.
6. Test del ViewModel en `src/test` (JUnit4, coroutines-test, fakes a mano, dispatcher de test): secuencia de estados (inicial, carga, éxito, error), cada acción y los eventos del Channel.
7. Si hay UI crítica, test Compose con Robolectric y el harness `BancoCompose`/`LimpiezaCompose` en `src/test` (no `androidTest`): estados fabricados y callbacks invocados.
8. Si toca permisos, ubicación, audio o ciclo de vida, pedir además `android-review`.

## Validaciones / tests
- `./gradlew testDebugUnitTest`.
- `./gradlew ktlintCheck detekt lintDebug`.
- `./gradlew assembleDebug` compila con la ruta registrada.

## Definition of Done
- [ ] `UiState` inmutable y `StateFlow` expuesto; sin `MutableStateFlow` público.
- [ ] Ningún composable contiene lógica de negocio ni depende de repositories.
- [ ] Ruta type-safe registrada en `AppNavHost` y navegable.
- [ ] Tests de ViewModel y, si aplica, Compose/Robolectric en verde.
- [ ] Sin dependencias nuevas sin `dependency-add`; sin secretos.
- [ ] `./gradlew ktlintCheck detekt lintDebug testDebugUnitTest assembleDebug` en verde.

## Docs a actualizar
- `docs/arquitectura.md` si cambia el mapa de navegación o módulos · docs/ESTADO.md (skill `session-handoff`)
