---
name: editor-component-editors
description: Create ECS component editors using IComponentEditor interface, ComponentEditorRegistry.DrawComponent wrapper, VectorPanel for vectors, and UIPropertyRenderer for simple properties. Covers registration in DI container and manual change detection patterns.
---

# Editor Component Editors

## Overview

Component editors render ECS component properties in the editor's Properties panel. They use the `IComponentEditor` interface with static utility methods for consistent UI styling.

## When to Use This Skill

- Creating a new component editor for an ECS component
- Editing vector properties (Vector2/Vector3) with axis color coding
- Editing primitive properties (int, float, bool, string)
- Need collapsible component UI with remove button
- Building custom property controls for components

---

## Core Architecture

### IComponentEditor Interface

```csharp
// Editor/ComponentEditors/Core/IComponentEditor.cs
public interface IComponentEditor
{
    void DrawComponent(Entity entity);
}
```

**Key Points:**
- Takes `Entity`, not the component directly
- Component is retrieved inside using `entity.GetComponent<T>()`
- No return value - mutates component properties directly

---

## Essential Pattern: ComponentEditorRegistry.DrawComponent<T>()

**Every component editor uses this static wrapper method** for consistent UI:

```csharp
ComponentEditorRegistry.DrawComponent<ComponentType>("Display Name", entity, entity =>
{
    var component = entity.GetComponent<ComponentType>();

    // Draw property editors here
});
```

**What it provides:**
- ✅ Collapsible tree node (DefaultOpen)
- ✅ Component name header
- ✅ Remove component button (-)
- ✅ Consistent padding and spacing
- ✅ Framed appearance
- ✅ Only renders if entity has the component

**Implementation (ComponentEditorRegistry.cs:60-87):**
- Uses `ImGuiTreeNodeFlags` for styling
- Adds remove button in top-right corner
- Calls your lambda only if component exists
- Handles tree pop automatically

---

## Property Editing Utilities

### 1. UIPropertyRenderer.DrawPropertyField()

**Best for:** Simple primitive properties (int, float, bool, string)

```csharp
UIPropertyRenderer.DrawPropertyField("Label", currentValue,
    newValue => component.Property = (TypeCast)newValue);
```

**Features:**
- Automatic type detection via `FieldEditorRegistry`
- Consistent label/input width ratio (33%/67%)
- Supports: `int`, `float`, `double`, `bool`, `string`, `Vector2`, `Vector3`, `Vector4`
- Boxing-based (object newValue)

**Example (CameraComponentEditor.cs:22-23):**
```csharp
UIPropertyRenderer.DrawPropertyField("Primary", cameraComponent.Primary,
    newValue => cameraComponent.Primary = (bool)newValue);
```

---

### 2. VectorPanel Static Methods

**Best for:** Vector properties needing axis color coding or reset buttons

#### Vector3 with Axis Colors

```csharp
var newPosition = component.Position;
VectorPanel.DrawVec3Control("Position", ref newPosition);

if (newPosition != component.Position)
    component.Position = newPosition;
```

**Features:**
- Colored axis buttons: X (red), Y (green), Z (blue)
- Click button to reset axis to default value
- Drag float inputs for each axis
- Consistent 33%/67% label/input ratio

**With Reset Value (TransformComponentEditor.cs:32):**
```csharp
var newScale = component.Scale;
VectorPanel.DrawVec3Control("Scale", ref newScale, resetValue: 1.0f);

if (newScale != component.Scale)
    component.Scale = newScale;
```

#### Vector2 Controls

```csharp
var newSize = component.Size;
VectorPanel.DrawVec2Control("Size", ref newSize);

if (newSize != component.Size)
    component.Size = newSize;
```

**VectorPanel.cs methods:**
- `DrawVec3Control(string label, ref Vector3 values, float resetValue = 0.0f)`
- `DrawVec2Control(string label, ref Vector2 values, float resetValue = 0.0f)`

---

### 3. LayoutDrawer.DrawComboBox()

**Best for:** Enum or string selection dropdowns

