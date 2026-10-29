---
name: Explore Codebase
description: Navigate and understand codebase structure using the knowledge graph
---

## Explore Codebase

Use the codebase-memory-mcp knowledge graph (project `C-Marcos-Proyectos-Zenda`) to explore and understand the codebase.

### Steps

1. `get_architecture(aspects=["all"])` para una vista de alto nivel: paquetes, servicios, dependencias y los clusters reales del grafo (comunidades Leiden, no solo la estructura de carpetas).
2. `search_graph(query="<tema>", label="Function"|"Class"|"Route")` para encontrar funciones, clases o rutas concretas por lenguaje natural.
3. `search_graph(name_pattern=".*regex.*")` cuando ya sabes el patrón de nombre exacto.
4. `trace_path(function_name=..., mode="calls"|"cross_service")` para relaciones entre módulos (incluye llamadas HTTP/async entre verticales).
5. `search_code(pattern=..., mode="compact")` como grep aumentado con el grafo cuando necesitas texto crudo con contexto de función.

### Tips

- Empieza amplio (`get_architecture`) y luego acota con `search_graph`.
- `search_graph` con `semantic_query=["palabra1","palabra2"]` encuentra código relacionado aunque no comparta vocabulario literal.
- Usa `min_degree`/`max_degree` en `search_graph` para filtrar nodos muy conectados (hubs) o muy aislados.

## Reglas de eficiencia de tokens

- Empieza con `get_architecture` (una sola llamada) antes de explorar nodo por nodo.
- Usa `mode="compact"` en `search_code` salvo que necesites el código fuente completo.
- Objetivo: mapear la zona relevante del código en ≤5 llamadas a herramientas de grafo.
