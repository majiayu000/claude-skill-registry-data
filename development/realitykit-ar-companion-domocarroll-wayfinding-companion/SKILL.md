---
name: realitykit-ar-companion
description: Comprehensive RealityKit skill optimized for building AR companion experiences on iOS and visionOS, with character animation, body/hand tracking, AI integration patterns, spatial audio, and entity lifecycle management
---

# RealityKit AR Companion Development Skill

A production-ready skill for developing AR companion applications using Apple's RealityKit framework, specifically tailored for creating interactive, persistent virtual characters.

## Quick Start for AR Companion MVP

### Minimum Viable Setup

```swift
import SwiftUI
import RealityKit
import ARKit

struct ARCompanionView: View {
    var body: some View {
        ARViewContainer()
            .edgesIgnoringSafeArea(.all)
    }
}

struct ARViewContainer: UIViewRepresentable {
    func makeUIView(context: Context) -> ARView {
        let arView = ARView(frame: .zero)

        // Configure AR session for companion placement
        let config = ARWorldTrackingConfiguration()
        config.planeDetection = [.horizontal]
        config.environmentTexturing = .automatic
        arView.session.run(config)

        // Create companion anchor on horizontal surface
        let anchor = AnchorEntity(plane: .horizontal)
        arView.scene.addAnchor(anchor)

        // Load companion entity asynchronously
        Task {
            do {
                let companion = try await Entity.loadAsync(named: "Companion")
                anchor.addChild(companion)
            } catch {
                print("Failed to load companion: \(error)")
            }
        }

        return arView
    }

    func updateUIView(_ uiView: ARView, context: Context) {}
}
```

## Core Concepts for Companion Development

### Entity-Component-System (ECS) Architecture

RealityKit uses an ECS architecture ideal for companion characters:

- **Entity**: The base container for your companion (position, hierarchy)
- **Component**: Modular behaviors attached to entities (animation, physics, audio)
- **System**: Logic that processes entities with specific components each frame

```swift
// Custom companion component
struct CompanionComponent: Component {
    var mood: CompanionMood = .neutral
    var energy: Float = 1.0
    var isInteracting: Bool = false
}

enum CompanionMood {
    case happy, neutral, curious, tired
}

// Register component before use
CompanionComponent.registerComponent()
```

### Custom System for Companion Behavior

```swift
class CompanionBehaviorSystem: System {
    static let query = EntityQuery(where: .has(CompanionComponent.self))

    required init(scene: Scene) {}

    func update(context: SceneUpdateContext) {
        for entity in context.entities(matching: Self.query, updatingSystemWhen: .rendering) {
            guard var companion = entity.components[CompanionComponent.self] else { continue }

            // Update companion state based on time/interaction
            companion.energy -= 0.0001 * Float(context.deltaTime)

            if companion.energy < 0.3 {
                companion.mood = .tired
            }

            entity.components[CompanionComponent.self] = companion
        }
    }
}

// Register system at app launch
CompanionBehaviorSystem.registerSystem()
```

## Character Animation and Rigging

### Loading Animated Characters

```swift
// Async loading of USDZ character with animations
func loadCompanionCharacter() async throws -> Entity {
    let character = try await Entity.load(named: "CompanionCharacter")

    // Access available animations
    if let animationResource = character.availableAnimations.first {
        character.playAnimation(animationResource.repeat())
    }

    return character
}
```

### Animation Playback Control

```swift
class CompanionAnimator {
    var companion: Entity
    var currentController: AnimationPlaybackController?

    init(companion: Entity) {
        self.companion = companion
    }

    func playAnimation(named name: String, loop: Bool = false) {
        // Stop current animation
        currentController?.stop()

        // Find and play new animation
        if let animation = companion.availableAnimations.first(where: {
            $0.name?.contains(name) == true
        }) {
            let resource = loop ? animation.repeat() : animation
            currentController = companion.playAnimation(resource)
        }
    }

    func transitionToIdle() {
        playAnimation(named: "idle", loop: true)
    }

    func playReaction(type: ReactionType) {
        switch type {
        case .wave:
            playAnimation(named: "wave")
        case .jump:
            playAnimation(named: "jump")
        case .nod:
            playAnimation(named: "nod")
        }
    }
}

enum ReactionType {
    case wave, jump, nod
}
```

### Using RealityActions for Procedural Animation

