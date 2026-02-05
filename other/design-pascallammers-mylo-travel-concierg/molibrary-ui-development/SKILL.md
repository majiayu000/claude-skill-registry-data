---
name: MoLibrary UI Development
description: This skill should be used when the user asks to "create UI component", "build Blazor page", "add MudBlazor component", "style MudBlazor", "fix CSS isolation", "use ::deep selector", "customize theme", "support dark mode", "migrate MudBlazor v8", "use OnAfterRenderAsync", or needs guidance on Blazor component lifecycle, MudBlazor styling patterns, CSS isolation, theme customization, or offline UI requirements in the MoLibrary framework.
version: 1.0.0
---

# MoLibrary UI Development Guide

This skill provides essential guidance for developing Blazor UI components with MudBlazor 8.9.0 in the MoLibrary framework.

## Critical Rules

### 1. CSS Isolation Requirements

**Never use `<style>` tags.** Always use CSS isolation with `.razor.css` files.

**CSS isolation only applies to HTML elements, NOT to Razor components.** MudBlazor components generate elements at runtime, so they won't receive the CSS isolation attribute.

To style MudBlazor components:
1. Wrap the component with a container element
2. Use the `::deep` selector pattern

```razor
<!-- Correct Pattern -->
<div class="table-wrapper">
    <MudTable Items="@items">
        ...
    </MudTable>
</div>
```

```css
/* In .razor.css file */
.table-wrapper ::deep .mud-table {
    background-color: var(--mud-palette-surface);
}

.table-wrapper ::deep tr.mud-selected {
    background-color: var(--mud-palette-action-default-hover) !important;
}
```

**Common mistake:** Using `::deep` without a wrapper element will not work.

For detailed CSS isolation fixing workflow, see `references/css-isolation-fix-workflow.md`.

### 2. MudBlazor Icon Property

Always use the `@` prefix when referencing icons:

```razor
<!-- Correct -->
<MudIconButton Icon="@Icons.Material.Filled.Add" />
<MudButton StartIcon="@Icons.Material.Filled.Save">Save</MudButton>

<!-- Wrong - Icon will not display -->
<MudIconButton Icon="Icons.Material.Filled.Add" />
```

### 3. Generic Component Type Parameters

Explicitly specify type parameter `T` for generic MudBlazor components:

```razor
<!-- Correct -->
<MudSwitch T="bool" @bind-Value="@isEnabled" />
<MudChip T="string" Value="@chipValue" />
<MudTextField T="string" @bind-Value="@textValue" />
<MudSelect T="int" @bind-Value="@selectedId">
    <MudSelectItem T="int" Value="1">Option 1</MudSelectItem>
</MudSelect>

<!-- Wrong - May cause type inference errors -->
<MudSwitch @bind-Value="@isEnabled" />
```

### 4. Component Lifecycle

**Never perform JavaScript interop or time-consuming operations in `OnInitializedAsync`.**

During static rendering, JS interop calls can only execute in `OnAfterRenderAsync`. Place initialization logic there:

```csharp
protected override async Task OnAfterRenderAsync(bool firstRender)
{
    if (firstRender)
    {
        // JavaScript interop
        await JSRuntime.InvokeVoidAsync("initializeChart");

        // Time-consuming data loading
        await LoadDataAsync();

        StateHasChanged();
    }
}
```

Use `CancellationToken` for async operations:

```csharp
@implements IAsyncDisposable

@code {
    private CancellationTokenSource? _cts;

    protected override async Task OnAfterRenderAsync(bool firstRender)
    {
        if (firstRender)
        {
            _cts = new CancellationTokenSource();
            await LoadDataAsync(_cts.Token);
        }
    }

    public async ValueTask DisposeAsync()
    {
        _cts?.Cancel();
        _cts?.Dispose();
    }
}
```

### 5. Theme and Color Usage

**Always use MudBlazor CSS variables for colors.** Never hardcode color values.

```css
/* Correct */
.my-component {
    background-color: var(--mud-palette-surface);
    color: var(--mud-palette-text-primary);
    border-color: var(--mud-palette-lines-default);
}

/* Wrong */
.my-component {
    background-color: #ffffff;
    color: #424242;
}
```

**Support both light and dark modes.** All custom colors must consider theme switching.

Common palette variables:
- `--mud-palette-primary` / `--mud-palette-primary-text`
- `--mud-palette-surface` / `--mud-palette-background`
- `--mud-palette-text-primary` / `--mud-palette-text-secondary`
- `--mud-palette-lines-default` / `--mud-palette-lines-inputs`
- `--mud-palette-action-default` / `--mud-palette-action-default-hover`

For complete CSS variable reference, see `references/mudblazor-css-variables.md`.

### 6. MudBlazor 8.9.0 API Requirements

**Use async methods.** Synchronous methods are deprecated:

```csharp
// Correct (v8)
var dialog = await DialogService.ShowAsync<MyDialog>();
await dataGrid.ExpandAllGroupsAsync();

// Wrong (deprecated)
var dialog = DialogService.Show<MyDialog>();
dataGrid.ExpandAllGroups();
```

**Typography class names changed:**

