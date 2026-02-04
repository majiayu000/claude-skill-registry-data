---
name: monto-design-system
description: Expert knowledge of the Monto platform design system including colors, typography, spacing, components, and UI patterns
---

# Monto Design System Expert

You are an expert in the Monto platform design system. Your role is to provide guidance on UI components, styling patterns, and design decisions that align with Monto's established design language.

## Design System Overview

Monto is a financial platform for invoice and payment management. The design emphasizes clarity, professionalism, and efficient workflows for financial operations.

### Core Design Principles

1. **Consistency** - Maintain uniform patterns across all components and pages
2. **Clarity** - Present financial data clearly with appropriate hierarchy
3. **Efficiency** - Optimize for quick task completion and reduced cognitive load
4. **Accessibility** - Ensure all users can navigate and understand the interface

## Color Palette

### Primary Colors

- **Primary Purple**: `#7B59FF` - Main brand color used for CTAs, links, and active states
  - Usage: Primary buttons, active tabs, selected states, key actions
  - Variants:
    - `bg-primary`
    - `text-primary`
    - `border-primary`
    - `hover:bg-primary/90`
    - `border-primary/30` (hover states)

### Neutral Colors

- **Grey Scale**:
  - Background: `#F6F7F9` (`bg-[#F6F7F9]`) - Table headers, section backgrounds
  - Border: `border-gray-200` - Standard borders
  - Border Light: `border-gray-100` - Subtle dividers
  - Text Primary: `text-gray-900` - Main content text
  - Text Secondary: `text-gray-700` - Labels, secondary info
  - Text Muted: `text-gray-600`, `text-gray-500` - Helper text, placeholders
  - Hover: `hover:bg-gray-50` - Row/card hover states

### Status Colors

- **Error/Destructive**:
  - Main: `#DF1C41` (error-main)
  - Background: `bg-red-50/50`
  - Border: `border-red-200`
  - Text: `text-error-main`

- **Warning**:
  - Background: `bg-amber-50`
  - Border: `border-amber-200`
  - Text: `text-amber-800`, `text-amber-900`
  - Icon: `text-warning-main`

- **Success**:
  - Background: `bg-green-50`
  - Border: `border-green-200`
  - Text: `text-green-800`, `text-green-900`
  - Icon: `text-success-main`

- **Info**:
  - Background: `bg-white`
  - Border: `border-primary`
  - Text: `text-gray-900`
  - Icon: `text-primary`

## Typography

### Font Family
- Primary: `font-sans` - System font stack
- Specific: Default sans-serif

### Font Sizes
- Small: `text-sm` (0.875rem/14px) - Table cells, labels, body text
- Extra Small: `text-xs` (0.75rem/12px) - Helper text, badges
- Base: `text-base` (1rem/16px) - Standard body text
- Large: `text-lg` (1.125rem/18px) - Section headings
- Extra Large: `text-xl` and above - Page titles

### Font Weights
- Normal: `font-normal` - Body text
- Medium: `font-medium` - Labels, subtle emphasis
- Semibold: `font-semibold` - Table headers, strong labels
- Bold: `font-bold` - Important values, totals

## Spacing System

### Standard Spacing Scale
- `space-y-1`: 0.25rem (4px)
- `space-y-2`: 0.5rem (8px)
- `space-y-3`: 0.75rem (12px)
- `space-y-4`: 1rem (16px)
- `space-y-6`: 1.5rem (24px) - **Standard section spacing**
- `space-y-8`: 2rem (32px)

### Component Spacing
- **Exception sections**: Use `space-y-6` for consistent vertical rhythm
- **Form fields**: `space-y-4` between fields
- **Card content**: `p-4` standard padding
- **Table cells**: `px-4` horizontal, `h-[65px]` or `h-[60px]` height
- **Table headers**: `h-[50px]` or `h-[65px]` height

## Core Components

### Buttons

**Primary Button**
```tsx
<Button className="bg-primary hover:bg-primary/90 text-white">
  Primary Action
</Button>
```

**Secondary/Ghost Button**
```tsx
<Button variant="ghost" size="sm">
  Secondary Action
</Button>
```

**Destructive Button**
```tsx
<Button variant="destructive">
  Delete
</Button>
```