```csharp
private static readonly string[] ProjectionTypeStrings = { "Perspective", "Orthographic" };

LayoutDrawer.DrawComboBox("Projection",
    ProjectionTypeStrings[(int)camera.ProjectionType],
    ProjectionTypeStrings,
    selectedType =>
    {
        camera.ProjectionType = selectedType switch
        {
            "Perspective" => ProjectionType.Perspective,
            "Orthographic" => ProjectionType.Orthographic,
            _ => camera.ProjectionType
        };
    });
```

---

## Complete Working Examples

### Example 1: Simple Component Editor (Camera)

```csharp
// CameraComponentEditor.cs (simplified)
using ECS;
using Editor.ComponentEditors.Core;
using Editor.UI.Drawers;
using Editor.UI.Elements;
using Engine.Scene.Components;

namespace Editor.ComponentEditors;

public class CameraComponentEditor : IComponentEditor
{
    private static readonly string[] ProjectionTypeStrings = { "Perspective", "Orthographic" };

    public void DrawComponent(Entity e)
    {
        ComponentEditorRegistry.DrawComponent<CameraComponent>("Camera", e, entity =>
        {
            var camera = entity.GetComponent<CameraComponent>().Camera;

            UIPropertyRenderer.DrawPropertyField("Size", camera.OrthographicSize,
                newValue => camera.OrthographicSize = (float)newValue);

            UIPropertyRenderer.DrawPropertyField("Near", camera.OrthographicNear,
                newValue => camera.OrthographicNear = (float)newValue);

            UIPropertyRenderer.DrawPropertyField("Far", camera.OrthographicFar,
                newValue => camera.OrthographicFar = (float)newValue);
        });
    }
}
```

---

### Example 2: Vector Component Editor (Transform)

```csharp
// TransformComponentEditor.cs (actual implementation)
using ECS;
using Editor.ComponentEditors.Core;
using Engine.Math;
using Engine.Scene.Components;

namespace Editor.ComponentEditors;

public class TransformComponentEditor : IComponentEditor
{
    public void DrawComponent(Entity e)
    {
        ComponentEditorRegistry.DrawComponent<TransformComponent>("Transform", e, entity =>
        {
            var tc = entity.GetComponent<TransformComponent>();

            // Translation
            var newTranslation = tc.Translation;
            VectorPanel.DrawVec3Control("Translation", ref newTranslation);
            if (newTranslation != tc.Translation)
                tc.Translation = newTranslation;

            // Rotation (convert radians to degrees for UI)
            var rotationRadians = tc.Rotation;
            Vector3 rotationDegrees = MathHelpers.ToDegrees(rotationRadians);
            VectorPanel.DrawVec3Control("Rotation", ref rotationDegrees);
            var newRotationRadians = MathHelpers.ToRadians(rotationDegrees);
            if (newRotationRadians != tc.Rotation)
                tc.Rotation = newRotationRadians;

            // Scale (reset to 1.0 instead of 0.0)
            var newScale = tc.Scale;
            VectorPanel.DrawVec3Control("Scale", ref newScale, resetValue: 1.0f);
            if (newScale != tc.Scale)
                tc.Scale = newScale;
        });
    }
}
```

**Key Pattern:** Copy to temp variable → modify → check if changed → assign back

---

### Example 3: Complex Component with Multiple Property Types

```csharp
public class MyComponentEditor : IComponentEditor
{
    public void DrawComponent(Entity e)
    {
        ComponentEditorRegistry.DrawComponent<MyComponent>("My Component", e, entity =>
        {
            var component = entity.GetComponent<MyComponent>();

            // Simple properties with UIPropertyRenderer
            UIPropertyRenderer.DrawPropertyField("Enabled", component.IsEnabled,
                newValue => component.IsEnabled = (bool)newValue);

            UIPropertyRenderer.DrawPropertyField("Speed", component.Speed,
                newValue => component.Speed = (float)newValue);

            // Vector with axis controls
            var newPosition = component.Position;
            VectorPanel.DrawVec3Control("Position", ref newPosition);
            if (newPosition != component.Position)
                component.Position = newPosition;

            // Dropdown selection
            string[] options = { "Option1", "Option2", "Option3" };
            LayoutDrawer.DrawComboBox("Mode", options[component.ModeIndex], options,
                selected =>
                {
                    component.ModeIndex = Array.IndexOf(options, selected);
                });

            // Custom UI elements with Drawers
            if (ButtonDrawer.DrawButton("Reset", ButtonDrawer.ButtonType.Primary))
            {
                component.Reset();
            }
        });
    }
}
```

