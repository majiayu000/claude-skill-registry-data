---
name: scenekit
description: "Build 3D scenes and visualizations using SceneKit. Use when creating 3D views with SCNView and SCNScene, building node hierarchies with SCNNode, applying materials and lighting, animating with SCNAction, simulating physics with SCNPhysicsBody, loading 3D models (.usdz, .scn), adding particle effects, or embedding SceneKit in SwiftUI with SceneView. Note: SceneKit was deprecated at WWDC 2025 and is in maintenance mode; RealityKit is recommended for new projects."
---

# SceneKit

Apple's high-level 3D rendering framework for building scenes and visualizations
on iOS using Swift 6.3. Provides a node-based scene graph, built-in geometry
primitives, physically based materials, lighting, animation, and physics.

**Deprecation notice (WWDC 2025):** SceneKit is officially deprecated across all
Apple platforms and is now in maintenance mode (critical bug fixes only). Existing
apps continue to work. For new projects or major updates, Apple recommends
RealityKit. See WWDC 2025 session 288 for migration guidance.

## Contents

- [Scene Setup](#scene-setup)
- [Nodes and Geometry](#nodes-and-geometry)
- [Materials](#materials)
- [Lighting](#lighting)
- [Cameras](#cameras)
- [Animation](#animation)
- [Physics](#physics)
- [Particle Systems](#particle-systems)
- [Loading Models](#loading-models)
- [SwiftUI Integration](#swiftui-integration)
- [Common Mistakes](#common-mistakes)
- [Review Checklist](#review-checklist)
- [References](#references)

## Scene Setup

### SCNView in UIKit

```swift
import SceneKit

let sceneView = SCNView(frame: view.bounds)
sceneView.scene = SCNScene()
sceneView.allowsCameraControl = true
sceneView.autoenablesDefaultLighting = true
sceneView.backgroundColor = .black
view.addSubview(sceneView)
```

`allowsCameraControl` adds built-in orbit, pan, and zoom gestures. Typically
disabled in production where custom camera control is needed.

### Creating an SCNScene

```swift
let scene = SCNScene()                                          // Empty
guard let scene = SCNScene(named: "art.scnassets/ship.scn")     // .scn asset catalog
    else { fatalError("Missing scene asset") }
let scene = try SCNScene(url: Bundle.main.url(                  // .usdz from bundle
    forResource: "spaceship", withExtension: "usdz")!)
```

## Nodes and Geometry

Every scene has a `rootNode`. All content exists as descendant nodes. Nodes
define position, orientation, and scale in their parent's coordinate system.
SceneKit uses a right-handed coordinate system: +X right, +Y up, +Z toward
the camera.

```swift
let parentNode = SCNNode()
scene.rootNode.addChildNode(parentNode)

let childNode = SCNNode()
childNode.position = SCNVector3(0, 1, 0)  // 1 unit above parent
parentNode.addChildNode(childNode)
```

### Transforms

```swift
node.position = SCNVector3(x: 0, y: 2, z: -5)
node.eulerAngles = SCNVector3(x: 0, y: .pi / 4, z: 0)  // 45-degree Y rotation
node.scale = SCNVector3(2, 2, 2)
node.simdPosition = SIMD3<Float>(0, 2, -5)  // Prefer simd for performance
```

### Built-in Primitives

`SCNBox`, `SCNSphere`, `SCNCylinder`, `SCNCone`, `SCNTorus`, `SCNCapsule`,
`SCNTube`, `SCNPlane`, `SCNFloor`, `SCNText`, `SCNShape` (extruded Bezier path).

```swift
let node = SCNNode(geometry: SCNSphere(radius: 0.5))
```

### Finding Nodes

```swift
let maxNode = scene.rootNode.childNode(withName: "Max", recursively: true)
let enemies = scene.rootNode.childNodes { node, _ in
    node.name?.hasPrefix("enemy") == true
}
```

## Materials

`SCNMaterial` defines surface appearance. Use `firstMaterial` for single-material
geometries or the `materials` array for multi-material.

### Color and Texture

```swift
let material = SCNMaterial()
material.diffuse.contents = UIColor.systemBlue     // Solid color
material.diffuse.contents = UIImage(named: "brick") // Texture
material.normal.contents = UIImage(named: "brick_normal")
sphere.firstMaterial = material
```

### Physically Based Rendering (PBR)

```swift
let pbr = SCNMaterial()
pbr.lightingModel = .physicallyBased
pbr.diffuse.contents = UIImage(named: "albedo")
pbr.metalness.contents = 0.8       // Scalar or texture
pbr.roughness.contents = 0.2       // Scalar or texture
pbr.normal.contents = UIImage(named: "normal")
pbr.ambientOcclusion.contents = UIImage(named: "ao")
```

### Lighting Models

`.physicallyBased` (metalness/roughness), `.blinn` (default), `.phong`,
`.lambert` (diffuse-only), `.constant` (unlit), `.shadowOnly`.

Each material property is an `SCNMaterialProperty` accepting `UIColor`,
`UIImage`, `CGFloat` scalar, `SKTexture`, `CALayer`, or `AVPlayer`.

### Transparency

```swift
material.transparency = 0.5
material.transparencyMode = .dualLayer
material.isDoubleSided = true
```

## Lighting

Attach an `SCNLight` to a node. The light's direction follows the node's
negative Z-axis.

### Light Types

```swift
// Ambient: uniform, no direction
let ambient = SCNLight()
ambient.type = .ambient
ambient.color = UIColor(white: 0.3, alpha: 1)

// Directional: parallel rays (sunlight)
let directional = SCNLight()
directional.type = .directional
directional.castsShadow = true

// Omni: point light, all directions
let omni = SCNLight()
omni.type = .omni
omni.attenuationEndDistance = 20

// Spot: cone-shaped
let spot = SCNLight()
spot.type = .spot
spot.spotInnerAngle = 20
spot.spotOuterAngle = 60
```

Attach to a node:

```swift
let lightNode = SCNNode()
lightNode.light = directional
lightNode.eulerAngles = SCNVector3(-Float.pi / 3, 0, 0)
lightNode.position = SCNVector3(0, 10, 10)
scene.rootNode.addChildNode(lightNode)
```

### Shadows

```swift
light.castsShadow = true
light.shadowMapSize = CGSize(width: 2048, height: 2048)
light.shadowSampleCount = 8
light.shadowRadius = 3.0
light.shadowColor = UIColor(white: 0, alpha: 0.5)
```

### Category Bit Masks

```swift
light.categoryBitMask = 1 << 1     // Category 2
node.categoryBitMask = 1 << 1      // Only lit by category-2 lights
```

SceneKit renders a maximum of 8 lights per node. Use `attenuationEndDistance`
on point/spot lights so SceneKit skips them for distant nodes.

## Cameras

Attach an `SCNCamera` to a node to define a viewpoint.

```swift
let cameraNode = SCNNode()
cameraNode.camera = SCNCamera()
cameraNode.position = SCNVector3(0, 5, 15)
cameraNode.look(at: SCNVector3Zero)
scene.rootNode.addChildNode(cameraNode)
sceneView.pointOfView = cameraNode
```

### Configuration

```swift
camera.fieldOfView = 60                        // Degrees
camera.zNear = 0.1
camera.zFar = 500
camera.automaticallyAdjustsZRange = true

// Orthographic
camera.usesOrthographicProjection = true
camera.orthographicScale = 10
```

Depth-of-field (`wantsDepthOfField`, `focusDistance`, `fStop`) and HDR effects
(`wantsHDR`, `bloomIntensity`, `bloomThreshold`, `screenSpaceAmbientOcclusionIntensity`)
are configured directly on `SCNCamera`.

## Animation

SceneKit provides three animation approaches.

### SCNAction (Declarative, Game-Oriented)

Reusable, composable animation objects attached to nodes.

```swift
let move = SCNAction.move(by: SCNVector3(0, 2, 0), duration: 1)
let rotate = SCNAction.rotateBy(x: 0, y: .pi, z: 0, duration: 1)
node.runAction(.group([move, rotate]))

// Sequential
node.runAction(.sequence([.fadeOut(duration: 0.3), .removeFromParentNode()]))

// Infinite loop
let pulse = SCNAction.sequence([
    .scale(to: 1.2, duration: 0.5),
    .scale(to: 1.0, duration: 0.5)
])
node.runAction(.repeatForever(pulse))
```

### SCNTransaction (Implicit Animation)

```swift
SCNTransaction.begin()
SCNTransaction.animationDuration = 1.0
node.position = SCNVector3(5, 0, 0)
node.opacity = 0.5
SCNTransaction.completionBlock = { print("Done") }
SCNTransaction.commit()
```

### Explicit Animations (Core Animation)

```swift
let animation = CABasicAnimation(keyPath: "rotation")
animation.toValue = NSValue(scnVector4: SCNVector4(0, 1, 0, Float.pi * 2))
animation.duration = 2
animation.repeatCount = .infinity
node.addAnimation(animation, forKey: "spin")
```

## Physics

### Physics Bodies

```swift
node.physicsBody = SCNPhysicsBody(type: .dynamic, shape: nil)   // Forces + collisions
floor.physicsBody = SCNPhysicsBody(type: .static, shape: nil)    // Immovable
platform.physicsBody = SCNPhysicsBody(type: .kinematic, shape: nil) // Code-driven
```

When `shape` is `nil`, SceneKit derives it from geometry. For performance, use
simplified shapes:

```swift
let shape = SCNPhysicsShape(
    geometry: SCNBox(width: 1, height: 2, length: 1, chamferRadius: 0),
    options: nil
)
node.physicsBody = SCNPhysicsBody(type: .dynamic, shape: shape)
node.physicsBody?.mass = 2.0
node.physicsBody?.restitution = 0.3
```

### Applying Forces

```swift
node.physicsBody?.applyForce(SCNVector3(0, 10, 0), asImpulse: false) // Continuous
node.physicsBody?.applyForce(SCNVector3(0, 5, 0), asImpulse: true)   // Instant
node.physicsBody?.applyTorque(SCNVector4(0, 1, 0, 2), asImpulse: true)
```

### Collision Detection

```swift
struct PhysicsCategory {
    static let player:     Int = 1 << 0
    static let enemy:      Int = 1 << 1
    static let ground:     Int = 1 << 2
}

playerNode.physicsBody?.categoryBitMask = PhysicsCategory.player
playerNode.physicsBody?.collisionBitMask = PhysicsCategory.ground | PhysicsCategory.enemy
playerNode.physicsBody?.contactTestBitMask = PhysicsCategory.enemy

scene.physicsWorld.contactDelegate = self

func physicsWorld(_ world: SCNPhysicsWorld, didBegin contact: SCNPhysicsContact) {
    handleCollision(between: contact.nodeA, and: contact.nodeB)
}
```

### Gravity

```swift
scene.physicsWorld.gravity = SCNVector3(0, -9.8, 0)
node.physicsBody?.isAffectedByGravity = false
```

## Particle Systems

`SCNParticleSystem` creates effects like fire, smoke, rain, and sparks.

```swift
let particles = SCNParticleSystem()
particles.birthRate = 100
particles.particleLifeSpan = 2
particles.particleSize = 0.1
particles.particleColor = .orange
particles.emitterShape = SCNSphere(radius: 0.5)
particles.particleVelocity = 2
particles.isAffectedByGravity = true
particles.blendMode = .additive

let emitterNode = SCNNode()
emitterNode.addParticleSystem(particles)
scene.rootNode.addChildNode(emitterNode)
```

Load from Xcode particle editor with
`SCNParticleSystem(named: "fire.scnp", inDirectory: nil)`. Particles can
collide with geometry via `colliderNodes`.

## Loading Models

SceneKit loads `.usdz`, `.scn`, `.dae`, `.obj`, and `.abc`. Prefer `.usdz`.

```swift
guard let scene = SCNScene(named: "art.scnassets/ship.scn") else { return }
let scene = try SCNScene(url: Bundle.main.url(
    forResource: "model", withExtension: "usdz")!)
guard let modelNode = scene.rootNode.childNode(withName: "mesh", recursively: true) else { return }
```

Use `SCNReferenceNode` with `.onDemand` loading policy for large models.
Use `SCNSceneSource` to inspect or selectively load entries from a file.

## SwiftUI Integration

`SceneView` embeds SceneKit in SwiftUI:

```swift
import SwiftUI
import SceneKit

struct SceneKitView: View {
    let scene: SCNScene = {
        let scene = SCNScene()
        let sphere = SCNNode(geometry: SCNSphere(radius: 1))
        sphere.geometry?.firstMaterial?.lightingModel = .physicallyBased
        sphere.geometry?.firstMaterial?.diffuse.contents = UIColor.systemBlue
        sphere.geometry?.firstMaterial?.metalness.contents = 0.8
        scene.rootNode.addChildNode(sphere)
        return scene
    }()

    var body: some View {
        SceneView(scene: scene,
                  options: [.allowsCameraControl, .autoenablesDefaultLighting])
    }
}
```

Options: `.allowsCameraControl`, `.autoenablesDefaultLighting`,
`.jitteringEnabled`, `.temporalAntialiasingEnabled`.

For render loop control, wrap `SCNView` in `UIViewRepresentable` with an
`SCNSceneRendererDelegate` coordinator. See [references/scenekit-patterns.md](references/scenekit-patterns.md).

## Common Mistakes

### Not adding a camera or lights

```swift
// DON'T: Scene renders blank or black -- no camera, no lights
sceneView.scene = scene

// DO: Add camera + lights, or use convenience flags
let cameraNode = SCNNode()
cameraNode.camera = SCNCamera()
cameraNode.position = SCNVector3(0, 5, 15)
scene.rootNode.addChildNode(cameraNode)
sceneView.pointOfView = cameraNode
sceneView.autoenablesDefaultLighting = true
```

### Using exact geometry for physics shapes

```swift
// DON'T
node.physicsBody = SCNPhysicsBody(type: .dynamic,
    shape: SCNPhysicsShape(geometry: complexMesh))

// DO: Simplified primitive
node.physicsBody = SCNPhysicsBody(type: .dynamic,
    shape: SCNPhysicsShape(
        geometry: SCNBox(width: 1, height: 2, length: 1, chamferRadius: 0),
        options: nil))
```

### Modifying transforms on dynamic bodies

```swift
// DON'T: Resets physics simulation
dynamicNode.position = SCNVector3(5, 0, 0)

// DO: Use forces/impulses
dynamicNode.physicsBody?.applyForce(SCNVector3(10, 0, 0), asImpulse: true)
```

### Exceeding 8 lights per node

```swift
// DON'T: 20 lights with no attenuation
for _ in 0..<20 {
    let light = SCNNode()
    light.light = SCNLight()
    light.light?.type = .omni
    scene.rootNode.addChildNode(light)
}

// DO: Set attenuationEndDistance so SceneKit skips distant lights
light.light?.attenuationEndDistance = 10
```

## Review Checklist

- [ ] Scene has at least one camera node set as `pointOfView`
- [ ] Scene has appropriate lighting (or `autoenablesDefaultLighting` for prototyping)
- [ ] Physics shapes use simplified geometry, not full mesh detail
- [ ] `contactTestBitMask` set for bodies that need collision callbacks
- [ ] `SCNPhysicsContactDelegate` assigned to `scene.physicsWorld.contactDelegate`
- [ ] Dynamic body transforms changed via forces/impulses, not direct position
- [ ] Lights limited to 8 per node; `attenuationEndDistance` set on point/spot lights
- [ ] Materials use `.physicallyBased` lighting model for realistic rendering
- [ ] 3D assets use `.usdz` format where possible
- [ ] `SCNReferenceNode` used for large models to enable lazy loading
- [ ] Particle `birthRate` and `particleLifeSpan` balanced to control particle count
- [ ] `categoryBitMask` used to scope lights and cameras to relevant nodes
- [ ] SwiftUI scenes use `SceneView` or `UIViewRepresentable`-wrapped `SCNView`
- [ ] Deprecation acknowledged; RealityKit evaluated for new projects

## References

- See [references/scenekit-patterns.md](references/scenekit-patterns.md) for custom geometry, shader modifiers,
  node constraints, morph targets, hit testing, scene serialization, render loop
  delegates, performance optimization, SpriteKit overlay, LOD, and Metal shaders.
- [SceneKit documentation](https://sosumi.ai/documentation/scenekit)
- [SCNScene](https://sosumi.ai/documentation/scenekit/scnscene)
- [SCNNode](https://sosumi.ai/documentation/scenekit/scnnode)
- [SCNView](https://sosumi.ai/documentation/scenekit/scnview)
- [SceneView (SwiftUI)](https://sosumi.ai/documentation/scenekit/sceneview)
- [SCNGeometry](https://sosumi.ai/documentation/scenekit/scngeometry)
- [SCNMaterial](https://sosumi.ai/documentation/scenekit/scnmaterial)
- [SCNLight](https://sosumi.ai/documentation/scenekit/scnlight)
- [SCNCamera](https://sosumi.ai/documentation/scenekit/scncamera)
- [SCNAction](https://sosumi.ai/documentation/scenekit/scnaction)
- [SCNPhysicsBody](https://sosumi.ai/documentation/scenekit/scnphysicsbody)
- [SCNParticleSystem](https://sosumi.ai/documentation/scenekit/scnparticlesystem)
- [WWDC 2025 session 288: Bring your SceneKit project to RealityKit](https://sosumi.ai/videos/play/wwdc2025/288/)
