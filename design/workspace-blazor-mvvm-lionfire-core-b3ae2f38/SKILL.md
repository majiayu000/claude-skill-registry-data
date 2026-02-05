---
name: workspace-blazor-mvvm
description: Guide for implementing LionFire workspace documents with Blazor MVVM patterns, including ObservableDataView component usage, workspace-scoped service injection, and reactive persistence. Use this skill when creating Blazor pages for workspace documents, fixing workspace service scoping issues, or implementing list/detail views with ObservableReader/Writer.
---

# Workspace Blazor MVVM Patterns

## When to Use This Skill

Use this skill when:
- Creating Blazor pages for workspace-scoped documents
- Using `ObservableDataView` component for list views
- Implementing detail pages with workspace services
- Debugging "Unable to resolve service for type 'IObservableReader'" errors
- Working with reactive persistence (`IObservableReader/Writer`) in Blazor
- Setting up workspace document types with CRUD UI

**Keywords**: workspace, ObservableDataView, IObservableReader, IObservableWriter, workspace services, CascadingParameter, Blazor MVVM, workspace scoping, workspace documents

---

## Quick Reference

### Critical Concept: Workspace Service Scoping

**The Problem**: `IObservableReader/Writer` services are **workspace-scoped**, not in the root DI container.

**The Solution**: Use `CascadingParameter` to get `WorkspaceServices` and resolve services manually.

```csharp
[CascadingParameter(Name = "WorkspaceServices")]
public IServiceProvider? WorkspaceServices { get; set; }

var reader = WorkspaceServices.GetService<IObservableReader<string, BotEntity>>();
```

**See**: `references/service-scoping.md` for complete explanation.

---

## Two Primary Patterns

### Pattern 1: ObservableDataView (List Views)

**When**: Displaying a list/grid of workspace documents with CRUD operations.

**Code** (~20-30 lines):
```razor
<ObservableDataView TKey="string"
                    TValue="BotEntity"
                    TValueVM="BotVM"
                    DataServiceProvider="@WorkspaceServices">
    <Columns>
        <PropertyColumn Property="x => x.Value.Name" />
    </Columns>
</ObservableDataView>

@code {
    [CascadingParameter(Name = "WorkspaceServices")]
    public IServiceProvider? WorkspaceServices { get; set; }
}
```

**See**: `examples/list-view-example.razor` for complete example.

### Pattern 2: Manual VM Creation (Detail Views)

**When**: Displaying/editing a single workspace document with custom layout.

**Code** (~60-80 lines):
```razor
@code {
    [CascadingParameter(Name = "WorkspaceServices")]
    public IServiceProvider? WorkspaceServices { get; set; }

    private ObservableReaderWriterItemVM<string, BotEntity, BotVM>? VM { get; set; }

    protected override async Task OnParametersSetAsync()
    {
        var reader = WorkspaceServices.GetService<IObservableReader<string, BotEntity>>();
        var writer = WorkspaceServices.GetService<IObservableWriter<string, BotEntity>>();

        VM = new ObservableReaderWriterItemVM<string, BotEntity, BotVM>(reader, writer);
        VM.Id = BotId;
    }
}
```

**See**: `examples/detail-view-example.razor` for complete example.

---

## Step-by-Step Workflows

### Workflow 1: Fix "Unable to Resolve Service" Error

When encountering:
```
InvalidOperationException: Unable to resolve service for type
'IObservableReader`2[System.String,MyEntity]'
```

**Steps**:

1. **Identify the issue**: Component trying to inject workspace-scoped services from root container

2. **Check current pattern**:
```csharp
// ❌ WRONG: Tries to inject from root
@inherits ReactiveInjectableComponentBase<ObservableReaderWriterItemVM<string, BotEntity, BotVM>>
```

3. **Fix with CascadingParameter**:
```csharp
// ✅ RIGHT: Get workspace services via cascading parameter
[CascadingParameter(Name = "WorkspaceServices")]
public IServiceProvider? WorkspaceServices { get; set; }

