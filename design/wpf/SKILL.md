---
name: wpf
description: 'ATC WPF controls library (160+ controls, forms, components, theming) and cross-platform XAML toolkit (MVVM, source generators, behaviors). Use when the user asks to build a WPF desktop application, add WPF controls or forms, implement MVVM with source generators, use ObservableProperty or RelayCommand attributes, create dependency properties, set up Light/Dark theming, add font icons, use layout panels like GridEx or FlexPanel, implement dialogs or flyouts, add toast notifications, work with value converters, implement drag-and-drop, build cross-platform XAML with WinUI 3 or Avalonia, or use the ObservableDtoViewModel generator.'
---

# ATC WPF & XAML Toolkit

Two complementary libraries for building enterprise-ready desktop applications:

- **Atc.Wpf** — 160+ WPF controls, forms, components, theming, and font icons organized in a four-tier architecture
- **Atc.XamlToolkit** — Cross-platform MVVM foundation with source generators, behaviors, messaging, and value converters supporting WPF, WinUI 3, and Avalonia

> **Mental model:** Atc.XamlToolkit provides the MVVM engine (ViewModelBase, commands, source generators). Atc.Wpf provides the visual building blocks (controls, forms, components, theming). Use them together for WPF; use Atc.XamlToolkit alone for WinUI 3 or Avalonia.

Detailed reference material lives in the `references/` folder — load on demand.

---

## References

| Reference | When to load |
|---|---|
| [Control Catalog](references/control-catalog.md) | Full inventory of 160+ controls by category |
| [Source Generators](references/source-generators.md) | ObservableProperty, RelayCommand, DependencyProperty, AttachedProperty, ObservableDtoViewModel, ComputedProperty |
| [Theming & Icons](references/theming-icons.md) | Light/Dark mode, NiceWindow, accent colors, font icon families |
| [MVVM Infrastructure](references/mvvm-infrastructure.md) | ViewModelBase, commands, messaging, validation, services |
| [Behaviors & Converters](references/behaviors-converters.md) | EventToCommand, animation, focus, keyboard navigation, 36+ value converters |
| [Layout Panels](references/layout-panels.md) | GridEx, FlexPanel, AutoGrid, StaggeredPanel, ResponsivePanel, UniformSpacingPanel |

---

## 1. Architecture Overview

### Four-Tier Control Architecture (Atc.Wpf)

| Tier | Package | Purpose | Examples |
|---|---|---|---|
| 1. Base | `Atc.Wpf` | MVVM, layouts, converters — no UI controls | ViewModelBase, GridEx, FlexPanel |
| 2. Controls | `Atc.Wpf.Controls` | Atomic/primitive controls | IntegerBox, ToggleSwitch, Carousel, ColorPicker |
| 3. Forms | `Atc.Wpf.Forms` | 25+ labeled form fields with validation | LabelTextBox, LabelComboBox, LabelDatePicker |
| 4. Components | `Atc.Wpf.Components` | Composite high-level components | InfoDialogBox, Flyout, JsonViewer, ToastNotification |

**Additional packages:**

| Package | Purpose |
|---|---|
| `Atc.Wpf.FontIcons` | Font-based icon rendering (6 icon families) |
| `Atc.Wpf.Theming` | Light/Dark mode theming infrastructure |
| `Atc.Wpf.Network` | Network scanning and discovery controls |
| `Atc.Wpf.Controls.Sample` | Controls for building sample/demo applications |

### Cross-Platform Packages (Atc.XamlToolkit)

| Package | Platform | Dependencies |
|---|---|---|
| `Atc.XamlToolkit` | All | Base: ViewModelBase, ObservableObject, messaging |
| `Atc.XamlToolkit.Wpf` | WPF | Commands, behaviors, converters for WPF |
| `Atc.XamlToolkit.WinUI` | WinUI 3 | Commands, behaviors, converters for WinUI |
| `Atc.XamlToolkit.Avalonia` | Avalonia | Commands, behaviors, converters for Avalonia |
| `Atc.XamlToolkit.SourceGenerators` | All | Source generators (bundled inside `Atc.XamlToolkit`, not a separate NuGet package) |
| `Atc.XamlToolkit.XamlStyler` | All | XAML formatting engine |

---

## 2. Quick Start — WPF Application

### Step 1: Install packages

```xml
<PackageReference Include="Atc.XamlToolkit.Wpf" Version="*" />
<PackageReference Include="Atc.Wpf.Components" Version="*" />
<PackageReference Include="Atc.Wpf.Theming" Version="*" />
```

### Step 2: Create a ViewModel with source generators

