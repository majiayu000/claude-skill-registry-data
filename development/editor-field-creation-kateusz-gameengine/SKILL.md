---
name: editor-field-creation
description: Implement IFieldEditor interface for custom type rendering in script inspector. Covers reflection-based field editing, FieldEditorRegistry registration, boxing/unboxing patterns, and extending the field editor system for new types.
---

# Editor Field Editors (IFieldEditor)

## Overview

Field Editors (`IFieldEditor`) provide **runtime polymorphic rendering** for script properties discovered via reflection. They use a **non-generic, boxing-based interface** to handle arbitrary types at runtime.

## When to Use This Skill

- **Creating custom field editors** for new types (Quaternion, Color, custom structs)
- Understanding how script properties are rendered in Script Inspector
- Extending `FieldEditorRegistry` with new type support
- Working with `UIPropertyRenderer.DrawPropertyField()` infrastructure
- **NOT for component editors**

---

## Purpose & Context

### Two Different Systems

The engine has **two separate property editing systems**:

| System | Purpose | Interface | Usage |
|--------|---------|-----------|-------|
| **IFieldEditor** | Runtime script properties (reflection) | `IFieldEditor` (non-generic, boxing) | Script Inspector |
| **VectorPanel/UIPropertyRenderer** | Compile-time component properties | Static methods | Component Editors |

---

## Core Interface

```csharp
// Editor/UI/FieldEditors/IFieldEditor.cs
public interface IFieldEditor
{
    /// <summary>
    /// Draws the editor UI for the field and returns true if the value was changed.
    /// </summary>
    /// <param name="label">The ImGui label for the field (should include unique ID)</param>
    /// <param name="value">The current field value (boxed)</param>
    /// <param name="newValue">The new value if changed</param>
    /// <returns>True if the value was modified by user interaction</returns>
    bool Draw(string label, object value, out object newValue);
}
```

**Key Characteristics:**
- ❌ **Not generic** - no `IFieldEditor<T>`
- ✅ **Boxing-based** - uses `object` for value and newValue
- ✅ **Returns bool** - true if user changed the value
- ✅ **Out parameter** - newValue is the modified value

---

## Built-in Field Editors

### Primitive Type Editors

| Type | Implementation | File |
|------|---------------|------|
| `int` | IntFieldEditor | IntFieldEditor.cs |
| `float` | FloatFieldEditor | FloatFieldEditor.cs |
| `double` | DoubleFieldEditor | DoubleFieldEditor.cs |
| `bool` | BoolFieldEditor | BoolFieldEditor.cs |
| `string` | StringFieldEditor | StringFieldEditor.cs |

### Vector Type Editors

| Type | Implementation | File |
|------|---------------|------|
| `Vector2` | Vector2FieldEditor | Vector2FieldEditor.cs |
| `Vector3` | Vector3FieldEditor | Vector3FieldEditor.cs |
| `Vector4` | Vector4FieldEditor | Vector4FieldEditor.cs |

All registered in `FieldEditorRegistry` static dictionary.

---

## FieldEditorRegistry

**Central registry mapping types to editors:**

```csharp
// Editor/UI/FieldEditors/FieldEditorRegistry.cs
public static class FieldEditorRegistry
{
    private static readonly Dictionary<Type, IFieldEditor> _editors = new()
    {
        { typeof(int), new IntFieldEditor() },
        { typeof(float), new FloatFieldEditor() },
        { typeof(double), new DoubleFieldEditor() },
        { typeof(bool), new BoolFieldEditor() },
        { typeof(string), new StringFieldEditor() },
        { typeof(Vector2), new Vector2FieldEditor() },
        { typeof(Vector3), new Vector3FieldEditor() },
        { typeof(Vector4), new Vector4FieldEditor() }
    };

    public static IFieldEditor? GetEditor(Type type)
    {
        return _editors.TryGetValue(type, out var editor) ? editor : null;
    }

    public static bool HasEditor(Type type)
    {
        return _editors.ContainsKey(type);
    }
}
```

**Usage Pattern (ScriptComponentEditor.cs:111-113):**
```csharp
var editor = FieldEditorRegistry.GetEditor(fieldType);
if (editor != null)
    return editor.Draw(label, value, out newValue);
```

---

## Implementing a Custom Field Editor

### Example 1: Simple Primitive Editor (IntFieldEditor)

