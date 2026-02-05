---
name: style-ui
description: Style and UI patterns for DaisyUI Emerald theme. Use when styling forms, cards, buttons, tables, and other UI components. Includes fancy card designs, color schemes, and visual effects.
---

# Style and UI Patterns

## Overview
This skill documents the UI styling patterns used in this project, focusing on DaisyUI with the Emerald theme. It covers fancy form cards, color schemes, visual effects, and consistent styling conventions.

## Theme Configuration

### Emerald Theme Setup
The project uses DaisyUI's Emerald theme as the default:

```css
/* In App.css */
@plugin 'daisyui' {
  themes: emerald --default, dark;
}
```

```typescript
/* In rsbuild.config.ts */
html: {
  htmlAttrs: {
    'data-theme': 'emerald',
  },
},
```

### Emerald Theme Colors
| Color | Usage | Tailwind Class |
|-------|-------|----------------|
| Primary | Main actions, links | `text-primary`, `bg-primary`, `border-primary` |
| Secondary | Alternative actions | `text-secondary`, `bg-secondary` |
| Accent | Highlights, tags | `text-accent`, `bg-accent` |
| Info | Information, previews | `text-info`, `bg-info` |
| Success | Published, confirmed | `text-success`, `bg-success` |
| Warning | Warnings, content | `text-warning`, `bg-warning` |
| Error | Errors, delete | `text-error`, `bg-error` |

## Fancy Card Pattern

### Card Structure
```tsx
<div className="card bg-base-100 shadow-lg border-t-4 border-t-primary hover:shadow-xl transition-shadow duration-300">
  <div className="card-body">
    {/* Card Header */}
    <div className="flex items-start gap-4">
      <div className="bg-primary/10 p-3 rounded-xl">
        <IconComponent className="w-6 h-6 text-primary" />
      </div>
      <div className="flex-1">
        <h2 className="card-title text-lg">Card Title</h2>
        <p className="text-sm text-base-content/60">
          Description text here
        </p>
      </div>
    </div>

    <div className="divider my-2"></div>

    {/* Card Content */}
    <div className="space-y-4">
      {/* Content goes here */}
    </div>
  </div>
</div>
```

### Card Color Variations
Use different border colors to distinguish sections:

```tsx
{/* Primary - Basic Information */}
<div className="card bg-base-100 shadow-lg border-t-4 border-t-primary hover:shadow-xl transition-shadow duration-300">
  <div className="bg-primary/10 p-3 rounded-xl">
    <FolderOpen className="w-6 h-6 text-primary" />
  </div>
</div>

{/* Secondary - Thumbnails/Media */}
<div className="card bg-base-100 shadow-lg border-t-4 border-t-secondary hover:shadow-xl transition-shadow duration-300">
  <div className="bg-secondary/10 p-3 rounded-xl">
    <ImagePlus className="w-6 h-6 text-secondary" />
  </div>
</div>

{/* Accent - Tags */}
<div className="card bg-base-100 shadow-lg border-t-4 border-t-accent hover:shadow-xl transition-shadow duration-300">
  <div className="bg-accent/10 p-3 rounded-xl">
    <Tag className="w-6 h-6 text-accent" />
  </div>
</div>

{/* Info - Preview Content */}
<div className="card bg-base-100 shadow-lg border-t-4 border-t-info hover:shadow-xl transition-shadow duration-300">
  <div className="bg-info/10 p-3 rounded-xl">
    <BookOpen className="w-6 h-6 text-info" />
  </div>
</div>

{/* Warning - Full Content */}
<div className="card bg-base-100 shadow-lg border-t-4 border-t-warning hover:shadow-xl transition-shadow duration-300">
  <div className="bg-warning/10 p-3 rounded-xl">
    <FileText className="w-6 h-6 text-warning" />
  </div>
</div>
```

### Icon Badge Pattern
```tsx
<div className="bg-{color}/10 p-3 rounded-xl">
  <IconComponent className="w-6 h-6 text-{color}" />
</div>
```

Replace `{color}` with: `primary`, `secondary`, `accent`, `info`, `warning`, `success`, `error`

## Form Input Styling

### Basic Input with Focus State
```tsx
<label className="form-control w-full">
  <div className="label">
    <span className="label-text font-medium">Label Text</span>
  </div>
  <input
    type="text"
    className={`input input-bordered w-full focus:input-primary ${errors.field ? 'input-error' : ''}`}
    placeholder="Placeholder text"
    disabled={isLoading}
  />
  {errors.field && (
    <div className="label">
      <span className="label-text-alt text-error">{errors.field.message}</span>
    </div>
  )}
</label>
```

