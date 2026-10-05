---
name: avalonia-visual-element
description: Rules and patterns for creating Avalonia UI visual elements (controls, dialogs, panels, windows). Use when creating or modifying XAML controls, dialogs, panels, or windows in this project.
---

# Avalonia Visual Element Creation Rules

Follow these rules strictly when creating or modifying any visual element (control, dialog, panel, window) in this project.

## Core Philosophy

- **Direct UI Access** — no MVVM, no reactive patterns, no stored state between UI and model
- **Action-driven** — everything happens by explicit user interaction
- **KISS** — minimal working version first, no premature abstractions
- **TDD** — write tests first, implement second

## XAML Rules

- **Theme:** Classic.Avalonia.Theme
- **Font size:** Always `{DynamicResource AppFontSize}` — NEVER hardcode font sizes
- **Named elements:** Use `x:FieldModifier="internal"` for code-behind access
- **Keep XAML simple** — layout and structure only, no complex data bindings
- **ComboBox items:** Use `DataTemplate` with `ItemTemplate` for displaying model objects

## Dialog / Window Layout

Use this structure for all dialogs:

```xml
<Window ...
        Title="Edit [Element]"
        Width="450" Height="380"
        MinWidth="400" MinHeight="320"
        FontSize="{DynamicResource AppFontSize}"
        WindowStartupLocation="CenterOwner"
        CanResize="true">

    <ScrollViewer VerticalScrollBarVisibility="Auto" HorizontalScrollBarVisibility="Disabled">
        <StackPanel Margin="20" Spacing="10">

            <!-- Section header -->
            <TextBlock Text="Section Title" FontWeight="SemiBold"
                       FontSize="{DynamicResource AppFontSize}"/>

            <!-- Input grid: 100px label, * control -->
            <Grid ColumnDefinitions="100,*" RowDefinitions="Auto,Auto">
                <TextBlock Grid.Row="0" Grid.Column="0" Text="Label:"
                           VerticalAlignment="Center"
                           FontSize="{DynamicResource AppFontSize}"/>
                <controls:MeasurementControl Grid.Row="0" Grid.Column="1"
                           x:Name="Control1" x:FieldModifier="internal"
                           FontSize="{DynamicResource AppFontSize}"/>

                <!-- Subsequent rows get top margin -->
                <TextBlock Grid.Row="1" Grid.Column="0" Text="Label:"
                           VerticalAlignment="Center"
                           FontSize="{DynamicResource AppFontSize}"
                           Margin="0,8,0,0"/>
                <controls:MeasurementControl Grid.Row="1" Grid.Column="1"
                           x:Name="Control2" x:FieldModifier="internal"
                           FontSize="{DynamicResource AppFontSize}"
                           Margin="0,8,0,0"/>
            </Grid>

            <!-- Checkboxes align under controls, not labels -->
            <Grid ColumnDefinitions="100,*">
                <CheckBox Grid.Column="1" x:Name="SomeCheckBox"
                          x:FieldModifier="internal" Content="Option"
                          FontSize="{DynamicResource AppFontSize}"/>
            </Grid>

            <!-- Buttons: centered, horizontal, 10px spacing, 80px wide -->
            <StackPanel Orientation="Horizontal" HorizontalAlignment="Center"
                        Spacing="10" Margin="0,20,0,0">
                <Button Content="OK" Click="OnOK" Width="80"
                        FontSize="{DynamicResource AppFontSize}"/>
                <Button Content="Cancel" Click="OnCancel" Width="80"
                        FontSize="{DynamicResource AppFontSize}"/>
            </StackPanel>
        </StackPanel>
    </ScrollViewer>
</Window>
```

### Dialog Layout Rules Summary

| Rule | Value |
|------|-------|
| Label column width | 100px |
| Control column | `*` (fill remaining) |
| Row spacing | `Margin="0,8,0,0"` on subsequent rows |
| Content margin | `Margin="20"` on outer StackPanel |
| Content spacing | `Spacing="10"` on outer StackPanel |
| Section headers | `FontWeight="SemiBold"` |
| Button width | 80px |
| Button spacing | 10px |
| Button top margin | `Margin="0,20,0,0"` |
| Checkbox alignment | Under controls (Grid.Column="1"), not labels |
| Window startup | `CenterOwner` |
| Resizable | `CanResize="true"` with Min dimensions |

## Dialog Code-Behind Pattern

