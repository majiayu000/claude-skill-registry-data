---
name: lend-ai-delegation
description: >
  Reglas de delegación del ecosistema — árbol de decisión, triggers
  de delegación automática y mecanismo con task() + agent-router MCP.
  Trigger: Cuando necesitás decidir a qué sub-agente delegar una tarea.
license: MIT
metadata:
  author: Leandro Benjamin L.
  version: "1.0"
---

# LEND.AI — Delegation Protocol

Regla de oro: Si matchea dominio, DELEGÁ. No ejecutes vos.
Regla de oro 2: TODO agente con sub_agents DEBE delegar tareas complejas a sus sub-agentes.
Regla de oro 3: Los sub-agentes también tienen sub-agentes — la delegación es RECURSIVA.

## Recursive Spawning (Deep Delegation)

Cada agente en el ecosistema puede spawnear sub-agentes, y esos sub-agentes
pueden spawnear los suyos, formando un árbol de delegación de hasta N niveles.

**Regla de profundidad:** Si una tarea es compleja, NO la resuelvas entera.
Dividila en sub-tareas y delegá cada una a un sub-agente especializado.

```
Ejemplo: una tarea de ML se descompone en:
lend-ai → data-analyst → data-modeler → ml-modeling → data-validation
  Layer 0    Layer 0.5       Layer 1       Layer 2        Layer 3
```

**Cuándo spawnear más profundo:**
- Dataset nuevo (>10K filas) → spawn data-profiling
- Feature engineering complejo → spawn ml-modeling
- Reporte/dashboard → spawn data-reporter → data-visualization
- Necesitás contenedor Docker → spawn docker-engineer → perf-engineer
- Componente UI complejo → spawn ui-crafter → frontend-react-development
- Pipeline CI/CD → spawn ci-cd-pilot → gitops-engineer

**Detección de dificultad (qué tan profundo ir):**
1. **T1 (simple)**: Resolvelo vos mismo. No spawnees.
2. **T2 (medio)**: Spawneá 1 sub-agente directo.
3. **T3 (complejo)**: Spawneá el mejor agente, que a su vez spawnea sub-agentes.
4. **T4+ (crítico)**: Spawneá árbol completo de 3+ niveles. Usá resolve_task_deep() del agent-router MCP para obtener el árbol completo.

## Árbol de Delegación

| Dominio | Sub-agente | task() call |
|---------|-----------|-------------|
| Data/ML/ETL/EDA/Reportes | data-analyst | `task('data-analyst', '...')` |
| Frontend/React/CSS/UX/TS | frontend-senior | `task('frontend-senior', '...')` |
| Infra/CI/CD/Docker/Cloud/Seguridad | devops | `task('devops', '...')` |
| Git/PRs/Commits/Issues | commits-real | `task('commits-real', '...')` |
| Memoria/Engram | engram-keeper | `task('engram-keeper', '...')` |
| Testing/Calidad | lend-ai-testing | `task('lend-ai-testing', '...')` |
| Docs/Documentación | lend-ai-docs | `task('lend-ai-docs', '...')` |
| Auto-mejora/Patrones | growth-engine | `task('growth-engine', '...')` |
| Mejora paralela (10 perspectivas) | enhance-engine | `task('enhance-engine', '...')` |
| Contenido/LinkedIn | content-engine | `task('content-engine', '...')` |
| SDD (cualquier fase) | sdd-init..sdd-archive | `task('sdd-<fase>', '...')` |
| Revisión adversarial | judgment-day | `task('judgment-day', '...')` |
| PRs encadenados (>400 líneas) | chained-pr | `task('chained-pr', '...')` |
| Creación de issues | issue-creation | `task('issue-creation', '...')` |
| Branch + PR workflow | branch-pr | `task('branch-pr', '...')` |

## Triggers de Delegación Automática

No preguntes — delegá directamente cuando:

1. **4-file rule**: la tarea requiere leer 4+ archivos → delegá exploración
2. **Multi-file write**: tocar 2+ archivos → delegá writer
3. **Pre-commit/PR**: antes de commit o PR tras cambios → delegá review fresco
4. **Error de entorno**: error de MCP o dependencia → delegá auditoría
5. **Long-session**: ~20 tool calls sin delegar → delegá a growth-engine
6. **Fresh review**: revisión adversarial → judgment-day

## Mecanismo

- Usá `task('agent-name', instructions)` para spawnear sub-agentes
- Pasá instrucciones claras: qué hacer, archivos involucrados, contexto relevante
- Si no sabés qué agente: llamá `resolve_task(descripción)` del MCP agent-router
- Esperá el resultado del sub-agente antes de continuar
- Nunca ejecutes trabajo de dominio directamente

## Post-delegación

- Recibí el resultado del sub-agente
- Verificá que completó lo pedido
- Guardá en Engram: qué se delegó, a quién, resultado
- Si el resultado necesita iteración, re-delegá

### Plugin Integration

| Plugin | Rol en Deep Delegation |
|--------|----------------------|
| opencode-subagent-statusline | Muestra el árbol jerárquico de sub-agentes activos (lend-ai » data-analyst » data-explorer) |
| opencode-dynamic-context-pruning | Poda contexto automáticamente después de cada nivel de delegación para mantener el budget de tokens |
| opencode-vibeguard | Warnnea si una cadena de delegación supera los 3-4 niveles de profundidad |
| opencode-sdd-engram-manage | Registra cada decisión de profundidad en Engram para trazabilidad |
| model-switcher-plugin (local) | Auto-asigna tiers según profundidad: nivel 1=T4, nivel 2=T3, nivel 3=T2, nivel 4+=T1 |

- **opencode-subagent-statusline**: Renderiza el árbol de delegación activo en la línea de estado, mostrando la jerarquía completa de sub-agentes en ejecución.
- **opencode-dynamic-context-pruning**: Después de cada nivel de delegación, elimina contexto innecesario para evitar saturar el budget de tokens en cadenas profundas.
- **opencode-vibeguard**: Monitorea la profundidad de la cadena de delegación y emite una advertencia si se exceden los límites recomendados (3-4 niveles).
- **opencode-sdd-engram-manage**: Persiste cada decisión de spawn y profundidad en Engram, permitiendo trazabilidad completa de las cadenas de delegación.
- **model-switcher-plugin (local)**: Asigna dinámicamente el tier del modelo según la profundidad actual de la delegación, optimizando costo y capacidad.
