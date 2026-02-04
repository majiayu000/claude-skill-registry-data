---
name: r3f-geometry
description: React Three Fiber geometry - built-in shapes, BufferGeometry, instancing, Drei helpers. Use when creating 3D shapes, custom geometry, or optimizing with instances.
---

# React Three Fiber Geometry

## Built-in Geometries

```tsx
<boxGeometry args={[1, 1, 1]} />
<sphereGeometry args={[1, 32, 32]} />
<planeGeometry args={[10, 10]} />
<cylinderGeometry args={[1, 1, 2, 32]} />
<coneGeometry args={[1, 2, 32]} />
<torusGeometry args={[1, 0.4, 16, 100]} />
<torusKnotGeometry args={[1, 0.4, 100, 16]} />
<icosahedronGeometry args={[1, 0]} />
<capsuleGeometry args={[0.5, 1, 4, 8]} />
```

## Drei Geometry Helpers

```tsx
import { Box, Sphere, Plane, RoundedBox, Text } from '@react-three/drei'

<Box args={[1, 1, 1]}>
  <meshStandardMaterial color="orange" />
</Box>

<Sphere args={[1, 32, 32]}>
  <meshStandardMaterial color="blue" />
</Sphere>

<RoundedBox args={[1, 1, 1]} radius={0.1} smoothness={4}>
  <meshStandardMaterial color="green" />
</RoundedBox>

<Text fontSize={1} color="white">Hello World</Text>
```

## Custom BufferGeometry

```tsx
import { useMemo } from 'react'
import * as THREE from 'three'

function CustomGeometry() {
  const geometry = useMemo(() => {
    const geo = new THREE.BufferGeometry()
    const vertices = new Float32Array([
      -1, -1, 0,  1, -1, 0,  1, 1, 0,  -1, 1, 0
    ])
    const indices = new Uint16Array([0, 1, 2, 0, 2, 3])

    geo.setAttribute('position', new THREE.BufferAttribute(vertices, 3))
    geo.setIndex(new THREE.BufferAttribute(indices, 1))
    geo.computeVertexNormals()
    return geo
  }, [])

  return (
    <mesh geometry={geometry}>
      <meshStandardMaterial />
    </mesh>
  )
}
```

## Instancing with Drei

```tsx
import { Instances, Instance } from '@react-three/drei'

function InstancedBoxes({ count = 100 }) {
  return (
    <Instances limit={count}>
      <boxGeometry />
      <meshStandardMaterial />
      {Array.from({ length: count }, (_, i) => (
        <Instance
          key={i}
          position={[Math.random() * 10, Math.random() * 10, Math.random() * 10]}
          rotation={[Math.random() * Math.PI, Math.random() * Math.PI, 0]}
          scale={0.5 + Math.random()}
          color={`hsl(${Math.random() * 360}, 70%, 50%)`}
        />
      ))}
    </Instances>
  )
}
```

## Merged Geometries (Static)

```tsx
import { Merged } from '@react-three/drei'

function MergedMeshes() {
  return (
    <Merged meshes={{ box: boxGeometry, sphere: sphereGeometry }}>
      {(models) => (
        <>
          <models.box position={[0, 0, 0]} />
          <models.box position={[2, 0, 0]} />
          <models.sphere position={[1, 2, 0]} />
        </>
      )}
    </Merged>
  )
}
```

## Points

```tsx
function ParticleCloud({ count = 1000 }) {
  const positions = useMemo(() => {
    const pos = new Float32Array(count * 3)
    for (let i = 0; i < count; i++) {
      pos[i * 3] = (Math.random() - 0.5) * 10
      pos[i * 3 + 1] = (Math.random() - 0.5) * 10
      pos[i * 3 + 2] = (Math.random() - 0.5) * 10
    }
    return pos
  }, [count])

  return (
    <points>
      <bufferGeometry>
        <bufferAttribute
          attach="attributes-position"
          count={count}
          array={positions}
          itemSize={3}
        />
      </bufferGeometry>
      <pointsMaterial size={0.1} color="white" />
    </points>
  )
}
```

## Utility Helpers

```tsx
import { Center, Bounds } from '@react-three/drei'

// Center geometry
<Center>
  <mesh>...</mesh>
</Center>

// Fit to view
<Bounds fit clip margin={1.2}>
  <mesh>...</mesh>
</Bounds>
```
