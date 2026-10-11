---
name: gltf-instanced-world
description: >
  Patrón completo para cargar assets GLTF en un mundo tile-based con Three.js,
  usando InstancedMesh para objetos repetidos (Layer 0 y Layer 1) y Mesh clone
  para ocupantes únicos (Layer 2). Cubre cache-first loading, extracción de
  geometría/material desde sub-meshes de GLTF, construcción de InstancedMesh,
  propagación de userData para raycasting, y medición de peso real de carga.
  Activa este skill antes de escribir cualquier GLTFLoader o InstancedMesh.
---

# gltf-instanced-world

## Principio fundamental

Un mundo tile-based tiene dos clases de objetos:
- **Repetidos** (tiles del suelo, props de ambiente): InstancedMesh → 1 draw call por tipo
- **Únicos** (edificios, personajes): Mesh clone → 1 draw call por instancia

La decisión InstancedMesh vs Mesh clone no es estética — es aritmética de draw calls.
Con 200 tiles de hierba y 3 tipos de tile: 3 draw calls con InstancedMesh, 200 sin él.

---

## Paso 1 — Cache-first loading

Nunca cargues el mismo archivo dos veces. Deduplica el set de archivos necesarios
antes de lanzar las peticiones.

```js
const loader = new GLTFLoader();
const cache  = new Map(); // filename → gltf

async function loadAssets(worldCells, tileFiles) {
  // Derivar set mínimo de archivos desde los datos del mundo
  const needed = new Set();
  worldCells.forEach(cell => {
    needed.add(tileFiles[cell.tileType]);
    if (cell.occupant)    needed.add(cell.occupant + '.gltf');
    cell.environment?.forEach(id => needed.add(id + '.gltf'));
  });

  // Carga en paralelo — Promise.allSettled nunca interrumpe por un fallo individual
  await Promise.allSettled(
    [...needed].map(file =>
      new Promise(res =>
        loader.load(
          file,
          gltf => { cache.set(file, gltf); res(); },
          undefined,
          err  => { console.warn('[skip]', file, err.message); res(); }
          // res() siempre, incluso en error — el mundo carga sin ese asset
        )
      )
    )
  );

  return cache;
}
```

---

## Paso 2 — Extracción de geometría y material

Los GLTF de KayKit tienen 1 sub-mesh por tile hex (confirmado en PoC).
Para assets con múltiples sub-meshes, crea un InstancedMesh por sub-mesh.

```js
function extractMeshes(gltf) {
  const meshes = [];
  gltf.scene.traverse(child => {
    if (child.isMesh) meshes.push(child);
  });
  if (!meshes.length) throw new Error('0 meshes en la escena GLTF');
  return meshes;
}
```

---

## Paso 3 — Construir InstancedMesh (Layer 0 y Layer 1)

```js
function buildInstancedLayer(gltf, positions, assetKey) {
  const srcMeshes = extractMeshes(gltf);
  const group     = new THREE.Group();
  const dummy     = new THREE.Object3D();

  srcMeshes.forEach(src => {
    const inst = new THREE.InstancedMesh(
      src.geometry,            // NO clonar — compartir la misma geometría
      src.material,            // NO clonar — compartir el mismo material
      positions.length
    );
    inst.userData.assetKey = assetKey; // para raycasting
    inst.castShadow    = true;
    inst.receiveShadow = true;

    positions.forEach((pos, i) => {
      dummy.position.copy(pos);
      dummy.rotation.y = ((i * 7) % 6) * (Math.PI / 3); // rotación hex discreta
      dummy.updateMatrix();
      inst.setMatrixAt(i, dummy.matrix);
    });

    inst.instanceMatrix.needsUpdate = true; // OBLIGATORIO después de setMatrixAt
    group.add(inst);
  });

  return group;
}
```

### Por qué no clonar geometría ni material en InstancedMesh

Clonar crea buffers duplicados en GPU. InstancedMesh está diseñado para compartirlos.
Solo clona si necesitas modificar la geometría de una instancia concreta (raro).

---

## Paso 4 — Mesh clone para ocupantes únicos (Layer 2)

```js
function placeOccupant(gltf, position, assetKey) {
  const obj = gltf.scene.clone(true); // true = deep clone con materiales
  obj.position.copy(position);

  // Propagar assetKey a TODOS los nodos del árbol
  // El raycaster puede impactar cualquier hijo — todos deben tener la clave
  obj.traverse(node => {
    node.userData.assetKey = assetKey;
  });

  return obj;
}
```

---

## Paso 5 — Raycasting con InstancedMesh y Mesh clone

```js
function handleClick(event, camera, scene) {
  const mouse = new THREE.Vector2(
    (event.clientX / innerWidth)  * 2 - 1,
    -(event.clientY / innerHeight) * 2 + 1
  );
  raycaster.setFromCamera(mouse, camera);

  const intersects = raycaster.intersectObjects(scene.children, true);
  if (!intersects.length) return null;

  let node = intersects[0].object;

  // Caso InstancedMesh: el objeto ES el nodo con assetKey
  // Caso Mesh clone: puede ser un hijo — subimos hasta encontrar assetKey
  while (node && node.parent && !node.userData.assetKey) {
    node = node.parent;
  }

  return node?.userData?.assetKey ?? null;
}
```

---

## Medición de peso real de carga

Para GLTF partidos en `.gltf` + `.bin`, medir ambos archivos.
El `.gltf` es JSON liviano; el `.bin` es el volumen real de datos geométricos.

```js
async function measureAssetWeight(gltfPath, binPath) {
  try {
    const [gRes, bRes] = await Promise.all([fetch(gltfPath), fetch(binPath)]);
    const [gBuf, bBuf] = await Promise.all([gRes.arrayBuffer(), bRes.arrayBuffer()]);
    return {
      gltfKB: (gBuf.byteLength / 1024).toFixed(1),
      binKB:  (bBuf.byteLength / 1024).toFixed(1),
      totalKB: ((gBuf.byteLength + bBuf.byteLength) / 1024).toFixed(1),
    };
  } catch (e) {
    return { gltfKB: 0, binKB: 0, totalKB: 0 };
  }
}
```

---

## Umbrales de referencia (calibrados con KayKit Medieval Hexagon Pack)

| Asset tipo        | Peso típico .gltf+.bin | Sub-meshes | Draw calls con instancing |
|-------------------|------------------------|------------|--------------------------|
| Hex tile (L0)     | 80-150 KB              | 1          | 1 por tipo de tile        |
| Prop ambiente (L1)| 50-200 KB              | 1-3        | 1-3 por tipo de prop      |
| Building (L2)     | 150-400 KB             | 2-6        | 1 por building único      |

---

## Pitfalls críticos

**1. `instanceMatrix.needsUpdate = true` es obligatorio.**
Sin esta línea, Three.js no sube la matriz al shader y todos los objetos aparecen en (0,0,0).

**2. No usar `Object.assign` para setear propiedades de Three.js.**
`position`, `rotation`, `scale` son getters en Object3D. Asignar con `set()` o `.copy()`.

**3. Promise.allSettled, no Promise.all.**
Un asset roto no debe tumbar el mundo entero. Con `allSettled`, el mundo carga sin ese archivo.

**4. Propagar userData.assetKey por traverse en clones.**
Si no lo haces, el raycaster impacta un hijo sin clave y el click no registra nada.

**5. No medir solo el .gltf.**
El `.gltf` JSON pesa pocos KB. El `.bin` es el 90% del peso real. Medir ambos.