```csharp
public partial class EditSomethingDialog : Window
{
    private readonly SomeElement _element;

    public EditSomethingDialog(SomeElement element)
    {
        _element = element ?? throw new ArgumentNullException(nameof(element));
        InitializeComponent();

        // Initialize controls
        Control1.UnitType = typeof(SomeUnit);
        PopulateFromElement();

        // Window state persistence
        Utilities.WindowStateManager.RestoreDialogSize(this, nameof(EditSomethingDialog));
        Closing += (s, e) => Utilities.WindowStateManager.SaveDialogSize(this, nameof(EditSomethingDialog));
    }

    private void PopulateFromElement()
    {
        Control1.SetValue(_element.SomeProperty);
    }

    public void Save()
    {
        var value = Control1.GetValue<SomeUnit>();
        if (value.HasValue) _element.SomeProperty = value.Value;
    }

    private void OnOK(object? sender, RoutedEventArgs e) { Save(); Close(); }
    private void OnCancel(object? sender, RoutedEventArgs e) { Close(); }
}
```

## Control Design Rules

### Architecture
- **Controller pattern:** Pure C# logic in `Controllers/`, thin UI wrapper in `Controls/`
- Controller has NO Avalonia dependencies — easy to unit test
- Control calls controller methods (via reflection for generic types)

### Behavior
- **No validation in controls** — validate at application level
- **Min/Max for UI only** — controls increment/decrement step, NOT input rejection
- **Precision transparency** — store original values; if user hasn't changed the display, return the original precise value
- **Events over properties** — raise `Changed` event, let the application decide what to do

### Value Access Pattern (direct UI access)

```csharp
// GET: always read from UI controls directly (no stored state)
public object? Value
{
    get => _controller.Value(NumericPart?.Text ?? "", unit, DecimalPoints, Culture);
    set
    {
        NumericPart.Text = text;
        SelectUnit(unit);
    }
}

// Events just notify — never update properties in handlers
NumericPart.TextChanged += (s, e) => Changed?.Invoke(this, EventArgs.Empty);
```