**Sizes**: `size="sm"`, `size="md"` (default), `size="lg"`

### Cards

**Standard Card**
```tsx
<Card>
  <CardHeader>
    <CardTitle>Title</CardTitle>
  </CardHeader>
  <CardContent>
    Content
  </CardContent>
</Card>
```

**SelectableCard** - For selection interfaces
```tsx
<SelectableCard
  selected={isSelected}
  onSelect={() => setSelected(true)}
>
  <SelectableCardContent>
    <SelectableCardField>
      <SelectableCardLabel>Label</SelectableCardLabel>
      <SelectableCardValue>Value</SelectableCardValue>
    </SelectableCardField>
  </SelectableCardContent>
</SelectableCard>
```

**Styling**:
- Border: `border-gray-200` (default), `border-primary border-2` (selected)
- Shadow: `shadow-sm` (default), `shadow-md` (hover)
- Border radius: `rounded-lg` or `rounded-xl`
- Padding: `p-4` or `p-6`

### Tables

**Standard Table Structure**
```tsx
<Table>
  <TableHeader>
    <TableRow className="bg-[#F6F7F9] hover:bg-[#F6F7F9]">
      <TableHead className="h-[50px] px-4">Header</TableHead>
    </TableRow>
  </TableHeader>
  <TableBody className="divide-y divide-gray-100">
    <TableRow className="h-[60px] hover:bg-gray-50 bg-white">
      <TableCell className="px-4">Content</TableCell>
    </TableRow>
  </TableBody>
</Table>
```

**Table Guidelines**:
- Headers: `bg-[#F6F7F9]` background, `font-semibold text-gray-700 text-sm`
- Cells: `text-sm font-normal`, `px-4` padding
- Rows: `hover:bg-gray-50` on body rows
- Dividers: `divide-y divide-gray-100` or `border-gray-50`
- Sticky headers: First column gets `sticky left-0 z-10 border-r border-gray-200`
- Actions column: `text-right w-auto` to fill remaining space

### Exception Banners

```tsx
<ExceptionBanner
  variant="error"
  icon="alert"
  title="Title"
>
  Description text
</ExceptionBanner>
```

**Variants**: `error`, `warning`, `info`, `success`
**Icons**: `alert`, `circle`, `info`, `lightbulb`, `sparkles`, `triangle-alert`

**Styling**:
- Title and description on separate lines
- Title: `font-medium` (not semibold)
- Padding: `p-3`
- Border radius: `rounded-lg`
- Icon size: `size={14}`, `strokeWidth={1.25}`

### Status Badges

Used for displaying record statuses like "Approved by Buyer", "Paid", "Rejected", etc.

```tsx
<StatusBadge status={record.status} />
```

Common statuses:
- Approved by Buyer
- Rejected by Buyer
- Paid
- Pending Approval
- Open
- Closed
- Cancelled

### Form Fields

**Standard Input**
```tsx
<div className="space-y-2">
  <label className="text-sm text-gray-500">Label</label>
  <Input value={value} readOnly className="bg-gray-50" />
</div>
```

**FormField Component**
```tsx
<FormField label="Label" value="Value" />
```

**Spacing**: Use `space-y-2` between label and input

## Layout Patterns

### Page Structure

```tsx
<div className="space-y-6">
  <h2 className="text-lg font-medium">Section Title</h2>

  {/* Content sections with consistent spacing */}
  <div className="space-y-6">
    {/* Section 1 */}
  </div>

  <div className="space-y-6">
    {/* Section 2 */}
  </div>
</div>
```

### Modal/Dialog

```tsx
<Dialog open={isOpen} onOpenChange={setIsOpen}>
  <DialogContent className="max-w-3xl">
    <DialogHeader>
      <DialogTitle>Title</DialogTitle>
    </DialogHeader>
    <div className="space-y-6">
      {/* Content */}
    </div>
  </DialogContent>
</Dialog>
```

**Max widths**: `max-w-md`, `max-w-lg`, `max-w-xl`, `max-w-2xl`, `max-w-3xl`

### Tabs

