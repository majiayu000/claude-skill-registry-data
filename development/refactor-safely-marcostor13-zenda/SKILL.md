---
name: Refactor Safely
description: Plan and execute safe refactoring using dependency analysis
---

## Refactor Safely

Use the codebase-memory-mcp knowledge graph (project `C-Marcos-Proyectos-Zenda`) to plan and execute refactoring with confidence.

### Steps

1. `search_graph(name_pattern=...)` o `search_graph(query=...)` para localizar el símbolo a refactorizar y su `qualified_name`.
2. `trace_path(function_name=..., mode="calls", direction="inbound", risk_labels=true)` para ver TODO lo que depende de él (callers directos e indirectos) y su nivel de riesgo por distancia.
3. `query_graph(query="MATCH (f:Function)-[:CALLS]->(t) WHERE t.qualified_name = '<qn>' RETURN f.qualified_name")` para un listado preciso de sitios a tocar en un rename/cambio de firma.
4. Antes de aplicar cambios grandes, revisa `query_graph` con `transitive_loop_depth`/`linear_scan_in_loop` si el refactor toca código en un hot path.
5. Después del cambio, corre `detect_changes(base_branch="main")` para verificar el impacto real contra lo planeado.

### Safety Checks

- Nunca asumas el `qualified_name` — siempre confírmalo con `search_graph` primero (`get_code_snippet` sugiere alternativas si es ambiguo).
- Revisa callers inbound antes de cambiar una firma pública.
- Corre `detect_changes` después del refactor para confirmar que el radio de impacto coincide con lo esperado.

## Reglas de eficiencia de tokens

- Usa `depth` bajo (2-3) en `trace_path` salvo que el grafo confirme que necesitas más saltos.
- En `query_graph`, añade `LIMIT` explícito en el Cypher para no traer resultados masivos.
- Objetivo: planear el refactor en ≤5 llamadas a herramientas de grafo.