### Select with Focus State
```tsx
<select
  className={`select select-bordered w-full focus:select-primary ${errors.field ? 'select-error' : ''}`}
  disabled={isLoading}
>
  <option value="" disabled>Select option</option>
  {options.map((opt) => (
    <option key={opt.id} value={opt.id}>{opt.name}</option>
  ))}
</select>
```

### Textarea with Focus State
```tsx
<textarea
  className={`textarea textarea-bordered w-full min-h-28 focus:textarea-info ${errors.field ? 'textarea-error' : ''}`}
  placeholder="Enter text..."
  disabled={isLoading}
/>
```

### Multi-Chip Input Container
```tsx
<div className="flex flex-wrap border-2 border-base-300 rounded-xl p-3 min-h-[52px] bg-base-100 focus-within:border-accent transition-colors">
  {/* Chips content */}
</div>
```

## Toggle/Switch Pattern

### Published Status Toggle
```tsx
<Controller
  name="published"
  control={control}
  render={({ field }) => (
    <div
      className={`flex items-center gap-3 border-2 rounded-xl px-4 h-12 transition-all duration-200 ${
        field.value
          ? 'border-success bg-success/5'
          : 'border-base-300 bg-base-100'
      }`}
    >
      <input
        type="checkbox"
        className={`toggle ${field.value ? 'toggle-success' : ''}`}
        checked={field.value}
        onChange={field.onChange}
        disabled={isLoading}
      />
      <span className={`font-medium ${field.value ? 'text-success' : 'text-base-content/60'}`}>
        {field.value ? 'Published' : 'Draft'}
      </span>
      {field.value && <Sparkles className="w-4 h-4 text-success ml-auto" />}
    </div>
  )}
/>
```

## Badge Patterns

### Optional Field Badge
```tsx
<div className="flex items-center justify-between">
  <h2 className="card-title text-lg">Section Title</h2>
  <span className="badge badge-accent badge-outline">Optional</span>
</div>
```

### Status Badge
```tsx
{/* Published/Draft */}
<span className={`badge badge-sm ${item.published ? 'badge-success' : 'badge-ghost'}`}>
  {item.published ? 'Published' : 'Draft'}
</span>

{/* Category Type */}
<span className={`badge badge-sm ${
  item.categoryType === 'Blog' ? 'badge-primary' : 'badge-secondary'
}`}>
  {item.categoryType}
</span>
```

### Tag Badges
```tsx
<div className="flex flex-wrap gap-1">
  {tags.slice(0, 3).map((tag) => (
    <span key={tag.id} className="badge badge-ghost badge-sm">
      {tag.name}
    </span>
  ))}
  {tags.length > 3 && (
    <span className="badge badge-ghost badge-sm">
      +{tags.length - 3}
    </span>
  )}
</div>
```

## Button Patterns

### Primary Action Button
```tsx
<button
  type="submit"
  className="btn btn-primary flex-1 gap-2 shadow-lg hover:shadow-primary/25"
  disabled={isLoading}
>
  {isSubmitting ? (
    <>
      <span className="loading loading-spinner loading-sm"></span>
      {id ? 'Updating...' : 'Creating...'}
    </>
  ) : (
    <>
      <Save className="w-4 h-4" />
      {id ? 'Update' : 'Create'}
    </>
  )}
</button>
```

### Ghost/Cancel Button
```tsx
<button
  type="button"
  className="btn btn-ghost gap-2 hover:bg-base-200"
  onClick={() => navigate('/admin/list')}
  disabled={isLoading}
>
  <ArrowLeft className="w-4 h-4" />
  Cancel
</button>
```

### Action Button Layout
```tsx
<div className="flex flex-col-reverse sm:flex-row gap-3 pt-4">
  <button className="btn btn-ghost gap-2">Cancel</button>
  <button className="btn btn-primary flex-1 gap-2">Submit</button>
</div>
```

### Small Outline Button
```tsx
<button className="btn btn-sm btn-secondary btn-outline gap-1">
  <Plus className="w-4 h-4" />
  Add Item
</button>
```

### Delete Button (Ghost with Error Color)
```tsx
<button
  className="btn btn-ghost btn-sm btn-square text-error hover:bg-error/10"
  onClick={handleDelete}
  title="Delete"
>
  <Trash2 className="w-4 h-4" />
</button>
```

## Empty State Pattern