---

## Dependency Injection Registration

Component editors are registered in the DI container and injected into `ComponentEditorRegistry`.

### Registration (Program.cs or similar)

```csharp
// Register individual component editors
container.Register<TransformComponentEditor>(Reuse.Singleton);
container.Register<CameraComponentEditor>(Reuse.Singleton);
container.Register<MyComponentEditor>(Reuse.Singleton);

// ComponentEditorRegistry constructor receives all editors
container.Register<ComponentEditorRegistry>(Reuse.Singleton);
```

### ComponentEditorRegistry Constructor Pattern

```csharp
public class ComponentEditorRegistry(
    TransformComponentEditor transformComponentEditor,
    CameraComponentEditor cameraComponentEditor,
    MyComponentEditor myComponentEditor) : IComponentEditorRegistry  // Add your editor here
{
    private readonly Dictionary<Type, IComponentEditor> _editors = new()
    {
        { typeof(TransformComponent), transformComponentEditor },
        { typeof(CameraComponent), cameraComponentEditor },
        { typeof(MyComponent), myComponentEditor }  // Register component type
    };

    public void DrawAllComponents(Entity entity)
    {
        foreach (var (componentType, editor) in _editors)
        {
            editor.DrawComponent(entity);
        }
    }
}
```

---

## Change Detection Patterns

### Pattern 1: Copy-Modify-Assign (for VectorPanel)

```csharp
var oldValue = component.Position;
VectorPanel.DrawVec3Control("Position", ref oldValue);

if (oldValue != component.Position)  // Value comparison
    component.Position = oldValue;
```

**Why:** VectorPanel modifies the `ref` parameter directly, so we need manual change detection.

---

### Pattern 2: Callback Assignment (for UIPropertyRenderer)

```csharp
UIPropertyRenderer.DrawPropertyField("Speed", component.Speed,
    newValue => component.Speed = (float)newValue);
```

**Why:** UIPropertyRenderer only calls callback if value changed. No manual check needed.

---

## Anti-Patterns

### ❌ Anti-Pattern 1: Not Using DrawComponent Wrapper

```csharp
// ❌ WRONG - Manual tree node management
public void DrawComponent(Entity e)
{
    if (ImGui.TreeNode("My Component"))
    {
        var component = e.GetComponent<MyComponent>();
        // ... draw properties
        ImGui.TreePop();
    }
}

// ✅ CORRECT - Use DrawComponent wrapper
public void DrawComponent(Entity e)
{
    ComponentEditorRegistry.DrawComponent<MyComponent>("My Component", e, entity =>
    {
        var component = entity.GetComponent<MyComponent>();
        // ... draw properties
    });
}
```

**Why:** DrawComponent provides consistent styling, remove button, and safety checks.

---

### ❌ Anti-Pattern 2: Direct ImGui Calls for Vectors

```csharp
// ❌ WRONG - Raw ImGui calls
ImGui.DragFloat3("Position", ref component.Position);

// ✅ CORRECT - Use VectorPanel for axis colors and reset buttons
var newPosition = component.Position;
VectorPanel.DrawVec3Control("Position", ref newPosition);
if (newPosition != component.Position)
    component.Position = newPosition;
```

**Why:** VectorPanel provides axis color coding, reset buttons, and consistent styling.

---

### ❌ Anti-Pattern 3: Direct Component Property Mutation with ref

```csharp
// ❌ WRONG - Modifying component property directly
VectorPanel.DrawVec3Control("Position", ref component.Position);  // May not work as expected

// ✅ CORRECT - Copy to temp variable first
var newPosition = component.Position;
VectorPanel.DrawVec3Control("Position", ref newPosition);
if (newPosition != component.Position)
    component.Position = newPosition;
```

**Why:** Component properties may be getters with backing fields or have change tracking.

---

### ❌ Anti-Pattern 4: Forgetting DI Registration

```csharp
// ❌ WRONG - Editor won't be found at runtime
public class MyComponentEditor : IComponentEditor { ... }
// (not registered in Program.cs)

// ✅ CORRECT - Register in DI container
container.Register<MyComponentEditor>(Reuse.Singleton);

// AND add to ComponentEditorRegistry constructor + dictionary
```