```tsx
<div className="border-b mb-6">
  <div className="flex space-x-8">
    <button
      className={cn(
        "py-3 px-1 relative font-medium text-sm",
        isActive
          ? "text-primary border-b-2 border-primary"
          : "text-gray-600 hover:text-gray-900"
      )}
    >
      Tab Label
      <span className={cn(
        "ml-2 px-2 py-0.5 rounded-full text-xs",
        isActive ? "bg-primary/10 text-primary" : "bg-gray-100 text-gray-600"
      )}>
        {count}
      </span>
    </button>
  </div>
</div>
```

## Interaction Patterns

### Hover States
- Cards: `hover:shadow-md` + `hover:border-primary/30`
- Table rows: `hover:bg-gray-50`
- Buttons: `hover:bg-primary/90` or `hover:text-gray-900`

### Active/Selected States
- Cards: `border-primary border-2`
- Tabs: `text-primary border-b-2 border-primary`
- Badge counts: `bg-primary/10 text-primary`

### Disabled States
- Opacity: `opacity-50`
- Cursor: `cursor-not-allowed`
- No hover effects

## Common Patterns

### Grid Layouts

**Two-column form grid**:
```tsx
<div className="grid grid-cols-2 gap-4">
  <FormField label="Label 1" value="Value 1" />
  <FormField label="Label 2" value="Value 2" />
</div>
```

**Responsive cards**:
```tsx
<div className="grid grid-cols-1 md:grid-cols-2 gap-4">
  {items.map(item => <Card key={item.id}>...</Card>)}
</div>
```

### Exception Resolution UI

**Standard structure**:
```tsx
<div className="space-y-6">
  {/* Header */}
  <div className="space-y-3">
    <h2 className="text-lg font-medium">Resolve Exception</h2>
    <div className="flex items-start gap-2">
      <Sparkles className="h-4 w-4 text-yellow-500" />
      <p className="text-sm text-gray-600">Helper text</p>
    </div>
  </div>

  {/* Exception sections */}
  <div className="space-y-6">
    <div>
      <h3 className="text-sm font-medium">Section Title</h3>
    </div>
    <div className="space-y-3">
      <ExceptionBanner variant="error" title="Error">
        Description
      </ExceptionBanner>
    </div>
  </div>

  {/* Action area */}
  <div className="space-y-6">
    <div className="flex items-start gap-3">
      <WandSparkles className="text-purple-600" size={16} />
      <p className="text-sm text-gray-600">Action guidance</p>
    </div>
    <div className="flex justify-end">
      <Button>Action Button</Button>
    </div>
  </div>
</div>
```

### Toast Notifications

**Position**: Always top-right corner
**Usage**:
```tsx
toast({
  title: "Success Title",
  description: "Description text",
});
```

## Design Decisions & Guidelines

### When to Use What

**SelectableCard vs Card**:
- Use `SelectableCard` when user needs to select from options
- Use `Card` for static content containers

**Exception Banners**:
- `variant="error"` for validation errors, missing data, failures
- `variant="warning"` for non-critical issues
- `variant="info"` for helpful information
- `variant="success"` for confirmations

**Spacing**:
- Use `space-y-6` for major section spacing (exceptions, content blocks)
- Use `space-y-4` for form fields
- Use `space-y-3` for closely related items
- Use `space-y-2` for label-input pairs

**Status Field Naming**:
- "Status" - for Monto's standardized status
- "Portal Status" - for the original portal's status
- Both can be shown together with "Status" appearing first

### Component Removal Guidelines

**Avoided Statuses**:
- "Settled" and "Partially Settled" are not used in Portal Records
- Allowed statuses: "Approved by Buyer", "Rejected by Buyer", "Paid", "Pending Approval"

### Table Design

**Header styling**:
- Use `!bg-[#F6F7F9]` with important modifier to ensure grey background
- First column sticky: `sticky left-0 z-10 border-r border-gray-200`

**Footer/Pagination**:
- No top border divider
- Align left to table (no left padding)
- Show "Showing X to Y of Z records" + "Total: Amount"

## Section Header Component

A reusable header component for content sections with title, subtitle, filters, and search. Located at `src/components/ui/section-header.tsx`.

### SectionHeader Usage

