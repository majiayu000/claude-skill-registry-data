---
name: saas-ui-patterns
description: Premium SaaS UI/UX patterns for JKKN COE Next.js CRUD pages. Use when creating new pages, redesigning existing pages, or ensuring UI consistency across the application. Triggers on "create page", "new module", "redesign", "UI pattern", "CRUD page", "table page", "SaaS design", "page layout", "scorecard", "pagination", "action menu", or when building any entity management page. Reference implementation is app/(coe)/grading/grades/page.tsx.
---

# SaaS UI Patterns

Standard UI/UX patterns for all JKKN COE CRUD/table pages.

**Reference implementations:**
- `app/(coe)/grading/grades/page.tsx` (canonical)
- `app/(coe)/master/courses/page.tsx`
- `app/(coe)/exam-management/examiners/page.tsx`

## Required Imports

```tsx
import { DropdownMenu, DropdownMenuContent, DropdownMenuItem, DropdownMenuSeparator, DropdownMenuTrigger } from "@/components/ui/dropdown-menu"
import { Tooltip, TooltipContent, TooltipProvider, TooltipTrigger } from "@/components/ui/tooltip"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { AlertDialog, AlertDialogAction, AlertDialogCancel, AlertDialogContent, AlertDialogDescription, AlertDialogFooter, AlertDialogHeader, AlertDialogTitle } from "@/components/ui/alert-dialog"
```

**Never import:** `AlertDialogTrigger`, `SheetDescription`

Lucide icons: `MoreHorizontal, ChevronDown, RefreshCw, Download, Upload, FileSpreadsheet, PlusCircle, Edit, Trash2, Search, ChevronLeft, ChevronRight`

## Component Patterns

For complete code snippets, see [references/patterns.md](references/patterns.md).

### 0. Page Layout (Outer Shell)

```tsx
<SidebarProvider>
  <AppSidebar />
  <SidebarInset className="flex flex-col min-h-screen">
    <AppHeader />
    <div className="flex flex-1 flex-col gap-4 p-4 pt-0 overflow-y-auto">
      {/* Breadcrumb */}
      {/* Scorecards */}
      {/* Table Card */}
    </div>
  </SidebarInset>
</SidebarProvider>
```

**Never use:**
- Fixed height: `h-[calc(100vh-...)]` on the outer div
- `PageTransition` wrapper (removed)
- `AppFooter` inside SidebarInset
- `overflow-hidden` on SidebarInset

### 1. Scorecards (border-l-4)

Use `<Card>` with `border-l-4 border-l-{color}-500 hover:shadow-md transition-shadow`. Colors: blue, emerald, amber, purple, green, rose, teal. Numbers: `text-2xl font-bold tracking-tight`. Labels: `text-xs font-medium text-muted-foreground mt-0.5`. Icon: `h-5 w-5 text-{color}-500/40` (right-aligned). Grid: `grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-3 flex-shrink-0`.

**Scorecard counts must use institution-filtered data, NOT raw data or search-filtered data:**

```tsx
// Institution-filtered base — for scorecards only (no search/status filter applied)
const institutionFiltered = useMemo(() => {
  if (shouldFilter && myjkknInstitutionIds?.length > 0) {
    return allItems.filter(s => myjkknInstitutionIds.includes(s.institution?.id))
  }
  return allItems
}, [allItems, shouldFilter, myjkknInstitutionIds])

// Table data = institutionFiltered + search + status
const filtered = useMemo(() => {
  let result = institutionFiltered
  // apply search/status filters...
  return result
}, [institutionFiltered, searchTerm, activeFilter])

// Scorecards derived from institutionFiltered (not allItems, not filtered)
const totalCount   = institutionFiltered.length
const activeCount  = institutionFiltered.filter(s => s.is_active).length
```

Behaviour:
- **All Institutions** selected → scorecards show totals for all records
- **Specific institution** selected → scorecards update to that institution's counts
- Search/status toolbar filters do **not** affect scorecard numbers

