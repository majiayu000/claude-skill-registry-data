---
name: editor-ui-infrastructure
description: Guide proper usage of Editor UI infrastructure including Drawers (ButtonDrawer, ModalDrawer, TableDrawer, etc.), Elements (drag-drop targets, ComponentSelector), FieldEditors, and EditorUIConstants. Use when implementing editor panels, component editors, or any ImGui UI code to ensure consistency and code reuse.
---

# Editor UI Infrastructure

## Table of Contents
1. [Overview](#overview)
2. [When to Use](#when-to-use)
3. [Conceptual Model](#conceptual-model)
   - [Drawers](#drawers)
   - [Elements](#elements)
   - [FieldEditors](#fieldeditors)
   - [EditorUIConstants](#editoruiconstants)
4. [Best Practices](#best-practices)
5. [Common Anti-Patterns](#common-anti-patterns)
6. [Integration Checklist](#integration-checklist)
7. [Reference Documentation](#reference-documentation)

---

## Overview

The Editor UI infrastructure provides four layers of reusable UI components ensuring consistent styling and behavior across all editor panels and component editors.

**Golden Rule**: Never reimplement existing UI patterns. Always check if a Drawer, Element, or FieldEditor exists before writing custom ImGui code.

**Benefits**:
- Visual consistency across all editor panels
- Reduced code duplication
- Easier maintenance and global style changes
- Better user experience through familiar patterns

---

## When to Use

Invoke this skill when:
- ✅ Implementing editor panels or component editors
- ✅ Adding UI elements to existing panels
- ✅ Questions about which UI utility to use
- ✅ Implementing drag-and-drop functionality
- ✅ Creating modal dialogs or confirmation prompts
- ✅ Rendering tables, trees, or structured data
- ✅ Adding buttons with consistent styling
- ✅ Working with field editors for primitive types

---

## Conceptual Model

### Drawers

**What**: Static utility classes for common UI patterns with consistent styling.

**When**: Use for standard UI operations (buttons, modals, tables, spacing, text).

**Available**: ButtonDrawer, ModalDrawer, TableDrawer, TreeDrawer, LayoutDrawer, TextDrawer, DragDropDrawer

**Key Example**:
```csharp
// ❌ WRONG - Raw ImGui
if (ImGui.Button("Save", new Vector2(120, 30)))
    Save();

// ✅ CORRECT - Use ButtonDrawer
if (ButtonDrawer.DrawButton("Save", onClick: Save))
{
    // Additional logic if needed
}
```

**Features**:
- Automatic sizing via EditorUIConstants
- Semantic color coding (Error/Warning/Success/Info)
- Tooltip support
- Callback-based API reduces boilerplate

**Common Methods**:
- `ButtonDrawer.DrawButton()` - Standard button
- `ButtonDrawer.DrawColoredButton()` - Semantic colored button (red/green/yellow/blue)
- `ModalDrawer.RenderConfirmationModal()` - OK/Cancel dialog
- `TableDrawer.BeginTable()` - Consistent table rendering
- `TreeDrawer.BeginTreeNode()` - Expandable tree nodes
- `LayoutDrawer.DrawSpacing()` - Consistent vertical spacing
- `TextDrawer.DrawText()` - Colored text (Error/Warning/Success/Info)

See [references/drawers-api.md](references/drawers-api.md) for complete API reference (15+ button variants, modal types, etc.).

---

### Elements

**What**: Complex, stateful UI components for specific interactions.

**When**: Use for specialized interactions (drag-drop, component selection, context menus).

**Available**: TextureDropTarget, AudioDropTarget, MeshDropTarget, ComponentSelector, EntityContextMenu, PrefabManager

**Key Example**:
```csharp
// ❌ WRONG - Custom drag-drop implementation
ImGui.Button("Texture");
if (ImGui.BeginDragDropTarget())
{
    // Complex validation, error handling, visual feedback...
}

// ✅ CORRECT - Use specialized drop target
TextureDropTarget.Draw("Texture",
    currentPath: component.TexturePath,
    onTextureChanged: path => component.TexturePath = path,
    assetsManager: _assetsManager
);
```

**Features**:
- Built-in validation (file extensions, asset existence)
- Visual feedback (hover highlights, error messages)
- Consistent error handling
- Asset manager integration

**Common Elements**:
- `TextureDropTarget` - Texture files (.png, .jpg)
- `AudioDropTarget` - Audio files (.wav, .ogg)
- `MeshDropTarget` - Mesh files (.obj, .fbx)
- `ComponentSelector` - Searchable component list for "Add Component"
- `EntityContextMenu` - Right-click menu (duplicate, delete, rename)
- `PrefabManager` - Prefab creation/instantiation

See [references/elements-api.md](references/elements-api.md) for complete API reference and usage patterns.

---

### FieldEditors

**What**: Generic type-safe editors for primitive types, used in component editors.

**When**: Use in component editors for properties (int, float, Vector3, string, bool).

**Available**: IFieldEditor<T> for bool, int, float, double, string, Vector2, Vector3, Vector4

**Key Example**:
```csharp
// ❌ WRONG - Direct ImGui calls
public class MyComponentEditor : IComponentEditor<MyComponent>
{
    public void DrawEditor(MyComponent component)
    {
        ImGui.DragFloat("Speed", ref component.Speed);
        ImGui.Checkbox("Enabled", ref component.IsEnabled);
    }
}

// ✅ CORRECT - Inject field editors
public class MyComponentEditor : IComponentEditor<MyComponent>
{
    private readonly IFieldEditor<float> _floatEditor;
    private readonly IFieldEditor<bool> _boolEditor;
    private readonly IFieldEditor<Vector3> _vectorEditor;

    public MyComponentEditor(
        IFieldEditor<float> floatEditor,
        IFieldEditor<bool> boolEditor,
        IFieldEditor<Vector3> vectorEditor)
    {
        _floatEditor = floatEditor;
        _boolEditor = boolEditor;
        _vectorEditor = vectorEditor;
    }

    public void DrawEditor(MyComponent component)
    {
        _floatEditor.DrawField("Speed", ref component.Speed);
        _boolEditor.DrawField("Enabled", ref component.IsEnabled);
        _vectorEditor.DrawField("Offset", ref component.Offset);
    }
}
```

**Features**:
- Automatic label rendering with PropertyLabelRatio (33/67 split)
- Consistent spacing using EditorUIConstants
- Drag behavior for numeric types
- Axis color coding for vectors (X=red, Y=green, Z=blue)
- Reset buttons for vectors (right-click)

**Dependency Injection Pattern**:
- Always inject field editors via constructor
- Registered in DryIoc container automatically
- Never create field editors inline

---

### EditorUIConstants

**What**: Centralized constants for consistent styling across all UI.

**When**: Use for ALL sizing, spacing, colors (never hardcode values).

**Key Categories**:
- **Button Sizes**: StandardButtonWidth (120), StandardButtonHeight (30)
- **Layout Ratios**: PropertyLabelRatio (0.33f), PropertyInputRatio (0.67f)
- **Spacing**: StandardPadding (8), LargePadding (16), SmallPadding (4)
- **Colors**: ErrorColor (red), WarningColor (yellow), SuccessColor (green), InfoColor (blue)
- **Axis Colors**: AxisXColor (red), AxisYColor (green), AxisZColor (blue)
- **Input Buffers**: MaxNameLength (128), MaxPathLength (512)

**Key Example**:
```csharp
// ❌ WRONG - Magic numbers
ImGui.Button("Export", new Vector2(150, 35));
ImGui.Dummy(new Vector2(0, 10));
ImGui.PushStyleColor(ImGuiCol.Text, new Vector4(1, 0, 0, 1));

// ✅ CORRECT - Use constants
ButtonDrawer.DrawButton("Export",
    width: EditorUIConstants.WideButtonWidth,
    height: EditorUIConstants.StandardButtonHeight);
LayoutDrawer.DrawSpacing();
ImGui.PushStyleColor(ImGuiCol.Text, EditorUIConstants.ErrorColor);
```

**Golden Rule**: EditorUIConstants is the ONLY static class allowed in the codebase (all other code uses DI).

See [references/constants-catalog.md](references/constants-catalog.md) for complete catalog and design rationale.

---

## Best Practices

### 1. Always Use Drawers Over Raw ImGui

**Why**: Ensures consistency, automatic sizing, proper callbacks.

```csharp
// Use ButtonDrawer for all buttons
ButtonDrawer.DrawButton("Save");
ButtonDrawer.DrawColoredButton("Delete", MessageType.Error);

// Use ModalDrawer for confirmations
ModalDrawer.RenderConfirmationModal("Delete?", ref _show, "Sure?", () => Delete());

// Use LayoutDrawer for spacing
LayoutDrawer.DrawSpacing(); // Not ImGui.Dummy()
```

### 2. Use Specialized Drop Targets for Asset References

**Why**: Built-in validation, error handling, visual feedback.

```csharp
// Use TextureDropTarget for textures
TextureDropTarget.Draw("Texture", onTextureChanged, assetsManager);

// Use AudioDropTarget for audio
AudioDropTarget.Draw("Audio Clip", onAudioChanged, assetsManager);

// Use MeshDropTarget for meshes
MeshDropTarget.Draw("Mesh", onMeshChanged, assetsManager);
```

### 3. Inject Field Editors in Component Editors

**Why**: DI pattern, consistency, automatic layout ratios.

```csharp
// Always inject field editors via primary constructor
public class MyComponentEditor(
    IFieldEditor<float> floatEditor,
    IFieldEditor<Vector3> vectorEditor) : IComponentEditor
{
    // Use in DrawEditor - injected parameters are available as fields
    public void DrawEditor()
    {
        floatEditor.DrawField("Speed", ref component.Speed);
        vectorEditor.DrawField("Position", ref component.Position);
    }
}
```

### 4. Use EditorUIConstants for All Sizing/Spacing

**Why**: Global style changes, visual consistency, no magic numbers.

```csharp
// Always use constants
ButtonDrawer.DrawButton("Export",
    width: EditorUIConstants.WideButtonWidth);
LayoutDrawer.DrawSpacing(EditorUIConstants.LargePadding);
ImGui.PushStyleColor(ImGuiCol.Text, EditorUIConstants.ErrorColor);

// NEVER hardcode
ImGui.Button("Export", new Vector2(150, 35)); // ❌ WRONG
ImGui.Dummy(new Vector2(0, 10)); // ❌ WRONG
```

### 5. Use Semantic Colors for Actions

**Why**: Visual consistency, user expectations (red=danger, green=success).

```csharp
// Destructive actions = Error (red)
ButtonDrawer.DrawColoredButton("Delete", MessageType.Error);
TextDrawer.DrawText("Validation failed", MessageType.Error);

// Confirmations = Success (green)
ButtonDrawer.DrawColoredButton("Save", MessageType.Success);
TextDrawer.DrawText("Saved successfully!", MessageType.Success);

// Cautions = Warning (yellow)
TextDrawer.DrawText("Overwriting existing file", MessageType.Warning);
```

### 6. Prefer ComponentSelector/EntityContextMenu Over Custom Menus

**Why**: Consistent UX, keyboard navigation, automatic component discovery.

```csharp
// Use ComponentSelector for "Add Component"
private readonly ComponentSelector _selector = new();

if (ButtonDrawer.DrawButton("Add Component"))
    _selector.Show(entity);
_selector.Draw(); // Call every frame

// Use EntityContextMenu for right-click
private readonly EntityContextMenu _contextMenu = new();

if (ImGui.IsItemClicked(ImGuiMouseButton.Right))
    _contextMenu.Show(entity, scene);
_contextMenu.Draw(); // Call every frame
```

---

## Common Anti-Patterns

### 1. Bypassing UI Infrastructure

**Problem**: Inconsistent sizing, breaks global style changes, harder to maintain.

```csharp
// ❌ WRONG - Raw ImGui
if (ImGui.Button("Save", new Vector2(120, 30)))
    Save();
ImGui.SetNextItemWidth(200);

// ✅ CORRECT - Use infrastructure
if (ButtonDrawer.DrawButton("Save"))
    Save();
ImGui.SetNextItemWidth(EditorUIConstants.DefaultColumnWidth);
```

**Why It's Bad**: Hardcoded values prevent global style updates, break visual consistency.

### 2. Custom Drag-Drop Logic

**Problem**: Complex validation, error handling, visual feedback must be reimplemented.

```csharp
// ❌ WRONG - Manual implementation
if (ImGui.BeginDragDropTarget())
{
    var payload = ImGui.AcceptDragDropPayload("CONTENT_BROWSER_ITEM");
    if (payload.NativePtr != null)
    {
        // File extension validation
        // Path validation
        // Error messages
        // Visual feedback
    }
}

// ✅ CORRECT - Use specialized target
TextureDropTarget.Draw("Texture", onChange, assetsManager);
```

**Why It's Bad**: Drop targets handle validation, errors, and visual feedback automatically.

### 3. Inline Field Editors

**Problem**: Breaks DI pattern, inconsistent layout ratios, no axis coloring.

```csharp
// ❌ WRONG - Direct ImGui
ImGui.DragFloat("Speed", ref speed);
ImGui.DragFloat3("Position", ref position);

// ✅ CORRECT - Inject and use field editors
_floatEditor.DrawField("Speed", ref speed);
_vectorEditor.DrawField("Position", ref position); // Automatic X/Y/Z colors
```

**Why It's Bad**: Loses PropertyLabelRatio (33/67 split), axis color coding, reset buttons.

---

## Integration Checklist

When implementing editor UI, ensure:

- [ ] All buttons use ButtonDrawer (not raw `ImGui.Button`)
- [ ] All asset references use drag-drop targets (TextureDropTarget, AudioDropTarget, etc.)
- [ ] All component editors inject field editors for primitive types
- [ ] All sizes/spacing use EditorUIConstants (no magic numbers)
- [ ] All colors use EditorUIConstants (ErrorColor, SuccessColor, AxisXColor, etc.)
- [ ] All modals use ModalDrawer.RenderConfirmationModal()
- [ ] All tables use TableDrawer.BeginTable()
- [ ] All trees use TreeDrawer
- [ ] All tooltips use LayoutDrawer.DrawTooltip()
- [ ] All spacing uses LayoutDrawer.DrawSpacing()

---

## Reference Documentation

### API References

Detailed API documentation for each infrastructure layer:

- **[references/drawers-api.md](references/drawers-api.md)**: Complete Drawer APIs
  - ButtonDrawer (15+ button variants)
  - ModalDrawer (confirmation dialogs, custom modals)
  - TableDrawer, TreeDrawer, LayoutDrawer, TextDrawer, DragDropDrawer
  - Common patterns and usage examples

- **[references/elements-api.md](references/elements-api.md)**: Complete Element APIs
  - Drag-drop targets (Texture, Audio, Mesh, Prefab)
  - ComponentSelector (searchable component list)
  - EntityContextMenu (right-click operations)
  - PrefabManager (prefab creation/instantiation)

- **[references/constants-catalog.md](references/constants-catalog.md)**: EditorUIConstants Catalog
  - Complete constant listing (button sizes, spacing, colors)
  - Design rationale (why PropertyLabelRatio = 0.33f, etc.)
  - Usage guidelines and quick reference

### Related Files

- `Editor/UI/Drawers/` - All drawer implementations
- `Editor/UI/Elements/` - All element implementations
- `Editor/UI/FieldEditors/` - All field editor implementations
- `Editor/UI/Constants/EditorUIConstants.cs` - Constant definitions

---

## Summary

The Editor UI infrastructure provides four layers:

1. **Drawers** (7 classes): Static utilities for common patterns (buttons, modals, tables)
2. **Elements** (9 components): Stateful components for complex interactions (drop targets, selectors)
3. **FieldEditors** (8 generic types): Type-safe editors for component properties
4. **EditorUIConstants** (30+ constants): Centralized styling values

**Key Principle**: Never reimplement existing patterns. Check Drawers/Elements/FieldEditors first, then write custom ImGui code only if no match exists.

