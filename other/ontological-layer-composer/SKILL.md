---
name: ontological-layer-composer
description: >
  Sistema de composición de mundos 3D basado en capas con semántica ontológica.
  Define el contrato entre datos (registry.json, world.json) y renderer (Three.js),
  establece la gramática de 3 capas (L0 tile, L1 environment, L2 occupant) más
  contextos alternativos (ui, dungeon), y provee la lógica de validación de
  compatibilidad tile→asset. Activa este skill antes de diseñar cualquier
  sistema de composición de mundo o escribir un place() / buildWorld().
---

# ontological-layer-composer

## Principio fundamental

El mundo se describe en datos. El renderer los ejecuta. Nunca mezclarlos.

```
world.json   →  DATOS     (qué hay dónde)
registry.json →  CATÁLOGO  (qué existe y sus reglas)
WorldComposer →  ORQUESTA  (lee ambos, no decide nada)
HexGridContext → RENDERER  (solo dibuja lo que el compositor le pasa)
```

---

## Los 3 contextos espaciales

```
CONTEXTO A — Hex World      (exterior, mapa principal)
CONTEXTO B — UI / Inventario (escena separada, cámara ortográfica)
CONTEXTO C — Dungeon        (interior, unidad base = block, futuro)
```

El compositor conoce los 3. El HexGridContext solo implementa el Contexto A.
Los assets de Contexto B y C no se cargan en la escena principal.

---

## Gramática de capas (Contexto A)

```
LAYER 0 — TILE       (exactamente 1 por celda, siempre presente)
  Renderizado con InstancedMesh
  Define el tipo de celda y restringe L1 y L2

LAYER 1 — ENVIRONMENT  (0 a 3 props por celda)
  Renderizado con InstancedMesh si hay ≥5 instancias del mismo tipo
  Prohibido en celdas con Occupant
  Validado contra tileType de la celda

LAYER 2 — OCCUPANT   (0 o 1 por celda, excluyente con L1)
  Renderizado con Mesh clone (son únicos)
  Validado contra tileType de la celda
```

---

## Formato de registry.json

Cada asset tiene un ID (= stem del archivo sin extensión) y sus reglas de composición.

```json
{
  "hex_grass": {
    "layer": 0,
    "file": "hex_grass.gltf",
    "tileType": "grass",
    "allowsEnv": true,
    "allowsOccupant": true,
    "sizeKB": 95.2,
    "hasBin": true
  },
  "hex_river_A": {
    "layer": 0,
    "file": "hex_river_A.gltf",
    "tileType": "river",
    "allowsEnv": false,
    "allowsOccupant": false,
    "sizeKB": 87.1,
    "hasBin": true
  },
  "tree_A": {
    "layer": 1,
    "file": "tree_A.gltf",
    "validOn": ["grass", "dirt", "mountain"],
    "sizeKB": 112.4,
    "hasBin": true
  },
  "building_castle_green": {
    "layer": 2,
    "subtype": "building",
    "file": "building_castle_green.gltf",
    "validOn": ["grass", "dirt"],
    "sizeKB": 234.8,
    "hasBin": true
  },
  "wand_A": {
    "layer": "ui",
    "context": "ui",
    "file": "wand_A.gltf",
    "sizeKB": 45.2,
    "hasBin": true
  },
  "bricks_A": {
    "layer": "dungeon",
    "context": "dungeon",
    "file": "bricks_A.gltf",
    "sizeKB": 38.7,
    "hasBin": true
  }
}
```

---

## Formato de world.json

```json
{
  "meta": {
    "name": "Valle del Reino",
    "hexSize": 1.0,
    "hexW": 1.82,
    "hexH": 1.575
  },
  "cells": [
    {
      "q": 0, "r": 0,
      "tileType": "grass",
      "environment": ["tree_A", "rock_small"],
      "occupant": null
    },
    {
      "q": 1, "r": 0,
      "tileType": "grass",
      "environment": [],
      "occupant": "building_castle_green"
    }
  ]
}
```

**Invariantes del formato:**
- `tileType` siempre corresponde a una clave en registry con `layer: 0`
- `environment` puede estar vacío, nunca null
- `occupant` puede ser null, nunca array
- Si `occupant !== null`, entonces `environment` debe ser `[]`

---

## Matriz de compatibilidad tile → capas