| Old (v7) | New (v8.9.0) |
|----------|--------------|
| `new Default()` | `new DefaultTypography()` |
| `new H1()` | `new H1Typography()` |
| `new Button()` | `new ButtonTypography()` |

**FontWeight and LineHeight are now strings:**

```csharp
// Correct (v8)
FontWeight = "400",
LineHeight = "1.43"

// Wrong (v7)
FontWeight = 400,
LineHeight = 1.43
```

**Shadow.Elevation array must have 26 elements (indices 0-25).**

For complete migration guide, see `references/migration-guide.md`.

### 7. Offline/Intranet Requirements

All UI modules must support offline environments:

- **No online font CDN**: Never reference Google Fonts, Adobe Fonts, etc.
- **Local fonts**: Store all fonts in `wwwroot/fonts/`
- **No external CDN**: All static resources must be local
- **Intranet compatibility**: Consider environments without internet access

For font management workflow, see `references/offline-requirements.md`.

## Component Architecture

### Component Hierarchy

- **Base Components (Common)**: Reusable atomic components
- **Business Components**: Feature-specific composite components
- **Page Components (Pages)**: Complete page-level components

### Single Responsibility

- Each component handles one specific function
- Complex features combine multiple simple components
- Separate presentation logic from business logic

### Component Communication

- Use `[Parameter]` for parent-to-child communication
- Use `EventCallback` for child-to-parent events
- Use state containers for complex state management

## Service Layer Patterns

### Return Value Convention

Use unified response model `Res<T>`:

```csharp
public async Task<Res<UserData>> GetUserAsync(int id)
{
    try
    {
        var user = await _repository.GetByIdAsync(id);
        return Res.Ok(user);
    }
    catch (Exception ex)
    {
        Logger.LogError(ex, "Failed to get user");
        return Res.Fail($"Failed to get user: {ex.Message}");
    }
}
```

### Service Call Pattern

```csharp
private async Task LoadDataAsync()
{
    if ((await UserService.GetDataAsync(id)).IsFailed(out var error, out var data))
    {
        Snackbar.Add($"Error: {error.Message}", Severity.Error);
        return;
    }

    // Process data
    ProcessData(data);
}
```

## Performance Optimization

### List Rendering

Use `@key` directive:

```razor
@foreach (var item in Items)
{
    <div @key="item.Id">
        <ItemComponent Item="@item" />
    </div>
}
```

### Large Data Sets

Use virtualization:

```razor
<MudVirtualize Items="@LargeDataSet" Context="item">
    <ItemTemplate>
        <ItemDisplay Item="@item" />
    </ItemTemplate>
</MudVirtualize>
```

### Avoid Unnecessary Rerenders

```csharp
protected override bool ShouldRender()
{
    return _hasDataChanged;
}
```

## Error Handling

Use `ErrorBoundary` for graceful error handling:

```razor
<ErrorBoundary>
    <ChildContent>
        <ComplexComponent />
    </ChildContent>
    <ErrorContent Context="exception">
        <MudAlert Severity="Severity.Error">
            Error: @exception.Message
        </MudAlert>
    </ErrorContent>
</ErrorBoundary>
```

## Additional Resources

### Reference Files

For comprehensive guidance, consult these reference files:

- **`references/blazor-best-practices.md`** - Component architecture, lifecycle, state management, form handling, accessibility patterns
- **`references/theme-css-guide.md`** - Theme architecture, CSS variable naming, special effects (glassmorphic, gradients), responsive design
- **`references/mudblazor-css-variables.md`** - Complete palette properties, shadows, layout properties, typography CSS variables
- **`references/component-reference.md`** - Component categories, common code examples, component properties
- **`references/migration-guide.md`** - Complete v8.9.0 breaking changes and migration patterns
- **`references/css-isolation-fix-workflow.md`** - Step-by-step workflow for fixing CSS isolation issues
- **`references/offline-requirements.md`** - Font management and offline environment requirements

### Scripts

Utility scripts for common operations:

- **`scripts/font_downloader.py`** - Download Google Fonts for offline use. Supports single URL download, batch download (`--download-all`), weight filtering (`--weights`), and custom output directory. See `references/offline-requirements.md` for detailed usage.

### Quick Search Patterns

Find component implementations:
```bash
Glob: "**/Mud{ComponentName}.razor"
Grep: "<Mud{ComponentName}"
```

Find component styles:
```bash
Glob: "**/_mud{componentname}.scss"
```

## Quick Reference

### MudBlazor Version
Current project uses **MudBlazor 8.9.0**.

### Essential Checklist

- [ ] Use CSS isolation with `.razor.css` files (no `<style>` tags)
- [ ] Wrap MudBlazor components with div + `::deep` for styling
- [ ] Use `@` prefix for Icon properties
- [ ] Specify `T` parameter for generic components
- [ ] Place JS interop in `OnAfterRenderAsync`
- [ ] Use MudBlazor CSS variables for colors
- [ ] Support both light and dark modes
- [ ] Use async methods (`ShowAsync`, not `Show`)
- [ ] Use `*Typography` class names (v8.9.0)
- [ ] Ensure offline/intranet compatibility
