---
description: Build Blazor components, pages, and layouts following the MudBlazor design system
---

# Frontend Development Skill

## Overview

This skill guides frontend development for the PLG Lead Qualification Tool, ensuring all Blazor components, pages, and layouts adhere to the established MudBlazor design system and project conventions.

## When to Use

Invoke this skill when:

- Creating new Blazor components
- Building pages or layouts
- Implementing UI features
- Working with MudBlazor components
- Adding loading states, empty states, or error handling UI

## Core References

**CRITICAL:** Before writing any frontend code, read:

| Document                | Purpose                                                         |
| ----------------------- | --------------------------------------------------------------- |
| `docs/design-system.md` | MudTheme colors, component patterns, accessibility requirements |
| `docs/screens.md`       | UI wireframes and component composition                         |

## Workflow

### Step 1: Understand the Context

1. Read `docs/design-system.md` for theme and patterns
2. Read `docs/screens.md` for the specific screen wireframe
3. Check existing components in `Components/` for similar patterns

### Step 2: Plan the Component

Before writing code, confirm:

- [ ] Component location (Components/, Pages/, Shared/)
- [ ] Parameter design
- [ ] Which MudBlazor components to use
- [ ] Loading, empty, and error states needed
- [ ] Color usage for qualification status

### Step 3: Implementation Checklist

Apply these rules from the design system:

#### Colors (MudBlazor)

- Use MudBlazor semantic colors: `Color.Primary`, `Color.Success`, `Color.Warning`, `Color.Error`
- NEVER hardcode hex colors in components
- Status colors per qualification:
  - STRONG: `Color.Success` (green)
  - MODERATE: `Color.Warning` (amber)
  - WEAK/DISQUALIFIED: `Color.Error` (red)
  - Processing: `Color.Info` (blue)

#### Typography

- Use `Typo.*` enum for consistent text styling
- Primary text: `Typo.body1`
- Secondary text: `Typo.body2` with `Color.Secondary`
- Headers: `Typo.h4` through `Typo.h6`
- Captions/labels: `Typo.caption`

#### Spacing (MudBlazor Classes)

- Use MudBlazor spacing classes: `pa-4`, `ma-2`, `mb-4`, etc.
- Page padding: `pa-6`
- Card padding: `pa-4`
- Component spacing: `Class="mb-4"`

#### MudBlazor Components

- **Cards**: `<MudPaper Elevation="0" Class="border rounded-lg">`
- **Tables**: `<MudDataGrid>` with `Dense="true"` and `Hover="true"`
- **Buttons**: `<MudButton Variant="Variant.Filled" Color="Color.Primary">`
- **Chips**: `<MudChip Color="@color" Size="Size.Small" Variant="Variant.Filled">`
- **Icons**: `<MudIcon Icon="@Icons.Material.Filled.Name">`
- **Loading**: `<MudProgressLinear Indeterminate="true">`

#### States

- Loading: `MudProgressLinear` with `Indeterminate="true"`
- Empty: Centered `MudIcon` + `MudText` + optional `MudButton`
- Error: `MudAlert` with `Severity.Error`

#### Icons

- Use Material Icons via `@Icons.Material.Filled.*` or `@Icons.Material.Outlined.*`
- Common icons:
  - Dashboard: `Icons.Material.Filled.Dashboard`
  - People: `Icons.Material.Filled.People`
  - Sync: `Icons.Material.Filled.Sync`
  - Check: `Icons.Material.Filled.CheckCircle`
  - Warning: `Icons.Material.Filled.Warning`

### Step 4: File Structure

```
Components/           # Reusable components
├── StatCard.razor
├── QualificationChip.razor
├── HotLeadsTable.razor
└── ScoreCard.razor

Pages/                # Page components
├── Index.razor       # Dashboard
├── Leads.razor       # Leads list
├── LeadDetail.razor  # Lead detail
└── SyncStatus.razor  # Sync monitoring

Shared/               # Layout components
└── MainLayout.razor
```

Component file pattern:

```razor
@* StatCard.razor *@

<MudPaper Elevation="0" Class="pa-4 border rounded-lg">
    <MudStack Spacing="1">
        <MudText Typo="Typo.caption" Class="text-secondary">@Title</MudText>
        <MudText Typo="Typo.h4" Class="font-weight-bold" Color="@TextColor">@Value</MudText>
    </MudStack>
</MudPaper>

@code {
    [Parameter]
    public string Title { get; set; } = "";

    [Parameter]
    public string Value { get; set; } = "";

    [Parameter]
    public Color TextColor { get; set; } = Color.Default;
}
```

### Step 5: Verification

Before marking complete:

- [ ] Uses MudBlazor semantic colors (no hardcoded hex)
- [ ] Loading states implemented for async operations
- [ ] Empty states for lists/collections
- [ ] Error states handle failures gracefully
- [ ] Qualification colors correct (green/amber/red)
- [ ] Mobile responsive (MudBlazor handles most of this)

## Quick Reference: Common Patterns

### Stat Card

```razor
<MudPaper Elevation="0" Class="pa-4 border rounded-lg">
    <MudStack Spacing="1">
        <MudText Typo="Typo.caption" Class="text-secondary">@Title</MudText>
        <MudText Typo="Typo.h4" Class="font-weight-bold">@Value</MudText>
    </MudStack>
</MudPaper>
```

### Qualification Chip

```razor
<MudChip Color="@GetQualificationColor(qualification)"
         Size="Size.Small"
         Variant="Variant.Filled">
    @qualification
</MudChip>

@code {
    private Color GetQualificationColor(string qualification) => qualification switch
    {
        "STRONG" => Color.Success,
        "MODERATE" => Color.Warning,
        "WEAK" => Color.Error,
        "DISQUALIFIED" => Color.Error,
        _ => Color.Default
    };
}
```

### Loading State

```razor
@if (_loading)
{
    <MudProgressLinear Color="Color.Primary" Indeterminate="true" Class="mb-4" />
}
else if (_error != null)
{
    <MudAlert Severity="Severity.Error" Class="mb-4">@_error</MudAlert>
}
else
{
    @* Content here *@
}
```

### Empty State

```razor
<MudPaper Elevation="0" Class="pa-8 text-center border rounded-lg">
    <MudIcon Icon="@Icons.Material.Filled.Inbox"
             Size="Size.Large"
             Color="Color.Secondary"
             Class="mb-4" />
    <MudText Typo="Typo.h6" Class="mb-2">No leads found</MudText>
    <MudText Typo="Typo.body2" Color="Color.Secondary" Class="mb-4">
        Leads will appear here once contacts are synced and evaluated.
    </MudText>
</MudPaper>
```

### Data Grid with Row Click

```razor
<MudDataGrid Items="@_leads"
             Dense="true"
             Hover="true"
             RowClick="@OnRowClick"
             T="LeadViewModel">
    <Columns>
        <PropertyColumn Property="x => x.Name" Title="Name" />
        <PropertyColumn Property="x => x.Company" Title="Company" />
        <TemplateColumn Title="Status">
            <CellTemplate>
                <QualificationChip Qualification="@context.Item.Qualification" />
            </CellTemplate>
        </TemplateColumn>
    </Columns>
</MudDataGrid>

@code {
    private void OnRowClick(DataGridRowClickEventArgs<LeadViewModel> args)
    {
        NavigationManager.NavigateTo($"/leads/{args.Item.Id}");
    }
}
```

### Score Card (Lead Detail)

```razor
<MudPaper Elevation="0" Class="pa-6 text-center border rounded-lg">
    <MudText Typo="Typo.h2" Color="@GetScoreColor(score)" Class="font-weight-bold">
        @score
    </MudText>
    <MudText Typo="Typo.caption" Color="Color.Secondary">
        AI Qualification Score
    </MudText>
</MudPaper>

@code {
    private Color GetScoreColor(int score) => score switch
    {
        >= 80 => Color.Success,
        >= 50 => Color.Warning,
        _ => Color.Error
    };
}
```

## Do NOT

- Hardcode hex colors (use MudBlazor Color enum)
- Skip loading/error/empty states
- Use custom CSS when MudBlazor provides the same functionality
- Forget to inject NavigationManager for routing
- Use synchronous data fetching in OnInitialized (use OnInitializedAsync)
- Create components without parameters for reusability