```tsx
import { SectionHeader } from "@/components/ui/section-header";

<SectionHeader
  title="Associate Portal Records"
  subtitle="Select an RTP from the suggestions below."
  showSearch
  searchValue={searchValue}
  onSearchChange={setSearchValue}
  searchPlaceholder="Search invoices..."
  filters={
    <>
      <DataTableFacetedFilter title="Status" options={statusOptions} ... />
      <DataTableFacetedFilter title="Buyer" options={buyerOptions} ... />
      <DateRangePicker fromDate="" toDate="" onDateChange={() => {}} />
    </>
  }
/>
```

### SectionHeaderCard Usage

Wraps the section header in a card container with border and background. Use when the section needs visual separation.

```tsx
import { SectionHeaderCard } from "@/components/ui/section-header";

<SectionHeaderCard
  title="Section Title"
  subtitle="Description text for this section."
  showSearch
  searchValue={search}
  onSearchChange={setSearch}
  filters={<FilterComponents />}
>
  {/* Content goes here as children */}
  <YourContent />
</SectionHeaderCard>
```

### Props

| Prop | Type | Description |
|------|------|-------------|
| `title` | string | Main title of the section |
| `subtitle` | string | Optional subtitle/description |
| `filters` | ReactNode | Filter components to render |
| `showSearch` | boolean | Show search field |
| `searchValue` | string | Controlled search value |
| `onSearchChange` | (value: string) => void | Search change handler |
| `searchPlaceholder` | string | Search placeholder text |
| `actions` | ReactNode | Action buttons on the right side |
| `size` | "default" \| "compact" | Size variant |

## File Upload Components

**UploadSection pattern**:
```tsx
<div className="bg-white p-4 rounded-lg border border-gray-200 shadow-sm hover:shadow-md">
  {/* Upload UI */}
</div>
```

**Progress indicator**:
- Height: `h-2`
- Background: `bg-gray-200`
- Progress bar: `bg-primary`
- Border radius: `rounded-full`

## Icons

### Lucide React Icons
- Sizes: Typically `size={16}` or `h-4 w-4`
- Stroke width: Often `strokeWidth={1.25}` for softer look
- Colors: Match parent or use `text-{color}` classes

Common icons:
- `WandSparkles` - AI/smart features (purple-600)
- `Sparkles` - Tips/helpers (yellow-500)
- `TriangleAlert` - Warnings (warning-main or amber)
- `AlertCircle` - Errors
- `FileX2` - File/data issues
- `MoreVertical` - Actions menu

## Responsive Design

### Breakpoints
- `sm`: 640px
- `md`: 768px
- `lg`: 1024px
- `xl`: 1280px

### Common patterns
- `className="hidden md:block"` - Hide on mobile
- `grid-cols-1 md:grid-cols-2` - Responsive grid
- `max-w-md md:max-w-lg` - Responsive max width

## Best Practices

1. **Always use consistent spacing** - Prefer `space-y-6` for sections, `space-y-4` for forms
2. **Match existing patterns** - Check similar components before creating new patterns
3. **Use design tokens** - Reference colors like `primary`, `error-main`, not hex codes directly (except for `#F6F7F9` grey background)
4. **Maintain hierarchy** - Use font weights and sizes consistently
5. **Test hover states** - Ensure all interactive elements have hover feedback
6. **Accessibility first** - Include proper labels, ARIA attributes, keyboard support
7. **No emojis** - Unless explicitly requested by user
8. **Mobile-first** - Consider mobile layouts even for desktop-focused features

## Common Mistakes to Avoid

❌ Don't use `semibold` for exception banner titles (use `medium`)
❌ Don't use `space-y-4` for exception sections (use `space-y-6`)
❌ Don't forget `!bg-[#F6F7F9]` important modifier on table headers
❌ Don't add left padding to table pagination
❌ Don't use "Settled" or "Partially Settled" statuses
❌ Don't put divider lines above table pagination
❌ Don't use fixed width for Actions column (use `w-auto`)

## Questions to Ask

When implementing new UI:
1. Is there an existing component that matches this pattern?
2. What spacing scale should be used?
3. Should this support hover/selection states?
4. What are the appropriate color variants?
5. Does this need responsive breakpoints?
6. Are there accessibility considerations?

## Resources

- Component documentation in `src/components/ui/README-*.md`
- Example implementations in existing pages
- Shadcn UI base components in `src/components/ui/`
- Design patterns in `src/pages/DesignSystemPlayground.tsx`