### What NOT to Do
- Do NOT use StyledProperty with TwoWay binding (causes circular notification loops)
- Do NOT update property values inside event handlers
- Do NOT use generic type parameters on UserControl (XAML doesn't support it) — use `Type` property + reflection instead
- Do NOT add recursion guards — if you need them, the design is wrong

## Controller Creation

Controllers are always created as part of a control — never standalone. They live in `Controllers/` and contain ALL complex logic so the control code-behind stays thin.

### Controller rules

1. **Zero Avalonia dependencies** — no `using Avalonia.*` anywhere
2. **Must be independently testable** — constructor takes no UI parameters
3. **Add `[assembly: InternalsVisibleTo("ProjectName.Tests")]`** at top of file
4. **Namespace:** `ProjectName.Controllers`
5. **Configuration via properties** with sensible defaults, not constructor parameters

### Standard controller API surface

Every input controller follows this method pattern (adapt names to your domain):

```csharp
public class SomethingController  // or SomethingController<T> where T : Enum
{
    // Configuration properties with defaults
    public double Increment { get; set; } = 1.0;
    public double Minimum { get; set; } = -10000.0;
    public double Maximum { get; set; } = 10000.0;
    public int? DecimalPoints { get; set; } = null;

    // 1. Enumerate options (for ComboBox population)
    public IReadOnlyList<OptionType> GetOptions(out int defaultIndex) { }

    // 2. Parse text → typed value (returns null on invalid/empty input)
    public ValueType? Value(string text, ..., int? accuracy, CultureInfo? culture = null) { }

    // 3. Format typed value → text + selection state (out parameters)
    public void ParseValue(ValueType value, out string text, out OptionType option,
                           int? decimalPoints = null, CultureInfo? culture = null) { }

    // 4. Increment/decrement (clamps to Min/Max, rounds to DecimalPoints)
    public string IncrementValue(string currentText, bool increment,
                                 CultureInfo? culture = null) { }

    // 5. Character filter for real-time input validation
    public bool AllowKeyInEditor(string currentText, int caretIndex,
                                 int selectionLength, char character,
                                 CultureInfo? culture = null) { }
}
```

Not every controller needs all five methods. Omit what the control doesn't need:
- Simple display controls may only need `Value()` and `ParseValue()`
- Geometry controllers (e.g., WindDirectionController) have domain-specific methods instead

### Culture handling

```csharp
// Always accept optional culture, default to InvariantCulture
public ValueType? Value(string text, ..., CultureInfo? culture = null)
{
    culture ??= CultureInfo.InvariantCulture;
    // ...
}
```

### Min/Max semantics in controllers

```csharp
// IncrementValue clamps to Min/Max
newValue = Math.Max(Minimum, Math.Min(Maximum, newValue));

// Value() does NOT reject out-of-range input
// Comment this explicitly:
// Note: Min/Max are only used for increment/decrement, not validation
```

### Generic controller + reflection bridge

When a controller is generic but XAML can't use generics:

**Controller** — generic, clean:
```csharp
public class MeasurementController<T> where T : Enum
{
    public Measurement<T>? Value(string text, T unit, int? accuracy, CultureInfo? culture = null) { }
}
```

**Control** — non-generic, uses `Type` property + reflection:
```csharp
public partial class MeasurementControl : UserControl
{
    private object? _controller;  // MeasurementController<T> via reflection
    private Type? _unitType;

    private void InitializeController()
    {
        var controllerType = typeof(MeasurementController<>).MakeGenericType(_unitType);
        _controller = Activator.CreateInstance(controllerType);
        SyncPropertiesToController();
    }

    // Call controller methods via reflection
    public object? Value
    {
        get
        {
            var valueMethod = _controller.GetType().GetMethod("Value");
            return valueMethod?.Invoke(_controller, new object?[] { text, unit, DecimalPoints, Culture });
        }
    }
}
```

### Syncing StyledProperty changes to controller

```csharp
this.PropertyChanged += (s, e) =>
{
    if (e.Property == IncrementProperty)
        _controller?.GetType().GetProperty("Increment")?.SetValue(_controller, (double)e.NewValue!);
    else if (e.Property == MinimumProperty)
        _controller?.GetType().GetProperty("Minimum")?.SetValue(_controller, (double)e.NewValue!);
    // ... etc
};
```

### Event wiring pattern

```csharp
private void WireEvents()
{
    this.GotFocus += (s, e) => NumericPart?.Focus();

    if (NumericPart != null)
    {
        NumericPart.KeyDown += NumericPart_KeyDown;
        NumericPart.AddHandler(TextInputEvent, NumericPart_TextInput, RoutingStrategies.Tunnel);
        NumericPart.TextChanged += (s, e) => Changed?.Invoke(this, EventArgs.Empty);
    }

    if (UnitPart != null)
    {
        UnitPart.SelectionChanged += (s, e) => Changed?.Invoke(this, EventArgs.Empty);
    }
}
```

### Keyboard handling pattern

```csharp
private void NumericPart_KeyDown(object? sender, KeyEventArgs e)
{
    if (e.Key == Key.Up)   { DoIncrement(true);  e.Handled = true; }
    if (e.Key == Key.Down) { DoIncrement(false); e.Handled = true; }
    if (e.Key == Key.Tab)  { UnitPart.Focus();   e.Handled = true; }
}

private void NumericPart_TextInput(object? sender, TextInputEventArgs e)
{
    // Delegate to controller.AllowKeyInEditor() — reject invalid chars
    var allowed = (bool)(allowKeyMethod?.Invoke(_controller, new object?[] {
        NumericPart.Text, NumericPart.CaretIndex,
        NumericPart.SelectionEnd - NumericPart.SelectionStart, c, Culture
    }) ?? false);

    if (!allowed) e.Handled = true;
}
```

## Panel Design

Panels are **desktop-only** (not shared with mobile). They follow the same layout rules as dialogs but are embedded in the main window rather than standalone windows.

### Panel Properties Pattern
```csharp
public MeasurementSystem MeasurementSystem { get; set; }  // Switch units
public SomeDataType Data { get; set; }                     // Get/Set all values
public event EventHandler Changed;                          // Notify parent
```

## File Organization

```
Controls/           → XAML + code-behind (thin UI layer)
Controllers/        → Pure C# logic (no UI dependencies)
Models/             → Data models (UnitItem, DragTableInfo, etc.)
```

## Testing

- **TDD:** Write tests FIRST using xUnit + Avalonia.Headless + AwesomeAssertions
- Test controllers directly (pure logic, no UI needed)
- Test controls with `[AvaloniaFact]` attribute
- Use DebugApp for visual/exploratory testing after tests pass
- Test with realistic ballistics domain values

## App.axaml Pattern

```xml
<Application.Resources>
    <x:Double x:Key="AppFontSize">13</x:Double>
</Application.Resources>

<Application.Styles>
    <StyleInclude Source="avares://Classic.Avalonia.Theme/ClassicTheme.axaml"/>
    <Style Selector=":is(TemplatedControl)">
        <Setter Property="FontSize" Value="{DynamicResource AppFontSize}" />
    </Style>
</Application.Styles>
```
