---
name: avalonia-ui-tests
description: Rules and patterns for writing tests of Avalonia UI visual elements (controls, dialogs, panels). Use when creating or modifying tests for XAML controls, dialogs, or panels.
---

# Avalonia UI Testing Rules

Follow these rules strictly when writing tests for visual elements (controls, dialogs, panels) in this project.

## Core Principles

- **TDD** — write tests FIRST, implement second
- **Test actual behavior** — don't test implementation details
- **AAA pattern** — Arrange, Act, Assert with comments marking each section
- **Realistic data** — use real ballistics domain values, not toy data
- **No event testing in headless** — UI events don't fire reliably in Avalonia headless; test events indirectly or defer to DebugApp

## Test Attributes

| What you're testing | Attribute |
|---------------------|-----------|
| Pure logic (controllers, models) | `[Fact]` or `[Theory]` |
| Anything that instantiates a control/dialog/window | `[AvaloniaFact]` |
| Parameterized tests | `[Theory]` + `[InlineData(...)]` |

**Rule:** If the test creates ANY Avalonia `UserControl`, `Window`, or `Control` subclass, it MUST use `[AvaloniaFact]` (not `[Fact]`). This includes dialogs.

## Test Naming Convention

```
MethodUnderTest_Scenario_ExpectedBehavior
```

Examples:
- `Value_WithValidText_ShouldReturnMeasurement`
- `Constructor_ValidArc_ControlsPopulatedFromElement`
- `Save_ModifiedControls_ElementUpdated`
- `GetUnits_ForDistanceUnit_ShouldReturnAllUnits`
- `IncrementValue_AtMaximum_ShouldNotExceedMaximum`

## Test File Organization

### Namespace & Location

| Test target | Namespace | Location |
|-------------|-----------|----------|
| Controller (pure logic) | `[Project].Tests.Controllers` | `Tests/Controllers/` |
| Control (UI) | `[Project].Tests.UI` | `Tests/UI/` |
| Dialog | `[Project].Tests.Dialogs` | `Tests/Dialogs/` |

### Within a file — use `#region` blocks

```csharp
public class MeasurementControllerTests
{
    #region Unit Enumeration Tests
    [Fact]
    public void GetUnits_ForDistanceUnit_ShouldReturnAllUnits() { }
    #endregion

    #region Value Parsing Tests
    [Fact]
    public void Value_WithValidText_ShouldReturnMeasurement() { }
    #endregion

    #region Increment/Decrement Tests
    [Fact]
    public void IncrementValue_AtMaximum_ShouldNotExceedMaximum() { }
    #endregion
}
```

## Assertions — AwesomeAssertions Only

Always use AwesomeAssertions fluent API. Never use `Assert.Equal()` or xUnit asserts.

```csharp
using AwesomeAssertions;

// Null checks
result.Should().NotBeNull();
result.Should().BeNull();

// Equality
value.Should().Be(expected);
value.Should().NotBe(unexpected);
value.Should().BeApproximately(expected, tolerance);

// Comparison
value.Should().BeGreaterThan(min);
value.Should().BeLessThanOrEqualTo(max);

// Boolean
flag.Should().BeTrue();
flag.Should().BeFalse();

// String
text.Should().Be("100.46");
text.Should().NotBeNullOrEmpty();
text.Should().Contain(".");

// Collection
items.Should().NotBeEmpty();
items.Should().HaveCount(5);
items.Should().Contain(item);
items.Should().AllSatisfy(x => x.Should().NotBeNull());

// Type
result.Should().BeOfType<EditLineDialog>();

// With context message
tables.Should().Contain(t => t.Value == enumValue,
    $"DragTableId.{enumValue} should be in the returned tables");
```

## Control Test Patterns

### Instantiation — always set UnitType first

```csharp
[AvaloniaFact]
public void Control_ShouldInitialize()
{
    // Arrange & Act
    var control = new MeasurementControl { UnitType = typeof(DistanceUnit) };

    // Assert
    control.Should().NotBeNull();
    control.IsEmpty.Should().BeTrue();
}
```