```swift
import RealityActions

// Register at app startup
ActionManagerSystem.registerSystem()

// Procedural bounce animation
func makeCompanionBounce(_ entity: Entity) {
    entity.start(RepeatForever(
        Sequence(
            MoveBy(duration: 0.3, delta: SIMD3(0, 0.1, 0)),
            MoveBy(duration: 0.3, delta: SIMD3(0, -0.1, 0))
        )
    ))
}

// Attention-grabbing wiggle
func wiggleForAttention(_ entity: Entity) {
    entity.start(Sequence(
        RotateBy(duration: 0.1, deltaAngles: SIMD3(0, 0.1, 0)),
        RotateBy(duration: 0.1, deltaAngles: SIMD3(0, -0.2, 0)),
        RotateBy(duration: 0.1, deltaAngles: SIMD3(0, 0.1, 0))
    ))
}

// Look at user smoothly
func lookAtUser(_ entity: Entity, userPosition: SIMD3<Float>) async {
    let direction = normalize(userPosition - entity.position)
    let targetRotation = simd_quatf(from: SIMD3(0, 0, 1), to: direction)

    await entity.run(RotateTo(duration: 0.5, orientation: targetRotation))
}
```

### Morph Target Animations (Facial Expressions)

Using RealityMorpher for blend shape animations (iOS/macOS only, not visionOS):

```swift
import RealityMorpher

// Apply facial expression blend shapes
func setCompanionExpression(_ entity: Entity, expression: FacialExpression) {
    // Requires model with blend shapes exported from 3D software
    // Set morph target weights for expressions
    switch expression {
    case .happy:
        // Set smile blend shape weight
        entity.setMorphWeight(named: "smile", weight: 1.0)
        entity.setMorphWeight(named: "eyeWide", weight: 0.3)
    case .sad:
        entity.setMorphWeight(named: "frown", weight: 0.8)
        entity.setMorphWeight(named: "eyeNarrow", weight: 0.4)
    case .surprised:
        entity.setMorphWeight(named: "mouthOpen", weight: 0.7)
        entity.setMorphWeight(named: "eyeWide", weight: 1.0)
    }
}

enum FacialExpression {
    case happy, sad, surprised, neutral
}
```

## Body and Hand Tracking for Interaction

### Body Tracking Setup

```swift
import RKLoader

class BodyTrackingManager {
    var arView: ARView
    var trackedCharacter: BodyTrackedEntity?

    init(arView: ARView) {
        self.arView = arView
    }

    func startBodyTracking() async throws {
        // Load body-tracked character
        let character = try await RKLoader.loadBodyTrackedEntityAsync(named: "TrackedCompanion")
        trackedCharacter = character

        // Create body anchor
        let bodyAnchor = AnchorEntity(.body)
        arView.scene.addAnchor(bodyAnchor)
        bodyAnchor.addChild(character)
    }

    func stopBodyTracking() {
        trackedCharacter?.removeFromParent()
        trackedCharacter = nil
    }
}
```

### Hand Tracking for visionOS

```swift
import HandVector

class HandInteractionManager: ObservableObject {
    @Published var detectedGesture: HandGesture = .none

    private let handTracking = HandTracking()

    func processHandUpdate(anchor: HandAnchor) {
        let handInfo = handTracking.generateHandInfo(from: anchor)

        // Check against built-in gestures
        if let similarity = handInfo?.similarity(of: .fiveFingers, to: .thumbsUp),
           similarity > 0.8 {
            detectedGesture = .thumbsUp
            return
        }

        if let similarity = handInfo?.similarity(of: .fiveFingers, to: .wave),
           similarity > 0.8 {
            detectedGesture = .wave
            return
        }

        // Check pinch gesture using FingerShape
        if let fingerShape = handInfo?.fingerShape,
           fingerShape.pinchDistance < 0.02 {
            detectedGesture = .pinch
            return
        }

        detectedGesture = .none
    }
}

enum HandGesture {
    case none, thumbsUp, wave, pinch, pointAt
}
```

### Companion Response to Hand Gestures

```swift
class GestureResponsiveCompanion {
    var companion: Entity
    var animator: CompanionAnimator

    func respondToGesture(_ gesture: HandGesture) {
        switch gesture {
        case .thumbsUp:
            animator.playReaction(type: .jump)
            playHappySound()
        case .wave:
            animator.playReaction(type: .wave)
        case .pinch:
            // Start interaction mode
            startInteractionMode()
        case .pointAt:
            // Look where user is pointing
            followPointDirection()
        case .none:
            break
        }
    }
}
```

## AI Integration Patterns for Companion Behavior

### State Machine for Companion AI

