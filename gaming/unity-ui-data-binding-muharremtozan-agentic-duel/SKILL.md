---
name: unity-ui-data-binding
description: Implementation of MVVM-style Data Binding for Unity UI Toolkit using the [CreateProperty] attribute and BindableProperty wrappers.
---

# Unity UI Toolkit Data Binding

Connect your game data (Model) to your interface (View) using modern high-performance data binding. This skill leverages Unity's `unity.properties` system to eliminate "Update" loop logic for UI updates.

## Core Features
1. **BindableProperty<T>**: A wrapper class that uses `[CreateProperty]` to expose values to the UI Toolkit binding engine.
2. **MVVM (Model-View-ViewModel)**: Separates raw game data from UI-formatted data using a ViewModel mediator.
3. **Reactive Synchronization**: UI elements update automatically when the underlying property value changes (or is polled by the engine).
4. **C# Based Binding**: Set up complex bindings programmatically without relying on the UI Builder's inspector fields.

## Core Files (Max 3)
- `BindableProperty.cs.txt`: Generic property wrapper for data sources.
- `BindingExample.cs.txt`: Practical example showing a Coin display and Health bar bound to a ViewModel.

## Usage

### 1. Define the ViewModel
Initialize `BindableProperty` fields that return formatted data from your model.
```csharp
public BindableProperty<string> HealthText { get; }
HealthText = BindableProperty<string>.Bind(() => $"HP: {model.hp}/{model.maxHp}");
```

### 2. Set the Data Source
Assign your ViewModel to the `dataSource` property of your root VisualElement.
```csharp
root.dataSource = myViewModel;
```

### 3. Establish the Binding
Use `SetBinding` on specific elements to link their properties (text, value, style) to paths in the ViewModel.
```csharp
label.SetBinding("text", "HealthText.Value");
```

## Key Principle
Always use **one-way** binding (ToTarget) for displays and **two-way** binding only for inputs (checkboxes, text fields). This keeps the "Source of Truth" in your Model.
