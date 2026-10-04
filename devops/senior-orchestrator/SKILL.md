---
name: senior-orchestrator
description: >
  Orquestación profesional del ecosistema — modelo routing, delegación
  de agentes, arquitectura y decisiones técnicas.
  Trigger: Cuando necesitás decidir qué modelo/tier usar, diseñar arquitectura, orquestar entre data/frontend/devops.
license: MIT
metadata:
  author: Leandro Benjamin L.
  version: "4.0"
---

# Skill: senior-orchestrator

Orquestación del ecosistema. Decidí qué agente, qué modelo, qué camino.

## Trigger

- Decidir qué modelo/tier usar para una tarea
- Diseñar arquitectura del ecosistema
- Delegar entre data-analyst, frontend-senior y devops
- Planear estrategia de modelos (local vs cloud)
- Configurar CI/CD, seguridad o infraestructura

## Model Routing (SIEMPRE antes de delegar)

Antes de spawnear cualquier sub-agente, consultá el model-router MCP
para determinar el tier óptimo:

```
1. Identificar la skill o agente que va a ejecutar
2. Llamar resolve_skill("nombre-skill") o resolve_agent("nombre-agente")
   → Devuelve tier y modelo recomendado
3. Si el tier es más caro de lo necesario para esta tarea puntual,
   ajustar manualmente con set_skill_tier() o set_agent_tier()
4. Spawnear el sub-agente con task()
5. (Opcional) resetear al default después si fue un override temporal
```

### Mapa de complejidad → tier

| Tipo de tarea | Tier | Modelo | Costo |
|--------------|------|--------|-------|
| Lectura, exploración, profiling | T1-lectura | Qwen3.6 Plus Free | gratis |
| Cotidiano, commits, ETL simple | T2-cotidiano | Big Pickle | gratis |
| Balanceado (default) | T3-balanced | MiniMax Free | gratis |
| Complejo, ML, análisis pesado | T4-complejo | DeepSeek V4 Flash | $0.14 |
| Arquitectura, diseño crítico, verify | T5-arquitectura | DeepSeek V4 Pro | $1.69 |

## Workflow LEND

1. ANALIZAR
   ├── Tipo de tarea: data, frontend, devops, o transversal
   ├── Complejidad: lectura, cotidiano, balanceado, complejo, arquitectura
   ├── Contexto: consultar Engram por decisiones previas
   ├── Consultar agent-router MCP: resolve_task() si hay duda
   └── Consultar model-router MCP: resolve_skill() para saber el tier

2. ASIGNAR MODELO (SIEMPRE)
   ├── llamar resolve_skill("skill") del model-router MCP → tier + modelo
   ├── Si el tier default no alcanza → set_skill_tier("skill", "T4-complejo")
   └── Si el tier default es caro al pedo → set_skill_tier("skill", "T2-cotidiano")

3. DELEGAR (no preguntes — ejecutá)
   ├── Data/ML/ETL → task('data-analyst', instrucciones)
   ├── Frontend/React/CSS → task('frontend-senior', instrucciones)
   ├── Infra/CI/CD/Cloud → task('devops', instrucciones)
   ├── Git/PRs/Commits → task('commits-real', instrucciones)
   ├── Memoria/Engram → task('engram-keeper', instrucciones)
   ├── SDD → task('sdd-<fase>', instrucciones)
   ├── Si hay ambigüedad → agent-router MCP resolve_task()
   └── Solo transversal: ejecutá vos mismo

4. HACER (el sub-agente ejecuta)
   ├── Pasá instrucciones claras al task()
   ├── Esperá el resultado del sub-agente
   ├── Verificá que completó lo pedido
   └── Registrá en Engram: qué se delegó, a quién, resultado, qué modelo se usó

5. ITERAR si es necesario
   ├── ¿Resultado correcto? → seguí
   ├── ¿Necesita ajustes? → re-delegá con feedback
   └── ¿Error? → diagnosticá y re-delegá

## Deep Delegation (Recursive Spawning)

**Nuevo: resolve_task_deep()** — Usá esta herramienta del agent-router MCP
para resolver tareas con árbol de delegación completo (3+ niveles de profundidad).

### Flujo de delegación profunda

```
Tarea compleja
  → resolve_task_deep("descripción", max_depth=3)
    → Devuelve árbol: agente → sub-agentes → sub-sub-agentes
  → Spawneá el agente raíz con instrucciones
    → El agente spawnea sub-agentes según la dificultad
      → Los sub-agentes spawnean más sub-agentes si es necesario
```

### Reglas de profundidad por capa

| Layer | Rol | Puede spawnear |
|-------|-----|----------------|
| 0 | Orquestador (lend-ai) | Layer 0.5: data-analyst, frontend-senior, devops |
| 0.5 | Domain supervisors | Layer 1: data-explorer, data-modeler, docker-engineer |
| 1 | Especialistas | Layer 2: data-analysis, ml-modeling, perf-engineer |
| 2+ | Deep specialists | Layer 3: data-profiling, data-validation, statistical-testing |

**Regla**: Si un agente tiene `sub_agents` en su manifest YAML y la
sub-tarea es lo suficientemente compleja → DEBE delegar. No ejecutar directamente.

## Patrones

- **Delegar siempre, preguntar solo en ambigüedad**
- **Usá siempre cuatro herramientas**: task() para sub-agentes, resolve_task() si hay duda, resolve_task_deep() para árbol completo, agent-router MCP para routing
- **Siempre delegá profundo**: si una tarea es compleja, no la resuelvas vos. Spawneá el árbol completo.
- **Nunca cambiar model-routing.config.json sin registrar en Engram**
- **Cada cambio arquitectónico requiere ADR**
- **MCPs se diagnostican antes de usar**
- **Engram siempre**: toda decisión técnica se persiste

## Anti-patrones

- ❌ Delegar sin consultar Engram primero — perdés contexto de decisiones previas
- ❌ Cambiar tiers sin registrar — nadie sabe por qué se usó T5 en una tarea simple
- ❌ No diagnosticar MCPs antes de usarlos — "esto no funciona" a mitad de camino
- ❌ Ignorar al usuario cuando es vago — preguntá hasta tener especificaciones claras
