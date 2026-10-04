---
name: dev-cycle
version: 1.1.0
type: protocol
author: Lukas Geiger
created: 2026-03-12
updated: 2026-06-13
description: "Ciclo de desarrollo de 8 fases: solicitudes de funciones, estado actual, planificación funcional, frontend, planificación de backend, código de backend, pruebas, casos de uso. Marco iterativo para el desarrollo sistemático de software."

standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: true
category: dev
tags: [development, dev-cycle, phases, workflow, systematic, iterative]
language: es
status: active
dependencies: {'tools': [], 'services': [], 'protocols': [], 'python': []}
provenance: {'origin': 'bach', 'origin_path': 'system/skills/workflows/dev-zyklus.md', 'origin_version': '1.0.0', 'origin_repo': 'github.com/ellmos-ai/bach', 'last_sync_from_origin': '2026-03-12', 'last_sync_to_origin': None, 'local_changes_since_sync': True}
---

<img src="../banner.png" width="100%" alt="dev-cycle banner">

> **Español** — Versión oficial en español de `dev-cycle`.


# Ciclo de Desarrollo (Dev Cycle) (Español)

> **Objetivo:** Proceso estructurado desde la solicitud de funciones hasta el sistema validado.
> Cada desarrollo pasa por estas 8 fases.

---

## Descripción general y propósito

```
  +--------------------------------------------------------------+
  |                    DEVELOPMENT CYCLE                         |
  +--------------------------------------------------------------+
  |                                                              |
  |  Phase 1   Feature Requests (functional requirements)        |
  |     |                                                        |
  |     v                                                        |
  |  Phase 2   Check Current State (What already exists?)        |
  |     |                                                        |
  |     v                                                        |
  |  Phase 3   Functional Planning                               |
  |            (Workflows, Agents, Experts, Skills, Services)    |
  |     |                                                        |
  |     v                                                        |
  |  Phase 4   Implement Functional Frontend                     |
  |            (Skill files, workflow markdown, agent profiles)   |
  |     |                                                        |
  |     v                                                        |
  |  Phase 5   Plan and Align Backend                            |
  |            (CLI handlers, DB schema, API endpoints)          |
  |     |                                                        |
  |     v                                                        |
  |  Phase 6   Implement Backend Tasks                           |
  |            (Python code, tools, DB migrations)               |
  |     |                                                        |
  |     v                                                        |
  |  Phase 7   Technical Tests and Bugfixes                      |
  |            (B/O/E tests, bugfix protocol)                    |
  |     |                                                        |
  |     v                                                        |
  |  Phase 8   Functional and Feature Test: USE CASES            |
  |            (End-to-end validation from user perspective)      |
  |                                                              |
  +--------------------------------------------------------------+

  Core principles throughout:
  - Functional description first (before code)
  - CLI First (everything controllable via terminal)
  - Clear separation of user data and system data
```

---

## Fase 1: Solicitudes de Funciones (Requisitos Funcionales)

**Qué:** Recopilar y formular requisitos funcionales.

**Entrada:**
- Deseos, ideas y problemas del usuario
- Sugerencias de socios (asistentes LLM)
- Perspectivas derivadas de los casos de uso (¡bucle de retroalimentación!)

**Salida:**
- Tareas en el sistema de tareas (p. ej., como issue, ticket o lista TODO)
- Los requisitos describen QUÉ se desea, no CÓMO

**Reglas:**
- Formular siempre los requisitos de forma funcional ("El usuario puede hacer X")
- No de forma técnica ("Implementar endpoint REST para X")
- Utilizar los casos de uso como fuente de requisitos (Fase 8 -> Fase 1)

---

## Fase 2: Comprobar el Estado Actual

**Qué:** Inventario de la funcionalidad existente.

**Lista de verificación:**
```
  [ ] Search existing tools/scripts
  [ ] Check documentation/help on the topic
  [ ] Check existing skills/agents/services
  [ ] Check DB schema (if relevant)
  [ ] Check use cases - has something similar been tested?
```

**Salida:**
- Documentación de lo que existe, lo que falta y lo que requiere extensión
- Prevención de duplicados

---

## Fase 3: Planificación Funcional

**Qué:** Planificar a nivel funcional — NO escribir código inmediatamente.

**Niveles de planificación:**

| Nivel | Pregunta | Artefacto |
|-------|----------|----------|
| Workflow | ¿CUÁNDO/CÓMO se realiza la coordinación? | workflows/*.md |
| Agent | ¿QUIÉN ejecuta? | agents/*.txt |
| Expert | ¿QUIÉN tiene conocimiento del dominio? | experts/*/ |
| Skill | ¿QUÉ se hace? | skills/*.md |
| Service | ¿CÓMO se hace técnicamente? | services/*/ |

**Reglas:**
- Pensar primero en lo funcional, luego en lo técnico
- Los workflows describen procesos, no detalles de implementación
- Cada agente necesita un perfil claro
- Los servicios deben funcionar sin datos de usuario

---

## Fase 4: Implementar el Frontend Funcional

**Qué:** Crear archivos de skills, markdown de workflows y perfiles de agentes.

