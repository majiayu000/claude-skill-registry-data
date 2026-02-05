---
name: editor-panel-creation
description: Step-by-step workflow for creating new editor panels including interface design, DI registration, EditorLayer integration, and menu bar setup. Focuses on panel architecture and lifecycle, not UI component APIs.
---

# Editor Panel Creation

## Overview
This skill provides comprehensive guidance for creating new ImGui-based editor panels, ensuring consistency with the engine's dependency injection architecture, UI styling standards, and editor integration patterns.

**CRITICAL REQUIREMENT**: All editor panels **MUST** use the UI infrastructure (Drawers, Elements, FieldEditors) instead of manual ImGui code. This ensures consistency, maintainability, and productivity across the entire editor.

## UI Infrastructure Reference

The editor provides comprehensive UI infrastructure:
- **UI Drawers**: ButtonDrawer, ModalDrawer, TableDrawer, TreeDrawer, TextDrawer, LayoutDrawer, DragDropDrawer
- **UI Elements**: TextureDropTarget, AudioDropTarget, ComponentSelector, EntityContextMenu, PrefabManager
- **Field Editors**: IFieldEditor (non-generic, primarily for script inspector - rarely used in panels)
- **Constants**: EditorUIConstants for all sizing, spacing, and colors

## When to Use
Invoke this skill when:
- Adding a new editor panel or tool window
- Creating asset browsers or managers
- Building debugging or profiling panels
- Implementing workflow tools for artists/designers
- Questions about editor panel architecture and lifecycle
- Integrating panels with the editor layer system
- Questions about DI registration and menu integration

## Panel Creation Workflow

