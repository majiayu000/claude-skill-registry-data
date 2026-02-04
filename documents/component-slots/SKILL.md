---
name: "component-slots"
description: "Adding data-slot attributes for CSS targeting and component documentation"
---

# Component Slots Skill

## Purpose

Data slots allow CSS to target specific parts of components for styling overrides without modifying the component itself.

## Quick Example

```tsx
// Component with slots
<div data-slot="card-wrapper">
  <div data-slot="card-header">
    <h2 data-slot="card-title">Title</h2>
  </div>
  <div data-slot="card-content">
    Content here
  </div>
</div>

// Parent can override styling
<Card className="[&_*[data-slot='card-title']]:text-red-500" />
```

## When to Add Slots

- Important structural elements (wrappers, containers)
- Elements that consumers might want to style
- Logical sections within a component
- Sub-components that need targeting

## Slot Naming Convention

Format: `{component-name}-{element-name}`

```tsx
// Good naming
data-slot="table-wrapper"
data-slot="table-header"
data-slot="table-row"
data-slot="table-cell"

// Avoid generic names
data-slot="wrapper"  // Too generic
data-slot="div"      // Not descriptive
```

## Complete Table Example

```tsx
<div data-slot="table-wrap">
  <table data-slot="table">
    <thead data-slot="thead">
      <tr data-slot="thead-tr">
        <th data-slot="thead-th">Name</th>
        <th data-slot="thead-th">Status</th>
      </tr>
    </thead>
    <tbody data-slot="tbody">
      <tr data-slot="tr">
        <td data-slot="td">John</td>
        <td data-slot="td">Active</td>
      </tr>
    </tbody>
    <tfoot data-slot="tfoot">
      <tr data-slot="total-row">
        <td data-slot="total-cell" colSpan={2}>
          Total: 1
        </td>
      </tr>
    </tfoot>
  </table>
</div>
```

## Documentation Format

After adding slots, document them at the top of the component file:

```tsx
/**
 * Card component with customizable styling
 *
 * @example
 * <Card className="[&_*[data-slot='card-title']]:text-lg" />
 *
 * ## Card Slots
 *
 * @slot {"card-wrapper"} data-slot="card-wrapper" - Main container
 * @slot {"card-header"} data-slot="card-header" - Header section
 * @slot {"card-title"} data-slot="card-title" - Title element
 * @slot {"card-content"} data-slot="card-content" - Content area
 * @slot {"card-footer"} data-slot="card-footer" - Footer section
 */
export const Card = ({ children, className }: CardProps) => {
  return (
    <div
      data-slot="card-wrapper"
      className={cn("rounded-lg border", className)}
    >
      {children}
    </div>
  );
};
```

## Complex Component with Sub-Components

```tsx
/**
 * Table component with inline editing
 *
 * @example
 * <Table className="[&_*[data-slot='thead-tr']]:border-t" />
 *
 * ## TableBase Slots
 *
 * @slot {"table-wrap"} data-slot="table-wrap" - Outer wrapper
 * @slot {"table"} data-slot="table" - Table element
 * @slot {"thead"} data-slot="thead" - Table header
 * @slot {"tbody"} data-slot="tbody" - Table body
 * @slot {"tfoot"} data-slot="tfoot" - Table footer
 * @slot {"no-data"} data-slot="no-data" - Empty state
 *
 * ## TableRow Slots
 *
 * @slot {"tr"} data-slot="tr" - Table row
 * @slot {"td"} data-slot="td" - Table cell
 * @slot {"expand-row-td"} data-slot="expand-row-td" - Expandable row cell
 *
 * ## TableHeader Slots
 *
 * @slot {"thead-tr"} data-slot="thead-tr" - Header row
 * @slot {"thead-th"} data-slot="thead-th" - Header cell
 * @slot {"thead-checkbox"} data-slot="thead-checkbox" - Header checkbox
 *
 * ## TableFooter Slots
 *
 * @slot {"total-row"} data-slot="total-row" - Totals row
 * @slot {"table-pagination"} data-slot="table-pagination" - Pagination wrapper
 * @slot {"table-pagination-page-size"} data-slot="table-pagination-page-size" - Page size selector
 */
```

## Bubbling Up Slots from Sub-Components

When your component uses sub-components with slots, document all available slots:

```tsx
/**
 * DataTable wraps TableBase and adds filtering
 *
 * ## DataTable Slots
 *
 * @slot {"data-table-wrapper"} data-slot="data-table-wrapper" - Main wrapper
 * @slot {"data-table-filters"} data-slot="data-table-filters" - Filter section
 * @slot {"data-table-actions"} data-slot="data-table-actions" - Action buttons
 *
 * ## Inherited TableBase Slots
 *
 * @slot {"table-wrap"} data-slot="table-wrap" - From TableBase
 * @slot {"table"} data-slot="table" - From TableBase
 * @slot {"thead"} data-slot="thead" - From TableBase
 * @slot {"tbody"} data-slot="tbody" - From TableBase
 * @slot {"tr"} data-slot="tr" - From TableBase
 * @slot {"td"} data-slot="td" - From TableBase
 */
```

## Usage Examples in Documentation

Show practical examples of how to use slots:

```tsx
/**
 * @example
 * // Change header background
 * <Table className="[&_*[data-slot='thead']]:bg-gray-100" />
 *
 * @example
 * // Style all cells
 * <Table className="[&_*[data-slot='td']]:p-4" />
 *
 * @example
 * // Customize footer
 * <Table className="[&_*[data-slot='tfoot']]:font-bold [&_*[data-slot='total-row']]:border-t-2" />
 */
```

## Best Practices

1. **Only add slots to important elements** - Don't over-slot every div
2. **Use consistent naming** - Follow the `{component}-{element}` pattern
3. **Document all slots** - Users need to know what's available
4. **Group by section** - Organize slot docs logically (header, body, footer)
5. **Provide examples** - Show practical usage patterns
6. **Bubble up sub-component slots** - Document inherited slots
7. **Keep names descriptive** - Avoid generic names like "wrapper" or "div"

## What NOT to Slot

- Internal implementation details
- Temporary elements
- Elements that won't need styling
- Every single wrapper div

## Key Rules

1. Add slots to important structural elements only
2. Use descriptive, consistent naming
3. Document all slots at the top of the component
4. Provide usage examples
5. Group documentation by logical sections
6. Include inherited slots from sub-components
7. Don't over-slot - be selective