```csharp
// All source generator attributes ([ObservableProperty], [RelayCommand], [ComputedProperty],
// [DependencyProperty], [AttachedProperty], [RoutedEvent], [ObservableDtoViewModel])
// live in the Atc.XamlToolkit.Mvvm namespace — same as ViewModelBase.
// Do NOT use Atc.XamlToolkit.SourceGenerators.Attributes — that namespace does not exist.
using Atc.XamlToolkit.Mvvm;

public partial class MainViewModel : ViewModelBase
{
    [ObservableProperty]
    private string name = string.Empty;

    [ObservableProperty]
    private int age;

    [RelayCommand]
    private async Task SaveAsync(CancellationToken cancellationToken)
    {
        IsBusy = true;
        // Save logic here
        IsBusy = false;
    }
}
```

This generates:
- `Name` property with `INotifyPropertyChanged`
- `Age` property with `INotifyPropertyChanged`
- `SaveCommand` async command property with cancellation support

### Step 3: Use themed window and controls

```xml
<theming:NiceWindow x:Class="MyApp.MainWindow"
    xmlns:theming="clr-namespace:Atc.Wpf.Theming.Windows;assembly=Atc.Wpf.Theming"
    xmlns:forms="clr-namespace:Atc.Wpf.Forms.Controls;assembly=Atc.Wpf.Forms"
    xmlns:controls="clr-namespace:Atc.Wpf.Controls.BaseControls;assembly=Atc.Wpf.Controls">

    <StackPanel>
        <forms:LabelTextBox LabelText="Name" Value="{Binding Name}" />
        <forms:LabelIntegerBox LabelText="Age" Value="{Binding Age}" />
        <Button Content="Save" Command="{Binding SaveCommand}" />
    </StackPanel>
</theming:NiceWindow>
```

---

## 3. Source Generators

All generators work at compile time — zero runtime reflection.

| Attribute | Platform | Generates |
|---|---|---|
| `[ObservableProperty]` | WPF, WinUI, Avalonia | Property with INotifyPropertyChanged |
| `[ComputedProperty]` | WPF, WinUI, Avalonia | Property with auto-detected dependencies |
| `[RelayCommand]` | WPF, WinUI, Avalonia | IRelayCommand property from method |
| `[DependencyProperty]` | WPF, WinUI | DependencyProperty registration |
| `[StyledProperty]` | Avalonia | StyledProperty registration |
| `[AttachedProperty]` | WPF, WinUI, Avalonia | Attached property with Get/Set methods |
| `[RoutedEvent]` | WPF only | RoutedEvent with EventManager registration |
| `[ObservableDtoViewModel]` | WPF, WinUI, Avalonia | ViewModel wrapper with IsDirty tracking |

### RelayCommand with Cancellation

```csharp
[RelayCommand(SupportsCancellation = true)]
private async Task LoadDataAsync(CancellationToken cancellationToken)
{
    // Long-running operation
}
```

Generates: `LoadDataCommand`, `LoadDataCancelCommand`, and `CancelLoadData()` method.

### ObservableDtoViewModel

```csharp
[ObservableDtoViewModel(typeof(PersonDto))]
public partial class PersonViewModel : ViewModelBase { }
```

Generates a full ViewModel wrapping `PersonDto` with:
- All properties with change notification
- `IsDirty` tracking
- `InnerModel` access to the underlying DTO
- Method proxies
- Validation attribute copying

See [Source Generators](references/source-generators.md) for all options and platform-specific details.

---

## 4. Controls Quick Reference

### Input Controls
`NumericBox`, `IntegerBox`, `DecimalBox`, `CurrencyBox`, `ToggleSwitch`, `RangeSlider`, `Rating`, `FilePicker`, `DirectoryPicker`

### Buttons
`ImageButton`, `SplitButton`, `AuthenticationButton`, `ConnectivityButton`

### Color Controls
`HueSlider`, `SaturationBrightnessPicker`, `TransparencySlider`, `WellKnownColorPicker`

### Data Display
`Alert`, `Card`, `Badge`, `Chip`, `Avatar`, `AvatarGroup`, `Divider`, `Carousel`, `Breadcrumb`, `Stepper`, `Segmented`, `Timeline`, `Popover`

### Layout Panels
`GridEx`, `AutoGrid`, `FlexPanel`, `StaggeredPanel`, `UniformSpacingPanel`, `ResponsivePanel`, `DockPanelPro`

### Selectors
`CountrySelector`, `LanguageSelector`, `FontFamilySelector`, `DualListSelector`

### Progress & Loading
`BusyOverlay`, `LoadingIndicator`, `Overlay`, `Skeleton`