```swift
class CompanionAI {
    enum State {
        case idle
        case following
        case playing
        case resting
        case responding
    }

    var currentState: State = .idle
    var companion: Entity
    var animator: CompanionAnimator

    private var stateTimer: Double = 0
    private var attentionTarget: SIMD3<Float>?

    func update(deltaTime: Double, userPosition: SIMD3<Float>) {
        stateTimer += deltaTime

        switch currentState {
        case .idle:
            handleIdleState(userPosition: userPosition)
        case .following:
            handleFollowingState(userPosition: userPosition)
        case .playing:
            handlePlayingState()
        case .resting:
            handleRestingState()
        case .responding:
            handleRespondingState()
        }
    }

    private func handleIdleState(userPosition: SIMD3<Float>) {
        // Occasionally look around
        if stateTimer > 3.0 {
            lookAtRandomPoint()
            stateTimer = 0
        }

        // If user is far, start following
        let distance = length(userPosition - companion.position)
        if distance > 2.0 {
            transitionTo(.following)
        }
    }

    private func handleFollowingState(userPosition: SIMD3<Float>) {
        let distance = length(userPosition - companion.position)

        // Move toward user
        if distance > 1.0 {
            let direction = normalize(userPosition - companion.position)
            let targetPosition = userPosition - direction * 1.0
            moveToward(targetPosition)
        } else {
            transitionTo(.idle)
        }
    }

    private func transitionTo(_ newState: State) {
        currentState = newState
        stateTimer = 0

        switch newState {
        case .idle:
            animator.transitionToIdle()
        case .following:
            animator.playAnimation(named: "walk", loop: true)
        case .playing:
            animator.playAnimation(named: "play", loop: true)
        case .resting:
            animator.playAnimation(named: "rest", loop: true)
        case .responding:
            break // Animation set by trigger
        }
    }
}
```

### Behavior Tree Pattern

```swift
protocol BehaviorNode {
    func evaluate(context: CompanionContext) -> BehaviorResult
}

enum BehaviorResult {
    case success
    case failure
    case running
}

struct CompanionContext {
    var companion: Entity
    var userPosition: SIMD3<Float>
    var energy: Float
    var mood: CompanionMood
    var deltaTime: Double
}

// Sequence: Run children in order until one fails
class SequenceNode: BehaviorNode {
    var children: [BehaviorNode]

    func evaluate(context: CompanionContext) -> BehaviorResult {
        for child in children {
            let result = child.evaluate(context: context)
            if result != .success {
                return result
            }
        }
        return .success
    }
}

// Selector: Run children until one succeeds
class SelectorNode: BehaviorNode {
    var children: [BehaviorNode]

    func evaluate(context: CompanionContext) -> BehaviorResult {
        for child in children {
            let result = child.evaluate(context: context)
            if result == .success {
                return .success
            }
        }
        return .failure
    }
}

// Example leaf nodes
class CheckEnergyNode: BehaviorNode {
    let threshold: Float

    func evaluate(context: CompanionContext) -> BehaviorResult {
        return context.energy > threshold ? .success : .failure
    }
}

class MoveToUserNode: BehaviorNode {
    func evaluate(context: CompanionContext) -> BehaviorResult {
        let distance = length(context.userPosition - context.companion.position)
        if distance < 1.0 {
            return .success
        }
        // Move toward user
        let direction = normalize(context.userPosition - context.companion.position)
        context.companion.position += direction * 0.01
        return .running
    }
}
```

## Spatial Audio for Immersive Companions

### Basic Spatial Audio Setup

```swift
func setupCompanionAudio(_ companion: Entity) {
    // Add spatial audio component
    var spatialAudio = SpatialAudioComponent()
    spatialAudio.gain = 0.8
    spatialAudio.directivity = .beam(focus: 0.5)
    companion.components.set(spatialAudio)
}

func playCompanionSound(_ companion: Entity, soundName: String) async {
    guard let audioResource = try? await AudioFileResource.load(
        named: soundName,
        in: nil,
        inputMode: .spatial,
        loadingStrategy: .preload,
        shouldLoop: false
    ) else { return }

    let audioController = companion.playAudio(audioResource)
}
```

### Ambient and Reactive Audio