**Rule:** `UnitType` must be set BEFORE calling `SetValue()` — it creates the internal controller.

### Value round-trip

```csharp
[AvaloniaFact]
public void Value_SetAndGet_ShouldRoundTrip()
{
    // Arrange
    var control = new MeasurementControl { UnitType = typeof(DistanceUnit) };
    var measurement = new Measurement<DistanceUnit>(100, DistanceUnit.Meter);

    // Act
    control.SetValue(measurement);
    var result = control.GetValue<DistanceUnit>();

    // Assert
    result.Should().NotBeNull();
    result!.Value.Value.Should().Be(100);
    result.Value.Unit.Should().Be(DistanceUnit.Meter);
}
```

### Precision transparency

```csharp
[AvaloniaFact]
public void Value_SetAndGet_WithoutEdit_ShouldPreserveOriginalPrecision()
{
    // Arrange
    var control = new BallisticCoefficientControl { DecimalPoints = 3 };
    var original = new BallisticCoefficient(0.45678, DragTableId.G1);

    // Act
    control.Value = original;

    // Assert — display is rounded but getter returns exact original
    control.NumericPart.Text.Should().Be("0.457");
    control.Value!.Value.Value.Should().Be(0.45678);
}
```

### Min/Max is for UI only, not validation

```csharp
[Fact]
public void Value_BelowMinimum_ShouldStillAccept()
{
    // Arrange: Min/Max are only for increment/decrement, not validation
    var controller = new MeasurementController<DistanceUnit> { Minimum = 0 };

    // Act: Negative values should be accepted
    var result = controller.Value("-10", DistanceUnit.Meter, null, CultureInfo.InvariantCulture);

    // Assert
    result.Should().NotBeNull();
    result!.Value.Value.Should().Be(-10);
}
```

### Direct UI access in tests

Tests can read internal control parts directly:

```csharp
// Text content
control.NumericPart.Text.Should().Be("100.46");

// ComboBox selection
control.UnitPart.Items.Count.Should().BeGreaterThan(0);
var selectedUnit = (UnitItem)control.UnitPart.SelectedItem!;
selectedUnit.Unit.Should().Be(DistanceUnit.Meter);

// CheckBox state
dialog.ClockwiseCheckBox.IsChecked.Should().BeTrue();
```

This works because control parts use `x:FieldModifier="internal"` and the test project has a project reference.

## Dialog Test Patterns

### Constructor populates from element

```csharp
[AvaloniaFact]
public void Constructor_ValidElement_ControlsPopulatedFromElement()
{
    // Arrange
    var arc = new ReticlePathElementArc
    {
        Position = new ReticlePosition(1, 2, AngularUnit.Mil),
        Radius = new Measurement<AngularUnit>(0.5, AngularUnit.Mil),
        ClockwiseDirection = true,
        MajorArc = true
    };

    // Act
    var dialog = new EditArcDialog(arc);

    // Assert
    dialog.PositionX.GetValue<AngularUnit>().Should().Be(arc.Position.X);
    dialog.PositionY.GetValue<AngularUnit>().Should().Be(arc.Position.Y);
    dialog.RadiusControl.GetValue<AngularUnit>().Should().Be(arc.Radius);
    dialog.ClockwiseCheckBox.IsChecked.Should().BeTrue();
    dialog.MajorArcCheckBox.IsChecked.Should().BeTrue();
}
```

### Save pushes values back to element

```csharp
[AvaloniaFact]
public void Save_ModifiedControls_ElementUpdated()
{
    // Arrange
    var arc = new ReticlePathElementArc
    {
        Position = new ReticlePosition(1, 2, AngularUnit.Mil),
        Radius = new Measurement<AngularUnit>(0.5, AngularUnit.Mil)
    };
    var dialog = new EditArcDialog(arc);

    // Act — modify controls
    dialog.PositionX.SetValue(new Measurement<AngularUnit>(10, AngularUnit.MOA));
    dialog.RadiusControl.SetValue(new Measurement<AngularUnit>(2, AngularUnit.Mil));

    // Assert — element NOT changed yet (no auto-save)
    arc.Position.X.Should().NotBe(new Measurement<AngularUnit>(10, AngularUnit.MOA));

    // Act — explicit save
    dialog.Save();

    // Assert — element IS changed now
    arc.Position.X.Should().Be(new Measurement<AngularUnit>(10, AngularUnit.MOA));
    arc.Radius.Should().Be(new Measurement<AngularUnit>(2, AngularUnit.Mil));
}
```

