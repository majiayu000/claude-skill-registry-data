---
name: ddd-hexagonal
description: "Biblioteca DDD (estratégico/táctico) + hexagonal + CQRS ligero + integración (outbox, sagas, ACL) para proyectos complejos en Laravel, TypeScript (Next/Node, Vue) y Python: 74 docs por tema, plantillas y checklist de cuándo NO."
---

# ddd-hexagonal (Senzu)

Biblioteca de 74 documentos cortos (≤ 250 líneas, con índice) en `references/<tema>/` + plantillas de código en
`templates/<stack>/` + plantillas de documentación en `templates/docs/`. Catálogo completo: `INDEX.md`.
**Nunca leas la biblioteca entera**: decide si aplica (§1), localiza el documento en la tabla (§2) y lee solo su sección.

## 1. ¿Hace falta? (responde antes de tocar código)
Aplica DDD + hexagonal si se cumplen **≥ 3**:
- [ ] Reglas de negocio con invariantes reales (estados, límites, cálculos, permisos complejos), no solo validación de formulario.
- [ ] Varios contextos con lenguaje distinto o integraciones externas que hay que aislar.
- [ ] Vida esperada > 1 año y/o equipo > 2 personas.
- [ ] Necesidad de testear la lógica sin BD/framework/LLM.
- [ ] Ya duele: controladores de 300 líneas, lógica duplicada, modelos Eloquent/Prisma con reglas de negocio.

Si no: **capas simples** con `code-quality` y dilo explícitamente. Duda razonable → `references/examples/decision-trees.md`
y `references/examples/crud-vs-ddd-side-by-side.md`. Sobre-arquitectura cuesta tanto como su ausencia.

## 2. Lectura mínima por tarea
| Tarea | Lee solo |
|---|---|
| Empezar un módulo/contexto nuevo | `examples/walkthrough-invoicing.md` (recorrido completo) + `stacks/<stack>/overview.md` |
| Delimitar contextos, mapa, lenguaje | `strategic/bounded-contexts.md`, `strategic/context-mapping.md`, `strategic/ubiquitous-language.md` |
| Taller con negocio | `strategic/event-storming.md` + `templates/docs/context-sheet.md`, `templates/docs/glossary.md` |
| Modelar: ¿entidad, VO, agregado? | `tactical/entities.md`, `tactical/value-objects.md`, `tactical/aggregates.md` (+ `examples/decision-trees.md`) |
| Repositorios, servicios de dominio, eventos | `tactical/repositories.md`, `tactical/domain-services.md`, `tactical/domain-events.md` |
| Reglas, invariantes, errores de dominio | `tactical/invariants-and-errors.md`, `tactical/specifications.md` |
| Caso de uso, comandos/queries, DTOs, transacción | `application/use-cases.md`, `application/commands-queries-cqrs.md`, `application/dtos-and-mapping.md`, `application/transactions-unit-of-work.md` |
| Autorización y validación por capas | `application/authorization.md`, `application/validation-layers.md` |
| Listados/pantallas (read models) | `application/read-models-projections.md`, `persistence/read-models-and-projections.md` |
| Puertos, adaptadores, DI, carpetas | `hexagonal/ports-and-adapters.md`, `hexagonal/dependency-injection.md`, `hexagonal/folder-structures.md` |
| ¿Clean, hexagonal o vertical slices? | `hexagonal/clean-vs-hexagonal-vs-vertical-slices.md` |
| Reglas de dependencia automatizadas | `hexagonal/dependency-rules-tooling.md`, `testing/architecture-tests.md` |
| Persistencia con Eloquent / Prisma / SQLAlchemy | `persistence/orm-mapping.md` + `persistence/eloquent-pitfalls.md` \| `prisma-drizzle.md` \| `sqlalchemy.md` |
| Integraciones: outbox, colas, sagas, ACL, idempotencia | `integration/<tema>.md` (uno por tema) |
| Tests por capa | `testing/domain-tests.md`, `use-case-tests.md`, `adapter-tests.md`, `test-data-builders.md` |
| Laravel: providers, HTTP/Inertia, jobs, módulos | `stacks/laravel/<tema>.md` + `templates/laravel/` |
| Next/Node/TS | `stacks/typescript/<tema>.md` + `templates/typescript/` |
| FastAPI / LangGraph | `stacks/python/<tema>.md` + `templates/python/` (+ `examples/walkthrough-agent-langgraph.md`) |
| SPA Vue / Inertia (dónde acaba el dominio) | `stacks/vue-front/overview.md`, `stacks/vue-front/inertia-and-spa-usecases.md` |
| Monolito modular, ¿microservicios? | `strategic/modular-monolith.md`, `strategic/when-microservices.md` |
| Migrar un MVC existente | `checklists/migration-from-mvc.md`, `checklists/smells-and-refactorings.md` |
| Revisar diseño o PR | `checklists/design-review-checklist.md`, `checklists/code-review-checklist.md`, `checklists/anti-patterns.md` |
| Nombrar cosas | `checklists/naming-conventions.md` |
| Registrar una decisión | `templates/docs/adr.md` |

## 3. Flujo
1. **Contexto**: nombra el bounded context y su lenguaje ubicuo (ficha + glosario). Un módulo por contexto.
2. **Modelo**: agregados pequeños con invariantes, value objects para todo lo que tenga reglas, eventos de dominio en pasado.
3. **Puertos**: interfaces en dominio/aplicación (repositorios, gateways, reloj, ids, publicador de eventos).
4. **Casos de uso**: uno por acción, command/DTO de entrada, una transacción, eventos tras commit.
5. **Adaptadores**: HTTP/Inertia/CLI/colas (driving) y Eloquent/Prisma/SQLAlchemy/APIs/LLM (driven) fuera del dominio.
6. **Tests**: dominio puro → casos de uso con fakes → adaptadores con integración real → API fina → tests de arquitectura.
7. **Reglas de dependencia en CI**: deptrac / dependency-cruiser / import-linter (configs en `templates/`).

## 4. Reglas duras
- El dominio **no importa framework ni ORM**. Dependencias siempre hacia dentro (Infrastructure → Application → Domain).
- Un caso de uso = una clase/función, una transacción; los casos de uso no se llaman entre sí.
- Invariantes en el agregado; efectos secundarios via eventos tras commit; un repositorio por agregado con métodos con intención.
- Read models para leer; no hidrates agregados para listados. CRUD trivial fuera de esto.

## 5. Salida esperada
Antes del código: contexto + glosario, decisión "aplica / no aplica" (checklist), estructura elegida, casos de uso y puertos.
Después: código por capas + tests de dominio + verificación (tests y reglas de dependencia en verde). Documenta la decisión con `templates/docs/adr.md` y **declárala** en `senzu/arquitectura/capas.json` (`code-quality` → `scripts/arquitectura.mjs --plantilla hexagonal|ddd-hexagonal --stack …`): el muro arquitectura-guard hace cumplir capas y contextos en cada cambio.
La documentación va a `senzu/arquitectura/` (`adr/`, `contextos/`, `glosario/`, `event-storming/`, `context-map.md`), salvo que el
proyecto ya tenga la suya (`docs/adr`, `docs/architecture`…): entonces se usa la del proyecto.
