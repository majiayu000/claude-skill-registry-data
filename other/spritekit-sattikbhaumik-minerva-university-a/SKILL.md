---
name: spritekit
description: "Build 2D games and animations using SpriteKit. Use when creating game scenes with SKScene and SKView, adding sprites with SKSpriteNode, animating with SKAction sequences, simulating physics with SKPhysicsBody and contact detection, creating particle effects with SKEmitterNode, building tile maps, using SKCameraNode, or integrating SpriteKit scenes in SwiftUI with SpriteView."
---

# SpriteKit

Build 2D games and interactive animations for iOS 26+ using SpriteKit and
Swift 6.3. Covers scene lifecycle, node hierarchy, actions, physics, particles,
camera, touch handling, and SwiftUI integration.

## Contents

- [Scene Setup](#scene-setup)
- [Nodes and Sprites](#nodes-and-sprites)
- [Actions and Animation](#actions-and-animation)
- [Physics](#physics)
- [Touch Handling](#touch-handling)
- [Camera](#camera)
- [Particle Effects](#particle-effects)
- [SwiftUI Integration](#swiftui-integration)
- [Common Mistakes](#common-mistakes)
- [Review Checklist](#review-checklist)
- [References](#references)

## Scene Setup

SpriteKit renders content through `SKView`, which presents an `SKScene` -- the
root node of a tree that the framework animates and renders each frame.

### Creating a Scene

Subclass `SKScene` and override lifecycle methods. The coordinate system
origin is at the bottom-left by default.

```swift
import SpriteKit

final class GameScene: SKScene {
    override func didMove(to view: SKView) {
        backgroundColor = .darkGray
        physicsWorld.contactDelegate = self
        physicsBody = SKPhysicsBody(edgeLoopFrom: frame)
        setupNodes()
    }

    override func update(_ currentTime: TimeInterval) {
        // Called once per frame before actions are evaluated.
    }
}
```

### Presenting a Scene (UIKit)

```swift
guard let skView = view as? SKView else { return }
skView.ignoresSiblingOrder = true

let scene = GameScene(size: skView.bounds.size)
scene.scaleMode = .resizeFill
skView.presentScene(scene)
```

### Scale Modes

Use `.resizeFill` when the scene should adapt to view size changes (rotation,
multitasking). Use `.aspectFill` for fixed-design game scenes. `.aspectFit`
letterboxes; `.fill` stretches and may distort.

### Frame Cycle

Each frame follows this order:

1. `update(_:)` -- game logic
2. Evaluate actions
3. `didEvaluateActions()` -- post-action logic
4. Simulate physics
5. `didSimulatePhysics()` -- post-physics adjustments
6. Apply constraints
7. `didApplyConstraints()`
8. `didFinishUpdate()` -- final adjustments before rendering

Override only the callbacks where work is needed.

## Nodes and Sprites

Use `SKNode` (without a visual) as an invisible container or layout group.
Child nodes inherit parent position, scale, rotation, alpha, and speed.
`SKSpriteNode` is the primary visual node.

### Common Node Types

| Class | Purpose |
|-------|---------|
| `SKSpriteNode` | Textured image or solid color |
| `SKLabelNode` | Text rendering |
| `SKShapeNode` | Vector paths (expensive per draw call) |
| `SKEmitterNode` | Particle effects |
| `SKCameraNode` | Viewport control |
| `SKTileMapNode` | Grid-based tiles |
| `SKAudioNode` | Positional audio |
| `SKCropNode` / `SKEffectNode` | Masking / CIFilter |
| `SK3DNode` | Embedded SceneKit content |

### Creating Sprites

```swift
let player = SKSpriteNode(imageNamed: "hero")
player.position = CGPoint(x: frame.midX, y: frame.midY)
player.name = "player"
addChild(player)
```

### Drawing Order

Set `ignoresSiblingOrder = true` on `SKView` for better performance; SpriteKit
then uses `zPosition` to determine order. Without it, nodes draw in tree order.

```swift
background.zPosition = -1
player.zPosition = 0
foregroundUI.zPosition = 10
```

### Naming and Searching

Assign `name` to find nodes without instance variables. Use `childNode(withName:)`,
`enumerateChildNodes(withName:using:)`, or `subscript`. Patterns: `//` searches
the entire tree, `*` matches any characters, `..` refers to the parent.

```swift
player.name = "player"
if let found = childNode(withName: "player") as? SKSpriteNode { /* ... */ }
```

## Actions and Animation

`SKAction` objects define changes applied to nodes over time. Actions are
immutable and reusable. Run with `node.run(_:)`.

### Basic Actions

```swift
let moveUp = SKAction.moveBy(x: 0, y: 100, duration: 0.5)
let grow = SKAction.scale(to: 1.5, duration: 0.3)
let spin = SKAction.rotate(byAngle: .pi * 2, duration: 1.0)
let fadeOut = SKAction.fadeOut(withDuration: 0.3)
let remove = SKAction.removeFromParent()
```

### Combining Actions

```swift
// Sequential: run one after another
let dropAndRemove = SKAction.sequence([
    SKAction.moveBy(x: 0, y: -500, duration: 1.0),
    SKAction.removeFromParent()
])

// Parallel: run simultaneously
let scaleAndFade = SKAction.group([
    SKAction.scale(to: 0.0, duration: 0.3),
    SKAction.fadeOut(withDuration: 0.3)
])

// Repeat
let pulse = SKAction.repeatForever(
    SKAction.sequence([
        SKAction.scale(to: 1.2, duration: 0.5),
        SKAction.scale(to: 1.0, duration: 0.5)
    ])
)
```

### Texture Animation

```swift
let walkFrames = (1...8).map { SKTexture(imageNamed: "walk_\($0)") }
let walkAction = SKAction.animate(with: walkFrames, timePerFrame: 0.1)
player.run(SKAction.repeatForever(walkAction))
```

Control the speed curve with `timingMode` (`.linear`, `.easeIn`, `.easeOut`,
`.easeInEaseOut`). Assign keys to actions for later access:

```swift
let easeIn = SKAction.moveTo(x: 300, duration: 1.0)
easeIn.timingMode = .easeInEaseOut

player.run(pulse, withKey: "pulse")
player.removeAction(forKey: "pulse") // stop later
```

## Physics

SpriteKit provides a built-in 2D physics engine. The scene's `physicsWorld`
manages gravity and collision detection.

### Adding Physics Bodies

```swift
// Circle body
player.physicsBody = SKPhysicsBody(circleOfRadius: player.size.width / 2)
player.physicsBody?.restitution = 0.3

// Static rectangle
ground.physicsBody = SKPhysicsBody(rectangleOf: ground.size)
ground.physicsBody?.isDynamic = false

// Texture-based body for irregular shapes
player.physicsBody = SKPhysicsBody(texture: player.texture!, size: player.size)
```

### Category and Contact Masks

Use bit masks to control collisions and contact callbacks:

```swift
struct PhysicsCategory {
    static let player:  UInt32 = 0b0001
    static let enemy:   UInt32 = 0b0010
    static let ground:  UInt32 = 0b0100
}

player.physicsBody?.categoryBitMask = PhysicsCategory.player
player.physicsBody?.contactTestBitMask = PhysicsCategory.enemy
player.physicsBody?.collisionBitMask = PhysicsCategory.ground
```

`categoryBitMask` identifies the body. `collisionBitMask` controls physics
response (bouncing). `contactTestBitMask` triggers `didBegin`/`didEnd`.

### Contact Detection

Implement `SKPhysicsContactDelegate` and set `physicsWorld.contactDelegate = self`
in `didMove(to:)`:

```swift
extension GameScene: SKPhysicsContactDelegate {
    func didBegin(_ contact: SKPhysicsContact) {
        let mask = contact.bodyA.categoryBitMask | contact.bodyB.categoryBitMask
        if mask == PhysicsCategory.player | PhysicsCategory.enemy {
            handlePlayerHit(contact)
        }
    }
}
```

### Forces and Impulses

```swift
player.physicsBody?.applyForce(CGVector(dx: 0, dy: 50))      // continuous
player.physicsBody?.applyImpulse(CGVector(dx: 0, dy: 200))   // instant
player.physicsBody?.applyAngularImpulse(0.5)                  // spin
```

Use `.applyImpulse` for jumps and projectile launches. Configure gravity with
`physicsWorld.gravity = CGVector(dx: 0, dy: -9.8)` and per-body with
`affectedByGravity`.

## Touch Handling

`SKScene` inherits from `UIResponder`. Override `touchesBegan`, `touchesMoved`,
`touchesEnded` on the scene. Use `nodes(at:)` to hit-test.

```swift
override func touchesBegan(_ touches: Set<UITouch>, with event: UIEvent?) {
    guard let touch = touches.first else { return }
    let location = touch.location(in: self)
    let tappedNodes = nodes(at: location)

    if tappedNodes.contains(where: { $0.name == "playButton" }) {
        startGame()
    }
}
```

For node-level touch handling, subclass the node and set
`isUserInteractionEnabled = true`. That node then receives touches directly
instead of the scene.

## Camera

`SKCameraNode` controls the visible portion of the scene. Add it as a child
and assign to `scene.camera`.

```swift
let cameraNode = SKCameraNode()
addChild(cameraNode)
camera = cameraNode
cameraNode.position = CGPoint(x: frame.midX, y: frame.midY)
```

### Following a Character

Update the camera position in `didSimulatePhysics()` or use constraints:

```swift
override func didSimulatePhysics() {
    cameraNode.position = player.position
}

// Constrain camera to world bounds
let xRange = SKRange(lowerLimit: frame.midX, upperLimit: worldWidth - frame.midX)
let yRange = SKRange(lowerLimit: frame.midY, upperLimit: worldHeight - frame.midY)
cameraNode.constraints = [SKConstraint.positionX(xRange, y: yRange)]
```

### Camera Zoom and HUD

Scale the camera node inversely: `setScale(0.5)` zooms in 2x, `setScale(2.0)`
zooms out 2x. Nodes added as children of the camera stay fixed on screen
(HUD elements):

```swift
let scoreLabel = SKLabelNode(text: "Score: 0")
scoreLabel.position = CGPoint(x: 0, y: frame.height / 2 - 40)
scoreLabel.fontName = "AvenirNext-Bold"
scoreLabel.fontSize = 24
cameraNode.addChild(scoreLabel)
```

## Particle Effects

`SKEmitterNode` generates particle effects. Design emitters in Xcode's
SpriteKit Particle File editor (`.sks`) or configure in code.

```swift
// Load from file
guard let emitter = SKEmitterNode(fileNamed: "Fire") else { return }
emitter.position = CGPoint(x: frame.midX, y: 100)
addChild(emitter)
```

### One-Shot Emitters

Set `numParticlesToEmit` for finite effects and remove after completion:

```swift
func spawnExplosion(at position: CGPoint) {
    guard let explosion = SKEmitterNode(fileNamed: "Explosion") else { return }
    explosion.position = position
    explosion.numParticlesToEmit = 100
    addChild(explosion)

    let wait = SKAction.wait(forDuration: TimeInterval(explosion.particleLifetime))
    explosion.run(SKAction.sequence([wait, .removeFromParent()]))
}
```

Set `targetNode` to the scene so particles stay in world space when the
emitter moves: `emitter.targetNode = self`.

## SwiftUI Integration

`SpriteView` embeds a SpriteKit scene in SwiftUI.

```swift
import SwiftUI
import SpriteKit

struct GameView: View {
    @State private var scene: GameScene = {
        let s = GameScene()
        s.size = CGSize(width: 390, height: 844)
        s.scaleMode = .resizeFill
        return s
    }()

    var body: some View {
        SpriteView(scene: scene)
            .ignoresSafeArea()
    }
}
```

### SpriteView Options

Pass `options: [.allowsTransparency]` for transparent backgrounds,
`.shouldCullNonVisibleNodes` for offscreen culling, or `.ignoresSiblingOrder`
for `zPosition`-based draw order. Use `debugOptions: [.showsFPS, .showsNodeCount]`
during development.

### Communicating Between SwiftUI and the Scene

Pass data through a shared `@Observable` object. Store the scene in `@State`
to avoid re-creation on view re-renders:

```swift
@Observable final class GameState {
    var score = 0
    var isPaused = false
}

struct GameContainerView: View {
    @State private var gameState = GameState()
    @State private var scene = GameScene()

    var body: some View {
        SpriteView(scene: scene, isPaused: gameState.isPaused)
            .onAppear { scene.gameState = gameState }
    }
}
```

## Common Mistakes

### Creating a new scene on every SwiftUI re-render

```swift
// DON'T: Scene is recreated on every body evaluation
var body: some View {
    SpriteView(scene: GameScene(size: CGSize(width: 390, height: 844)))
}

// DO: Create once and reuse
@State private var scene = GameScene(size: CGSize(width: 390, height: 844))
var body: some View {
    SpriteView(scene: scene)
}
```

### Adding a child node that already has a parent

A node can only have one parent. Remove from the current parent first or
create a separate instance. Adding a node that already has a parent crashes.

### Forgetting to set contactTestBitMask

```swift
// DON'T: Bodies collide but didBegin is never called
player.physicsBody?.categoryBitMask = PhysicsCategory.player
enemy.physicsBody?.categoryBitMask = PhysicsCategory.enemy

// DO: Set contactTestBitMask to receive contact callbacks
player.physicsBody?.contactTestBitMask = PhysicsCategory.enemy
```

### Using SKShapeNode for performance-critical rendering

`SKShapeNode` uses a separate draw call per instance. Prefer `SKSpriteNode`
with a texture for repeated elements to enable batched rendering.

### Not removing nodes that leave the screen

```swift
// DON'T
enemy.run(SKAction.moveBy(x: -800, y: 0, duration: 3.0))
addChild(enemy)

// DO: Remove after leaving the visible area
enemy.run(SKAction.sequence([
    SKAction.moveBy(x: -800, y: 0, duration: 3.0),
    SKAction.removeFromParent()
]))
addChild(enemy)
```

### Setting physicsWorld.contactDelegate too late

Set `physicsWorld.contactDelegate = self` in `didMove(to:)`, not in
`update(_:)` or after a delay.

## Review Checklist

- [ ] Scene subclass overrides `didMove(to:)` for setup, not `init`
- [ ] `scaleMode` chosen appropriately for the game's design
- [ ] `ignoresSiblingOrder` set to `true` on `SKView` for performance
- [ ] `zPosition` used consistently when `ignoresSiblingOrder` is enabled
- [ ] Physics `contactDelegate` set in `didMove(to:)`
- [ ] Category, collision, and contact bit masks configured correctly
- [ ] `contactTestBitMask` set for any pair needing `didBegin`/`didEnd` callbacks
- [ ] Static bodies use `isDynamic = false`
- [ ] `SKShapeNode` avoided in performance-critical paths; `SKSpriteNode` preferred
- [ ] Actions that move nodes offscreen include `.removeFromParent()` in sequence
- [ ] One-shot emitters remove themselves after particle lifetime expires
- [ ] Emitter `targetNode` set when particles should stay in world space
- [ ] Scene stored in `@State` when used with `SpriteView` in SwiftUI
- [ ] Texture atlases used for related sprites to reduce draw calls
- [ ] `update(_:)` uses delta time for frame-rate-independent movement
- [ ] Nodes removed from parent before being re-added elsewhere

## References

- See [references/spritekit-patterns.md](references/spritekit-patterns.md) for tile maps, texture atlases, shaders,
  scene transitions, game loop patterns, audio, and SceneKit embedding.
- [SpriteKit documentation](https://sosumi.ai/documentation/spritekit)
- [SKScene](https://sosumi.ai/documentation/spritekit/skscene)
- [SKSpriteNode](https://sosumi.ai/documentation/spritekit/skspritenode)
- [SKAction](https://sosumi.ai/documentation/spritekit/skaction)
- [SKPhysicsBody](https://sosumi.ai/documentation/spritekit/skphysicsbody)
- [SKEmitterNode](https://sosumi.ai/documentation/spritekit/skemitternode)
- [SKCameraNode](https://sosumi.ai/documentation/spritekit/skcameranode)
- [SpriteView](https://sosumi.ai/documentation/spritekit/spriteview)
- [SKTileMapNode](https://sosumi.ai/documentation/spritekit/sktilemapnode)