Follow these 6 steps to create a new panel. Use the [Testing Checklist](#testing-checklist) to verify completeness.

### Step 1: Define Panel Interface
**Location**: `Editor/Panels/`

**Pattern**: All panels use interface-based design for testability and DI

**Interface Template**:
```csharp
namespace Editor.Panels;

/// <summary>
/// Interface for the [PanelName] panel.
/// </summary>
public interface IMyNewPanel
{
    /// <summary>
    /// Renders the panel using ImGui.
    /// </summary>
    void OnImGuiRender();

    /// <summary>
    /// Gets or sets whether the panel is currently open.
    /// </summary>
    bool IsOpen { get; set; }
}
```

**Naming Convention**:
- Interface: `I[PanelName]Panel` or `I[PanelName]`
- Implementation: `[PanelName]Panel` or `[PanelName]`
- Examples: `ISceneHierarchyPanel`, `IConsolePanel`, `ITileMapPanel`

### Step 2: Implement Panel Class
**Location**: `Editor/Panels/`

**Guidelines**:
- **MUST use UI Drawers** (ButtonDrawer, ModalDrawer, etc.) instead of manual ImGui code
- **MUST use UI Elements** (TextureDropTarget, ComponentSelector, etc.) for complex interactions
- Use constructor injection for ALL dependencies
- Use `EditorUIConstants` for sizing, spacing, colors (Drawers handle this automatically)
- Maintain panel state in private fields
- Implement proper disposal if managing resources
- Follow ImGui immediate-mode UI patterns

**Panel Template**:
```csharp
namespace Editor.Panels;

using Editor.UI;
using Editor.UI.Drawers;
using Editor.UI.Elements;
using Editor.UI.FieldEditors;
using ImGuiNET;
using Editor.Managers;

/// <summary>
/// Panel for managing and displaying [functionality].
/// </summary>
public class MyNewPanel(
    ISceneManager sceneManager,
    IProjectManager projectManager) : IMyNewPanel
{
    // Panel state
    private bool _isOpen = true;
    private bool _showConfirmModal = false;
    private string _filterText = string.Empty;
    private int _selectedIndex = -1;

    // Input buffers (use EditorUIConstants for sizes)
    private readonly byte[] _nameBuffer = new byte[EditorUIConstants.MaxNameLength];

    /// <inheritdoc/>
    public bool IsOpen
    {
        get => _isOpen;
        set => _isOpen = value;
    }

    /// <inheritdoc/>
    public void OnImGuiRender()
    {
        if (!_isOpen)
            return;

        ImGuiWindowFlags flags = ImGuiWindowFlags.None;

        if (ImGui.Begin("My Panel", ref _isOpen, flags))
        {
            DrawToolbar();
            LayoutDrawer.DrawSeparator();
            DrawContent();
        }
        ImGui.End();

        // Render modals (must be outside Begin/End)
        ModalDrawer.RenderConfirmationModal(
            title: "Confirm Action",
            showModal: ref _showConfirmModal,
            message: "Are you sure?",
            onOk: () => PerformAction());
    }

    private void DrawToolbar()
    {
        // Use ButtonDrawer for styled buttons
        if (ButtonDrawer.DrawButton("Save", ButtonDrawer.ButtonType.Primary))
        {
            SaveData();
        }

        ImGui.SameLine();

        if (ButtonDrawer.DrawButton("Clear", ButtonDrawer.ButtonType.Secondary))
        {
            _showConfirmModal = true;
        }
    }

    private void DrawContent()
    {
        // Use LayoutDrawer for spacing
        LayoutDrawer.DrawSpacing(EditorUIConstants.StandardPadding);

        // Panel-specific content here
    }

    private void SaveData()
    {
        // Implementation
    }

    private void PerformAction()
    {
        // Implementation
    }
}
```

### Step 3: Register in Dependency Injection
**Location**: `Editor/Program.cs`

**Registration Pattern**:
```csharp
private static void ConfigureServices(Container container)
{
    // ... existing registrations

    // Register new panel
    container.Register<IMyNewPanel, MyNewPanel>(Reuse.Singleton);
}
```

**Guidelines**:
- Always register as singleton (one instance per editor session)
- Register interface → implementation mapping
- Ensure all dependencies are registered before the panel

### Step 4: Inject into EditorLayer
**Location**: `Editor/EditorLayer.cs`

**Constructor Injection**:
```csharp
public class EditorLayer(
    // ... existing parameters
    ISceneHierarchyPanel sceneHierarchyPanel,
    IPropertiesPanel propertiesPanel,
    IConsolePanel consolePanel,
    IMyNewPanel myNewPanel) : Layer
{
    public override void OnImGuiRender()
    {
        // ... existing panel renders
        sceneHierarchyPanel.OnImGuiRender();
        propertiesPanel.OnImGuiRender();
        consolePanel.OnImGuiRender();
        myNewPanel.OnImGuiRender();
    }
}
```

### Step 5: Add Menu Integration
**Location**: `Editor/EditorLayer.cs` (in menu bar rendering)

**Add Panel Toggle Menu**:
```csharp
private void DrawMenuBar()
{
    if (ImGui.BeginMenu("Window"))
    {
        // Existing menu items
        if (ImGui.MenuItem("Scene Hierarchy", "", _sceneHierarchyPanel.IsOpen))
            _sceneHierarchyPanel.IsOpen = !_sceneHierarchyPanel.IsOpen;

        if (ImGui.MenuItem("Properties", "", _propertiesPanel.IsOpen))
            _propertiesPanel.IsOpen = !_propertiesPanel.IsOpen;

        // New panel menu item
        if (ImGui.MenuItem("My Panel", "", _myNewPanel.IsOpen))
            _myNewPanel.IsOpen = !_myNewPanel.IsOpen;

        ImGui.EndMenu();
    }
}
```

**Keyboard Shortcut** (optional):
```csharp
private void HandleShortcuts()
{
    // Existing shortcuts
    // Ctrl+Shift+M to toggle My Panel
    if (ImGui.IsKeyDown(ImGuiKey.LeftCtrl) &&
        ImGui.IsKeyDown(ImGuiKey.LeftShift) &&
        ImGui.IsKeyPressed(ImGuiKey.M))
    {
        _myNewPanel.IsOpen = !_myNewPanel.IsOpen;
    }
}
```

### Step 6: Use UI Infrastructure (MANDATORY)

**CRITICAL: All panels MUST use the UI infrastructure** - never write manual ImGui code for patterns covered by Drawers, Elements, or FieldEditors!

**Common UI Components:**

1. **Buttons** - Use `ButtonDrawer.DrawButton()` with button types (Primary, Secondary, Danger, Success)
2. **Modals** - Use `ModalDrawer.RenderConfirmationModal()` for all confirmation dialogs
3. **Tables** - Use `TableDrawer.BeginTable()` / `TableDrawer.DrawRow()` / `TableDrawer.EndTable()`
4. **Spacing** - Use `LayoutDrawer.DrawSpacing()` / `LayoutDrawer.DrawSeparator()`
5. **Asset References** - Use `TextureDropTarget.Draw()`, `AudioDropTarget.Draw()`, etc.
6. **Property Editing** - Use ImGui widgets directly (ImGui.DragFloat, ImGui.InputText, etc.) or create custom UI patterns

**Example: Minimal Panel with UI Infrastructure**

```csharp
using Editor.UI.Drawers;
using Editor.UI.Elements;

public class MyPanel : IMyPanel
{
    private bool _showConfirmModal;
    private float _speed = 1.0f;
    private string _iconPath = "";

    public void OnImGuiRender()
    {
        if (!_isOpen) return;

        if (ImGui.Begin("My Panel", ref _isOpen))
        {
            // Use ButtonDrawer for styled buttons
            if (ButtonDrawer.DrawButton("Save", ButtonDrawer.ButtonType.Primary))
            {
                Save();
            }

            LayoutDrawer.DrawSeparator();

            // Use ImGui for properties
            ImGui.DragFloat("Speed", ref _speed, 0.1f);

            // Use drag-drop targets for assets
            TextureDropTarget.Draw("Icon", _iconPath, (newPath) => _iconPath = newPath);
        }
        ImGui.End();

        // Modals outside Begin/End
        ModalDrawer.RenderConfirmationModal(
            title: "Confirm",
            showModal: ref _showConfirmModal,
            message: "Are you sure?",
            onOk: () => PerformAction());
    }
}
```

**Key Rules:**
- ❌ Never use `ImGui.Button()` - use `ButtonDrawer.DrawButton()`
- ❌ Never use `ImGui.BeginPopupModal()` - use `ModalDrawer.RenderConfirmationModal()`
- ✅ Use `ImGui.DragFloat()`, `ImGui.InputText()`, etc. for property editing (IFieldEditor is for script inspector only)
- ❌ Never manually implement drag-drop - use `TextureDropTarget.Draw()`, etc.

## Advanced Panel Patterns

### Dockable Panel
```csharp
public void OnImGuiRender()
{
    if (!_isOpen)
        return;

    ImGuiWindowFlags flags = ImGuiWindowFlags.None;

    if (ImGui.Begin("My Panel", ref _isOpen, flags))
    {
        // Panel is dockable by default in ImGui
        DrawContent();
    }
    ImGui.End();
}
```

### Panel with Tabs
```csharp
private void DrawContent()
{
    if (ImGui.BeginTabBar("##MyTabs"))
    {
        if (ImGui.BeginTabItem("Tab 1"))
        {
            DrawTab1Content();
            ImGui.EndTabItem();
        }

        if (ImGui.BeginTabItem("Tab 2"))
        {
            DrawTab2Content();
            ImGui.EndTabItem();
        }

        ImGui.EndTabBar();
    }
}
```

### Panel with Context Menu
```csharp
private void DrawItem(string itemName)
{
    ImGui.Selectable(itemName);

    if (ImGui.BeginPopupContextItem($"##{itemName}Context"))
    {
        if (ImGui.MenuItem("Edit"))
            EditItem(itemName);

        if (ImGui.MenuItem("Delete"))
            DeleteItem(itemName);

        ImGui.EndPopup();
    }
}
```

### Panel with Modal Dialog
**ALWAYS use ModalDrawer instead of manual ImGui popups.**

```csharp
using Editor.UI.Drawers;

private bool _showDeleteConfirmation = false;

private void DrawContent()
{
    // Trigger modal with styled button
    if (ButtonDrawer.DrawButton("Delete", ButtonDrawer.ButtonType.Danger))
        _showDeleteConfirmation = true;

    // Render modal using ModalDrawer
    ModalDrawer.RenderConfirmationModal(
        title: "Delete Confirmation",
        showModal: ref _showDeleteConfirmation,
        message: "Are you sure you want to delete?",
        onOk: () => PerformDelete());
}
```

## Existing Panels Reference

The editor has 17 panels in `Editor/Panels/` and `Editor/Features/`. Reference these for implementation patterns:
- **Core**: SceneHierarchyPanel, PropertiesPanel, ViewportPanel, GameViewPanel
- **Assets**: ContentBrowserPanel, AssetPanel, TileMapPanel
- **Tools**: ConsolePanel, StatsPanel, AudioPanel, PhysicsPanel
- **Settings**: ProjectSettingsPanel, BuildSettingsPanel, PreferencesPanel, SceneSettingsPanel
- **Utilities**: ShortcutsPanel, AboutPanel

See implementations in `Editor/Panels/` for UI consistency patterns.

## Dependency Injection Best Practices

### Common Service Dependencies

```csharp
// Scene management
private readonly ISceneManager _sceneManager;

// Project management
private readonly IProjectManager _projectManager;

// Factories
private readonly ITextureFactory _textureFactory;
private readonly IShaderFactory _shaderFactory;
private readonly IAudioClipFactory _audioClipFactory;

// Systems
private readonly SystemManager _systemManager;

// Other panels (for cross-panel communication)
private readonly ISceneHierarchyPanel _sceneHierarchyPanel;
```

### Constructor Pattern (Use Primary Constructor)
```csharp
public class MyPanel(
    ISceneManager sceneManager,
    IProjectManager projectManager,
    ITextureFactory textureFactory) : IMyPanel
{
    // Dependencies are automatically available as private readonly fields
    // No null validation needed - non-nullable reference types handle this
}
```

### Never Create Static Singletons
```csharp
// ❌ WRONG - Do not create static singletons
public static class MyPanelManager
{
    public static MyPanelManager Instance { get; } = new();
}

// ✅ CORRECT - Use DI container registration
container.Register<IMyPanel, MyPanel>(Reuse.Singleton);
```

## Testing Checklist

- [ ] Panel interface defined
- [ ] Panel implementation with constructor injection
- [ ] All dependencies properly injected (no nulls)
- [ ] **UI Drawers used instead of manual ImGui code** (ButtonDrawer, ModalDrawer, etc.)
- [ ] **UI Elements used for complex interactions** (drag-drop targets, component selector)
- [ ] ImGui widgets used for property editing (IFieldEditor not needed in most panels)
- [ ] `EditorUIConstants` used throughout (no magic numbers)
- [ ] Registered in `Program.cs` DI container
- [ ] Injected into `EditorLayer`
- [ ] Menu item added to Window menu
- [ ] Panel opens and closes correctly
- [ ] Panel state persists during session
- [ ] Panel works with docking system
- [ ] Keyboard shortcuts added (if applicable)
- [ ] Panel performs expected functionality
- [ ] Cross-panel communication works (if needed)

## Documentation Requirements

### Code Documentation
- XML comments on interface and public methods
- Clear parameter descriptions
- Usage examples in comments

## Common Pitfalls to Avoid

1. **❌ Manual ImGui code instead of Drawers** - ALWAYS use ButtonDrawer, ModalDrawer, TableDrawer, etc.
2. **❌ Manual drag-drop instead of Elements** - Use TextureDropTarget, AudioDropTarget, etc.
3. **❌ Confusing IFieldEditor usage** - IFieldEditor is for script inspector only, use ImGui widgets for panel properties
4. **❌ Hardcoded UI values** - Always use EditorUIConstants
5. **❌ Static state** - Use instance fields, inject dependencies
6. **❌ Missing null checks** - Validate constructor parameters
7. **❌ Inconsistent styling** - Follow existing panel patterns and use UI infrastructure
8. **❌ Direct service access** - Use dependency injection
9. **❌ Forgetting IsOpen check** - Always check before rendering
10. **❌ ImGui misuse** - Follow Begin/End pairing strictly
11. **❌ Performance issues** - Avoid heavy computation in OnImGuiRender
12. **❌ Duplicating UI patterns** - Check if a Drawer/Element already exists first