### 25+ Labeled Form Controls
`LabelTextBox`, `LabelIntegerBox`, `LabelDecimalBox`, `LabelComboBox`, `LabelDatePicker`, `LabelColorPicker`, `LabelToggleSwitch`, `LabelFilePicker`, `LabelDirectoryPicker`, and more — each with built-in label, validation, and consistent styling.

### Composite Components
`InfoDialogBox`, `QuestionDialogBox`, `InputDialogBox`, `InputFormDialogBox`, `ColorPickerDialogBox`, `BasicApplicationSettingsDialogBox`, `Flyout`, `FlyoutHost`, `JsonViewer`, `TerminalViewer`, `ToastNotification`, `PrintPreviewWindow`, `UndoRedoHistoryView`

See [Control Catalog](references/control-catalog.md) for the full inventory.

---

## 5. Theming

**NiceWindow** — themed window replacement with built-in title bar, minimize/maximize/close buttons, Light/Dark mode support:

```xml
<theming:NiceWindow x:Class="MyApp.MainWindow" ... >
```

**ThemeSelector** — built-in control for switching themes:
```xml
<theming:ThemeSelector />
```

**AccentColorSelector** — pick accent color:
```xml
<theming:AccentColorSelector />
```

See [Theming & Icons](references/theming-icons.md).

---

## 6. Font Icons

Six icon families available via `Atc.Wpf.FontIcons`:

| Family | Variants | Glyphs |
|---|---|---|
| FontAwesome 5 | Regular, Solid, Brands | 1,600+ |
| FontAwesome 7 | Regular, Solid, Brands | 2,000+ |
| Bootstrap Icons | — | 1,800+ |
| Material Design | — | 2,100+ |
| Weather Icons | — | 200+ |
| IcoFont | — | 2,100+ |

Usage in XAML:
```xml
<fontIcons:FontIcon IconType="FontAwesome5Solid" IconName="fa-check" FontSize="16" />
```

---

## 7. MVVM Infrastructure

### ViewModelBase Built-in Properties

| Property | Type | Purpose |
|---|---|---|
| `IsEnable` | bool | Enable/disable state |
| `IsVisible` | bool | Visibility state |
| `IsBusy` | bool | Loading/processing state |
| `IsDirty` | bool | Change tracking |
| `IsSelected` | bool | Selection state |

### Commands

| Type | Async | Cancellation |
|---|---|---|
| `RelayCommand` | No | No |
| `RelayCommand<T>` | No | No |
| `RelayCommandAsync` | Yes | Yes |
| `RelayCommandAsync<T>` | Yes | Yes |

### Messaging System

```csharp
// Send
Messenger.Default.Send(new GenericMessage<string>("Hello"));

// Receive
Messenger.Default.Register<GenericMessage<string>>(this, msg => { ... });
```

Message types: `GenericMessage<T>`, `NotificationMessage`, `PropertyChangedMessage<T>`, `NotificationMessageAction`.

### Services

| Service | Interface | Purpose |
|---|---|---|
| Clipboard | `IClipboardService` | Clipboard operations |
| UndoRedo | `IUndoRedoService` | Undo/redo stack |
| Hotkeys | `IHotkeyService` | Global hotkey registration |
| Navigation | `INavigationService` | Page/view navigation |
| Printing | `IPrintService` | Print and preview |
| Toast | `IToastNotificationService` | Toast notifications |
| Capture | `ICaptureService` | Screen capture |
| BusyIndicator | `IBusyIndicatorService` | Global busy state |

See [MVVM Infrastructure](references/mvvm-infrastructure.md).

---

## 8. Behaviors

Cross-platform behaviors (WPF, WinUI 3, Avalonia):

| Behavior | Purpose |
|---|---|
| `EventToCommandBehavior` | Execute commands from any UI event |
| `AnimationBehavior` | FadeIn/Out, SlideIn, ScaleIn/Out (8 types) |
| `FocusBehavior` | Initial focus, two-way bindable, select-all-on-focus |
| `KeyboardNavigationBehavior` | Arrow keys, Enter, Escape, Tab navigation |

### 36+ Value Converters

Bool converters, string converters, null converters, visibility converters, and multi-value converters. See [Behaviors & Converters](references/behaviors-converters.md).

---

## 9. Network Scanning

`Atc.Wpf.Network` provides a `NetworkScannerView` control for IP scanning, port scanning, and device discovery. Requires `Atc.Network` package.

---

## 10. Requirements

| Requirement | Version |
|---|---|
| .NET SDK | 10.0+ |
| Runtime | .NET 10 Desktop Runtime (WPF) |
| OS | Windows 10 or later |
| C# | 14.0 |
