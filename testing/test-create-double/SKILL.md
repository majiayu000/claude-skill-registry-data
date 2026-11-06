---
name: test-create-double
description: Crear dobles deterministas reutilizables (fixture, mock o fake) sin azar, tiempo ni GPS reales; no para escribir los tests (test-write) ni para tests flaky (test-debug-flaky).
argument-hint: "[fixture|mock|fake]"
allowed-tools: Read, Grep, Glob, Write, Edit, Bash(./gradlew *)
---

# test-create-double

Crea el doble `$ARGUMENTS` (por defecto `fake` si falta) en el código de test compartido del módulo: `motor/src/test` (dominio puro) o el directorio de test compartido de `app/`.

## Cuándo usarla
- Varios tests necesitan el mismo dato, repositorio, reloj, generador de ids, fuente de posiciones o motor de voz.
- Un test usa `Instant.now()`, `System.currentTimeMillis()`, `Random`, GPS o red real y hay que sustituirlo.

## Cuándo NO usarla
- Escribir el test que consume el doble → usa `test-write`.
- Un test intermitente → usa `test-debug-flaky`.
- Dependencias nuevas de test → skill `dependency-add`.

## Precondiciones
- Identificar la interfaz/puerto a sustituir y leer su definición real (no inventar firmas).
- Mirar antes lo existente en los directorios de test de `motor/` y `app/`. Reutilizar, no duplicar.

## Pasos
1. Elegir el tipo con `$ARGUMENTS`:

| Valor | Cuándo | Cómo |
|---|---|---|
| `fixture` | Datos de ejemplo (traza, tramo, sectores, nota, alerta) | Función `make<Entidad>(overrides)` con valores constantes; fechas fijas, nunca `now()`; trazas sintéticas o recortes de `docs/rutas/` |
| `fake` | Colaborador con comportamiento (preferido para repositorios) | Implementación en memoria de la interfaz real; estado inspeccionable; reloj e ids inyectados |
| `mock` | Solo en bordes sin lógica (SDK, sistema Android) | MockK; verificar la llamada de salida, no detalles internos |

2. Reloj e ids: nunca leer tiempo ni azar reales. Inyectar un reloj fijo/avanzable y un generador de ids determinista.
3. Fakes específicos:
   - Reloj: avanzable a mano para probar cronometraje, parciales y deltas sin esperas.
   - Fuente de posiciones: emite una lista de fixes (lat, lon, alt, velocidad, tiempo) a demanda; permite simular pérdida de señal y saltos.
   - Voz: registra las frases pedidas con su instante, sin audio real, para comprobar anticipación y orden de notas.
   - Repositorio: mapa en memoria con las mismas reglas que el real.
4. Ubicación: dominio puro en `motor/`; lo que dependa de Android en el directorio de test compartido de `app/`, no en `src/test` de una feature.
5. Añadir un test mínimo del propio doble (respeta el contrato de la interfaz) y usarlo en al menos un test real.

## Validaciones / tests
- `./gradlew :motor:test testDebugUnitTest`.
- Determinismo: ejecutar dos veces seguidas y comprobar el mismo resultado.

## Definition of Done
- [ ] Doble sin azar, reloj real, `Thread.sleep`, GPS ni red.
- [ ] Mocks solo en bordes; repositorios, reloj, ids y posiciones como fakes.
- [ ] Ubicado en el módulo de test compartido y usado por un test real.
- [ ] Sin dependencia nueva sin `dependency-add`.
- [ ] Gate qa fast en verde.

## Docs a actualizar
- `docs/testing.md` si existe · docs/ESTADO.md (skill `session-handoff`)
