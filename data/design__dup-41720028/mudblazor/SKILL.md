---
name: mudblazor
description: Build enterprise Blazor applications with MudBlazor component library. Use when creating forms, data grids, dialogs, navigation, theming, layout systems, or integrating with Neatoo domain objects. Covers installation, components, validation, data display, and enterprise patterns.
allowed-tools: Read, Write, Edit, Glob, Grep, Bash(dotnet:*), WebFetch
---

# MudBlazor - Enterprise Blazor UI Development

## Overview

MudBlazor is a comprehensive Material Design component library for Blazor that provides production-ready UI components for building enterprise web applications. It emphasizes customizable theming, extensive component options, and developer-friendly APIs.

### Key Capabilities

| Category | Components |
|----------|------------|
| **Forms** | TextField, NumericField, Select, Autocomplete, DatePicker, CheckBox, Switch, RadioGroup |
| **Data Display** | DataGrid, Table, Card, List, TreeView, Tabs |
| **Feedback** | Dialog, Snackbar, Alert, Progress indicators |
| **Navigation** | NavMenu, Breadcrumbs, Tabs, Links |
| **Layout** | Grid, Container, Paper, Stack, Drawer, AppBar |

### When to Use This Skill

Use this skill when:
- Building forms with validation and user feedback
- Creating data tables and grids with sorting, filtering, and paging
- Implementing dialog-based workflows
- Setting up application layouts and navigation
- Theming and styling Blazor applications
- Integrating MudBlazor with Neatoo domain objects

## Quick Start

### Installation

```bash
dotnet add package MudBlazor
```

### Required Configuration

**Program.cs:**
```csharp
using MudBlazor.Services;

builder.Services.AddMudServices();
```

**_Imports.razor:**
```razor
@using MudBlazor
```

**MainLayout.razor - Required Providers:**
```razor
<MudThemeProvider />
<MudPopoverProvider />
<MudDialogProvider />
<MudSnackbarProvider />

<MudLayout>
    @Body
</MudLayout>
```

**App.razor or index.html - Required Assets:**
```html
<link href="https://fonts.googleapis.com/css?family=Roboto:300,400,500,700&display=swap" rel="stylesheet" />
<link href="_content/MudBlazor/MudBlazor.min.css" rel="stylesheet" />
<script src="_content/MudBlazor/MudBlazor.min.js"></script>
```

## Critical Rules

### MudForm vs EditForm

| Scenario | Use |
|----------|-----|
| MudBlazor's validation system | `MudForm` with `OnClick` handlers |
| ASP.NET Core validation | `EditForm` with `ButtonType.Submit` |

**WARNING: NEVER use `ButtonType="ButtonType.Submit"` with MudForm.**

### Four Required Providers

All four providers must be in MainLayout for MudBlazor to function:

| Provider | Purpose |
|----------|---------|
| `MudThemeProvider` | Theme and styling |
| `MudPopoverProvider` | Popover positioning |
| `MudDialogProvider` | Dialog service |
| `MudSnackbarProvider` | Snackbar notifications |

### Complex Object Selection

**WARNING:** When using `MudSelect` or `MudDataGrid` with complex objects, you MUST implement `IEquatable<T>` or provide a `Comparer`. Selection will not work correctly otherwise.

### Dialog Result Handling

**WARNING:** Always check if dialog was canceled before accessing result data. Accessing `result.Data` on a canceled dialog will throw.

See [Best Practices](best-practices.md) for code examples.

## Additional Resources

For detailed guidance, see:
- [Core Concepts](core-concepts.md) - Variants, spacing utilities, color system
- [Installation & Setup](installation.md) - Full setup guide, providers, assets
- [Form Components](form-components.md) - TextField, Select, DatePicker, validation
- [Data Display](data-display.md) - DataGrid, Table, Cards
- [Feedback Components](feedback-components.md) - Dialog, Snackbar, Alert
- [Layout System](layout-system.md) - Grid, Container, responsive patterns
- [Navigation](navigation.md) - NavMenu, Tabs, Breadcrumbs
- [Theming](theming.md) - Custom themes, dark mode, CSS variables
- [Neatoo Integration](neatoo-integration.md) - MudNeatoo components for domain objects
- [Best Practices](best-practices.md) - Patterns, anti-patterns, performance

## Official Documentation

- [MudBlazor Documentation](https://mudblazor.com/docs/overview)
- [MudBlazor GitHub](https://github.com/MudBlazor/MudBlazor)
- [MudBlazor Examples](https://try.mudblazor.com/)