### Null property initialization

```csharp
[AvaloniaFact]
public void Save_NullPosition_InitializesPosition()
{
    // Arrange
    var arc = new ReticlePathElementArc { Position = null };
    var dialog = new EditArcDialog(arc);

    // Act
    dialog.PositionX.SetValue(new Measurement<AngularUnit>(5, AngularUnit.Mil));
    dialog.Save();

    // Assert
    arc.Position.Should().NotBeNull();
    arc.Position!.X.Should().Be(new Measurement<AngularUnit>(5, AngularUnit.Mil));
}
```

### DialogFactory coverage

```csharp
[AvaloniaFact]
public void CreateDialogForElement_ReticleLine_ReturnsEditLineDialog()
{
    var line = new ReticleLine { Start = new ReticlePosition(0, 0, AngularUnit.Mil) };

    var dialog = DialogFactory.CreateDialogForElement(line);

    dialog.Should().NotBeNull();
    dialog.Should().BeOfType<EditLineDialog>();
}

[AvaloniaFact]
public void CreateDialogForElement_UnknownType_ReturnsNull()
{
    DialogFactory.CreateDialogForElement(new object()).Should().BeNull();
}
```

## Parameterized Tests

Use `[Theory]` + `[InlineData]` when testing the same logic across multiple inputs:

```csharp
[Theory]
[InlineData(MeasurementSystem.Metric, "Range (m)")]
[InlineData(MeasurementSystem.Imperial, "Range (yd)")]
public void XAxisTitle_ForSystem_ReturnsCorrectTitle(
    MeasurementSystem system, string expected)
{
    var controller = new ChartController(system, AngularUnit.MOA, mode, dropBase, trajectory);
    controller.XAxisTitle.Should().Be(expected);
}
```

## Test Data Helpers

For complex test data, create `private static` helper methods in the test class:

```csharp
private static TrajectoryPoint[] CreateSampleTrajectory()
{
    return new[]
    {
        CreatePoint(0, 900, 2.70, 0, 0, 0, 0, 0, 0),
        CreatePoint(100, 820, 2.46, 2.5, 2.0, 0.8, 1.5, 1.0, 0.4),
        CreatePoint(200, 745, 2.23, 8.2, 5.1, 1.4, 3.2, 2.5, 0.9),
    };
}

private static ReticleDefinition CreateTestReticle()
{
    return new ReticleDefinition
    {
        Size = new ReticlePosition(10, 10, AngularUnit.Mil),
        Zero = new ReticlePosition(5, 5, AngularUnit.Mil)
    };
}
```

## Culture-Aware Testing

Test both invariant and locale-specific cultures when testing value parsing:

```csharp
[Fact]
public void Value_WithInvariantCulture_ShouldUseDotDecimal()
{
    var result = controller.Value("100.5", DistanceUnit.Meter, null, CultureInfo.InvariantCulture);
    result!.Value.Value.Should().Be(100.5);
}

[Fact]
public void Value_WithGermanCulture_ShouldUseCommaDecimal()
{
    var culture = new CultureInfo("de-DE");
    var result = controller.Value("100,5", DistanceUnit.Meter, null, culture);
    result!.Value.Value.Should().Be(100.5);
}
```

## What NOT to Do

- Do NOT use `Assert.Equal()` — use AwesomeAssertions `.Should().Be()`
- Do NOT use `[Fact]` for tests that create Avalonia controls — use `[AvaloniaFact]`
- Do NOT test event firing directly in headless — events are unreliable; test indirectly
- Do NOT test implementation details — test observable behavior
- Do NOT share mutable state between tests
- Do NOT create abstract test base classes — keep tests simple and flat
- Do NOT validate that controls reject out-of-range input — Min/Max is UI-only