protected override async Task OnParametersSetAsync()
{
    var reader = WorkspaceServices.GetService<IObservableReader<string, BotEntity>>();
    var writer = WorkspaceServices.GetService<IObservableWriter<string, BotEntity>>();
    VM = new ObservableReaderWriterItemVM<string, BotEntity, BotVM>(reader, writer);
    VM.Id = ItemId;
}
```

4. **Verify registration**:
```csharp
// In Program.cs, ensure:
services
    .AddWorkspaceChildType<BotEntity>()                    // ← Must have this!
    .AddWorkspaceDocumentService<string, BotEntity>();
```

**For detailed explanation**: Load `references/service-scoping.md`.

---

### Workflow 2: Create List Page for Workspace Documents

**Goal**: Display a reactive grid of workspace documents with CRUD operations.

**Steps**:

1. **Verify entity and VM are defined**:
```csharp
[Alias("Bot")]
public partial class BotEntity : ReactiveObject
{
    [Reactive] private string? _name;
}

public class BotVM : KeyValueVM<string, BotEntity>
{
    public BotVM(string key, BotEntity value) : base(key, value) { }
}
```

2. **Verify registration**:
```csharp
services
    .AddWorkspaceChildType<BotEntity>()
    .AddWorkspaceDocumentService<string, BotEntity>()
    .AddTransient<BotVM>();
```

3. **Create list page** using `ObservableDataView`:
   - Load `examples/list-view-example.razor`
   - Adapt for your entity type
   - Key: Set `DataServiceProvider="@WorkspaceServices"`

4. **Customize columns** as needed (PropertyColumn, TemplateColumn)

5. **Add navigation** to detail page:
```razor
<MudButton Href="@($"/bots/{context.Item.Key}")">Edit</MudButton>
```

**For complete pattern details**: Load `references/blazor-mvvm-patterns.md`.

---

### Workflow 3: Create Detail Page for Workspace Document

**Goal**: Display/edit a single workspace document.

**Steps**:

1. **Create page with route parameter**:
```razor
@page "/bots/{BotId}"

@code {
    [Parameter]
    public string? BotId { get; set; }
}
```

2. **Get workspace services**:
```razor
@inject ILogger<Bot> Logger
@inject IServiceProvider ServiceProvider

@code {
    [CascadingParameter(Name = "WorkspaceServices")]
    public IServiceProvider? WorkspaceServices { get; set; }
}
```

3. **Resolve reader/writer and create VM**:
   - Load `examples/detail-view-example.razor`
   - Adapt service resolution pattern
   - Create `ObservableReaderWriterItemVM`

4. **Bind UI to VM.Value**:
```razor
<MudTextField @bind-Value="VM.Value.Name" Label="Name" />
```

5. **Implement Save**:
```csharp
private async Task Save() => await VM.Write();
```

**For complete pattern details**: Load `references/blazor-mvvm-patterns.md`.

---

### Workflow 4: Add New Workspace Document Type

**Goal**: Add a new document type (e.g., Portfolio) to existing workspace application.

**Steps**:

1. **Define entity**:
```csharp
[Alias("Portfolio")]
public partial class PortfolioEntity : ReactiveObject
{
    [Reactive] private string? _name;
    // ... other properties
}
```

2. **Define ViewModel**:
```csharp
public class PortfolioVM : KeyValueVM<string, PortfolioEntity>
{
    public PortfolioVM(string key, PortfolioEntity value) : base(key, value) { }
}
```

3. **Register**:
```csharp
services
    .AddWorkspaceChildType<PortfolioEntity>()
    .AddWorkspaceDocumentService<string, PortfolioEntity>()
    .AddTransient<PortfolioVM>();
