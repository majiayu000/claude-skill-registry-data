---
name: polaris-fundamentals
description: Core Polaris Web Components fundamentals including component library structure, design tokens, responsive patterns, and SSR compatibility. Auto-invoked when working with Polaris components.
allowed-tools: [Read, Grep, Glob]
documentation_path: ../../../polaris-web-components
---

# Polaris Fundamentals Skill

## Purpose
Provides foundational knowledge of Polaris Web Components, including setup, component categories, design tokens, and best practices.

## When This Skill Activates
- Working with Polaris Web Components
- Building Shopify app UIs
- Implementing design system patterns
- Choosing components for specific use cases

## Core Concepts

### Component Categories

Polaris Web Components are organized into six categories:

**1. Actions** - Interactive elements that trigger actions
- Buttons, links, icon buttons, button groups

**2. Forms** - Input and selection components
- Text fields, checkboxes, selects, file uploads, color pickers

**3. Feedback** - Status and notification components
- Banners, toasts, progress bars, spinners, skeletons

**4. Media** - Visual content components
- Avatars, icons, thumbnails, video thumbnails

**5. Structure** - Layout and organization components
- Pages, cards, sections, boxes, grids, stacks, tables

**6. Titles and Text** - Typography components
- Headings, text, paragraphs, badges, chips

### Design Tokens

#### Spacing Scale
```tsx
gap="050"  // 2px
gap="100"  // 4px
gap="200"  // 8px
gap="300"  // 12px
gap="400"  // 16px (default)
gap="500"  // 20px
gap="600"  // 24px
gap="800"  // 32px
gap="1000" // 40px
gap="1600" // 64px
```

#### Background Colors
```tsx
background="bg-surface"           // Default surface
background="bg-surface-secondary" // Secondary surface
background="bg-surface-tertiary"  // Tertiary surface
background="bg-surface-success"   // Success state
background="bg-surface-warning"   // Warning state
background="bg-surface-critical"  // Error state
```

#### Border Options
```tsx
border="base"     // Default border
border="success"  // Success border
border="warning"  // Warning border
border="critical" // Error border
```

#### Border Radius
```tsx
borderRadius="base"  // 4px
borderRadius="large" // 8px
borderRadius="full"  // 50% (circular)
```

#### Text Tones
```tsx
tone="subdued"   // Secondary text
tone="success"   // Success message
tone="warning"   // Warning message
tone="critical"  // Error message
```

### Typography Variants

```tsx
variant="heading3xl"  // Page titles
variant="heading2xl"  // Section headers
variant="headingXl"   // Card titles
variant="headingLg"   // Subsection headers
variant="headingMd"   // Card headers
variant="headingSm"   // Small headers
variant="bodyLg"      // Large body text
variant="bodyMd"      // Default body text (default)
variant="bodySm"      // Small body text
```

### Responsive Breakpoints

```tsx
// Mobile first approach
columns="1"          // Mobile (default)
sm-columns="2"       // Small devices (≥577px)
md-columns="3"       // Medium devices (≥769px)
lg-columns="4"       // Large devices (≥1025px)

// Example usage
<s-grid columns="1" md-columns="2" lg-columns="4">
  <div>Column 1</div>
  <div>Column 2</div>
  <div>Column 3</div>
  <div>Column 4</div>
</s-grid>
```

## React Hydration (SSR Apps)

### ⚠️ CRITICAL: Event Handler Pattern

**NEVER use inline event handlers** - they cause hydration mismatches in SSR apps.

```tsx
// ❌ WRONG - Hydration mismatch
<s-button onclick={handleClick}>Click</s-button>

// ✅ CORRECT - Use data attributes + useEffect
<s-button data-my-button>Click</s-button>

useEffect(() => {
  const button = document.querySelector('[data-my-button]');
  if (button) {
    button.addEventListener('click', handleClick);
  }
  return () => button?.removeEventListener('click', handleClick);
}, []);
```

## Common Component Patterns

### Button Variants
```tsx
<s-button>Default</s-button>
<s-button variant="primary">Primary</s-button>
<s-button variant="destructive">Delete</s-button>
<s-button variant="plain">Plain</s-button>
<s-button size="slim">Small</s-button>
<s-button loading>Loading</s-button>
<s-button disabled>Disabled</s-button>
```