```tsx
<Card className="border-l-4 border-l-blue-500 hover:shadow-md transition-shadow">
  <CardContent className="p-4">
    <div className="flex items-center justify-between">
      <div>
        <p className="text-2xl font-bold tracking-tight">{count}</p>
        <p className="text-xs font-medium text-muted-foreground mt-0.5">Label</p>
      </div>
      <Icon className="h-5 w-5 text-blue-500/40" />
    </div>
  </CardContent>
</Card>
```

**Never use:**
- `grid-cols-2 md:grid-cols-4 gap-4` without `flex-shrink-0`
- Icon container divs: `h-10 w-10 rounded-lg bg-blue-50 flex items-center justify-center`
- Colored number text: `text-green-700`, `text-yellow-700`, `text-slate-900` on the number
- `text-sm text-slate-600` labels (use `text-xs font-medium text-muted-foreground`)
- `plain divs with colored backgrounds`, `rounded-2xl`, `shadow-sm`, `ring-1`, `font-grotesk`
- `flex items-center gap-3` layout (use `flex items-center justify-between`)

### 2. Table Card

Wrap in `<TooltipProvider delayDuration={300}>`. Card: `flex-1 flex flex-col min-h-0`. Table is inside a **bounded div** with min/max height — the page scrolls, not the full card.

```tsx
<TooltipProvider delayDuration={300}>
  <Card className="flex-1 flex flex-col min-h-0">
    <CardHeader className="flex-shrink-0 px-4 py-3 border-b">
      {/* Toolbar */}
    </CardHeader>
    <CardContent className="px-4 pb-4 pt-0 flex-1 flex flex-col min-h-0">
      <div className="rounded-md border flex-1 overflow-hidden mt-3 min-h-[380px] max-h-[520px]">
        <div className="h-full overflow-auto">
          <Table>
            <TableHeader className="sticky top-0 z-10 bg-muted/50">
              {/* headers: text-xs font-semibold */}
            </TableHeader>
            <TableBody>
              {/* rows: hover:bg-muted/50, cells: text-sm */}
            </TableBody>
          </Table>
        </div>
      </div>
      {/* Pagination goes here, outside the bounded div */}
    </CardContent>
  </Card>
</TooltipProvider>
```

**Never use:**
- `flex-1 overflow-auto p-0` on CardContent (use `px-4 pb-4 pt-0 flex-1 flex flex-col min-h-0`)
- `border-slate-200 shadow-sm rounded-2xl` on main Card
- `rounded-xl border border-slate-200 overflow-hidden bg-white` table wrapper
- `bg-slate-50 border-b border-slate-200` on TableHeader
- `bg-slate-50`, `border-slate-*` anywhere in table
- `bg-slate-50/50` on CardContent
- `text-sm font-semibold text-slate-700` on TableHead (use `text-xs font-semibold`)
- `font-grotesk` on cells
- `text-muted-foreground` on table data cells
- inline `style={{ minHeight, maxHeight }}` (use Tailwind `min-h-[380px] max-h-[520px]`)

### 3. Toolbar (CardHeader)

```
CardHeader className="flex-shrink-0 px-4 py-3 border-b"
```

Row 1 (title + actions): `flex items-center justify-between`
- Title: `text-base font-semibold` + `text-xs text-muted-foreground`
- Actions: `flex items-center gap-1.5`

Row 2 (filters + search): `flex items-center gap-2 flex-wrap`
- Filter Selects: `h-8 text-sm` (no `border-slate-*`, `focus:border-emerald-*`, `rounded-lg`)
- Search: `pl-8 h-8 text-sm` with `flex-1 max-w-sm` or `lg:w-[260px]`
- Refresh: icon-only `h-8 w-8 p-0` wrapped in `<Tooltip>`
- Export: `<DropdownMenu>` with Template/Excel/JSON items, button `h-8 text-sm px-3`, content `w-44`
- Import: `h-8 text-sm px-3`
- Add: `h-8 text-sm px-4`

