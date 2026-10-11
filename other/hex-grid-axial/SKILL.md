---
name: hex-grid-axial
description: >
  Sistema de coordenadas y utilidades matemáticas para grids hexagonales
  en Three.js usando coordenadas axiales (q, r). Cubre la conversión
  axial→mundo, constantes de espaciado calibradas para KayKit, cálculo
  de vecinos, generación de grids desde datos JSON, y la razón por la
  que coordenadas axiales son superiores a offset para cualquier lógica
  de pathfinding o relaciones entre celdas. Activa este skill antes de
  escribir cualquier posicionamiento de tiles hexagonales.
---

# hex-grid-axial

## Por qué coordenadas axiales, no offset

Las coordenadas offset (col, row) son intuitivas visualmente pero rotas matemáticamente:
- La vecindad de una celda tiene fórmulas distintas según si la fila es par o impar
- La distancia entre dos celdas requiere conversión intermedia
- Pathfinding con A* en offset es código propenso a bugs

Las coordenadas axiales (q, r) tienen matemática uniforme:
- Vecinos: siempre los mismos 6 deltas, sin casos especiales
- Distancia: `max(|q1-q2|, |r1-r2|, |q1+r1-q2-r2|) / 2`
- Pathfinding: A* limpio sin condicionales de paridad

**Regla:** el archivo `world.json` siempre almacena `(q, r)`. La posición 3D
se calcula siempre desde `(q, r)`. Nunca almacenar posiciones 3D en los datos.

---

## Constantes calibradas con KayKit Medieval Hexagon Pack

Estas constantes fueron medidas empíricamente con assets reales en el PoC.
No cambiarlas sin recalibrar con los assets concretos.

```js
const HEX_SIZE = 1.0;   // radio lógico del hexágono (unidad base)
const HEX_W    = 1.82;  // espaciado horizontal entre centros (medido en PoC)
const HEX_H    = 1.575; // espaciado vertical entre centros  (medido en PoC)
// HEX_W ≈ √3 × HEX_SIZE  → confirma hexágonos pointy-top
// HEX_H ≈ 1.5 × HEX_SIZE → confirma fórmula axial estándar
```

---

## Conversión axial → posición Three.js (pointy-top)

```js
// Hexágonos pointy-top (vértice arriba), que es lo que usa KayKit
function axialToWorld(q, r) {
  return new THREE.Vector3(
    HEX_W * (q + r * 0.5),  // x: desplazamiento horizontal con media celda por fila
    0,                        // y: siempre 0 en el grid base (elevación se añade aparte)
    HEX_H * r                // z: desplazamiento vertical
  );
}

// Ejemplo:
// (0,  0) → (0,     0,    0)    centro
// (1,  0) → (1.82,  0,    0)    un hex a la derecha
// (0,  1) → (0.91,  0, 1.575)   un hex abajo-derecha
// (-1, 1) → (-0.91, 0, 1.575)   un hex abajo-izquierda
```

---

## Posición con elevación (Layer 1 y Layer 2)

```js
function axialToWorldElevated(q, r, elevationY = 0) {
  const base = axialToWorld(q, r);
  base.y = elevationY;
  return base;
}

// Uso típico:
// Tile base (L0):   elevationY = 0
// Props (L1):       elevationY = 0.14  (justo encima del tile)
// Ocupantes (L2):   elevationY = 0     (algunos assets tienen su propia base)
```

---

## Los 6 vecinos en coordenadas axiales

```js
const HEX_DIRECTIONS = [
  { dq:  1, dr:  0 }, // derecha
  { dq:  1, dr: -1 }, // arriba-derecha
  { dq:  0, dr: -1 }, // arriba-izquierda
  { dq: -1, dr:  0 }, // izquierda
  { dq: -1, dr:  1 }, // abajo-izquierda
  { dq:  0, dr:  1 }, // abajo-derecha
];

function getNeighbors(q, r) {
  return HEX_DIRECTIONS.map(d => ({ q: q + d.dq, r: r + d.dr }));
}

// Sin condicionales de paridad. Funciona igual para cualquier (q, r).
```

---

## Distancia entre dos celdas

```js
function hexDistance(q1, r1, q2, r2) {
  const dq = q1 - q2;
  const dr = r1 - r2;
  return Math.max(Math.abs(dq), Math.abs(dr), Math.abs(dq + dr));
}
// Nota: en coordenadas axiales, q + r + s = 0 donde s = -(q+r)
// La distancia es (|dq| + |dr| + |ds|) / 2 = max(|dq|, |dr|, |dq+dr|)
```

---

## Generación de grid rectangular desde datos

```js
// Cargar mundo desde world.json
async function loadWorldCells(url) {
  const res  = await fetch(url);
  const data = await res.json();
  return data.cells; // array de { q, r, tileType, environment, occupant }
}

// O desde datos inlineados en el HTML
const WORLD_CELLS = [
  { q:  0, r:  0, tileType: 'grass',  environment: [], occupant: 'building_castle_green' },
  { q:  1, r:  0, tileType: 'road',   environment: [], occupant: null },
  // ...
];
```

---

## Grid rectangular procedural (para testing)

```js
function generateRectGrid(cols, rows) {
  const cells = [];
  const midQ  = Math.floor(cols / 2);
  const midR  = Math.floor(rows / 2);
  for (let r = 0; r < rows; r++) {
    for (let q = 0; q < cols; q++) {
      cells.push({ q: q - midQ, r: r - midR, tileType: 'grass', environment: [], occupant: null });
    }
  }
  return cells;
}
// generateRectGrid(5, 5) → 25 celdas centradas en (0,0)
```

---

## Conversión offset → axial (para migrar datos legacy)

```js
// Si tienes datos en coordenadas offset (col, row) con filas pares sin desplazamiento:
function offsetToAxial(col, row) {
  const q = col - Math.floor(row / 2);
  const r = row;
  return { q, r };
}
```

---

## Rotación discreta de tiles

Los hexágonos tienen simetría de orden 6. Rotar en múltiplos de 60° (π/3 radianes).

```js
function hexRotation(seed) {
  // Genera una rotación determinista basada en índice para variedad visual
  return ((seed * 7) % 6) * (Math.PI / 3);
}
// Usar: dummy.rotation.y = hexRotation(i); antes de setMatrixAt
```

---

## Referencia rápida

| Operación              | Fórmula axial                          | Complejidad |
|------------------------|----------------------------------------|-------------|
| Posición 3D            | `(HEX_W*(q+r*0.5), 0, HEX_H*r)`      | O(1)        |
| Vecinos                | `(q±dq, r±dr)` con 6 deltas fijos     | O(1)        |
| Distancia              | `max(|dq|, |dr|, |dq+dr|)`            | O(1)        |
| ¿Dentro del grid?      | lookup en Map `${q},${r}` → celda     | O(1)        |
| Ring de radio N        | 6 lados × N pasos con delta rotado    | O(N)        |