```csharp
// Editor/UI/FieldEditors/IntFieldEditor.cs
using ImGuiNET;

namespace Editor.UI.FieldEditors;

public class IntFieldEditor : IFieldEditor
{
    public bool Draw(string label, object value, out object newValue)
    {
        var intValue = (int)value;  // Unbox
        var changed = ImGui.DragInt(label, ref intValue);
        newValue = intValue;  // Box
        return changed;
    }
}
```

**Pattern:**
1. Unbox `object value` to concrete type
2. Call ImGui widget with `ref` parameter
3. Box result into `out object newValue`
4. Return changed flag

---

### Example 2: Vector Editor (Vector3FieldEditor)

```csharp
// Editor/UI/FieldEditors/Vector3FieldEditor.cs
using System.Numerics;
using ImGuiNET;

namespace Editor.UI.FieldEditors;

public class Vector3FieldEditor : IFieldEditor
{
    public bool Draw(string label, object value, out object newValue)
    {
        var v = (Vector3)value;  // Unbox
        var changed = ImGui.DragFloat3(label, ref v);
        newValue = v;  // Box
        return changed;
    }
}
```

---

### Example 3: Custom Type Editor (Quaternion)

```csharp
using System.Numerics;
using ImGuiNET;

namespace Editor.UI.FieldEditors;

public class QuaternionFieldEditor : IFieldEditor
{
    public bool Draw(string label, object value, out object newValue)
    {
        var quat = (Quaternion)value;

        // Convert to Euler angles for editing
        var euler = QuaternionToEuler(quat);
        var changed = ImGui.DragFloat3(label, ref euler);

        if (changed)
        {
            // Convert back to quaternion
            newValue = EulerToQuaternion(euler);
        }
        else
        {
            newValue = quat;
        }

        return changed;
    }

    private static Vector3 QuaternionToEuler(Quaternion q)
    {
        // Implementation...
    }

    private static Quaternion EulerToQuaternion(Vector3 euler)
    {
        // Implementation...
    }
}
```

---

## Registering Custom Field Editors

### Step 1: Implement IFieldEditor

```csharp
public class MyCustomTypeEditor : IFieldEditor
{
    public bool Draw(string label, object value, out object newValue)
    {
        var typed = (MyCustomType)value;

        // Draw UI and modify 'typed'
        bool changed = /* ... */;

        newValue = typed;
        return changed;
    }
}
```

### Step 2: Register in FieldEditorRegistry

**Option A: Add to static dictionary (modify FieldEditorRegistry.cs)**

```csharp
private static readonly Dictionary<Type, IFieldEditor> _editors = new()
{
    // ... existing editors
    { typeof(MyCustomType), new MyCustomTypeEditor() }
};
```

**Option B: Add runtime registration method (extensible)**

```csharp
// Add to FieldEditorRegistry.cs
public static void RegisterEditor(Type type, IFieldEditor editor)
{
    _editors[type] = editor;
}

// Usage in initialization code
FieldEditorRegistry.RegisterEditor(typeof(Quaternion), new QuaternionFieldEditor());
```

---

## Usage in Script Inspector

### How ScriptComponentEditor Uses IFieldEditor

```csharp
// ScriptComponentEditor.cs (simplified)
private bool TryDrawFieldEditor(string label, Type type, object value, out object newValue)
{
    newValue = value;

    var editor = FieldEditorRegistry.GetEditor(type);
    if (editor != null)
        return editor.Draw(label, value, out newValue);

    // Fallback: unsupported type
    ImGui.TextDisabled($"Unsupported type: {type.Name}");
    return false;
}

// Called per script field
if (TryDrawFieldEditor(fieldLabel, fieldType, fieldValue, out var newValue))
{
    script.SetFieldValue(fieldName, newValue);  // Reflection-based assignment
}
```

**Flow:**
1. Script reflection discovers field type at runtime
2. `FieldEditorRegistry.GetEditor(type)` looks up editor
3. If found, call `editor.Draw()` with boxed value
4. If changed, use reflection to assign new value back to script field

---

## Usage with UIPropertyRenderer

### UIPropertyRenderer.DrawPropertyField()

**Convenience wrapper** for simple use cases:

