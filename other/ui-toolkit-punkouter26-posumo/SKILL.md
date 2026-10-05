---
name: ui-toolkit
description: "UI Toolkit — UXML document structure, USS styling (CSS-like), UQuery, data binding, ListView virtualization, custom visual elements."
globs: ["**/*.uxml", "**/*.uss", "**/UIDocument*"]
---

# UI Toolkit

## UXML Structure

```xml
<ui:UXML xmlns:ui="UnityEngine.UIElements">
    <ui:Style src="styles.uss" />

    <ui:VisualElement class="screen">
        <ui:Label text="Game Title" class="title" />

        <ui:VisualElement class="button-container">
            <ui:Button text="Play" name="btn-play" class="menu-btn" />
            <ui:Button text="Settings" name="btn-settings" class="menu-btn" />
            <ui:Button text="Quit" name="btn-quit" class="menu-btn danger" />
        </ui:VisualElement>

        <ui:Slider label="Volume" name="volume-slider" low-value="0" high-value="1" value="0.8" />
        <ui:Toggle label="Fullscreen" name="fullscreen-toggle" />
    </ui:VisualElement>
</ui:UXML>
```

## USS Styling (CSS-like)

```css
.screen {
    flex-grow: 1;
    align-items: center;
    justify-content: center;
    background-color: rgba(0, 0, 0, 0.8);
}

.title {
    font-size: 48px;
    color: white;
    -unity-font-style: bold;
    margin-bottom: 40px;
}

.menu-btn {
    width: 250px;
    height: 50px;
    margin: 8px;
    font-size: 20px;
    background-color: rgb(60, 60, 60);
    color: white;
    border-radius: 8px;
    border-width: 0;
    transition-duration: 0.2s;
}

.menu-btn:hover {
    background-color: rgb(80, 80, 80);
    scale: 1.05;
}

.menu-btn:active {
    background-color: rgb(40, 40, 40);
}

.danger {
    color: rgb(255, 100, 100);
}
```

### Key USS Differences from CSS
- Flex layout only (no floats, no grid)
- Use `-unity-` prefix for Unity-specific properties
- Colors: `rgb()`, `rgba()`, `#hex`
- Transitions: `transition-duration`, `transition-property`
- No `em`/`rem` — use `px` or `%`

## Controller Script

```csharp
public sealed class MainMenuController : MonoBehaviour
{
    [SerializeField] private UIDocument _document;

    private void OnEnable()
    {
        VisualElement root = _document.rootVisualElement;

        root.Q<Button>("btn-play").clicked += OnPlayClicked;
        root.Q<Button>("btn-settings").clicked += OnSettingsClicked;
        root.Q<Button>("btn-quit").clicked += OnQuitClicked;

        Slider volumeSlider = root.Q<Slider>("volume-slider");
        volumeSlider.RegisterValueChangedCallback(evt => OnVolumeChanged(evt.newValue));
    }

    private void OnPlayClicked() { /* Load game scene */ }
    private void OnSettingsClicked() { /* Show settings panel */ }
    private void OnQuitClicked() { Application.Quit(); }
    private void OnVolumeChanged(float value) { /* Set audio volume */ }
}
```

## UQuery

```csharp
VisualElement root = _document.rootVisualElement;

// By name
Button playBtn = root.Q<Button>("btn-play");

// By class
var allButtons = root.Query<Button>(className: "menu-btn").ToList();

// By type
var allLabels = root.Query<Label>().ToList();

// Nested query
var containerBtns = root.Q("button-container").Query<Button>().ToList();
```

## ListView (Virtualized Scrolling)

```csharp
ListView listView = root.Q<ListView>("inventory-list");
listView.makeItem = () => new Label(); // Create UI element
listView.bindItem = (element, index) =>
{
    ((Label)element).text = _items[index].Name;
};
listView.itemsSource = _items;
listView.fixedItemHeight = 40;
listView.selectionType = SelectionType.Single;
listView.selectionChanged += OnSelectionChanged;
```

## Custom Visual Element

```csharp
public sealed class HealthBar : VisualElement
{
    private VisualElement _fill;

    public float Value
    {
        set => _fill.style.width = new Length(value * 100f, LengthUnit.Percent);
    }

    public HealthBar()
    {
        AddToClassList("health-bar");
        _fill = new VisualElement();
        _fill.AddToClassList("health-fill");
        Add(_fill);
    }

    // Required for UXML instantiation
    public new sealed class UxmlFactory : UxmlFactory<HealthBar> { }
}
```

## Event System

```csharp
// Register callbacks
element.RegisterCallback<ClickEvent>(evt => { });
element.RegisterCallback<PointerEnterEvent>(evt => { });
element.RegisterCallback<KeyDownEvent>(evt => { });

// Unregister
element.UnregisterCallback<ClickEvent>(handler);
```