```

4. **Create pages** (follow Workflow 2 and 3 above)

5. **Result**: Portfolios appear in workspace subdirectory `Portfolios/`

---

## Key Components Reference

### ObservableDataView

**Purpose**: Pre-built MudDataGrid component with reactive workspace data integration.

**Key Parameters**:
- `TKey`, `TValue`, `TValueVM` - Type parameters
- `DataServiceProvider` - **CRITICAL**: Pass `@WorkspaceServices` here
- `AllowedEditModes` - EditMode.None, .Cell, .Form, .All
- `ReadOnly` - Enable/disable editing
- `Columns` - Custom column definitions

**Automatic Features**:
- CRUD toolbar (Add/Edit/Delete buttons)
- Reactive updates (file changes auto-refresh UI)
- VM creation (automatic via constructor)
- Sorting, filtering, grouping

### ObservableReaderWriterItemVM

**Purpose**: ViewModel wrapper for single workspace documents.

**Constructor**:
```csharp
public ObservableReaderWriterItemVM(
    IObservableReader<TKey, TValue> reader,
    IObservableWriter<TKey, TValue> writer)
```

**Key Properties**:
- `Id` - The document key (triggers load when set)
- `Value` - The wrapped entity (as TValueVM)
- `Writer` - Access to persistence

**Key Methods**:
- `Write()` - Save changes to file

---

## Common Pitfalls

### ❌ Pitfall 1: Injecting Workspace Services from Root

```csharp
// ❌ WRONG
@inject IObservableReader<string, BotEntity> Reader

// ✅ RIGHT
[CascadingParameter(Name = "WorkspaceServices")]
public IServiceProvider? WorkspaceServices { get; set; }

var reader = WorkspaceServices.GetService<IObservableReader<string, BotEntity>>();
```

### ❌ Pitfall 2: Forgetting DataServiceProvider

```razor
<!-- ❌ WRONG -->
<ObservableDataView TKey="string" TValue="BotEntity" TValueVM="BotVM" />

<!-- ✅ RIGHT -->
<ObservableDataView TKey="string" TValue="BotEntity" TValueVM="BotVM"
                    DataServiceProvider="@WorkspaceServices" />
```

### ❌ Pitfall 3: Not Registering Document Type

```csharp
// ❌ WRONG - Missing AddWorkspaceChildType
services.AddWorkspaceDocumentService<string, BotEntity>();

// ✅ RIGHT
services
    .AddWorkspaceChildType<BotEntity>()                    // ← MUST have this
    .AddWorkspaceDocumentService<string, BotEntity>();
```

---

## References

Detailed documentation (load as needed):

- **`references/service-scoping.md`** - Deep dive on workspace service scoping and DI
  - Why workspace services are scoped
  - Complete registration flow
  - Troubleshooting DI errors

- **`references/blazor-mvvm-patterns.md`** - Complete Blazor MVVM pattern guide
  - ObservableDataView pattern details
  - Manual VM pattern details
  - When to use which pattern
  - Navigation between list/detail

- **`references/workspaces-architecture.md`** - Workspace architecture overview
  - What workspaces are
  - Service scoping model
  - Document type system
  - When to use workspaces

---

## Quick Decision Tree

```
Need to display workspace documents?
├─ Multiple items (list/grid)?
│  └─ Use ObservableDataView ✅
│     → See examples/list-view-example.razor
└─ Single item (detail/edit)?
   └─ Use Manual VM Pattern ✅
      → See examples/detail-view-example.razor

Getting "Unable to resolve service" error?
└─ Using @inject instead of CascadingParameter?
   └─ Fix: Use CascadingParameter for WorkspaceServices
      → See references/service-scoping.md
```

---

## Summary

**This skill teaches two complementary patterns**:

1. **ObservableDataView** - Automatic reactive grids with minimal code
2. **Manual VM Creation** - Full control for detail views

**Both require**: `CascadingParameter` to access workspace-scoped services.

**Most Common Issue**: Trying to inject workspace services from root DI container.

**Solution**: Always use `CascadingParameter(Name = "WorkspaceServices")`.
