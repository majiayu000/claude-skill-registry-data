---
name: component-workflow
description: Guide the creation of new ECS components following established architectural patterns including component class creation, JSON serialization support, editor UI implementation, dependency injection registration, and documentation. Use when adding new component types to the engine or extending existing component functionality.
---

# Component Workflow

## Overview
This skill provides step-by-step guidance for adding new ECS components to the game engine, ensuring consistency with architectural patterns.

**Current Architecture**: Instance-based `IComponentEditor` with constructor injection (no static methods). Uses `ComponentEditorRegistry.DrawComponent<T>()` for UI framing and leverages UI infrastructure (UIPropertyRenderer, VectorPanel, LayoutDrawer, drag-drop targets).

## When to Use
Invoke this skill when:
- Adding or extending ECS component types
- Implementing component serialization or custom JSON converters
- Creating component editors for the Properties panel
- Understanding ComponentEditorRegistry integration or UI infrastructure patterns

## Table of Contents
1. [Component Creation Workflow](#component-creation-workflow)
   - [Step 1: Create Component Class](#step-1-create-component-class)
   - [Step 2: Implement Serialization Support](#step-2-implement-serialization-support)
   - [Step 3: Create Component Editor](#step-3-create-component-editor)
   - [Step 4: Register Editor in Dependency Injection](#step-4-register-editor-in-dependency-injection)
   - [Step 5: Component Addition via ComponentSelector](#step-5-component-addition-via-componentselector)
   - [Step 6: Create System (if needed)](#step-6-create-system-if-needed)
2. [Common Mistakes](#common-mistakes)
3. [Performance Considerations](#performance-considerations)

## Component Creation Workflow

### Step 1: Create Component Class
**Location**: `Engine/Scene/Components/`

**Guidelines**:
- Components should be data-only classes (without logic, use systems for logic)
- Use properties for data fields
- Provide sensible defaults
- Keep components small and focused
- Prefer value types (structs/record structs) for small components
- Use reference types (classes/records) for larger components
- Matrix/transform calculations are acceptable in components

**Naming Convention**:
- Suffix with "Component": `MyNewComponent`
- Use PascalCase: `AudioSourceComponent`, `TransformComponent`

**Example Component**:
```csharp
namespace Engine.Scene.Components;

public class ParticleEmitterComponent
{
    public int MaxParticles { get; set; } = 100;
    public float EmissionRate { get; set; } = 10.0f;
    public float ParticleLifetime { get; set; } = 2.0f;
    public Vector4 StartColor { get; set; } = Vector4.One;
    public Vector4 EndColor { get; set; } = new Vector4(1, 1, 1, 0);
    public bool IsActive { get; set; } = true;
}
```

**For Small Components** (use record struct):
```csharp
namespace Engine.Scene.Components;

public record struct VelocityComponent(Vector2 Velocity);
```

### Step 2: Implement Serialization Support
**Location**: `Engine/Scene/Serializer/` (if custom converter needed)

**Standard Serialization** (automatic):
Most components work with default JSON serialization. The `SceneSerializer` handles standard properties automatically.

**Custom Serialization** (when needed):
- Complex types (e.g., `TileMapComponent`, `AnimationComponent`)
- Resource references (textures, audio clips)
- Specialized data structures

**Register Converter** (if custom):
Add to `SceneSerializer` or serialization configuration:
```csharp
options.Converters.Add(new ParticleEmitterComponentConverter());
```

### Step 3: Create Component Editor
**Location**: `Editor/ComponentEditors/`

**Guidelines**:
- Implement `IComponentEditor` interface from `Editor.ComponentEditors.Core`
- Use constructor injection for dependencies (services, UI elements)
- Use `ComponentEditorRegistry.DrawComponent<T>()` helper for consistent UI framing
- Leverage UI infrastructure for common patterns:
  - **UIPropertyRenderer** - Automatic type-based rendering for primitives
  - **VectorPanel** - Vector2/Vector3/Vector4 controls with X/Y/Z labels
  - **LayoutDrawer** - Indentation, separators, spacing utilities
  - **ButtonDrawer** - Consistent button styling (Primary, Secondary, Danger)
  - **Drag-Drop Targets** - TextureDropTarget, AudioDropTarget, MeshDropTarget, ModelDropTarget, PrefabDropTarget
- Use `EditorUIConstants` for all UI dimensions and spacing
- Validate input ranges where appropriate

**Example Component Editor (Basic)**:
```csharp
namespace Editor.ComponentEditors;

using ECS;
using Editor.ComponentEditors.Core;
using Editor.UI.Drawers;
using Editor.UI.Elements;
using Engine.Scene.Components;

public class ParticleEmitterComponentEditor : IComponentEditor
{
    public void DrawComponent(Entity entity)
    {
        ComponentEditorRegistry.DrawComponent<ParticleEmitterComponent>("Particle Emitter", entity, e =>
        {
            var component = e.GetComponent<ParticleEmitterComponent>();

            // Use UIPropertyRenderer for automatic type-based rendering
            UIPropertyRenderer.DrawPropertyField("Max Particles", component.MaxParticles,
                newValue => component.MaxParticles = Math.Max(1, (int)newValue));

            // Vector controls for colors
            VectorPanel.DrawVec4Control("Start Color", ref component.StartColor);
            VectorPanel.DrawVec4Control("End Color", ref component.EndColor);
        });
    }
}
```

### Step 4: Register Editor in Dependency Injection
**Location**: `Editor/Program.cs` and `Editor/ComponentEditors/Core/ComponentEditorRegistry.cs`

**All component editors must be registered** to work with the ComponentEditorRegistry system.

**Step 4a: Register Editor in Program.cs**:
```csharp
// In ConfigureServices method
container.Register<ParticleEmitterComponentEditor>(Reuse.Singleton);
```

**If editor has dependencies, register those too**:
```csharp
// Dependencies are usually already registered, but verify:
container.Register<TextureDropTarget>(Reuse.Singleton);
container.Register<AudioDropTarget>(Reuse.Singleton);
// ... etc
```

**Step 4b: Add Editor to ComponentEditorRegistry**:
```csharp
// In ComponentEditorRegistry.cs - use primary constructor
public class ComponentEditorRegistry(
    // ... other existing editors
    ParticleEmitterComponentEditor particleEmitterComponentEditor) // Add parameter
{
    private readonly Dictionary<Type, IComponentEditor> _editors = new()
    {
        // ... other mappings
        { typeof(ParticleEmitterComponent), particleEmitterComponentEditor } // Add mapping
    };
}
```

**Verify Registration**:
After completing Steps 4a and 4b, verify your component editor is properly registered:
1. Build the project: `dotnet build`
2. Launch the editor: `cd Editor && dotnet run`
3. Create or open a scene
4. Select an entity
5. Click "Add Component" in the Properties panel
6. Search for your component name - it should appear in the list
7. Add the component - the editor UI should render using your `DrawComponent()` implementation

If the component doesn't appear or the UI doesn't render, check:
- DI registration in `Program.cs` (Step 4a)
- ComponentEditorRegistry constructor parameter and dictionary entry (Step 4b)
- Build succeeded without errors

### Step 5: Component Addition via ComponentSelector
**Location**: `Editor/UI/Elements/ComponentSelector.cs` (automatic)

**How Component Addition Works**:
The `ComponentSelector` UI element automatically provides a searchable list of all available components. It's already integrated into the Properties Panel and Entity Context Menu.

**No manual integration needed** - components are added via reflection-based component discovery in the ComponentSelector.

**To verify component is discoverable**:
1. Component must be in `Engine.Scene.Components` namespace
2. Component must implement `IComponent` interface (or be a recognized component type)
3. Editor will automatically show "Add Component" button in Properties Panel
4. ComponentSelector will list your new component

### Step 6: Create System (if needed)
**Location**: `Engine/Scene/Systems/`

**When to Create a System**:
- Component requires per-frame updates
- Component has logic that operates on entities
- Component needs to interact with rendering, physics, or other systems

**Example System**:
```csharp
namespace Engine.Scene.Systems;

public class ParticleSystem : ISystem
{
    // Priority ranges: 0-99 = early (input, physics), 100-199 = game logic,
    // 200+ = rendering/post-processing. Lower values execute first.
    // Common values: Physics=100, Game Logic=150, Rendering=200, UI=300
    public int Priority => 150; // Execute before rendering

    public void OnAttach(Scene scene) { }

    public void OnDetach(Scene scene) { }

    public void OnUpdate(Scene scene, TimeSpan deltaTime)
    {
        // Update particle logic here
    }

    public void OnEvent(Scene scene, Event e) { }
}
```

**Register System**:
```csharp
// In SceneSystemRegistry.cs
public static void RegisterDefaultSystems(SystemManager systemManager, IServiceProvider services)
{
    // ... existing systems
    systemManager.AddSystem(services.GetRequiredService<ParticleSystem>());
}

// In Program.cs (Engine or Editor)
container.Register<ParticleSystem>(Reuse.Singleton);
```

## Common Mistakes

Avoid these frequent pitfalls when creating components:

### ❌ Forgetting DI Registration
**Problem**: Component editor doesn't appear in Properties panel after adding component to entity.

**Cause**: Missing registration in `Program.cs` (Step 4a) or missing entry in `ComponentEditorRegistry` constructor (Step 4b).

**Solution**: Follow the verification checklist in Step 4. Check both registration points.

### ❌ Using Static Methods Instead of Instance Methods
**Problem**: Cannot inject dependencies, breaks DI pattern, makes testing difficult.
**Solution**: Use instance methods with constructor injection. Component editors must implement `IComponentEditor` interface with injected dependencies (e.g., `TextureDropTarget`, `AudioDropTarget`).

### ❌ Skipping `[JsonIgnore]` on Runtime Data
**Problem**: Runtime data (cached objects, computed values) gets serialized, bloating save files.
**Solution**: Mark runtime-only properties with `[JsonIgnore]` attribute.
```csharp
public string AudioClipPath { get; set; } = string.Empty;  // Serialized
[JsonIgnore] public AudioClip? LoadedClip { get; set; }    // Runtime only
```

### ❌ Putting Game Logic in Components
**Problem**: Violates ECS architecture. Components are data-only.
**Solution**: Move logic to Systems. Components store data, Systems process behavior.
```csharp
// Component: Data only (properties + defaults)
public class HealthComponent { public float Health { get; set; } = 100f; }
// System: Logic (damage processing, death handling, etc.)
public class HealthSystem : ISystem { /* OnUpdate handles logic */ }
```

## Performance Considerations

- **Avoid allocations**: Don't create objects in component properties
- **Keep components small**: Large components hurt cache coherency
- **Use value types**: When component is small (<= 16 bytes)
- **Minimize references**: Each reference is a pointer chase
- **Group related data**: Components accessed together should be similar size
