---
name: winui-patterns
description: WinUI 3 and XAML patterns for the Pomodoro Time Tracker. Activates when working with ViewModels, XAML pages, data binding, or UI components.
allowed-tools:
  - Read
  - Glob
  - Grep
---

# WinUI 3 Patterns Skill

**Activates when:** ViewModels, XAML, data binding, or UI components mentioned.

## Shared WinUI Guidelines

@~/.claude/prompts/winui/mvvm/no-value-converters.md
@~/.claude/prompts/winui/fundamentals/page-setup.md
@~/.claude/prompts/winui/mvvm/dialog-callbacks.md
@~/.claude/prompts/winui/mvvm/timer-pattern.md
@~/.claude/prompts/dotnet/fundamentals/async-await.md

---

## Project-Specific Conventions

### CRITICAL: No Value Converters

```csharp
// ❌ NEVER
Visibility="{x:Bind Converter={StaticResource BoolToVisibility}}"

// ✅ ALWAYS
public bool IsVisible => SomeCondition;
Visibility="{x:Bind ViewModel.IsVisible, Mode=OneWay}"
```

WinUI 3's x:Bind auto-converts `bool` to `Visibility`.

### Always Use x:Bind

```xml
<!-- ✅ CORRECT - Compile-time checked -->
<TextBox Text="{x:Bind ViewModel.Name, Mode=TwoWay, UpdateSourceTrigger=PropertyChanged}" />

<!-- ❌ WRONG - Runtime binding -->
<TextBox Text="{Binding Name, Mode=TwoWay}" />
```

### Binding Modes

| Mode | Use Case |
|------|----------|
| `OneTime` | Static data |
| `OneWay` | Display-only |
| `TwoWay` | User input |

### Key Namespaces

```csharp
using PomodoroTimeTracker.ViewModels;
using PomodoroTimeTracker.Application.DTOs;
using PomodoroTimeTracker.Application.Interfaces;
```

### DI Registration

```csharp
// ViewModels - Transient (CRUD) or Singleton (Timers)
services.AddTransient<ClientDetailViewModel>();
services.AddSingleton<PomodoroViewModel>();

// UI Services - Singleton
services.AddSingleton<INavigationService, NavigationService>();
services.AddSingleton<IDialogService, DialogService>();
```

### Common Mistakes to Avoid

1. **InitializeComponent before ViewModel** - ViewModel must exist first
2. **Binding instead of x:Bind** - Always use x:Bind
3. **async void** - Only for framework handlers
4. **Value converters** - Use explicit properties instead
5. **XamlRoot missing** - ContentDialog requires `XamlRoot = this.XamlRoot`