---

## Workflow: Creating a New Component Editor

### Step 1: Create Editor Class

```csharp
// Editor/ComponentEditors/MyComponentEditor.cs
using ECS;
using Editor.ComponentEditors.Core;
using Editor.Panels;
using Editor.UI.Drawers;
using Editor.UI.Elements;
using Engine.Scene.Components;

namespace Editor.ComponentEditors;

public class MyComponentEditor : IComponentEditor
{
    public void DrawComponent(Entity e)
    {
        ComponentEditorRegistry.DrawComponent<MyComponent>("My Component", e, entity =>
        {
            var component = entity.GetComponent<MyComponent>();

            // TODO: Add property editors here
        });
    }
}
```

### Step 2: Register in DI Container (Program.cs)

```csharp
// In editor startup
container.Register<MyComponentEditor>(Reuse.Singleton);
```

### Step 3: Add to ComponentEditorRegistry

```csharp
// ComponentEditorRegistry.cs - use primary constructor
public class ComponentEditorRegistry(
    // ... existing editors
    MyComponentEditor myComponentEditor) // Add parameter
{
    private readonly Dictionary<Type, IComponentEditor> _editors = new()
    {
        // ... existing registrations
        { typeof(MyComponent), myComponentEditor }  // Add to dictionary
    };
}
```

### Step 4: Implement Property Editors

Choose the appropriate method for each property type:

```csharp
// Primitives: Use UIPropertyRenderer
UIPropertyRenderer.DrawPropertyField("Health", component.Health,
    newValue => component.Health = (int)newValue);

// Vectors: Use VectorPanel
var newPos = component.Position;
VectorPanel.DrawVec3Control("Position", ref newPos);
if (newPos != component.Position)
    component.Position = newPos;

// Enums: Use LayoutDrawer
string[] options = Enum.GetNames<MyEnum>();
LayoutDrawer.DrawComboBox("Mode", options[(int)component.Mode], options,
    selected => component.Mode = (MyEnum)Array.IndexOf(options, selected));
```

---

## Available UI Utilities

### From UIPropertyRenderer
- `DrawPropertyField(string label, object value, Action<object> onValueChanged)`
  - Supports: int, float, double, bool, string, Vector2, Vector3, Vector4
  - Uses FieldEditorRegistry internally

### From VectorPanel
- `DrawVec3Control(string label, ref Vector3 values, float resetValue = 0.0f)`
- `DrawVec2Control(string label, ref Vector2 values, float resetValue = 0.0f)`

### From LayoutDrawer
- `DrawComboBox(string label, string current, string[] options, Action<string> onSelected)`

### From ButtonDrawer
- `DrawButton(string label, ButtonType type = ButtonType.Default)` → returns bool
- `DrawButton(string label, float width, float height, Action? onClick = null)`

### From TextDrawer
- `DrawErrorText(string text)`
- `DrawWarningText(string text)`
- `DrawSuccessText(string text)`

### From ModalDrawer
- `RenderConfirmationModal(string id, ref bool show, string message, Action onConfirm)`

---

## Summary

**Component Editor Checklist:**
1. ✅ Implement `IComponentEditor` interface
2. ✅ Use `ComponentEditorRegistry.DrawComponent<T>()` wrapper
3. ✅ Use `VectorPanel` for vectors (axis colors, reset buttons)
4. ✅ Use `UIPropertyRenderer` for simple primitives
5. ✅ Use `LayoutDrawer` for dropdowns
6. ✅ Manual change detection for ref parameters
7. ✅ Register in DI container (`Program.cs`)
8. ✅ Add to `ComponentEditorRegistry` constructor + dictionary

**Key Files:**
- `Editor/ComponentEditors/Core/IComponentEditor.cs` - Interface
- `Editor/ComponentEditors/Core/ComponentEditorRegistry.cs` - Registry and wrapper
- `Editor/Panels/VectorPanel.cs` - Vector controls
- `Editor/UI/Elements/UIPropertyRenderer.cs` - Property field wrapper
- `Editor/UI/Drawers/LayoutDrawer.cs` - Combo boxes
- `Editor/ComponentEditors/TransformComponentEditor.cs` - Vector example
- `Editor/ComponentEditors/CameraComponentEditor.cs` - Mixed properties example
