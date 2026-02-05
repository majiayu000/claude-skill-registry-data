---
name: leychile
description: Queries Chilean legislation from the Biblioteca del Congreso Nacional using SPARQL and Linked Data. Use when searching for Chilean laws, decrees, regulations, congressional information, or when user mentions specific Chilean legal codes.
---

# Ley Chile API Skill

Use this skill to query Chilean legislation from the Biblioteca del Congreso Nacional (BCN).

## Overview

This is a **free, public API** - no authentication required. It provides access to Chilean laws, decrees, regulations, legal norms, and congressional information via Linked Open Data.

## API Methods

### 1. SPARQL Endpoint (Primary)

Main data access method at `https://datos.bcn.cl/sparql`.

```bash
curl -s 'https://datos.bcn.cl/sparql' \
  --data-urlencode "query=YOUR_SPARQL_QUERY" \
  -H "Accept: application/json" \
  --max-time 30
```

### 2. Resource URIs (Direct Data Access)

Access individual resources in JSON or RDF format:

```bash
# JSON format
curl -sL "https://datos.bcn.cl/recurso/cl/ley/330/datos.json"

# RDF format
curl -sL "https://datos.bcn.cl/recurso/cl/ley/330/datos.rdf"
```

**URI Pattern:** `https://datos.bcn.cl/recurso/cl/{type}/{path}/datos.{format}`

Types include: `ley`, `dfl`, `dto`, `res`, etc.

---

## SPARQL Query Examples

### Query Norms (Laws, Decrees, etc.)

```bash
curl -s 'https://datos.bcn.cl/sparql' \
  --data-urlencode "query=
PREFIX bcnnorms: <http://datos.bcn.cl/ontologies/bcn-norms#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX dc: <http://purl.org/dc/elements/1.1/>

SELECT ?norma ?label ?title ?leychileCode
WHERE {
  ?norma a bcnnorms:Norm .
  OPTIONAL { ?norma rdfs:label ?label }
  OPTIONAL { ?norma dc:title ?title }
  OPTIONAL { ?norma bcnnorms:leychileCode ?leychileCode }
}
LIMIT 10" \
  -H "Accept: application/json"
```

### Find Law by idNorma (LeyChile Code)

```bash
curl -s 'https://datos.bcn.cl/sparql' \
  --data-urlencode "query=
PREFIX bcnnorms: <http://datos.bcn.cl/ontologies/bcn-norms#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT ?norma ?label
WHERE {
  ?norma a bcnnorms:Norm .
  ?norma bcnnorms:leychileCode ?code .
  FILTER(?code = 172986)
  OPTIONAL { ?norma rdfs:label ?label }
}
LIMIT 5" \
  -H "Accept: application/json"
```

### Search Law Projects (Bills)

```bash
curl -s 'https://datos.bcn.cl/sparql' \
  --data-urlencode "query=
PREFIX bcn: <http://datos.bcn.cl/ontologies/bcn-resources#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT ?proyecto ?label
WHERE {
  ?proyecto a bcn:ProyectoDeLey .
  OPTIONAL { ?proyecto rdfs:label ?label }
}
LIMIT 10" \
  -H "Accept: application/json"
```

### Get Parliamentary Sessions

```bash
curl -s 'https://datos.bcn.cl/sparql' \
  --data-urlencode "query=
PREFIX congress: <http://datos.bcn.cl/ontologies/bcn-congress#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT ?sesion ?label
WHERE {
  ?sesion a congress:SesionParlamentaria .
  OPTIONAL { ?sesion rdfs:label ?label }
}
LIMIT 10" \
  -H "Accept: application/json"
```

### List Available Entity Types

```bash
curl -s 'https://datos.bcn.cl/sparql' \
  --data-urlencode "query=SELECT DISTINCT ?type WHERE { ?s a ?type . FILTER(CONTAINS(STR(?type), 'bcn')) } LIMIT 100" \
  -H "Accept: application/json"
```

---

## Ontologies/Namespaces

