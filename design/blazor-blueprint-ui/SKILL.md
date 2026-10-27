---
name: blazor-blueprint-ui
description: Build and customize .NET 10+ Blazor UIs with BlazorBlueprint. Use when choosing between BlazorBlueprint.Components and BlazorBlueprint.Primitives, wiring setup and providers, using ToastService/DialogService/localization, selecting icon packs, applying shadcn-ui-style theming, or copying and adapting BlazorBlueprint blueprints.
metadata: 
    version: 0.4.0
    author: arisng
    lastVerified: 2026-10-12
    libraryVersion: 4.1
---

# BlazorBlueprint UI

Build modern Blazor web applications using the current BlazorBlueprint component library.

**Repository:** https://github.com/blazorblueprintui/ui
**Documentation:** https://blazorblueprintui.com
**Original Source:** https://blazorblueprintui.com/llms.txt
**Full Bundle:** https://blazorblueprintui.com/llms/llms-full.txt

Examples in the refreshed references use the official upstream `Bb*` naming.

## Package Overview

Core packages:

- **BlazorBlueprint.Components** - Styled component library; includes primitives
- **BlazorBlueprint.Primitives** - Headless accessibility and behavior layer
- **BlazorBlueprint.Icons.Lucide** - Lucide icon pack (1,753 icons)
- **BlazorBlueprint.Icons.Heroicons** - Heroicons pack (1,288 icons)
- **BlazorBlueprint.Icons.Feather** - Feather icon pack (286 icons)
- **BlazorBlueprint.Icons.FontAwesome** - Font Awesome 6 Free pack (2,066 icons, 3 variants)

## Quick Navigation

### Setup & Installation
Read [references/setup.md](references/setup.md) for:
- NuGet installation and service registration
- CSS, imports, and provider setup
- `BbPortalHost`, `BbToastProvider`, and `BbDialogProvider`
- Theme variables and dark mode
- Verification and troubleshooting

### Services & Localization
Read [references/services.md](references/services.md) for:
- `AddBlazorBlueprintComponents()` vs `AddBlazorBlueprintPrimitives()`
- `ToastService` and `DialogService`
- provider requirements and programmatic dialog usage

Read [references/localization.md](references/localization.md) for:
- `IBbLocalizer` and startup string overrides
- `IStringLocalizer` integration patterns
- culture-sensitive component text and formatting

### Icons
Read [references/icons.md](references/icons.md) for icon component usage and styling guidance.

### Blueprints & Primitives
Read [references/blueprints.md](references/blueprints.md) for:
- category routing across auth, sidebar, apps, dashboards, forms, data, marketing, and ecommerce
- the upstream blueprint catalog and per-category files
- copy/adapt workflow for production-shaped screens

Read [references/primitives.md](references/primitives.md) for:
- when to stay on `BlazorBlueprint.Components`
- when to switch to `BlazorBlueprint.Primitives`
- headless behavior and custom design-system guidance

### Common Patterns
Read [references/patterns.md](references/patterns.md) for:
- controlled vs uncontrolled state
- `EditForm` + `BbField` conventions
- root provider patterns
- dashboard / app shell defaults
- blueprint-first acceleration

## Component Categories

### Form Components (30+ form-related)
Read [references/components-forms.md](references/components-forms.md) for:
- text, typed, and structured inputs
- selection controls and searchable selection
- date/time, date+time, and OTP flows
- uploads, editors, and advanced inputs
- form sections, wizards, dynamic forms, and `BbFormField*` wrappers
- v4.1 additions: `BbListBox`, `BbPickList`, `BbSignature`

### Layout & Navigation Components (15+)
Read [references/components-layout.md](references/components-layout.md) for:
- sidebars, responsive nav, navigation menus, and breadcrumbs
- cards, tabs, accordions, collapsible content, and IDE-style docking
- resizable work areas, scroll areas, separators, and aspect-ratio containers
- routing guidance for shells vs display/data surfaces

### Overlay Components (14+)
Read [references/components-overlays.md](references/components-overlays.md) for:
- dialogs, alert dialogs, sheets, drawers, and popovers
- menus, tooltips, hover cards, and command surfaces
- `DialogService` and `ToastService` usage
- provider and portal requirements

### Display & Data Components (18+)
Read [references/components-display-data.md](references/components-display-data.md) for:
- alerts, badges, avatars, shortcuts, loading states, and empty states
- items, timelines, typography, carousel, click-to-copy, and chat components
- `BbDataTable`, `BbDataGrid`, and `BbDataView` routing
- v4.1 additions: `BbPivotDataGrid`, `BbGantt`, `BbBarcode`, `BbQrCode`
- dashboard/data-screen and event calendar guidance

### Chart Components (14 types)
Read [references/components-charts.md](references/components-charts.md) for:
- the current Apache ECharts-based chart stack
- `BbChart` composite charts and `ChartConfig`
- dedicated bar, line, area, pie, radial bar, gauge, radar, scatter, candlestick, rose, and sankey charts
- v4.1 addition: `BbMapChart` (with `BbMap`) for geo visualization
- `BbChartContainer` and chart theming

> Counts are approximate and grow with each library release. The authoritative component list is at https://blazorblueprintui.com/llms/llms-full.txt.

## Key Architecture Patterns

### Controlled vs uncontrolled state

**Uncontrolled:**
```razor
<BbTabs DefaultValue="overview">...</BbTabs>
```

**Controlled:**
```razor
<BbTabs @bind-Value="currentTab">...</BbTabs>
```