```swift
class CompanionAudioManager {
    var companion: Entity
    var ambientController: AudioPlaybackController?

    func startAmbientSounds() async {
        guard let ambient = try? await AudioFileResource.load(
            named: "companion_ambient",
            inputMode: .spatial,
            loadingStrategy: .stream,
            shouldLoop: true
        ) else { return }

        ambientController = companion.playAudio(ambient)
        ambientController?.gain = 0.3
    }

    func playReactionSound(for mood: CompanionMood) async {
        let soundName: String
        switch mood {
        case .happy:
            soundName = "companion_happy"
        case .curious:
            soundName = "companion_curious"
        case .tired:
            soundName = "companion_yawn"
        case .neutral:
            soundName = "companion_chirp"
        }

        guard let sound = try? await AudioFileResource.load(
            named: soundName,
            inputMode: .spatial,
            shouldLoop: false
        ) else { return }

        companion.playAudio(sound)
    }

    func stopAmbient() {
        ambientController?.stop()
        ambientController = nil
    }
}
```

## Entity Lifecycle Management

### Persistent Companion Manager

```swift
@MainActor
class CompanionLifecycleManager: ObservableObject {
    @Published var companion: Entity?
    @Published var isLoaded: Bool = false
    @Published var companionState: CompanionSaveState?

    private var arView: ARView?
    private var anchor: AnchorEntity?

    // MARK: - Lifecycle

    func initialize(arView: ARView) async throws {
        self.arView = arView

        // Create anchor for companion
        anchor = AnchorEntity(plane: .horizontal)
        arView.scene.addAnchor(anchor!)

        // Load companion
        let loadedCompanion = try await Entity.load(named: "Companion")
        companion = loadedCompanion
        anchor?.addChild(loadedCompanion)

        // Restore saved state if available
        if let savedState = loadSavedState() {
            applyState(savedState)
        }

        isLoaded = true
    }

    func suspend() {
        // Save state before suspending
        saveCurrentState()

        // Pause animations
        companion?.availableAnimations.forEach { animation in
            companion?.stopAllAnimations()
        }
    }

    func resume() {
        // Resume idle animation
        if let idle = companion?.availableAnimations.first(where: {
            $0.name?.contains("idle") == true
        }) {
            companion?.playAnimation(idle.repeat())
        }
    }

    func cleanup() {
        saveCurrentState()
        companion?.removeFromParent()
        anchor?.removeFromParent()
        companion = nil
        anchor = nil
        isLoaded = false
    }

    // MARK: - Persistence

    func saveCurrentState() {
        guard let companion = companion else { return }

        let state = CompanionSaveState(
            position: companion.position,
            orientation: companion.orientation,
            energy: companion.components[CompanionComponent.self]?.energy ?? 1.0,
            mood: companion.components[CompanionComponent.self]?.mood ?? .neutral,
            lastInteraction: Date()
        )

        if let encoded = try? JSONEncoder().encode(state) {
            UserDefaults.standard.set(encoded, forKey: "companionState")
        }
    }

    func loadSavedState() -> CompanionSaveState? {
        guard let data = UserDefaults.standard.data(forKey: "companionState"),
              let state = try? JSONDecoder().decode(CompanionSaveState.self, from: data) else {
            return nil
        }
        return state
    }

    func applyState(_ state: CompanionSaveState) {
        companion?.position = state.position
        companion?.orientation = state.orientation

        var component = CompanionComponent()
        component.energy = state.energy
        component.mood = state.mood
        companion?.components.set(component)

        companionState = state
    }
}

struct CompanionSaveState: Codable {
    var position: SIMD3<Float>
    var orientation: simd_quatf
    var energy: Float
    var mood: CompanionMood
    var lastInteraction: Date
}

extension CompanionMood: Codable {}
extension SIMD3: Codable where Scalar: Codable {}
extension simd_quatf: Codable {}
```

### Scene Lifecycle Integration

```swift
import SwiftUI

struct ARCompanionApp: App {
    @StateObject var companionManager = CompanionLifecycleManager()
    @Environment(\.scenePhase) var scenePhase

    var body: some Scene {
        WindowGroup {
            ContentView()
                .environmentObject(companionManager)
                .onChange(of: scenePhase) { oldPhase, newPhase in
                    switch newPhase {
                    case .active:
                        companionManager.resume()
                    case .inactive:
                        companionManager.suspend()
                    case .background:
                        companionManager.saveCurrentState()
                    @unknown default:
                        break
                    }
                }
        }
    }
}
```

## Gesture and Touch Handling

### Touch-Based Interaction