```csharp
// UIPropertyRenderer.cs:26-56
public static bool DrawPropertyField(string label, object? value, Action<object> onValueChanged)
{
    if (value == null)
        return false;

    var valueType = value.GetType();
    var editor = FieldEditorRegistry.GetEditor(valueType);

    if (editor == null)
    {
        DrawPropertyRow(label, () =>
        {
            ImGui.TextDisabled($"Unsupported type: {valueType.Name}");
        });
        return false;
    }

    bool changed = false;
    DrawPropertyRow(label, () =>
    {
        var inputLabel = $"##{label}";
        if (editor.Draw(inputLabel, value, out var newValue))
        {
            onValueChanged(newValue);
            changed = true;
        }
    });

    return changed;
}
```

**Usage (CameraComponentEditor.cs:22-23):**
```csharp
UIPropertyRenderer.DrawPropertyField("Primary", cameraComponent.Primary,
    newValue => cameraComponent.Primary = (bool)newValue);
```

**What it adds:**
- Label/input column layout (33%/67% ratio)
- Null checking
- Fallback message for unsupported types
- Callback pattern instead of out parameter

---

## Complete Example: Color Field Editor

```csharp
using System.Numerics;
using ImGuiNET;

namespace Editor.UI.FieldEditors;

/// <summary>
/// Field editor for System.Drawing.Color or custom Color struct.
/// Renders as RGB sliders with preview.
/// </summary>
public class ColorFieldEditor : IFieldEditor
{
    public bool Draw(string label, object value, out object newValue)
    {
        // Assume Color struct with R, G, B, A float properties (0-1 range)
        var color = (Color)value;

        // Convert to Vector4 for ImGui
        var vec4 = new Vector4(color.R, color.G, color.B, color.A);

        bool changed = ImGui.ColorEdit4(label, ref vec4,
            ImGuiColorEditFlags.Float |
            ImGuiColorEditFlags.AlphaPreview);

        if (changed)
        {
            newValue = new Color(vec4.X, vec4.Y, vec4.Z, vec4.W);
        }
        else
        {
            newValue = color;
        }

        return changed;
    }
}

// Register in FieldEditorRegistry
{ typeof(Color), new ColorFieldEditor() }
```

---

## Performance Considerations

### Boxing Overhead

**IFieldEditor uses boxing** for flexibility:

```csharp
var intValue = (int)value;  // Unboxing allocation
newValue = intValue;  // Boxing allocation
```

**Impact:**
- 2 allocations per field per frame rendered
- Acceptable for script inspector (low frequency, few fields)
- **NOT suitable for hot loops** (use VectorPanel static methods instead)

### When to Use Each System

| Scenario | Use This | Reason |
|----------|----------|--------|
| Script public fields (reflection) | IFieldEditor | Type unknown at compile time |
| Component properties (known types) | VectorPanel / UIPropertyRenderer | No boxing, compile-time type safety |
| Hot loop / per-frame rendering | Static methods | Zero allocation |
| Custom type in scripts | IFieldEditor | Extensible via registry |
| Custom type in components | Custom static utility | Performance |

---

## Anti-Patterns

### ❌ Anti-Pattern 1: Using IFieldEditor for Component Editors

```csharp
// ❌ WRONG - Unnecessary boxing for known types
public class TransformComponentEditor : IComponentEditor
{
    private readonly IFieldEditor _vector3Editor;

    public void DrawComponent(Entity e)
    {
        var tc = e.GetComponent<TransformComponent>();
        object pos = tc.Position;  // Box
        if (_vector3Editor.Draw("Position", pos, out var newPos))
        {
            tc.Position = (Vector3)newPos;  // Unbox
        }
    }
}

// ✅ CORRECT - Use static VectorPanel methods
public class TransformComponentEditor : IComponentEditor
{
    public void DrawComponent(Entity e)
    {
        var tc = e.GetComponent<TransformComponent>();
        var newPos = tc.Position;
        VectorPanel.DrawVec3Control("Position", ref newPos);
        if (newPos != tc.Position)
            tc.Position = newPos;
    }
}
```

**Why:** Component types are known at compile time. Use static methods to avoid boxing.

---

### ❌ Anti-Pattern 2: Forgetting to Register Editor

```csharp
// ❌ WRONG - Editor implemented but not registered
public class QuaternionFieldEditor : IFieldEditor { ... }

// Script inspector will show "Unsupported type: Quaternion"

// ✅ CORRECT - Register in FieldEditorRegistry
{ typeof(Quaternion), new QuaternionFieldEditor() }
```

---

### ❌ Anti-Pattern 3: Mutating Boxed Value Reference