**Never use:**
- `px-8 py-6` on CardHeader (always `px-4 py-3`)
- Large icon + title block: `h-12 w-12 rounded-xl bg-emerald-50` + `text-xl font-bold text-slate-900`
- `space-y-4` between rows (use `space-y-3`)
- `h-9` on any filter/action button (always `h-8`)
- `rounded-lg` on filter SelectTrigger
- `rounded-xl bg-emerald-600 hover:bg-emerald-700 text-white` on Add button
- Gradient headers (`bg-gradient-to-r`), `font-grotesk`, `text-xl font-bold`

### 4. Action Column (MoreHorizontal)

Replace inline Edit/Delete with `<DropdownMenu>` triggered by `MoreHorizontal h-4 w-4`. Button: `h-7 w-7 p-0`. Delete item: `text-red-600 focus:text-red-600 focus:bg-red-50 dark:focus:bg-red-950/20`. Sets `deleteTarget` state.

### 5. Standalone Delete AlertDialog

```tsx
const [deleteTarget, setDeleteTarget] = useState<Entity | null>(null)
```

Controlled by `deleteTarget` state, placed **OUTSIDE** the table (after Sheet, before SidebarProvider close). Never nest `AlertDialogTrigger` inside table rows.

### 6. Dynamic Pagination

```tsx
const [itemsPerPage, setItemsPerPage] = useState(10)  // plain number, never "all" union
```

`pageSizeOptions` useMemo with smart filtering. "All" only when total > default. `effectivePerPage` for calculations. Pagination UI inside CardContent, below table:

```
<div className="flex items-center justify-between pt-3 px-4 pb-3 border-t">
```

Page size: `<Select>` with `h-7 w-[70px] text-xs`. Nav: `ChevronLeft`/`ChevronRight` buttons `h-7 w-7 p-0`. Page indicator: `text-xs text-muted-foreground px-2 tabular-nums`.

**Never use:** First/Previous/Next/Last text buttons, page number buttons, `number | "all"` type.

### 7. Global Institution Filter

Every page must respect the global institution selector in the sidebar. Use `useInstitutionFilter()` from `@/hooks/use-institution-filter`.

```tsx
const {
  mustSelectInstitution,  // true = "All Institutions" selected (super_admin)
  shouldFilter,           // true = filter is active (specific institution selected)
  myjkknInstitutionIds,   // MyJKKN institution UUIDs for current institution
  institutionId,          // COE institution UUID
  isReady,                // wait for this before fetching
} = useInstitutionFilter()
```

**Institution column in table** — show only when "All Institutions" selected:
```tsx
// Header
{mustSelectInstitution && <TableHead className="text-xs font-semibold">Institution</TableHead>}

// Cell
{mustSelectInstitution && <TableCell className="text-sm">{row.institution_code}</TableCell>}

// colSpan in loading/empty rows — adjust total column count
colSpan={mustSelectInstitution ? 9 : 8}
```

**COE data filtering** — use `appendToUrl` or `filterData`:
```tsx
// Fetch with institution filter in URL
useEffect(() => {
  if (!isReady) return
  const url = appendToUrl('/api/entity')
  fetch(url).then(...)
}, [isReady, filter])

// Or filter local array
const filtered = filterData(allItems, 'institution_code')
```

**MyJKKN data filtering** — filter client-side by `myjkknInstitutionIds`:
```tsx
// In useMemo — filter staff/learners from MyJKKN by institution
if (shouldFilter && myjkknInstitutionIds?.length > 0) {
  result = result.filter(s => myjkknInstitutionIds.includes(s.institution?.id))
}
```

**Reset page on institution change:**
```tsx
useEffect(() => { setCurrentPage(1) }, [shouldFilter, myjkknInstitutionIds])
```

**Role behaviour:**

| User | `mustSelectInstitution` | `shouldFilter` | Effect |
|------|------------------------|----------------|--------|
| Normal user | `false` | `true` | Auto-filtered to own institution |
| super_admin (All) | `true` | `false` | All data shown, Institution column visible |
| super_admin (specific) | `false` | `true` | Filtered to selected institution |

**Never use:**
- A local institution dropdown filter in the toolbar (global filter handles this)
- Fetching without checking `isReady` first
- Filtering only server-side (MyJKKN API often ignores server filters — always also filter client-side)