```swift
class CompanionInteractionHandler {
    var arView: ARView
    var companion: Entity?

    init(arView: ARView) {
        self.arView = arView
        setupGestures()
    }

    private func setupGestures() {
        let tapGesture = UITapGestureRecognizer(target: self, action: #selector(handleTap))
        arView.addGestureRecognizer(tapGesture)

        let panGesture = UIPanGestureRecognizer(target: self, action: #selector(handlePan))
        arView.addGestureRecognizer(panGesture)
    }

    @objc func handleTap(_ gesture: UITapGestureRecognizer) {
        let location = gesture.location(in: arView)

        // Check if tapped on companion
        if let hitEntity = arView.entity(at: location),
           hitEntity == companion || hitEntity.isDescendant(of: companion!) {
            onCompanionTapped()
        } else {
            // Raycast to find new position for companion
            if let result = arView.raycast(from: location,
                                           allowing: .estimatedPlane,
                                           alignment: .horizontal).first {
                moveCompanionTo(result.worldTransform.translation)
            }
        }
    }

    @objc func handlePan(_ gesture: UIPanGestureRecognizer) {
        guard let companion = companion else { return }

        let location = gesture.location(in: arView)

        switch gesture.state {
        case .changed:
            if let result = arView.raycast(from: location,
                                           allowing: .estimatedPlane,
                                           alignment: .horizontal).first {
                companion.position = result.worldTransform.translation
            }
        case .ended:
            // Companion reached destination
            onCompanionMoved()
        default:
            break
        }
    }

    func onCompanionTapped() {
        // Trigger interaction response
        companion?.components[CompanionComponent.self]?.isInteracting = true
    }

    func moveCompanionTo(_ position: SIMD3<Float>) {
        // Animate companion to new position
        companion?.move(to: Transform(translation: position),
                       relativeTo: companion?.parent,
                       duration: 1.0)
    }

    func onCompanionMoved() {
        // Play arrival animation
    }
}

// Helper extension
extension simd_float4x4 {
    var translation: SIMD3<Float> {
        SIMD3(columns.3.x, columns.3.y, columns.3.z)
    }
}
```

### RealityUI Integration for 3D Controls

```swift
import RealityUI

class CompanionUIManager {
    var arView: ARView
    var companion: Entity?

    init(arView: ARView) {
        self.arView = arView
        RealityUI.registerComponents()
        RealityUI.enableGestures(.all, on: arView)
    }

    func addInteractionControls() {
        guard let companion = companion else { return }

        // Add a toggle for companion following mode
        let followToggle = RUISwitch()
        followToggle.position = SIMD3(0.3, 0.5, 0)
        followToggle.changedCallback = { [weak self] toggle in
            self?.setFollowMode(toggle.isOn)
        }
        companion.addChild(followToggle)

        // Add mood slider
        let moodSlider = RUISlider(length: 0.5, start: 0.5)
        moodSlider.position = SIMD3(-0.3, 0.5, 0)
        moodSlider.updateCallback = { [weak self] slider, state in
            self?.updateCompanionMood(value: slider.value)
        }
        companion.addChild(moodSlider)
    }

    func setFollowMode(_ enabled: Bool) {
        // Toggle following behavior
    }

    func updateCompanionMood(value: Float) {
        // Map slider value to mood
    }
}
```

## ARView Configuration

### Optimal Configuration for Companions

```swift
func configureARViewForCompanion(_ arView: ARView) {
    // Enable environment texturing for realistic lighting
    let config = ARWorldTrackingConfiguration()
    config.planeDetection = [.horizontal]
    config.environmentTexturing = .automatic
    config.frameSemantics.insert(.personSegmentationWithDepth)

    // Enable people occlusion (companion appears behind real people)
    if ARWorldTrackingConfiguration.supportsFrameSemantics(.personSegmentationWithDepth) {
        arView.environment.sceneUnderstanding.options.insert(.occlusion)
    }

    // Configure rendering
    arView.renderOptions = [
        .disablePersonOcclusion, // Remove if you want occlusion
        .disableMotionBlur
    ]

    // Enable camera exposure adaptation
    arView.environment.lighting.intensityExponent = 1.0

    arView.session.run(config)
}
```

### Debug Visualization

```swift
func enableDebugVisualization(_ arView: ARView, enabled: Bool) {
    if enabled {
        arView.debugOptions = [
            .showFeaturePoints,
            .showAnchorOrigins,
            .showPhysics,
            .showSceneUnderstanding
        ]
    } else {
        arView.debugOptions = []
    }
}
```

## Troubleshooting Guide

### Common Issues and Solutions