### Form Empty State
```tsx
<div className="text-center py-10 border-2 border-dashed border-base-300 rounded-xl bg-base-200/30">
  <div className="bg-secondary/10 w-16 h-16 rounded-full flex items-center justify-center mx-auto mb-3">
    <Languages className="w-8 h-8 text-secondary/50" />
  </div>
  <p className="text-base-content/50 text-sm mb-3">No items added yet</p>
  <button
    type="button"
    className="btn btn-sm btn-ghost text-secondary"
    onClick={handleAdd}
  >
    <Plus className="w-4 h-4" />
    Add first item
  </button>
</div>
```

### List Empty State
```tsx
<div className="flex flex-col items-center justify-center py-16 px-4">
  <div className="bg-base-200 rounded-full p-4 mb-4">
    <FileText className="w-8 h-8 text-base-content/40" />
  </div>
  <h3 className="text-lg font-semibold mb-1">
    {hasActiveFilters ? 'No items found' : 'No items yet'}
  </h3>
  <p className="text-base-content/60 text-center mb-4">
    {hasActiveFilters
      ? 'Try adjusting your search or filter criteria'
      : 'Get started by creating your first item'}
  </p>
  {hasActiveFilters ? (
    <button className="btn btn-ghost btn-sm" onClick={clearFilters}>
      Clear filters
    </button>
  ) : (
    <Link to="/create" className="btn btn-primary btn-sm gap-2">
      <Plus className="w-4 h-4" />
      Create Item
    </Link>
  )}
</div>
```

## Table Styling

### Modern Table
```tsx
<div className="card bg-base-100 shadow-sm">
  <div className="overflow-x-auto">
    <table className="table">
      <thead>
        <tr className="bg-base-200/50">
          <th className="cursor-pointer hover:bg-base-200 transition-colors">
            Column Name
            <SortIcon columnKey="field" />
          </th>
        </tr>
      </thead>
      <tbody>
        {items.map((item) => (
          <tr key={item.id} className="hover:bg-base-200/30 transition-colors">
            <td className="font-medium">{item.name}</td>
            <td>
              <code className="text-xs bg-base-200 px-2 py-1 rounded">
                {item.slug}
              </code>
            </td>
          </tr>
        ))}
      </tbody>
    </table>
  </div>
</div>
```

### Sort Icon Component
```tsx
const SortIcon = ({ columnKey }: { columnKey: string }) => {
  if (sortConfig?.key !== columnKey) return null;
  return sortConfig.direction === 'asc' ? (
    <ChevronUp className="inline w-4 h-4 ml-1" />
  ) : (
    <ChevronDown className="inline w-4 h-4 ml-1" />
  );
};
```

## Filter UI Pattern

### Collapsible Filter
```tsx
<details className="group bg-base-100 shadow-sm rounded-lg">
  <summary className="flex items-center justify-between cursor-pointer list-none p-4 font-medium">
    <div className="flex items-center gap-2">
      <span>Filters</span>
      {hasActiveFilters && (
        <span className="badge badge-primary badge-sm">
          {filteredItems.length} / {items.length}
        </span>
      )}
    </div>
    <ChevronDown className="w-4 h-4 transition-transform group-open:rotate-180" />
  </summary>
  <div className="px-4 pb-4">
    <div className="flex flex-col sm:flex-row gap-3">
      {/* Filter inputs */}
    </div>
  </div>
</details>
```

### Search Input with Clear
```tsx
<label className="input input-bordered flex items-center gap-2 flex-1">
  <Search className="w-4 h-4 opacity-50" />
  <input
    type="text"
    placeholder="Search..."
    className="grow"
    value={searchTerm}
    onChange={(e) => setSearchTerm(e.target.value)}
  />
  {searchTerm && (
    <button
      type="button"
      className="btn btn-ghost btn-xs btn-circle"
      onClick={() => setSearchTerm('')}
    >
      <X className="w-3 h-3" />
    </button>
  )}
</label>
```

## Tab Pattern

### Boxed Tabs with Active State
```tsx
<div className="tabs tabs-boxed bg-base-200 p-1 rounded-xl mb-4">
  {tabs.map((tab, index) => (
    <button
      key={tab.id}
      type="button"
      className={`tab gap-2 transition-all ${
        activeTab === index ? 'tab-active bg-secondary text-secondary-content' : ''
      }`}
      onClick={() => setActiveTab(index)}
    >
      <Globe className="w-3 h-3" />
      {tab.label}
    </button>
  ))}
</div>
```

### Tab Content Container
```tsx
<div className={`space-y-4 p-4 bg-base-200/30 rounded-xl ${activeTab === index ? '' : 'hidden'}`}>
  {/* Tab content */}
</div>
```

