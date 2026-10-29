---
name: Review Changes
description: Perform a structured code review using change detection and impact
---

## Review Changes

Perform a thorough, risk-aware code review using the codebase-memory-mcp knowledge graph (project `C-Marcos-Proyectos-Zenda`).

### Steps

1. `detect_changes(base_branch="main")` (o `since="<ref>"`) para obtener el análisis de cambios con impacto.
2. Para cada función/archivo de alto riesgo, `trace_path(function_name=..., mode="calls", direction="inbound", risk_labels=true)` para ver qué se rompe si falla.
3. `search_graph(query="<nombre de la función>", label="Function")` seguido de `query_graph` con patrón `tests_for`-like (busca archivos `.spec.ts` que importan/llaman al símbolo) para verificar cobertura de tests.
4. `get_code_snippet(qualified_name=..., include_neighbors=true)` para leer el cambio en contexto cuando el diff crudo no basta.
5. Para cambios sin test, señala casos de prueba concretos a escribir.

### Output Format

Agrupa los hallazgos por nivel de riesgo (alto/medio/bajo) con:
- Qué cambió y por qué importa
- Estado de cobertura de tests
- Mejoras sugeridas
- Recomendación general de merge

## Reglas de eficiencia de tokens

- Empieza siempre con `detect_changes` (una sola llamada resume todo el diff con riesgo).
- Solo pide `get_code_snippet` de las funciones de riesgo alto/medio, no de todo el diff.
- Objetivo: completar la review en ≤5 llamadas a herramientas de grafo.