El "frontend" aquí es la capa de descripción funcional:
- Archivos de workflow (.md)
- Perfiles de agente (.txt)
- Conocimiento de expertos
- Descripciones de servicios
- Archivos de ayuda

**Salida:**
- Todas las descripciones funcionales existen
- Un socio LLM podría leer y entender el workflow
- La capa funcional está totalmente documentada

---

## Fase 5: Planificar y Alinear el Backend

**Qué:** Alinear la arquitectura técnica con el frontend funcional.

**Áreas de planificación:**

| Área | Pregunta | Ubicación |
|------|----------|----------|
| CLI Handlers | ¿Qué comandos? | handlers/*.py |
| DB Schema | ¿Qué tablas/columnas? | schema/*.sql |
| API Endpoints | ¿Qué endpoints GUI? | server.py |
| Tools | ¿Qué scripts de Python? | tools/*.py |

**Salida:**
- Plan técnico alineado con el frontend funcional
- Diseño del esquema de la base de datos (DB schema)
- Estructura de comandos CLI

---

## Fase 6: Implementar Tareas de Backend

**Qué:** Escribir código Python, migraciones de BD y handlers de CLI.

**Lista de verificación (por tarea):**
```
  [ ] Works without user data (empty DB)?
  [ ] CLI command available?
  [ ] Input can come from files/folders?
  [ ] Output goes to structured DB?
  [ ] Scan/import is repeatable (idempotent)?
  [ ] No hardcoded path?
  [ ] Tool registered and documented?
  [ ] Help file created?
```

---

## Fase 7: Pruebas Técnicas y Corrección de Errores (Bugfixes)

**Qué:** Garantizar la corrección técnica.

**Tipos de prueba (B/O/E):**

| Tipo | Perspectiva | Descripción |
|------|-------------|-------------|
| B-Tests | Externa/Automatizada | Pruebas automatizadas, CI/CD |
| O-Tests | Funcional (Entrada->Salida) | Verificación funcional manual |
| E-Tests | Subjetiva/Experiencia | Evaluación de UX, ergonomía |

**Ante errores (bugs):**
- Aplicar el protocolo de corrección de errores (bugfix protocol)
- Observar la regla de los 20 minutos (cambiar de enfoque tras 20 min)
- Documentar las lecciones aprendidas

---

## Fase 8: Prueba Funcional y de Funcionalidades — CASOS DE USO

**Qué:** Validación de extremo a extremo (end-to-end) desde la perspectiva del usuario.

**Los casos de uso sirven para AMBOS propósitos:**
1. **Indicadores de funcionalidades** — ¿Qué se desea? ¿Qué debería ser posible?
2. **Escenarios de prueba** — ¿Funciona realmente de la A a la Z?

**Formato del caso de uso:**
```
  USECASE_NNN: Short Title

  PRECONDITION: What must be in place?
  INPUT:        What does the user enter / what data?
  EXPECTED:     What should the result be?
  TESTS:        Which components are tested?
```

**Bucle de retroalimentación (Feedback Loop):**
- Casos de uso fallidos -> nuevas tareas en la Fase 1
- Casos de uso exitosos -> funcionalidades validadas
- Nuevas ideas de casos de uso -> registrar como tareas

---

## Resumen: El Ciclo

```
  Phase 8 (Use Cases)
       |
       | New requirements / bugs
       v
  Phase 1 (Feature Requests)  -->  Phase 2 (Current State)
       ^                                    |
       |                                    v
  Phase 7 (Tests/Bugs)         Phase 3 (Functional Planning)
       ^                                    |
       |                                    v
  Phase 6 (Backend Code)       Phase 4 (Functional Frontend)
       ^                                    |
       |                                    v
       +──────────────────── Phase 5 (Backend Planning)
```

El ciclo es un bucle: Los casos de uso validan las funcionalidades y, al mismo tiempo, generan nuevos requisitos.

---

## Skills específicas por fase

| Fase | Skill especializada | Desencadenante (Trigger) |
|-------|-------------------|---------|
| Fases 1-3 | Project bootstrapper (si está disponible) | Crear un nuevo proyecto (desde cero / greenfield) |
| Fase 2 | [project-onboarding](../../project-onboarding/SKILL.en.md) | Asumir un proyecto existente |
| Fases 2-3 | [docs-analysis](../../docs-analysis/SKILL.en.md) | Verificar documentos de requisitos frente al código |
| Fases 5-6 | [pipeline-optimizer](../../pipeline-optimizer/SKILL.en.md) | Renovar estructuras existentes |
| Fase 7 | [bugfix-protocol](../../bugfix-protocol/SKILL.en.md) | Depuración sistemática en 6 fases |
| Fases 7-8 | [bugsweep](../../bugsweep/SKILL.en.md) | Barrido convergente de errores antes de un lanzamiento |

Si tu colección de skills tiene un índice de skills, búscala para obtener más skills específicas por fase.

---

## Historial de cambios

### 1.1.0 (2026-06-13)
- Nueva tabla "Skills específicas por fase" con referencias a project-onboarding, docs-analysis, pipeline-optimizer, bugfix-protocol y bugsweep

### 1.0.0 (2026-03-12)
- Adaptado desde BACH (dev-zyklus v1.0.0)

---

*Creado: 2026-01-28 | Adaptado: 2026-03-12*