| tileType | allowsEnv | allowsOccupant | Notas |
|----------|-----------|----------------|-------|
| grass    | ✔         | ✔              | El tile más permisivo |
| dirt     | ✔         | ✔              | Igual que grass |
| road     | ✗         | ✔              | Solo personajes/puentes |
| river    | ✗         | ✗              | Celda bloqueada |
| water    | ✗         | ✗              | Celda bloqueada |
| mountain | ✔         | ✗              | Solo props pequeños |
| sand     | ✔         | ✔              | Cactus, tiendas |
| snow     | ✔         | ✗              | Solo props resistentes |

---

## Función place() con validación

```js
function place(cells, registry, q, r, assetId) {
  const cell  = cells.find(c => c.q === q && c.r === r);
  const asset = registry[assetId];

  if (!cell)  throw new Error(`Celda (${q},${r}) no existe`);
  if (!asset) throw new Error(`Asset '${assetId}' no está en el registry`);

  // Validar contexto — assets de ui/dungeon no van en el hex world
  if (asset.layer === 'ui' || asset.layer === 'dungeon') {
    throw new Error(`'${assetId}' pertenece al contexto '${asset.context}', no al hex world`);
  }

  // Validar tile base para L1 y L2
  if (asset.layer === 1 || asset.layer === 2) {
    const tileEntry = registry[`hex_${cell.tileType}`] ?? registry[`hex_${cell.tileType}_A`];
    if (!asset.validOn?.includes(cell.tileType)) {
      throw new Error(`'${assetId}' no es válido sobre tileType '${cell.tileType}'`);
    }
  }

  // Aplicar reglas de exclusión L1 ↔ L2
  if (asset.layer === 2) {
    if (cell.occupant) throw new Error(`Celda (${q},${r}) ya tiene ocupante`);
    cell.environment = []; // L2 limpia L1
    cell.occupant    = assetId;
  }

  if (asset.layer === 1) {
    if (cell.occupant) throw new Error(`Celda (${q},${r}) tiene ocupante — no se puede añadir ambiente`);
    if (cell.environment.length >= 3) throw new Error(`Máximo 3 props de ambiente por celda`);
    cell.environment.push(assetId);
  }

  return cell;
}
```

---

## Interfaz pública del HexGridContext

```js
class HexGridContext {
  init(worldData, registry)   // Carga datos, prepara pools
  loadAssets()                // Descarga y cachea GLTFs necesarios
  build()                     // Construye la escena Three.js
  place(q, r, assetId)        // Valida y coloca un asset en runtime
  clear(q, r, layer)          // Limpia una capa de una celda
  getCell(q, r)               // Devuelve el modelo de celda actual
  dispose()                   // Libera GPU (geometrías, materiales, texturas)
}
```

Solo `init`, `loadAssets` y `build` son necesarios para el flujo básico.
`place` y `clear` son para interacción en runtime.
`dispose` es obligatorio si el contexto puede desmontarse (SPA, cambio de vista).

---

## Separación de responsabilidades

| Módulo            | Responsabilidad                          | No hace |
|-------------------|------------------------------------------|---------|
| registry.json     | Definir reglas de cada asset             | Posiciones, escena |
| world.json        | Describir el estado del mundo            | Lógica de render |
| WorldComposer     | Leer ambos y coordinar contextos         | Dibujar nada |
| HexGridContext    | Dibujar el Contexto A                    | Validar reglas |
| UIContext         | Dibujar el Contexto B                    | Nada del world |
| DungeonContext    | Dibujar el Contexto C (futuro)           | Nada del world |

---

## Pitfalls críticos

**1. Un asset de contexto "ui" nunca entra en la escena hex.**
El renderer del hex world no debe intentar cargar `wand_A.gltf`.
Filtrar por `registry[id].layer` antes de incluir en el set de carga.

**2. `environment: null` rompe el formato.**
Siempre inicializar como `[]`, nunca como `null`.

**3. La compatibilidad se valida en `place()`, no en el renderer.**
El renderer confía en que los datos son válidos. La validación ocurre antes de mutar world.json.

**4. El registry crece, el código no.**
Añadir packs nuevos = añadir entradas al JSON. El compositor no cambia.
Si el código necesita cambiar para soportar un asset nuevo, el diseño está roto.
