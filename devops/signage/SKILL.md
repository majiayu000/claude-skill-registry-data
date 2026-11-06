---
name: signage
description: Create realistic signage, markings, labels and decals for futuristic Three.js WebGPU environments such as trains, stations, roads, buildings, habitats and industrial infrastructure.
---

# Signage

Target: Three.js 0.187.0, WebGPU renderer (`three/webgpu`) and TSL node materials (`three/tsl`); WebGPU only, no WebGL fallback, no GLSL strings.

Prefer texture-based decals or dedicated sign geometry for most signage. Do not create individual 3D letters for every ordinary sign unless the letters are physically raised, illuminated or close enough to justify geometry.

## Choose the representation

Use a decal/texture when:

- the sign is essentially printed
- it is flat
- it is numerous
- it is viewed at medium/far distance
- the lettering does not need physical relief
- the sign needs many text variants

Use actual geometry when:

- letters are raised
- letters are illuminated
- the sign has substantial thickness
- it is a hero object
- side visibility matters
- shadows from the lettering matter

For flat signage, a small dedicated sign plane or decal-style mesh is often preferable to TextGeometry.

Three.js provides DecalGeometry for projecting detail onto meshes, but projections can distort around corners. Avoid projecting across sharp/complex curvature when accuracy matters.

## Texture approach

For a sign texture:

- keep text crisp
- use correct colour space
- use sufficient resolution for viewing distance
- use alpha only when necessary
- keep the sign substrate separate from lettering when material response differs
- avoid enormous unique textures for tiny signs

A sign face drawn to a canvas, on a thin board with real thickness:

```js
import * as THREE from 'three/webgpu';
import { texture, uv } from 'three/tsl';

export function createSign(text, { w = 1.2, h = 0.3, px = 512, lit = false } = {}) {
  const c = Object.assign(document.createElement('canvas'), { width: px, height: Math.round(px * h / w) });
  const g = c.getContext('2d');
  g.fillStyle = '#1d2329'; g.fillRect(0, 0, c.width, c.height);
  g.fillStyle = '#f2f2ee'; g.font = `600 ${c.height * 0.55}px sans-serif`;
  g.textAlign = 'center'; g.textBaseline = 'middle'; g.fillText(text, c.width / 2, c.height / 2);
  const map = new THREE.CanvasTexture(c);
  map.colorSpace = THREE.SRGBColorSpace; map.anisotropy = 8;
  const face = new THREE.MeshStandardNodeMaterial({ roughness: 0.6, metalness: 0 });
  face.colorNode = texture(map, uv());
  if (lit) face.emissiveNode = texture(map, uv()).mul(0.8);       // a lit panel glows; most signs do not
  const edge = new THREE.MeshStandardNodeMaterial({ color: 0x5a6068, roughness: 0.45, metalness: 0.8 });
  // BoxGeometry face order: +x, -x, +y, -y, +z (the sign face), -z
  return new THREE.Mesh(new THREE.BoxGeometry(w, h, 0.03), [edge, edge, edge, edge, face, edge]);
}
```

Share one atlas across many small signs rather than a canvas each when they are numerous.

## Futuristic signage

Use a coherent visual language across the environment:

- station identifiers
- platform numbers
- route markings
- safety markings
- maintenance labels
- directional arrows
- emergency signs
- service identifiers

Signs should communicate real information.

## Physical construction

Model:

- sign board
- frame
- brackets
- mounts
- recessed displays
- illuminated housings

when these are visible.

For printed graphics, let the texture provide the lettering rather than adding unnecessary geometry.

## Lighting

Illuminated signs should use appropriate emissive treatment, but still have physical housing, thickness and mounting.

Do not make every sign emissive.
