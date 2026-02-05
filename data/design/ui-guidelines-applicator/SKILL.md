---
name: ui-guidelines-applicator
description: Apply consistent UI design guidelines to components. Use this skill when building React/TypeScript components, designing UI patterns, or ensuring design system compliance. This skill provides comprehensive guidelines, validation tools, and component templates for maintaining visual consistency and accessibility standards.
---

# UI Guidelines Applicator

## Overview

This skill enables the creation of consistent, accessible, and well-designed UI components that follow established design system guidelines. It provides comprehensive design rules, component patterns, validation tools, and templates to ensure visual consistency across all user interfaces.

## When to Use This Skill

Use this skill when:

- Building new React/TypeScript components
- Creating responsive layouts and interfaces
- Ensuring accessibility compliance (WCAG 2.1 AA)
- Validating existing components against design guidelines
- Establishing or maintaining a design system
- Implementing consistent typography, colors, and spacing
- Creating reusable component patterns

## Core Capabilities

### 1. Design Guidelines Application

Apply comprehensive UI guidelines including:

- **Color System**: Primary, secondary, and neutral color palettes with proper contrast ratios
- **Typography**: Font sizes, weights, line heights, and spacing
- **Spacing System**: 4px-based scale with consistent usage patterns
- **Component Patterns**: Standardized implementations for buttons, forms, cards, navigation
- **Accessibility**: WCAG 2.1 AA compliance with proper ARIA attributes and keyboard navigation

### 2. Component Validation

Use the validation script to check components:

```bash
python scripts/validate_ui_guidelines.py path/to/components --format json
```

Validation checks:

- Color palette compliance
- Spacing scale adherence
- Typography consistency
- Accessibility requirements
- Semantic HTML usage

### 3. Template-Based Development

Leverage pre-built component templates from `assets/component-templates/`:

- Button component with variants and sizes
- Form field patterns with validation states
- Card layouts with consistent padding and shadows
- Modal and navigation patterns

### 4. Design System Configuration

Use `assets/design-system-config.json` as the single source of truth for:

- Color definitions and semantic usage
- Typography scales and font stacks
- Spacing values and border radius
- Component-specific styling rules
- Accessibility standards

## Implementation Workflow

### Step 1: Reference the Guidelines

Always start by consulting `references/ui-guidelines.md` for:

- Color usage rules and contrast requirements
- Typography scales and font choices
- Spacing values and layout patterns
- Component behavior guidelines

### Step 2: Choose Component Pattern

Select the appropriate pattern from `references/component-patterns.md`:

- Review existing component implementations
- Follow established props interfaces
- Use consistent naming conventions
- Implement proper accessibility attributes

### Step 3: Use Templates or Create from Scratch

For new components:

- Use templates from `assets/component-templates/` when available
- Follow the design system configuration from `assets/design-system-config.json`
- Ensure responsive design with mobile-first approach
- Include proper TypeScript types and interfaces

### Step 4: Validate Implementation

Run validation checks before finalizing:

```bash
# Validate specific files
python scripts/validate_ui_guidelines.py src/components/Button.tsx

# Validate entire component directory
python scripts/validate_ui_guidelines.py src/components/ --format text --output validation-report.txt

# Generate JSON report for CI/CD integration
python scripts/validate_ui_guidelines.py src/components/ --format json --output validation-results.json
```

### Step 5: Document and Test

- Document component usage and props
- Include accessibility testing
- Verify responsive behavior
- Test keyboard navigation and screen reader compatibility

## Common Component Patterns

### Button Implementation

```tsx
// Use the button template as a starting point
import { Button } from './assets/component-templates/button-template';

// Primary action button
<Button variant="primary" size="md">Submit</Button>

// Secondary action with icon
<Button variant="secondary" size="sm" leftIcon={<Icon />}>Cancel</Button>
```

### Form Field Pattern

```tsx
// Follow the form field structure from component-patterns.md
<div className="form-field">
  <label className="form-label">Field Label</label>
  <input type="text" className="form-input" placeholder="Enter text" />
  {error && <span className="form-error">Error message</span>}
</div>
```

### Card Layout

```tsx
// Use consistent card styling
<div className="card">
  <h3 className="card-title">Card Title</h3>
  <p className="card-content">Card content goes here</p>
  <div className="card-actions">
    <Button variant="primary">Action</Button>
  </div>
</div>
```

## Validation Results Interpretation

### Error Level Issues

- **Must Fix**: Accessibility violations, missing required attributes
- **Impact**: Broken functionality or compliance failures

### Warning Level Issues

- **Should Fix**: Design inconsistencies, non-standard patterns
- **Impact**: Visual inconsistency or maintainability issues

### Info Level Issues

- **Consider Fixing**: Optimization opportunities, best practice suggestions
- **Impact**: Minor improvements or future considerations

## Integration with Template Engines

This skill integrates seamlessly with your existing template engine architecture:

- Use design tokens in template variables
- Apply consistent styling across different adapters
- Validate generated components against the same guidelines
- Maintain design system consistency regardless of output format

## Best Practices

1. **Always validate** components before merging
2. **Use semantic HTML** for better accessibility
3. **Test with screen readers** and keyboard navigation
4. **Follow mobile-first responsive design**
5. **Maintain consistent naming** across components
6. **Document component usage** and limitations
7. **Use the design system config** as the single source of truth

## Resources

This skill includes comprehensive resources for implementing consistent UI guidelines:

### scripts/

Executable code for validation and automation:

**validate_ui_guidelines.py** - Main validation script that:

- Validates CSS/SCSS files against color palette, spacing scale, and typography guidelines
- Checks JSX/TSX files for semantic HTML and accessibility compliance
- Generates detailed reports in text or JSON format
- Supports CI/CD integration with configurable exit codes
- Validates focus states, color contrast, and ARIA attributes

**Usage examples:**

```bash
# Validate single file
python scripts/validate_ui_guidelines.py src/components/Button.tsx

# Validate directory with custom config
python scripts/validate_ui_guidelines.py src/components/ --config custom-config.json

# Generate JSON report for CI/CD
python scripts/validate_ui_guidelines.py src/ --format json --output validation.json
```

### references/

Comprehensive documentation and guidelines:

**ui-guidelines.md** - Complete design system specification including:

- Design principles and accessibility requirements
- Color system with semantic usage guidelines
- Typography scales and font specifications
- Spacing system based on 4px grid
- Component patterns and implementation guidelines
- Iconography and layout patterns
- Animation and interaction guidelines

**component-patterns.md** - Detailed component implementations:

- Button patterns with variants and sizing
- Form field structures and validation states
- Card layouts and responsive patterns
- Navigation and breadcrumb implementations
- Modal and table patterns
- Loading states and notification patterns
- Responsive design implementation guidelines

### assets/

Templates and configuration files:

**component-templates/** - Pre-built component templates:

- `button-template.tsx` - Complete button component with variants, sizes, loading states, and accessibility
- Template follows TypeScript best practices with proper interfaces and forwardRef
- Implements consistent styling with Tailwind-like class naming
- Includes accessibility attributes and ARIA support

**design-system-config.json** - Single source of truth for design system:

- Complete color palette with semantic naming
- Typography scales including font sizes, weights, and line heights
- Spacing values and border radius definitions
- Component-specific styling configurations
- Accessibility standards and breakpoint definitions
- Shadow and animation configurations

These resources work together to provide a complete solution for implementing consistent UI guidelines across any component development workflow.