### Composition pattern

```razor
<BbCard>
    <BbCardHeader><BbCardTitle>Title</BbCardTitle></BbCardHeader>
    <BbCardContent>Content</BbCardContent>
    <BbCardFooter>Actions</BbCardFooter>
</BbCard>
```

### AsChild pattern

```razor
<BbDialog>
    <BbDialogTrigger AsChild>
        <BbButton Variant="ButtonVariant.Destructive">Delete</BbButton>
    </BbDialogTrigger>
    <BbDialogContent>...</BbDialogContent>
</BbDialog>
```

> **Note**: `AsChild` defaults to `true` for most triggers (dialog, sheet, popover, dropdown menu, collapsible, alert dialog, hover card). In v4, `BbTooltipTrigger`, `BbDrawerTrigger` and `BbDrawerClose` default to `false` — set `AsChild="true"` when the child consumes the trigger context (e.g. a `BbButton`). Drawer triggers render a real `<button>`, so a `BbButton` child without `AsChild="true"` produces invalid nested buttons. See [patterns.md § AsChild defaults](references/patterns.md).

### Portal and provider pattern

Overlay components render through `BbPortalHost`. App-wide toasts and service-driven dialogs also need `BbToastProvider` and `BbDialogProvider` in the root layout.

## Known Pitfalls

These are hard-won constraints — check them before generating any BB component code:

1. **CaptureUnmatchedValues is supported, not universal** — Most BB components now accept arbitrary HTML attributes (`@onclick`, `style`, `class`, `data-*`, etc.) and pass them through to the root element. However, not every component declares `[Parameter(CaptureUnmatchedValues = true)]` — check the upstream docs or source for your specific component. For components that lack it, use a wrapper element. See [patterns.md § Unmatched attribute capture](references/patterns.md).

2. **`bb:`-prefixed utilities** — In v4 every utility in `blazorblueprint.css` is prefixed `bb:` and lives in its own cascade layer. Your `Class` values stay unprefixed (`Class="p-6"` overrides the library's `bb:p-4` through the class merge). Page-level Tailwind classes only render when the app has its own Tailwind build; without one, add a Tailwind build (standalone CLI needs no Node) or use `bb:` classes as a stopgap. The only consumer-facing prefixed utilities are the safelisted `bb:shimmer` and `bb:scroll-fade-x`. See [setup.md § bb: utility prefix](references/setup.md).

3. **Lucide icon names change** — Several names have been renamed upstream (e.g. `check-circle` → `circle-check`, `home` → `house`). A broken icon renders ⚠️. Verify names at `https://blazorblueprintui.com/llms/icons/lucide.txt`. See [icons.md § Renamed icons](references/icons.md).

4. **Auth pages are SSR-only** — Login/signup blueprints use `[ExcludeFromInteractiveRouting]`. Use HTML form POST + `[SupplyParameterFromForm]`; do not add `@rendermode InteractiveServer`. See [blueprints.md § Auth pages and SSR](references/blueprints.md).

5. **.NET 10 minimum** — Version 4 targets `net10.0` only; .NET 8/9 apps cannot consume it. Keep Components and Primitives on matching v4 releases. See [migration guide](https://blazorblueprintui.com/llms/migration-v3-to-v4.txt) for the full v3→v4 checklist.

6. **Portal hosts moved out of `.Services`** — `BbPortalHost` and friends now live in `BlazorBlueprint.Primitives`, not `BlazorBlueprint.Primitives.Services`. An unresolved `<BbPortalHost />` is not a build error: it emits literal `<bbportalhost>` HTML and every overlay silently fails. See [setup.md § Configure layout providers](references/setup.md).

## Workflow

1. **Read setup.md** for installation and providers.
2. **Choose components vs primitives** before building custom shells or behavior-heavy surfaces.
3. **Pick a category**: forms, layout/navigation, overlays, display/data, or charts.
4. **Load patterns.md** when composing multiple surfaces together.
5. **Load blueprints.md** when you need a production-shaped screen quickly.
6. **Style through theme variables** and validate dark mode.

## When to Load References

- **setup.md:** first-time setup, providers, theming, dark mode, icons import questions
- **services.md:** DI registration differences, `ToastService`, `DialogService`, provider requirements
- **localization.md:** label overrides, `IBbLocalizer` customization, culture-sensitive component text
- **blueprints.md:** rapid auth, sidebar, dashboard, data, marketing, or ecommerce screen scaffolding
- **primitives.md:** headless composition, custom design systems, or behavior-only reuse
- **components-forms.md:** editing flows, validation, selection, wizards, schema-driven forms
- **components-layout.md:** shells, responsive navigation, cards, tabs, resizable work areas
- **components-overlays.md:** dialogs, menus, tooltips, command palettes, toasts
- **components-display-data.md:** alerts, status display, tables, grids, data views, empty/loading states
- **components-charts.md:** dashboards, KPI visuals, mixed/composite chart composition
- **patterns.md:** cross-component conventions and blueprint-first workflows

## Blueprints and Primitives

- **Blueprints** provide ready-to-copy compositions for auth, sidebar shells, dashboards, forms, data screens, marketing, and ecommerce. Read [references/blueprints.md](references/blueprints.md) for category routing and upstream blueprint entry points.
- **Primitives** are the headless layer for advanced users who want BlazorBlueprint behavior without the styled component surface. Read [references/primitives.md](references/primitives.md) when markup ownership matters more than the default component styling.
