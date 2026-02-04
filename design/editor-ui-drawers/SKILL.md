---
name: editor-ui-drawers
description: Comprehensive guide for using Editor UI Drawers (ButtonDrawer, ModalDrawer, TableDrawer, TreeDrawer, LayoutDrawer, TextDrawer, DragDropDrawer). Use when implementing any UI in editor panels to ensure consistency.
---

# Editor UI Drawers

## Table of Contents
1. [Overview](#overview)
2. [When to Use This Skill](#when-to-use-this-skill)
3. [ButtonDrawer](#1-buttondrawer)
4. [ModalDrawer](#2-modaldrawer)
5. [TableDrawer](#3-tabledrawer)
6. [TreeDrawer](#4-treedrawer)
7. [LayoutDrawer](#5-layoutdrawer)
8. [TextDrawer](#6-textdrawer)
9. [DragDropDrawer](#7-dragdropdrawer)
10. [EditorUIConstants Reference](#editoruiconstants-reference)
11. [Summary](#summary)

## Overview
Drawers are static utility classes that provide common UI patterns with consistent styling. They wrap ImGui calls and automatically apply EditorUIConstants for sizing, spacing, and colors.

## When to Use This Skill
- Adding buttons to any editor panel
- Creating modal dialogs or confirmations
- Rendering tables or trees
- Need spacing, separators, or tooltips
- Drawing colored text
- Implementing drag-drop visualization

## Core Principle
**Never use raw ImGui calls when a Drawer exists.** Drawers ensure consistency and maintainability.

---

## 1. ButtonDrawer

Provides 11+ button variants with consistent sizing and behavior.

### Available Methods

#### Standard Buttons
```csharp
// Standard button (uses EditorUIConstants.StandardButtonWidth/Height)
if (ButtonDrawer.DrawButton("Save"))
    Save();

// Custom size button
if (ButtonDrawer.DrawButton("Export", width: 150, height: 30))
    Export();

// With onClick callback
ButtonDrawer.DrawButton("Load", onClick: Load);

// With disabled state
ButtonDrawer.DrawButton("Delete", disabled: !canDelete);

// Full-width button (stretches to available width)
if (ButtonDrawer.DrawFullWidthButton("Create New Scene"))
    CreateScene();
```

#### Specialized Buttons
```csharp
// Compact button (minimal padding, toolbar use)
if (ButtonDrawer.DrawCompactButton("×"))
    Close();

// Small utility button (uses EditorUIConstants.SmallButtonSize)
if (ButtonDrawer.DrawSmallButton("+", tooltip: "Add Item"))
    AddItem();

// Colored semantic button
if (ButtonDrawer.DrawColoredButton("Delete", MessageType.Error))
    Delete();

if (ButtonDrawer.DrawColoredButton("Save", MessageType.Success))
    Save();

if (ButtonDrawer.DrawColoredButton("Reload", MessageType.Warning))
    Reload();
```

#### Modal Buttons
```csharp
// Modal button with standard sizing
ButtonDrawer.DrawModalButton("OK", onClick: () => Confirm());

// Modal button pair (OK/Cancel with proper spacing)
ButtonDrawer.DrawModalButtonPair(
    okLabel: "Create",
    cancelLabel: "Cancel",
    onOk: () => CreateProject(),
    onCancel: () => CloseModal(),
    okDisabled: !isValid);
```

#### Toggle & Icon Buttons
```csharp
// Toggle button (changes label based on state)
ButtonDrawer.DrawToggleButton("Loop ON", "Loop OFF", ref isLooping);

// Icon button with selection state
if (ButtonDrawer.DrawIconButton("play_btn", playIconTexture, size, isSelected: isPlaying))
    TogglePlay();

// Transparent icon button (for toolbars)
if (ButtonDrawer.DrawTransparentIconButton("stop_btn", stopIconTexture, size, tooltip: "Stop"))
    Stop();
```

#### Button Groups
```csharp
// Toolbar button group (automatic spacing)
ButtonDrawer.DrawToolbarButtonGroup(
    ("Play", () => Play()),
    ("Pause", () => Pause()),
    ("Stop", () => Stop())
);
```

### Usage Examples

```csharp
// ✅ CORRECT - Use ButtonDrawer
if (ButtonDrawer.DrawButton("Save"))
{
    Save();
}

// ✅ CORRECT - Use semantic colored button
ButtonDrawer.DrawColoredButton("Delete", MessageType.Error);

// ❌ WRONG - Don't use raw ImGui
if (ImGui.Button("Save", new Vector2(120, 30)))  // Don't do this!
{
    Save();
}
```

---

## 2. ModalDrawer

Handles modal dialogs, popups, and confirmation prompts.

### Available Methods

#### Centered Modal (Manual)
```csharp
private bool _showModal;

public void OnImGuiRender()
{
    if (ButtonDrawer.DrawButton("Open"))
        _showModal = true;

    // Begin modal (centers automatically)
    if (ModalDrawer.BeginCenteredModal("My Modal", ref _showModal))
    {
        ImGui.Text("Modal content here");

        if (ButtonDrawer.DrawButton("Close"))
            _showModal = false;

        ModalDrawer.EndModal();
    }
}
```

#### Confirmation Modal (Complete)
```csharp
private bool _showConfirm;

public void OnImGuiRender()
{
    // Trigger modal
    if (ButtonDrawer.DrawButton("Delete"))
        _showConfirm = true;

    // Render confirmation modal (call every frame)
    ModalDrawer.RenderConfirmationModal(
        title: "Confirm Delete",
        showModal: ref _showConfirm,
        message: "Are you sure you want to delete this item?",
        onOk: () => DeleteItem(),
        onCancel: () => Console.WriteLine("Cancelled"),
        okLabel: "Delete",
        cancelLabel: "Cancel");
}
```

#### Input Modal
```csharp
private bool _showInput;
private string _inputValue = "";

public void OnImGuiRender()
{
    if (ButtonDrawer.DrawButton("Rename"))
        _showInput = true;

    ModalDrawer.RenderInputModal(
        title: "Rename Entity",
        showModal: ref _showInput,
        promptText: "Enter new name:",
        inputValue: ref _inputValue,
        maxLength: 100,
        validationMessage: string.IsNullOrEmpty(_inputValue) ? "Name cannot be empty" : null,
        errorMessage: null,
        isValid: !string.IsNullOrEmpty(_inputValue),
        onOk: () => Rename(_inputValue),
        onCancel: () => _inputValue = "");
}
```

#### Message Box
```csharp
private bool _showMessage;

ModalDrawer.RenderMessageBox(
    title: "Error",
    showModal: ref _showMessage,
    message: "Failed to load file!",
    messageType: MessageType.Error,
    onClose: () => Console.WriteLine("Message closed"));
```

#### List Selection Modal
```csharp
private bool _showSelector;
private string[] _items = { "Option 1", "Option 2", "Option 3" };

ModalDrawer.RenderListSelectionModal(
    title: "Select Item",
    showModal: ref _showSelector,
    items: _items,
    onItemSelected: item => Console.WriteLine($"Selected: {item}"),
    onCancel: () => Console.WriteLine("Cancelled"),
    emptyMessage: "No items available");
```

---

## 3. TableDrawer

Renders tables with consistent styling and behavior.

### Available Methods

#### Basic Tables
```csharp
// Two-column key-value table
TableDrawer.DrawTwoColumnTable(
    id: "Shortcuts",
    leftHeader: "Key",
    rightHeader: "Action",
    leftWidth: 100,
    renderRows: () =>
    {
        TableDrawer.DrawTableRow(
            () => ImGui.Text("Ctrl+S"),
            () => ImGui.Text("Save"));
        TableDrawer.DrawTableRow(
            () => ImGui.Text("Ctrl+O"),
            () => ImGui.Text("Open"));
    });

// Standard table (manual)
if (TableDrawer.BeginStandardTable("MyTable", columnCount: 3))
{
    ImGui.TableSetupColumn("Name");
    ImGui.TableSetupColumn("Type");
    ImGui.TableSetupColumn("Size");
    ImGui.TableHeadersRow();

    TableDrawer.DrawTableRow(
        () => ImGui.Text("File1"),
        () => ImGui.Text("Image"),
        () => ImGui.Text("1.2 MB"));

    ImGui.EndTable();
}
```

#### Generic Data Table
```csharp
var columns = new TableDrawer.ColumnDefinition[]
{
    new() { Label = "Name", Flags = ImGuiTableColumnFlags.WidthStretch },
    new() { Label = "Type", Flags = ImGuiTableColumnFlags.WidthFixed, InitWidth = 100 }
};

TableDrawer.DrawDataTable(
    id: "Files",
    columns: columns,
    items: files,
    renderRow: file =>
    {
        TableDrawer.DrawTableRow(
            () => ImGui.Text(file.Name),
            () => ImGui.Text(file.Type));
    },
    emptyMessage: "No files found");
```

#### Selectable Data Table
```csharp
TableDrawer.DrawSelectableDataTable(
    id: "Entities",
    columns: columns,
    items: entities,
    selectedItem: _selectedEntity,
    getItemId: e => e.Id.ToString(),
    onItemSelected: e => _selectedEntity = e,
    renderRow: entity =>
    {
        // Cell renderers for each column
        ImGui.TableSetColumnIndex(0);
        ImGui.Text(entity.Name);
        ImGui.TableSetColumnIndex(1);
        ImGui.Text(entity.Type);
    });
```

#### Sortable Table Headers
```csharp
private string _sortColumn = "Name";
private bool _sortAscending = true;

if (TableDrawer.BeginStandardTable("SortableTable", 2))
{
    ImGui.TableSetupColumn("Name");
    ImGui.TableSetupColumn("Size");
    ImGui.TableHeadersRow();

    // Custom sortable headers
    ImGui.TableSetColumnIndex(0);
    TableDrawer.DrawSortableHeader("Name", "Name", _sortColumn, _sortAscending,
        (col, asc) => { _sortColumn = col; _sortAscending = asc; SortData(); });

    // ... render rows ...

    ImGui.EndTable();
}
```

#### Helper Methods
```csharp
// Selectable row with custom rendering
TableDrawer.DrawSelectableRow(
    rowId: "row1",
    isSelected: true,
    onClicked: () => OnRowClick(),
    () => ImGui.Text("Cell 1"),
    () => ImGui.Text("Cell 2"));

// Colored cell
ImGui.TableSetColumnIndex(0);
TableDrawer.DrawColoredCell("Error", EditorUIConstants.ErrorColor);

// Empty table message
TableDrawer.DrawEmptyTableMessage("No data available", MessageType.Info);
```

---

## 4. TreeDrawer

Renders tree structures with expand/collapse behavior.

### Available Methods

#### Selectable Tree Nodes
```csharp
// Tree node with selection
if (TreeDrawer.DrawSelectableTreeNode("Entity", isSelected: _selected == entity,
    onClicked: () => SelectEntity(entity),
    onContextMenu: () => ShowContextMenu()))
{
    // Render children
    TreeDrawer.DrawSelectableTreeNode("Child Entity", isSelected: false);

    ImGui.TreePop();
}
```

#### Selectable Items (Flat List)
```csharp
// For flat lists with context menu and double-click
TreeDrawer.DrawSelectableItem(
    label: "File.txt",
    isSelected: _selected == file,
    onClicked: () => SelectFile(file),
    onContextMenu: () => ShowFileContextMenu(),
    onDoubleClick: () => OpenFile(file));
```

#### Colored Tree Nodes
```csharp
// Highlight search results or special states
if (TreeDrawer.DrawColoredTreeNode("Important", EditorUIConstants.WarningColor,
    isSelected: false))
{
    // Render children...
    ImGui.TreePop();
}
```

#### Recursive Hierarchy
```csharp
// Render entire hierarchy recursively
TreeDrawer.DrawHierarchy(
    node: rootEntity,
    getChildren: e => e.Children,
    getLabel: e => e.Name,
    isSelected: e => e == _selectedEntity,
    onClicked: e => _selectedEntity = e,
    onContextMenu: e => ShowEntityContextMenu(e));
```

### Usage Example
```csharp
// ✅ CORRECT - Use TreeDrawer with context menu
if (TreeDrawer.DrawSelectableTreeNode("Root", isSelected: _selected == root,
    onClicked: () => Select(root),
    onContextMenu: () =>
    {
        if (ImGui.MenuItem("Delete"))
            Delete(root);
    }))
{
    // Children...
    ImGui.TreePop();
}
```

---

## 5. LayoutDrawer

Layout utilities for spacing, inputs, checkboxes, and context menus.

### Available Methods

#### Search & Filter Inputs
```csharp
// Search input with clear button
private string _searchQuery = "";

LayoutDrawer.DrawSearchInput(
    hint: "Search files...",
    searchQuery: ref _searchQuery,
    onQueryChanged: query => FilterFiles(query));

// Filter input
private string _filter = "";
LayoutDrawer.DrawFilterInput("##filter", ref _filter, width: 200);
```

#### Separators & Spacing
```csharp
// Separator with spacing before and after
LayoutDrawer.DrawSeparatorWithSpacing();

// Only spacing before
LayoutDrawer.DrawSeparatorWithSpacing(addSpacingBefore: true, addSpacingAfter: false);
```

#### Colored Checkbox
```csharp
// Checkbox with custom color (for log filters, etc.)
private bool _showErrors = true;
LayoutDrawer.DrawColoredCheckbox("Errors", ref _showErrors, EditorUIConstants.ErrorColor);
```

#### Indented Sections
```csharp
// Indent content block
LayoutDrawer.DrawIndentedSection(() =>
{
    ImGui.Text("Indented text");
    ImGui.Text("More indented text");
});
```

#### Combo Boxes
```csharp
// Standard combo box
private string _current = "Option1";
private string[] _options = { "Option1", "Option2", "Option3" };

LayoutDrawer.DrawComboBox(
    label: "Choose",
    currentItem: _current,
    items: _options,
    onSelected: item => _current = item,
    width: 200);
```

#### Context Menus
```csharp
// Context menu for last item
ImGui.Text("Right-click me");
LayoutDrawer.DrawContextMenu("item1",
    ("Delete", () => Delete()),
    ("Rename", () => Rename()),
    ("Duplicate", () => Duplicate()));
```

#### Tooltips
```csharp
// Tooltip for last item
ImGui.Button("Hover Me");
LayoutDrawer.DrawTooltip("This is a helpful tooltip");
```

---

## 6. TextDrawer

Text rendering with semantic color coding.

### Available Methods

```csharp
// Generic colored text
TextDrawer.DrawColoredText("Custom Color", new Vector4(1, 0.5f, 0, 1));

// Semantic colored text
TextDrawer.DrawErrorText("Error occurred!");
TextDrawer.DrawWarningText("Warning: Low memory");
TextDrawer.DrawSuccessText("Operation successful");
TextDrawer.DrawInfoText("Information message");
```

### Usage Example
```csharp
// ✅ CORRECT - Use TextDrawer for semantic colors
TextDrawer.DrawErrorText("Failed to load file");

// ❌ WRONG - Don't manually push/pop colors
ImGui.PushStyleColor(ImGuiCol.Text, new Vector4(1, 0, 0, 1));  // Don't do this!
ImGui.Text("Error");
ImGui.PopStyleColor();
```

---

## 7. DragDropDrawer

Handles drag-and-drop visualization and logic.

### Available Methods

#### Drag Source
```csharp
// Create drag source for file
ImGui.Button("Drag Me");
if (ImGui.IsItemActive())
{
    DragDropDrawer.CreateDragDropSource(
        dragDropId: DragDropDrawer.ContentBrowserItemPayload,
        payloadData: filePath,
        dragPreview: () => ImGui.Text($"Moving {Path.GetFileName(filePath)}"));
}
```

#### Drop Target
```csharp
// File drop target with validation
ImGui.Button("Drop Here");
DragDropDrawer.HandleFileDropTarget(
    payloadType: DragDropDrawer.ContentBrowserItemPayload,
    validator: path => path.EndsWith(".png"),
    onDropped: path => LoadTexture(path));

// Drop target without validation
ImGui.Button("Drop Anything");
DragDropDrawer.HandleFileDropTarget(
    payloadType: DragDropDrawer.ContentBrowserItemPayload,
    validator: null,
    onDropped: path => ProcessFile(path));
```

#### Extension Validators
```csharp
// Create reusable validator
var imageValidator = DragDropDrawer.CreateExtensionValidator(
    extensions: new[] { ".png", ".jpg", ".bmp" },
    checkFileExists: true);

// Use validator
DragDropDrawer.HandleFileDropTarget(
    payloadType: DragDropDrawer.ContentBrowserItemPayload,
    validator: imageValidator,
    onDropped: path => LoadImage(path));

// Helper validation methods
if (DragDropDrawer.HasValidExtension(path, ".png", ".jpg"))
    Console.WriteLine("Valid image");

if (DragDropDrawer.IsValidFile(path, ".cs", ".txt"))
    Console.WriteLine("File exists and has valid extension");
```

### Constants
```csharp
// Standard payload type for content browser items
DragDropDrawer.ContentBrowserItemPayload  // Value: "CONTENT_BROWSER_ITEM"
```

---

## EditorUIConstants Reference

See [constants-reference.md](./constants-reference.md) for complete documentation.

### Quick Reference

**Button Sizes**:
- `StandardButtonWidth` = 120
- `StandardButtonHeight` = 0 (auto-height)
- `WideButtonWidth` = 150
- `SmallButtonSize` = 20
- `IconSize` = 16

**Spacing**:
- `StandardPadding` = 4
- `LargePadding` = 8
- `SmallPadding` = 2

**Colors**:
- `ErrorColor` = Bright red (1.0, 0.3, 0.3)
- `WarningColor` = Yellow (1.0, 1.0, 0.0)
- `SuccessColor` = Bright green (0.3, 1.0, 0.3)
- `InfoColor` = Light gray (0.7, 0.7, 0.7)

**Axis Colors** (for vectors):
- `AxisXColor` = Red (0.8, 0.1, 0.15)
- `AxisYColor` = Green (0.2, 0.7, 0.2)
- `AxisZColor` = Blue (0.1, 0.25, 0.8)

**Layout**:
- `PropertyLabelRatio` = 0.33 (1/3 width)
- `PropertyInputRatio` = 0.67 (2/3 width)
- `DefaultColumnWidth` = 60
- `WideColumnWidth` = 120
- `FilterInputWidth` = 200

---

## Summary

**7 Drawer Classes**:
1. **ButtonDrawer** - 11+ button variants (standard, colored, icon, toggle, modal)
2. **ModalDrawer** - 5 modal types (centered, confirmation, input, message, list selection)
3. **TableDrawer** - Data tables, sortable headers, selectable rows
4. **TreeDrawer** - Hierarchical trees with selection and context menus
5. **LayoutDrawer** - Search, filters, separators, combos, context menus, tooltips
6. **TextDrawer** - Semantic colored text (error, warning, success, info)
7. **DragDropDrawer** - File drag-drop with validation

**Key Principles**:
- Always use Drawers instead of raw ImGui
- All sizing uses EditorUIConstants
- Semantic colors via MessageType enum or dedicated methods
- Consistent patterns across the editor
