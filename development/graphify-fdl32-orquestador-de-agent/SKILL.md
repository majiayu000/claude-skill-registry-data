---
name: graphify
version: 2.0.0
description: Construye un grafo de conocimiento persistente del codebase para explorarlo con poco consumo de tokens. Usar cuando el proyecto supera 30 ficheros fuente o 5.000 palabras, o es la segunda sesion sobre el mismo codigo. No usar para proyectos pequenos donde leer los ficheros sale mas barato; si el grafo ya existe, actualizalo con --update en vez de reconstruirlo.
triggers: [/graphify, graph, map]
author: agent
role: shared
stage: support
cycle_phase: [F5-implementacion]
writes_memory: false
quality_gate: false
tags: [core, system]
---

# graphify

Transforma un codebase en un grafo de conocimiento persistente. Permite explorar arquitectura y relaciones entre módulos sin leer archivos crudos en cada sesión. Reducción típica: **70x menos tokens** por consulta en corpus > 30 archivos.

## Cuándo activar

El Builder DEBE activar esta skill antes de explorar el codebase cuando:
- El proyecto tiene **> 30 archivos** fuente, o
- El corpus total supera **5.000 palabras**, o
- Es la **segunda sesión** sobre el mismo proyecto

Si el grafo ya existe (`graphify-out/graph.json`), usar `--update` en vez de reconstruirlo.

## Workflow

### Paso 1: Comprobar si existe grafo previo

```bash
ls graphify-out/graph.json 2>/dev/null && echo "EXISTE" || echo "NUEVO"
```

- Si **EXISTE** → ir a Paso 3 (update)
- Si **NUEVO** → continuar con Paso 2

### Paso 2: Construir grafo inicial

Escanear el directorio objetivo y estimar el corpus (elige el shell disponible):

```powershell
# PowerShell (runtime canonico en Windows)
(Get-ChildItem src -Recurse -Include *.py, *.md -File).Count
(Get-ChildItem src -Recurse -Include *.py -File | Get-Content | Measure-Object -Word).Words
```

```bash
# bash (Linux/macOS)
find src/ -type f \( -name "*.py" -o -name "*.md" \) | wc -l
find src/ -type f -name "*.py" -exec wc -w {} + | tail -1
```

Luego lanzar extracción en paralelo. Dividir los archivos en lotes de 20-25 y despachar todos los subagentes en **un solo mensaje** (máxima paralelización):

**Instrucción para cada subagente:**
```
Extrae entidades y relaciones del siguiente lote de archivos.
Para cada archivo:
1. Identifica: clases, funciones, módulos, conceptos clave
2. Identifica relaciones: imports, llamadas, herencias, dependencias
3. Marca cada relación con confianza:
   - EXTRACTED (1.0): explícita en código (import, class X(Y))
   - INFERRED (0.4-0.9): implícita pero probable (mismo módulo, patrón similar)
   - AMBIGUOUS (0.1-0.3): posible pero incierta
4. Preserva: autor, source_url si hay YAML frontmatter

Formato de salida JSON:
{
  "nodes": [{"id": "nombre", "type": "class|function|module|concept", "file": "ruta"}],
  "edges": [{"from": "A", "to": "B", "type": "imports|calls|extends|uses", "confidence": 1.0, "tag": "EXTRACTED"}]
}
```

Para archivos de código (.py, .js, etc.) usar análisis AST determinístico:
```bash
python -c "
import ast, json, sys
tree = ast.parse(open(sys.argv[1]).read())
# Extraer imports, clases, funciones sin usar LLM
"
```

### Paso 3: Actualizar grafo existente

```bash
# Solo procesar archivos modificados desde última actualización
find src/ -newer graphify-out/graph.json -type f
```

Procesar únicamente los archivos nuevos/modificados y hacer merge con el grafo existente.

### Paso 4: Persistir resultado

Guardar en `graphify-out/graph.json`:
```json
{
  "generated": "ISO-8601 timestamp",
  "corpus": {"files": 0, "words": 0},
  "nodes": [],
  "edges": [],
  "communities": {}
}
```

Guardar también `graphify-out/GRAPH_REPORT.md` con:
- Nodos de alto grado (god nodes / módulos centrales)
- Conexiones sorprendentes entre módulos
- Comunidades detectadas (clusters de funcionalidad)
- Coste de construcción (tokens usados)

### Paso 5: Consultar el grafo

En vez de leer archivos, usar consultas sobre el grafo:

```
query "¿dónde se valida X?"        → BFS desde nodo X, profundidad 2
path "A" → "B"                     → camino más corto entre dos módulos
explain "NombreClase"              → todos los nodos conectados a NombreClase
community "autenticación"          → cluster completo de módulos relacionados
```

Traducción a operaciones sobre graph.json (stdlib puro, sin dependencias).
Formato real del artefacto: `{"nodes": {ruta: metadata}, "edges": [{"source", "target", "type"}]}`.

```python
import json
from collections import defaultdict, deque

data = json.load(open("graphify-out/graph.json", encoding="utf-8"))
adj = defaultdict(set)
for edge in data["edges"]:
    adj[edge["source"]].add(edge["target"])
    adj[edge["target"]].add(edge["source"])

# BFS query (vecindario a profundidad 2)
def bfs(start, depth_limit=2):
    seen, frontier = {start}, deque([(start, 0)])
    while frontier:
        node, depth = frontier.popleft()
        if depth == depth_limit:
            continue
        for nxt in adj[node] - seen:
            seen.add(nxt)
            frontier.append((nxt, depth + 1))
    return seen

# Shortest path
def shortest_path(a, b):
    prev, frontier, seen = {a: None}, deque([a]), {a}
    while frontier:
        node = frontier.popleft()
        if node == b:
            path = []
            while node is not None:
                path.append(node)
                node = prev[node]
            return path[::-1]
        for nxt in adj[node] - seen:
            seen.add(nxt)
            prev[nxt] = node
            frontier.append(nxt)
    return None
```

## Output

```
graphify-out/
├── graph.json          # Grafo persistente (fuente de verdad)
├── GRAPH_REPORT.md     # Informe: god nodes, conexiones, comunidades
└── cache/              # SHA256 por archivo (detección de cambios)
```

## Integración con el flujo Manager → Builder

El Builder ejecuta graphify al inicio de la fase IMPLEMENT cuando el corpus es grande:

```markdown
## Inicio de sesión Builder (proyecto grande)

1. Leer PROJECT.md
2. Comprobar graphify-out/graph.json
   - Si existe y < 7 días: usar directamente
   - Si no existe o > 7 días: ejecutar `/graphify src/ --update`
3. Consultar grafo para entender arquitectura antes de tocar código
4. Implementar según work_plan.md
```

## Constraints

- **NUNCA** inventar edges — relaciones inciertas se marcan AMBIGUOUS, no se omiten ni inventan
- **SIEMPRE** reportar coste de tokens de construcción en GRAPH_REPORT.md
- **NO** reconstruir si `graph.json` existe y el corpus no ha cambiado (usar `--update`)
- Para corpus > 200 archivos o > 2M palabras, advertir y sugerir limitar el scope (`src/` en vez de raíz)
- **NO** activar en proyectos pequeños (< 30 archivos): el overhead de construcción supera el beneficio

## References

- `references/graph-query-patterns.md` - Patrones de consulta sobre NetworkX
- `references/ast-extraction.md` - Extracción AST sin LLM para código Python
