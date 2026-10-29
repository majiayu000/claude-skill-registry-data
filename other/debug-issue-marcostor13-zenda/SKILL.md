---
name: Debug Issue
description: Systematically debug issues using graph-powered code navigation
---

## Debug Issue

Use the codebase-memory-mcp knowledge graph (project `C-Marcos-Proyectos-Zenda`) to systematically trace and debug issues.

### Steps

1. `search_graph(query="<síntoma o nombre de función/ruta>")` para ubicar el código relacionado.
2. `trace_path(function_name=..., mode="calls")` para ver quién llama y a quién llama la función sospechosa.
3. `trace_path(function_name=..., mode="data_flow")` si el bug es de propagación de un valor/argumento concreto.
4. `detect_changes(since="HEAD~5")` (o el ref relevante) para ver si un cambio reciente causó el bug.
5. `get_code_snippet(qualified_name=...)` para leer el código exacto una vez localizado (usa el `qualified_name` devuelto por `search_graph`, no adivines la ruta).

### Tips

- Revisa tanto callers como callees para entender el contexto completo.
- Los cambios recientes (`detect_changes`) son la causa más común de bugs nuevos.
- Usa `query_graph` con Cypher para patrones multi-hop que `trace_path` no cubre (p.ej. cruzar por rutas HTTP).

## Reglas de eficiencia de tokens

- Empieza siempre con `search_graph` acotado (usa `label`, `file_pattern` o `limit` bajo) antes de `query_graph` libre.
- Pide `get_code_snippet` solo del símbolo exacto que necesitas, no de archivos completos.
- Objetivo: resolver el debug en ≤5 llamadas a herramientas de grafo.