### Text Field States
```tsx
<s-text-field
  label="Product Title"
  value={title}
  error={errors.title}        // Show error
  disabled={isDisabled}       // Disable input
  required                    // Mark required
  helpText="Customer-facing"  // Help text
  placeholder="Enter title"   // Placeholder
/>
```

### Card Structure
```tsx
<s-card>
  <s-stack gap="400" direction="vertical">
    <s-heading>Card Title</s-heading>
    <s-divider />
    <s-text>Card content</s-text>
    <s-divider />
    <s-button-group>
      <s-button variant="primary">Save</s-button>
      <s-button>Cancel</s-button>
    </s-button-group>
  </s-stack>
</s-card>
```

### Loading Pattern
```tsx
{isLoading ? (
  <s-card>
    <s-stack gap="400" direction="vertical">
      <s-skeleton-display-text />
      <s-skeleton-display-text />
      <s-skeleton-display-text />
    </s-stack>
  </s-card>
) : (
  <s-card>{/* Actual content */}</s-card>
)}
```

### Empty State Pattern
```tsx
{items.length === 0 ? (
  <s-empty-state
    heading="No items yet"
    image="https://cdn.shopify.com/..."
  >
    <s-text>Get started by adding your first item</s-text>
    <s-button variant="primary">Add Item</s-button>
  </s-empty-state>
) : (
  // Item list
)}
```

## Page Structure

### Standard Page Layout
```tsx
<s-page heading="Page Title">
  <s-section>
    {/* First section */}
  </s-section>

  <s-section>
    {/* Second section */}
  </s-section>
</s-page>
```

### Page with Primary Action
```tsx
<s-page
  heading="Products"
  primaryAction={{
    content: "Add Product",
    url: "/products/new"
  }}
>
  {/* Page content */}
</s-page>
```

## Accessibility

### Semantic HTML
```tsx
<s-heading as="h1">Main Title</s-heading>
<s-heading as="h2">Section Title</s-heading>
<s-text as="p">Paragraph text</s-text>
```

### ARIA Labels
```tsx
<s-icon-button
  icon="delete"
  aria-label="Delete product"
/>

<s-search-field
  aria-label="Search products"
  placeholder="Search..."
/>
```

### Keyboard Navigation
- All interactive elements are keyboard accessible
- Use Tab to navigate
- Enter/Space to activate buttons
- Escape to close modals

## Best Practices

1. **Use Design Tokens** - Never hardcode colors, spacing, or typography
2. **Mobile First** - Start with mobile layout, enhance for desktop
3. **Semantic HTML** - Use the `as` prop for proper HTML elements
4. **Loading States** - Always show skeleton loaders during data fetch
5. **Empty States** - Provide guidance when no data exists
6. **Error Handling** - Use inline errors for form validation
7. **Accessibility** - Ensure keyboard navigation and ARIA labels
8. **Consistent Spacing** - Use Polaris spacing scale (gap="400")
9. **SSR Compatible** - Use data attributes for event handlers
10. **Follow Patterns** - Use established Polaris patterns

## Component Selection Guide

| Need | Component | Example |
|------|-----------|---------|
| Primary action | `<s-button variant="primary">` | Save, Submit |
| Secondary action | `<s-button>` | Cancel, Back |
| Destructive action | `<s-button variant="destructive">` | Delete, Remove |
| Page container | `<s-page>` | All pages |
| Content container | `<s-card>` | Forms, data displays |
| Text input | `<s-text-field>` | Title, description |
| Selection | `<s-select>` | Category, status |
| Multiple choices | `<s-checkbox>` | Features, options |
| Success message | `<s-banner tone="success">` | Saved successfully |
| Error message | `<s-banner tone="critical">` | Failed to save |
| Status indicator | `<s-badge>` | Active, Draft |
| Data table | `<s-table>` | Products, orders |
| Vertical spacing | `<s-stack direction="vertical">` | Form fields |
| Horizontal layout | `<s-grid>` | Dashboard cards |

## Documentation Reference

For complete component documentation, see:
- `polaris-web-components/components/` - All component docs
- `polaris-web-components/patterns/` - Composition patterns
- `polaris-web-components/using-polaris-web-components.md` - Setup guide

---

**Remember**: Polaris ensures your app matches Shopify's design system and provides a consistent, accessible user experience.
