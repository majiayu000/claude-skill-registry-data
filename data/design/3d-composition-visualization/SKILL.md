---
name: 3D Composition Visualization
description: Build 3D visualizations using Three.js and React Three Fiber. Use when implementing 3D components, debugging rendering issues, optimizing performance, or creating interactive visualization features.
---

# 3D Composition Visualization Skill

## Purpose

This skill provides guidance for building the Composition app's 3D visualization system using Three.js and React Three Fiber (R3F).

## When to Use

- Creating new 3D visualization components
- Implementing interaction modes (explode, zoom, slice)
- Debugging rendering or performance issues
- Optimizing 3D performance
- Adding visual effects or materials

## Core Libraries

```json
{
  "@react-three/fiber": "React renderer for Three.js",
  "@react-three/drei": "Useful helpers and abstractions",
  "@react-three/postprocessing": "Post-processing effects",
  "three": "Core 3D library",
  "leva": "Debug GUI for development",
  "@react-spring/three": "Animations"
}
```

## Component Architecture

### Scene Setup
```tsx
import { Canvas } from '@react-three/fiber'
import { OrbitControls, Environment } from '@react-three/drei'

function CompositionScene({ composition }) {
  return (
    <Canvas
      shadows
      dpr={[1, 2]}
      camera={{ position: [0, 0, 5], fov: 50 }}
    >
      <color attach="background" args={['#0a0a0a']} />
      <ambientLight intensity={0.4} />
      <directionalLight position={[10, 10, 5]} castShadow />
      <Environment preset="studio" />
      <OrbitControls enableDamping />

      <CompositionGroup composition={composition} />
    </Canvas>
  )
}
```

### Composition Node Renderer
```tsx
function CompositionNode({ node, depth, position }) {
  const size = calculateSize(node.percentage)
  const material = getMaterialForType(node.type)

  return (
    <group position={position}>
      <mesh>
        <sphereGeometry args={[size, 32, 32]} />
        {material}
      </mesh>

      {node.children?.map((child, i) => (
        <CompositionNode
          key={child.id}
          node={child}
          depth={depth + 1}
          position={calculateChildPosition(i, node.children.length)}
        />
      ))}
    </group>
  )
}
```

## Visualization Modes

### Exploded View
```tsx
function ExplodedView({ nodes, exploded }) {
  const { positions } = useSpring({
    positions: nodes.map((n, i) =>
      exploded
        ? [Math.cos(i * angle) * radius, 0, Math.sin(i * angle) * radius]
        : [0, 0, 0]
    ),
    config: { mass: 1, tension: 180, friction: 24 }
  })

  // Render nodes at animated positions
}
```

### Zoom/Drill-Down
```tsx
function ZoomableComposition({ root }) {
  const [focus, setFocus] = useState(root)
  const [path, setPath] = useState([root])

  const drillDown = (node) => {
    setFocus(node)
    setPath([...path, node])
  }

  const navigateUp = () => {
    const newPath = path.slice(0, -1)
    setPath(newPath)
    setFocus(newPath[newPath.length - 1])
  }

  // Animate camera to focus on selected node
}
```

### Cross-Section
```tsx
function CrossSection({ composition }) {
  const [clipPosition, setClipPosition] = useState(0)

  return (
    <group>
      <mesh>
        <planeGeometry args={[100, 100]} />
        <meshBasicMaterial
          side={DoubleSide}
          colorWrite={false}
          depthWrite={false}
        />
      </mesh>

      {/* Render composition with clipping plane */}
    </group>
  )
}
```

## Material System

```tsx
// Material presets by composition type
const materials = {
  metal: {
    metalness: 0.9,
    roughness: 0.2,
    envMapIntensity: 1
  },
  organic: {
    metalness: 0,
    roughness: 0.8,
    color: '#4a7c59'
  },
  glass: {
    transmission: 0.9,
    roughness: 0.1,
    ior: 1.5
  },
  element: (element) => ({
    color: periodicTableColors[element],
    metalness: isMetallic(element) ? 0.8 : 0.1,
    roughness: 0.4
  })
}
```

## Performance Optimization

### Instancing for Many Objects
```tsx
function MoleculeCloud({ atoms }) {
  return (
    <Instances limit={10000} range={atoms.length}>
      <sphereGeometry args={[0.1, 16, 16]} />
      <meshStandardMaterial />

      {atoms.map((atom, i) => (
        <Instance
          key={i}
          position={atom.position}
          scale={atom.radius}
          color={elementColors[atom.element]}
        />
      ))}
    </Instances>
  )
}
```

### Level of Detail
```tsx
function DetailedComponent({ detail }) {
  const { camera } = useThree()
  const distance = useRef(0)

  useFrame(() => {
    distance.current = camera.position.distanceTo(meshRef.current.position)
  })

  const segments = distance.current < 5 ? 64 : distance.current < 20 ? 32 : 16

  return (
    <mesh ref={meshRef}>
      <sphereGeometry args={[1, segments, segments]} />
      <meshStandardMaterial />
    </mesh>
  )
}
```

### Memory Management
```tsx
useEffect(() => {
  return () => {
    // Dispose of Three.js objects
    geometry.dispose()
    material.dispose()
    texture?.dispose()
  }
}, [])
```

## Interaction System

```tsx
function InteractiveNode({ node, onSelect, onDrillDown }) {
  const [hovered, setHovered] = useState(false)

  return (
    <mesh
      onPointerOver={(e) => {
        e.stopPropagation()
        setHovered(true)
        document.body.style.cursor = 'pointer'
      }}
      onPointerOut={() => {
        setHovered(false)
        document.body.style.cursor = 'auto'
      }}
      onClick={(e) => {
        e.stopPropagation()
        onSelect(node)
      }}
      onDoubleClick={(e) => {
        e.stopPropagation()
        onDrillDown(node)
      }}
    >
      <sphereGeometry />
      <meshStandardMaterial
        color={hovered ? '#ff6b6b' : '#4ecdc4'}
        emissive={hovered ? '#ff6b6b' : '#000000'}
        emissiveIntensity={hovered ? 0.2 : 0}
      />
    </mesh>
  )
}
```

## Responsive Design

```tsx
function ResponsiveCanvas() {
  const isMobile = useMediaQuery('(max-width: 768px)')

  return (
    <Canvas
      dpr={isMobile ? [1, 1.5] : [1, 2]}
      gl={{
        antialias: !isMobile,
        powerPreference: isMobile ? 'low-power' : 'high-performance'
      }}
    >
      {/* Adjust complexity based on device */}
    </Canvas>
  )
}
```

## Debugging Tools

```tsx
// Development helpers
import { Stats, useHelper } from '@react-three/drei'
import { DirectionalLightHelper } from 'three'

function DevTools() {
  const lightRef = useRef()
  useHelper(lightRef, DirectionalLightHelper, 1)

  return (
    <>
      <Stats />
      <axesHelper args={[5]} />
      <gridHelper args={[10, 10]} />
      <directionalLight ref={lightRef} />
    </>
  )
}
```

## Common Patterns

### Loading 3D Models
```tsx
import { useGLTF } from '@react-three/drei'

function ProductModel({ url }) {
  const { scene } = useGLTF(url)
  return <primitive object={scene} />
}

// Preload
useGLTF.preload('/models/product.glb')
```

### Animated Transitions
```tsx
import { useSpring, animated } from '@react-spring/three'

function AnimatedNode({ targetPosition }) {
  const { position } = useSpring({
    position: targetPosition,
    config: { mass: 1, tension: 170, friction: 26 }
  })

  return <animated.mesh position={position} />
}
```