## Pagination Pattern

```tsx
<div className="card-body border-t border-base-200 py-3">
  <div className="flex flex-col sm:flex-row items-center justify-between gap-3">
    <span className="text-sm text-base-content/60">
      Showing {startIndex + 1} to {endIndex} of {total} items
    </span>
    <div className="join">
      <button
        className="join-item btn btn-sm"
        disabled={currentPage === 1}
        onClick={() => setCurrentPage((p) => p - 1)}
      >
        Previous
      </button>
      {/* Page numbers */}
      <button
        className="join-item btn btn-sm"
        disabled={currentPage === totalPages}
        onClick={() => setCurrentPage((p) => p + 1)}
      >
        Next
      </button>
    </div>
  </div>
</div>
```

## Modal Pattern

### DaisyUI Dialog Modal
```tsx
<dialog id="modal_id" className={`modal ${isOpen ? 'modal-open' : ''}`}>
  <div className="modal-box">
    <h3 className="font-bold text-lg">Modal Title</h3>
    <p className="py-4">Modal content goes here.</p>
    <div className="modal-action">
      <button className="btn btn-ghost" onClick={handleCancel}>
        Cancel
      </button>
      <button className="btn btn-error" onClick={handleConfirm}>
        {isLoading ? (
          <>
            <span className="loading loading-spinner loading-sm"></span>
            Processing...
          </>
        ) : (
          'Confirm'
        )}
      </button>
    </div>
  </div>
  <form method="dialog" className="modal-backdrop" onClick={handleCancel}>
    <button>close</button>
  </form>
</dialog>
```

## Icon Usage

### Icon Sizes
```tsx
// Small (buttons, inline)
<Icon className="w-4 h-4" />

// Medium (card headers)
<Icon className="w-5 h-5" />

// Large (card icon badges)
<Icon className="w-6 h-6" />

// Extra Large (empty states)
<Icon className="w-8 h-8" />
```

### Common Icons
```tsx
import {
  // Navigation
  Home, ArrowLeft, ChevronDown, ChevronUp,

  // Actions
  Plus, Save, Pencil, Trash2, X, Search,

  // Content Types
  FileText, FolderOpen, ImagePlus, BookOpen,

  // Features
  Tag, Globe, Languages, Sparkles,

  // Status
  Check, AlertCircle, Info,
} from 'lucide-react';
```

## Opacity/Transparency Patterns

### Text Opacity
```tsx
text-base-content/60   // Muted text (descriptions)
text-base-content/50   // More muted (help text)
text-base-content/40   // Very muted (placeholders, empty states)
```

### Background Opacity
```tsx
bg-primary/10          // Light tinted background (icon badges)
bg-base-200/30         // Subtle background (tab content)
bg-success/5           // Very light tint (active toggle)
hover:bg-error/10      // Hover state for error actions
```

## Transition Patterns

### Shadow Transition (Cards)
```tsx
className="shadow-lg hover:shadow-xl transition-shadow duration-300"
```

### Color Transition (Inputs)
```tsx
className="border-base-300 focus-within:border-accent transition-colors"
```

### Transform Transition (Icons)
```tsx
className="transition-transform group-open:rotate-180"
```

### All Transitions (Toggle States)
```tsx
className="transition-all duration-200"
```

## Responsive Patterns

### Form Grid
```tsx
<div className="grid grid-cols-1 md:grid-cols-2 gap-4">
  {/* Form fields */}
</div>
```

### Button Layout
```tsx
<div className="flex flex-col-reverse sm:flex-row gap-3">
  {/* Buttons */}
</div>
```

### Filter Layout
```tsx
<div className="flex flex-col sm:flex-row gap-3">
  {/* Filter inputs */}
</div>
```

## Best Practices

1. **Consistent Color Scheme**: Use the same border color and icon color for each card section
2. **Hover Effects**: Add `hover:shadow-xl transition-shadow duration-300` to interactive cards
3. **Focus States**: Use `focus:input-{color}` for matching focus colors
4. **Dividers**: Use `<div className="divider my-2"></div>` between card header and content
5. **Icon Badges**: Wrap icons in colored rounded containers for visual hierarchy
6. **Optional Labels**: Use `badge badge-{color} badge-outline` for optional field indicators
7. **Empty States**: Include icon, message, and action button
8. **Loading States**: Use DaisyUI loading spinners with appropriate sizes
9. **Error States**: Use `text-error` and `input-error` classes consistently
10. **Full Width Forms**: Remove max-width constraints for full-width layouts