**Companion Not Appearing**
```swift
// Ensure anchor is properly configured
let anchor = AnchorEntity(plane: .horizontal, minimumBounds: [0.2, 0.2])

// Check if plane detection is working
arView.session.delegate = self

extension YourClass: ARSessionDelegate {
    func session(_ session: ARSession, didAdd anchors: [ARAnchor]) {
        for anchor in anchors {
            if let planeAnchor = anchor as? ARPlaneAnchor {
                print("Plane detected: \(planeAnchor.extent)")
            }
        }
    }
}
```

**Animation Not Playing**
```swift
// Check available animations
print("Available animations: \(entity.availableAnimations.map { $0.name })")

// Ensure animation resource is valid
guard !entity.availableAnimations.isEmpty else {
    print("No animations found in entity")
    return
}
```

**Performance Issues**
```swift
// Reduce draw calls
entity.generateCollisionShapes(recursive: true) // Do once, not per frame

// Use simpler collision shapes
let simpleShape = ShapeResource.generateSphere(radius: 0.5)
entity.collision = CollisionComponent(shapes: [simpleShape])

// Limit update frequency for AI
class ThrottledCompanionAI {
    var updateInterval: Double = 0.1 // 10 updates per second
    var timeSinceUpdate: Double = 0

    func update(deltaTime: Double) {
        timeSinceUpdate += deltaTime
        if timeSinceUpdate >= updateInterval {
            performUpdate()
            timeSinceUpdate = 0
        }
    }
}
```

**Companion Drifts or Moves Unexpectedly**
```swift
// Use world tracking quality checks
extension YourClass: ARSessionDelegate {
    func session(_ session: ARSession, cameraDidChangeTrackingState camera: ARCamera) {
        switch camera.trackingState {
        case .limited(let reason):
            handleLimitedTracking(reason)
        case .normal:
            resumeNormalOperation()
        case .notAvailable:
            showTrackingUnavailableUI()
        }
    }
}
```

## Best Practices Summary

1. **Always use async loading** for companion models to prevent UI freezes
2. **Register custom components and systems** at app launch, before any RealityKit usage
3. **Save companion state** on app suspension for continuity
4. **Throttle AI updates** to 10-30fps to balance responsiveness and performance
5. **Use spatial audio** to make companions feel present in the space
6. **Handle tracking state changes** gracefully with user feedback
7. **Test on real devices** - simulator limitations affect gesture and tracking accuracy
8. **Implement accessibility** features for inclusive AR experiences

## Resource Links

### Official Apple Documentation
- [RealityKit Overview](https://developer.apple.com/augmented-reality/realitykit/)
- [RealityKit Documentation](https://developer.apple.com/documentation/realitykit)
- [Understanding RealityKit's Modular Architecture](https://developer.apple.com/documentation/visionos/understanding-the-realitykit-modular-architecture)
- [Entity Component System](https://developer.apple.com/documentation/realitykit/implementing-systems-for-entities-in-a-scene)

### Essential WWDC Sessions
- [Building Apps with RealityKit (2019)](https://developer.apple.com/videos/play/wwdc2019/605/)
- [Dive into RealityKit 2 (2021)](https://developer.apple.com/videos/play/wwdc2021/10074/)
- [Build spatial experiences with RealityKit (2023)](https://developer.apple.com/videos/play/wwdc2023/10080/)

### Community Packages
- [RealityActions](https://github.com/migueldeicaza/RealityActions) - Procedural animation framework
- [BodyTracking](https://github.com/Reality-Dev/BodyTracking) - Body tracking utilities
- [FocusEntity](https://github.com/maxxfrazer/FocusEntity) - AR placement indicator
- [RealityUI](https://github.com/maxxfrazer/RealityUI) - 3D UI components
- [HandVector](https://github.com/XanderXu/HandVector) - visionOS hand tracking
- [GoncharKit](https://github.com/gonchar/GoncharKit) - visionOS helper utilities
- [RealityMorpher](https://github.com/Utsira/RealityMorpher) - Blend shape animations

### Sample Projects
- [RealityKit-Sampler](https://github.com/john-rocky/RealityKit-Sampler) - Comprehensive feature samples
- [ImmersiveMoveAndRotate](https://github.com/simonbs/ImmersiveMoveAndRotate) - Gesture handling example
- [SwiftStrike](https://developer.apple.com/documentation/realitykit/swiftstrike_creating_a_game_with_realitykit) - Apple's multiplayer game sample

---

**Skill Version:** 2.0.0-enhanced
**Focus:** AR Companion Development
**Platforms:** iOS 15+, visionOS 1.0+
**Generated by:** Metatron (Enhanced from Skill Seeker output)