### 8. Form Sheet (Clean)

- Content: `sm:max-w-[720px] overflow-y-auto` (or `sm:max-w-[800px]` for wider forms)
- Header: `pb-4 border-b` with `text-lg font-semibold` title
- Description: `<p className="text-sm text-muted-foreground">` (never `SheetDescription`)
- Body: `<div className="mt-6 space-y-8">`
- Sections: `text-xs font-semibold text-muted-foreground uppercase tracking-wider`
- Subsequent sections: add `pt-2 border-t`
- Action buttons: `<div className="flex justify-end gap-3 pt-6 border-t">` with plain `h-10 px-6`

**Never use:** gradient headers, `rounded-xl bg-emerald-600`, `border-slate-*` on buttons, `SheetDescription` component.

### 8. Loading/Empty States

- Loading: `RefreshCw animate-spin h-5 w-5` + `text-sm` message in `h-32 text-center` with `text-muted-foreground`
- Empty: entity icon `h-8 w-8 opacity-20` + `text-sm` title + `text-xs` subtitle

**Never use:** custom spinner divs (`border-2 border-primary border-t-transparent`), `h-10 w-10`, `text-muted-foreground/40`.

## Typography Rules

| Element | Class | Never Use |
|---------|-------|-----------|
| Card title | `text-base font-semibold` | `text-xl font-bold`, `text-lg font-bold` |
| Card description | `text-xs text-muted-foreground` | `text-sm text-slate-600` |
| Table cells | `text-sm` | `text-[11px]`, `font-grotesk` |
| Table headers | `text-xs font-semibold` | `text-sm font-semibold text-slate-700` |
| Form labels | `text-sm font-semibold` | `text-sm font-medium` (in form only) |
| Scorecard numbers | `text-2xl font-bold tracking-tight` | `text-3xl`, `font-grotesk`, colored variants |
| Scorecard labels | `text-xs font-medium text-muted-foreground mt-0.5` | `text-sm text-slate-600` |
| Badges | `text-xs` | |
| Section labels | `text-xs font-semibold uppercase tracking-wider` | gradient dividers |
| Sheet title | `text-lg font-semibold` | `text-xl font-bold` |

## Anti-Patterns (Never Use)

### Styling
- `font-grotesk` - never use anywhere
- `text-[11px]` or any arbitrary pixel sizes
- `rounded-2xl`, `rounded-3xl`, `rounded-xl` on cards/containers
- `ring-1 ring-*-100` decorative rings
- `shadow-sm` on Card components
- `border-slate-*` specific border colors (use default borders)
- `text-slate-*` specific text colors (use `text-foreground`/`text-muted-foreground`)
- `bg-slate-50` (use `bg-muted/50`)
- `bg-slate-50/50` on CardContent (use `p-0`)
- `px-8 py-6` on CardHeader (use `px-4 py-3`)
- `focus:border-emerald-*`, `focus:ring-emerald-*` on inputs
- `bg-emerald-600 hover:bg-emerald-700 text-white` on action buttons
- `bg-gradient-to-r` on card headers
- `h-9` on filter selects or action buttons (use `h-8`)

### Structure
- `AlertDialogTrigger` wrapping delete buttons (use standalone `deleteTarget`)
- `SheetDescription` component (use `<p>` tag)
- Separate Edit/Delete buttons in table rows (use MoreHorizontal dropdown)
- `const itemsPerPage = 10` without useState
- `useState<number | "all">` for items per page (use plain `useState(10)`)
- Icon container divs (`h-10 w-10 rounded-lg bg-*-50` or `h-12 w-12 rounded-xl bg-*-50 ring-1`)
- Large icon+title block in CardHeader (the `flex items-center gap-3` with icon circle + `text-xl font-bold`)
- `rounded-xl border border-slate-200 overflow-hidden bg-white` wrapper div around `<Table>`
- Gradient section dividers with colored icon circles
- First/Previous/Next/Last text pagination buttons
- Page number buttons in pagination
- `text-muted-foreground` on table data cells
