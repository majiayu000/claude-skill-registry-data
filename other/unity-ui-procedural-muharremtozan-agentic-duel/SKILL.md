---
name: unity-ui-procedural
description: Advanced UI construction using C# code instead of UI Builder. Includes fluent extension methods and reusable pointer manipulators.
---

# Unity UI Toolkit Procedural UI

Build lightning-fast, highly dynamic user interfaces entirely through code. This skill enables the "Logic-First" UI workflow, perfect for complex systems like inventories, tooltips, and dynamic HUDs.

## Core Features
1. **Fluent Hiyerarşi Construction**: Use chained extension methods like `.CreateChild<T>()` and `.WithClass()` to build UI trees that read like documentation.
2. **Generic Pointer Manipulators**: Decouple interaction logic (Drag, Resize, Selection) from visuals using the `Manipulator` API.
3. **No-Builder Workflow**: Eliminates the need for complex UXML files, making UI version-control friendly and procedurally scalable.
4. **BEM Integration**: Extension methods prioritize CSS class application to maintain a clean styling system.

## Core Files (Max 3)
- `UIToolkitExtensions.cs.txt`: Generic methods for chaining element creation and styling.
- `DragManipulator.cs.txt`: A cross-platform pointer-based drag system for any VisualElement.
- `ProceduralViewExample.cs.txt`: A "Hotbar/Inventory" demo showing the power of the fluent syntax.

## Usage

### 1. Build a Panel (The Fluent Way)
```csharp
var root = GetComponent<UIDocument>().rootVisualElement;
root.CreateChild<VisualElement>( "main-menu" )
    .WithClass( "menu--active" )
    .CreateChild<Button>( "menu__btn--start" )
    .text = "Start Game";
```

### 2. Add Interactions
```csharp
var window = root.Q( "inventory-window" );
window.AddManipulator( new DragManipulator() );
```

## Key Principle
Always use **USS classes** for styling even when building procedurally. Avoid setting `.style.width` or colors directly in C# unless it is for dynamic calculations (like health bars).