| Prefix | Namespace | Description |
|--------|-----------|-------------|
| bcn-norms | `http://datos.bcn.cl/ontologies/bcn-norms#` | **Norms** (Norm, leychileCode, publishDate) |
| bcn-resources | `http://datos.bcn.cl/ontologies/bcn-resources#` | Legislative resources (ProyectoDeLey, Articulo) |
| bcn-congress | `http://datos.bcn.cl/ontologies/bcn-congress#` | Congressional entities (SesionParlamentaria) |
| bcn-biographies | `http://datos.bcn.cl/ontologies/bcn-biographies#` | Biographies (Senador, Diputado) |
| dc | `http://purl.org/dc/elements/1.1/` | Dublin Core (title, language) |
| rdfs | `http://www.w3.org/2000/01/rdf-schema#` | RDF Schema (label) |

## Key Properties (bcn-norms)

| Property | Description |
|----------|-------------|
| `bcnnorms:leychileCode` | The idNorma used in LeyChile URLs |
| `bcnnorms:publishDate` | Publication date |
| `bcnnorms:promulgationDate` | Promulgation date |
| `bcnnorms:hasNumber` | Law/decree number |
| `bcnnorms:createdBy` | Issuing ministry/organism |
| `bcnnorms:hasHtmlDocument` | Link to LeyChile HTML page |

---

## Common Law IDs (leychileCode / idNorma)

| Law | idNorma | URI Path |
|-----|---------|----------|
| Constitucion | 242302 | - |
| Codigo Civil | 172986 | `/cl/dfl/ministerio-de-justicia/2000-05-30/1` |
| Codigo Penal | 1984 | - |
| Codigo del Trabajo | 207436 | - |
| Ley de Proteccion de Datos (19.628) | 141599 | - |

---

## Web Navigation (Human Browsing)

For viewing laws in a browser:
```
https://www.bcn.cl/leychile/navegar?idNorma={ID_NORMA}
```

Historical version:
```
https://www.bcn.cl/leychile/navegar?idNorma={ID_NORMA}&idVersion={YYYY-MM-DD}
```

> **Note:** These pages are JavaScript-rendered. Use SPARQL or Resource URIs for programmatic access.

---

## Performance Notes

- Use `--max-time 30` with curl for safety
- Queries for `ProyectoDeLey` and `SesionParlamentaria` are fast
- Queries with `FILTER` on text can be slow
- Use `STR(?variable)` instead of `LCASE(?variable)` in FILTER to avoid type errors

---

## Response Format

### SPARQL JSON Response
```json
{
  "head": { "vars": ["norma", "label"] },
  "results": {
    "bindings": [
      {
        "norma": { "type": "uri", "value": "http://datos.bcn.cl/recurso/..." },
        "label": { "type": "literal", "value": "Ley 330" }
      }
    ]
  }
}
```

### Resource URI JSON Response
```json
{
  "http://datos.bcn.cl/recurso/cl/ley/.../330/es@1896-01-29": {
    "http://www.w3.org/1999/02/22-rdf-syntax-ns#type": [...],
    "http://www.w3.org/2000/01/rdf-schema#label": [...],
    "http://datos.bcn.cl/ontologies/bcn-norms#leychileCode": [
      { "type": "literal", "value": 22181 }
    ]
  }
}
```

---

## Deprecated/Unavailable APIs

### Ley Facil API (401 Unauthorized as of Dec 2025)
```bash
# NO LONGER WORKS
curl -s "https://www.bcn.cl/leyfacil/recurso/trabajo"
```

### XML Export API (401 Unauthorized)
```bash
# NO LONGER WORKS
curl -s "https://www.leychile.cl/Consulta/obtxml?opt=7&idNorma=172986"
```

---

## References

- Open Data Portal: https://datos.bcn.cl/es/
- SPARQL Endpoint: https://datos.bcn.cl/sparql
- URI Documentation: https://datos.bcn.cl/es/informacion/documentacion/tipos-de-uri
- SPARQL Examples: https://datos.bcn.cl/es/informacion/documentacion/consultas-sparql
- Main Portal: https://www.bcn.cl/leychile/
- API Spec Page: https://www.bcn.cl/leychile/consulta/legislacion_abierta_web_service