```csharp
// ❌ WRONG - Mutating unboxed value reference
public bool Draw(string label, object value, out object newValue)
{
    var vec = (Vector3)value;
    ImGui.DragFloat("X", ref vec.X);  // Modifies local copy
    newValue = value;  // Returns original!
    return true;
}

// ✅ CORRECT - Box the modified value
public bool Draw(string label, object value, out object newValue)
{
    var vec = (Vector3)value;
    bool changed = ImGui.DragFloat3(label, ref vec);
    newValue = vec;  // Box the modified value
    return changed;
}
```

---

### ❌ Anti-Pattern 4: Not Handling Null Values

```csharp
// ❌ WRONG - Crashes on null reference types
public bool Draw(string label, object value, out object newValue)
{
    var str = (string)value;  // NullReferenceException if value is null
    // ...
}

// ✅ CORRECT - Handle null for reference types
public bool Draw(string label, object value, out object newValue)
{
    var str = (value as string) ?? string.Empty;
    // ...
    newValue = str;
    return changed;
}
```

---

## Workflow: Adding a Custom Field Editor

### Step 1: Create Field Editor Class

```csharp
// Editor/UI/FieldEditors/MyTypeFieldEditor.cs
using ImGuiNET;

namespace Editor.UI.FieldEditors;

public class MyTypeFieldEditor : IFieldEditor
{
    public bool Draw(string label, object value, out object newValue)
    {
        var typed = (MyType)value;

        // TODO: Implement ImGui rendering
        bool changed = false;

        newValue = typed;
        return changed;
    }
}
```

### Step 2: Implement Rendering Logic

```csharp
public bool Draw(string label, object value, out object newValue)
{
    var myValue = (MyType)value;

    // Example: Edit two float fields
    bool changed = false;

    float field1 = myValue.Field1;
    changed |= ImGui.DragFloat($"{label} Field1", ref field1);

    float field2 = myValue.Field2;
    changed |= ImGui.DragFloat($"{label} Field2", ref field2);

    if (changed)
    {
        newValue = new MyType { Field1 = field1, Field2 = field2 };
    }
    else
    {
        newValue = myValue;
    }

    return changed;
}
```

### Step 3: Register in FieldEditorRegistry

```csharp
// FieldEditorRegistry.cs
private static readonly Dictionary<Type, IFieldEditor> _editors = new()
{
    // ... existing editors
    { typeof(MyType), new MyTypeFieldEditor() }
};
```

### Step 4: Test in Script Inspector

Create a test script with a public field:

```csharp
public class TestScript : NativeScript
{
    public MyType TestField = new();

    // Field editor will automatically render this field in Script Inspector
}
```

---

## Summary

### IFieldEditor System
- ✅ **Non-generic interface** with boxing (`object value`, `out object newValue`)
- ✅ **Runtime polymorphism** for reflection-based script field editing
- ✅ **FieldEditorRegistry** maps `Type → IFieldEditor`
- ✅ Used by `ScriptComponentEditor` and `UIPropertyRenderer`
- ❌ **Not for component editors** (use VectorPanel/static methods instead)

### When to Create Custom Field Editors
- Adding support for new types in script inspector
- Custom struct/class types used in scripts
- Specialized rendering for complex types (Quaternion, Color, etc.)

### Key Differences: IFieldEditor vs. Component Editing

| Aspect | IFieldEditor | VectorPanel/UIPropertyRenderer |
|--------|-------------|-------------------------------|
| **Interface** | `IFieldEditor.Draw()` | Static methods |
| **Type Safety** | Boxing (object) | Generic/ref parameters |
| **Performance** | 2 allocs per field | Zero allocs |
| **Purpose** | Runtime script fields | Compile-time component properties |
| **Registry** | FieldEditorRegistry | N/A (static dispatch) |
| **Extensibility** | Type → Editor mapping | Add static methods |


### Key Files
- `Editor/UI/FieldEditors/IFieldEditor.cs` - Interface definition
- `Editor/UI/FieldEditors/FieldEditorRegistry.cs` - Registry and lookup
- `Editor/UI/FieldEditors/Vector3FieldEditor.cs` - Example implementation
- `Editor/ComponentEditors/ScriptComponentEditor.cs:111` - Usage in script inspector
- `Editor/UI/Elements/UIPropertyRenderer.cs:32` - Convenience wrapper
