---
name: zyntro-ui-guidelines
description: Apply ZyntroTest brand guidelines and design system to all UI components. Use this skill when building, modifying, or reviewing any HTML/CSS components, pages, or features for ZyntroTest.com to ensure brand consistency, proper styling, and adherence to the established design system. This skill should be proactively applied whenever creating or editing visual elements, forms, buttons, cards, layouts, or any user-facing components.
---

# ZyntroTest UI Guidelines Skill

## Purpose

This skill provides comprehensive brand guidelines and UI component standards for ZyntroTest.com, ensuring all components maintain visual consistency, follow the established design system, and deliver a professional, cohesive user experience. Apply these guidelines to all UI development work.

## When to Use This Skill

Use this skill proactively whenever:

- **Building new components** - Creating buttons, cards, forms, sections, or any UI element
- **Creating new pages** - Developing new HTML pages or templates
- **Modifying existing components** - Updating styles, layouts, or visual elements
- **Reviewing code** - Checking if components follow brand guidelines
- **Refactoring UI** - Improving consistency and adherence to design system
- **Debugging visual issues** - Ensuring proper use of design tokens
- **Adding features** - Any work that involves user-facing elements

**Do not wait for the user to ask** - proactively apply these guidelines to maintain brand consistency.

## How to Use This Skill

### 1. Load Brand Guidelines

When starting any UI work, first read the complete brand guidelines:

```bash
Read: references/brand-guidelines.md
```

This file contains:
- Complete color palette with CSS variable names
- Typography system (fonts, sizes, weights)
- Spacing system and layout guidelines
- Shadow, radius, and transition standards
- Accessibility requirements
- Brand voice and messaging

**Key Reference Sections:**
- **Colors:** Always use CSS variables (`var(--primary-blue)`, `var(--gray-600)`, etc.)
- **Typography:** Use `var(--text-xl)`, `var(--font-display)`, etc.
- **Spacing:** Use `var(--space-md)`, `var(--space-lg)`, etc.
- **Component Patterns:** Standard styling for buttons, cards, forms

### 2. Reference Component Library

When building specific components, consult the component library:

```bash
Read: references/component-library.md
```

This file provides:
- Complete HTML structure for standard components
- Usage guidelines and best practices
- Responsive patterns and mobile-first examples
- Accessibility patterns
- Component composition examples

**Search Patterns:**
- Need a button? Search for "Button Components"
- Need a card? Search for "Card Components"
- Need a form? Search for "Form Components"
- Need layout guidance? Search for "Section Components"

### 3. Apply Guidelines to Your Work

When creating or modifying components:

#### For New Components:

1. **Check if a standard component exists** in `component-library.md`
   - If it exists, use the exact HTML structure and classes
   - Maintain consistency with existing patterns

2. **Apply design system values** from `brand-guidelines.md`
   - Use CSS variables for all colors, spacing, typography
   - Never use arbitrary values (e.g., `#FF0000` instead of `var(--primary-blue)`)
   - Follow the spacing system (`var(--space-md)` not `20px`)

3. **Ensure mobile-first responsive design**
   - Start with mobile styles
   - Use media queries for tablet (768px+) and desktop (1024px+)
   - Test component behavior at all breakpoints

4. **Include proper accessibility**
   - Add ARIA labels where needed
   - Ensure keyboard navigation works
   - Maintain proper color contrast
   - Include focus states

#### For Existing Component Modifications:

1. **Verify current component** matches brand guidelines
   - Check colors are using CSS variables
   - Verify spacing follows the system
   - Ensure typography is correct

2. **Make changes while maintaining consistency**
   - Don't introduce new arbitrary values
   - Keep the same visual language
   - Maintain the component hierarchy

3. **Update related components** if needed
   - If changing a button style, update all buttons
   - Maintain consistency across the site

#### Quality Checklist:

Before completing any UI work, verify:

- ✅ All colors use CSS variables (no hex codes like `#2563eb` directly)
- ✅ All spacing uses CSS variables (`var(--space-*)`)
- ✅ Typography uses font variables and size scales
- ✅ Component follows mobile-first approach
- ✅ Hover/focus states are included
- ✅ Accessibility requirements are met (ARIA, contrast, keyboard nav)
- ✅ Component matches existing patterns in component-library.md
- ✅ Responsive breakpoints are properly implemented
- ✅ Transitions use standard timing (`var(--transition-base)`)

### 4. Common Scenarios

#### Scenario: Creating a New Button

```bash
# Step 1: Read component library for button patterns
Read: references/component-library.md

# Step 2: Find "Button Components" section

# Step 3: Use the exact HTML structure and classes:
<a href="#" class="btn btn-primary">Button Text</a>

# Step 4: Verify it uses brand colors:
# .btn-primary uses var(--primary-blue) ✅
```

#### Scenario: Building a New Card Component

```bash
# Step 1: Check if card pattern exists
Read: references/component-library.md (search for "Card Components")

# Step 2: Use standard card structure with design system values
<div class="service-card">
    <div class="service-icon">🔬</div>
    <h3>Title (var(--text-xl))</h3>
    <p>Description (var(--text-base))</p>
</div>

# Step 3: Apply standard styling:
# - Border-radius: var(--radius-lg)
# - Shadow: var(--shadow-md)
# - Padding: var(--space-lg)
```

#### Scenario: Creating a New Page

```bash
# Step 1: Read brand guidelines for overall structure
Read: references/brand-guidelines.md

# Step 2: Read component library for layout patterns
Read: references/component-library.md (search for "Section Components")

# Step 3: Build page using:
# - Standard header component
# - Hero section (if needed)
# - Content sections with proper spacing
# - Standard footer component

# Step 4: Ensure consistency:
# - Use section padding: var(--space-2xl) mobile, var(--space-3xl) desktop
# - Use container with proper padding
# - Follow typography hierarchy
```

#### Scenario: Fixing Visual Inconsistency

```bash
# Step 1: Identify what's inconsistent
# Example: Button uses #2563eb instead of var(--primary-blue)

# Step 2: Check brand guidelines for correct value
Read: references/brand-guidelines.md (search for "Primary Colors")

# Step 3: Replace with CSS variable
# Before: background: #2563eb;
# After: background: var(--primary-blue);

# Step 4: Check for other instances and fix them too
```

### 5. Brand Voice in Copy

When writing copy for components, follow these principles:

- **Professional & Scientific:** Use clear, accurate language
- **Trustworthy:** Emphasize reliability and compliance
- **Modern:** Use contemporary, accessible phrasing
- **Action-Oriented:** Clear CTAs (e.g., "Get Your COA", "Request Analysis")

See `references/brand-guidelines.md` > "Brand Voice & Messaging" for detailed guidelines.

## Output Format

When creating or modifying components, provide:

1. **Complete HTML** with proper structure and semantic elements
2. **CSS with design system variables** (never arbitrary values)
3. **Responsive media queries** if needed
4. **Accessibility attributes** (ARIA labels, roles, etc.)
5. **Comments explaining** any deviations from standard patterns

## Integration Notes

### Working with Existing Codebase

The ZyntroTest.com project already implements this design system in:
- `css/style.css` - Contains all CSS variables and component styles
- `js/script.js` - Contains shared UI functionality
- Multiple HTML pages use these components

When modifying the codebase:
- Maintain the existing CSS variable definitions in `:root`
- Use existing component classes when possible
- Follow the established file structure

### CSS Variable Reference

All design system values are defined as CSS variables in `css/style.css`:

```css
:root {
    /* Colors */
    --primary-blue: #2563eb;
    --gray-900: #0f172a;
    --white: #ffffff;

    /* Typography */
    --font-primary: 'Roboto', sans-serif;
    --text-xl: 1.25rem;

    /* Spacing */
    --space-lg: 2rem;

    /* Effects */
    --shadow-md: 0 4px 6px -1px rgb(0 0 0 / 0.1);
    --radius-md: 0.5rem;
    --transition-base: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
}
```

Always reference these variables, never duplicate or hard-code values.

## Examples

### Example 1: Creating a New Service Card

**User Request:** "Add a new service card for hemp testing"

**Correct Approach:**

```bash
# Step 1: Read component library for service card pattern
Read: references/component-library.md

# Step 2: Use standard service card structure
```

```html
<div class="service-card">
    <div class="service-icon">🌿</div>
    <h3>Cannabis/Hemp Testing</h3>
    <p>Quantify THC/CBD and screen for pesticides or mycotoxins using LCMS-DAD.</p>
    <ul class="service-features">
        <li>✓ Cannabinoid potency profile</li>
        <li>✓ Pesticide screening</li>
        <li>✓ 5-7 business day turnaround</li>
    </ul>
    <div class="service-price">Starting at $225/sample</div>
    <a href="contact.html" class="btn btn-primary">Request Quote</a>
</div>
```

**Why this is correct:**
- Uses existing `.service-card` component
- Follows established HTML structure
- Uses brand icons (emoji-based)
- Uses standard button component
- Maintains consistent feature list format

### Example 2: Adding a New CTA Section

**User Request:** "Add a call-to-action section encouraging users to submit samples"

**Correct Approach:**

```bash
# Step 1: Check brand guidelines for CTA language
Read: references/brand-guidelines.md (search for "Call-to-Action Language")

# Step 2: Use standard section component
Read: references/component-library.md (search for "Hero Section")
```

```html
<section class="cta-section" style="background: var(--gray-50); padding: var(--space-3xl) 0;">
    <div class="container" style="text-align: center;">
        <h2 style="color: var(--gray-900); font-size: var(--text-3xl); margin-bottom: var(--space-md);">
            Ready to Get Started?
        </h2>
        <p style="color: var(--gray-600); font-size: var(--text-lg); margin-bottom: var(--space-xl); max-width: 600px; margin-left: auto; margin-right: auto;">
            Submit your samples today and receive detailed, accurate COAs within 3-5 business days.
        </p>
        <div style="display: flex; gap: var(--space-md); justify-content: center; flex-wrap: wrap;">
            <a href="sample-submission.html" class="btn btn-primary">Submit Sample</a>
            <a href="contact.html" class="btn btn-outline">Contact Lab</a>
        </div>
    </div>
</section>
```

**Why this is correct:**
- Uses CSS variables for all styling (`var(--gray-50)`, `var(--space-3xl)`, etc.)
- Follows typography scale (`var(--text-3xl)`, `var(--text-lg)`)
- Uses brand-appropriate CTA language
- Includes primary and secondary CTAs
- Maintains proper spacing system
- Mobile-responsive with flexbox and wrap

### Example 3: Reviewing Existing Code

**User Request:** "Review this button and fix any issues"

**Existing Code:**
```html
<a href="#" style="background: #2563eb; padding: 15px 30px; color: white; border-radius: 8px;">
    Click Here
</a>
```

**Corrected Code:**
```html
<a href="#" class="btn btn-primary">
    Get Started
</a>
```

**Changes Made:**
- ✅ Removed inline styles, using standard button class
- ✅ Now uses CSS variables via `.btn-primary` class
- ✅ Uses proper padding/spacing from design system
- ✅ Improved CTA language ("Get Started" vs "Click Here")
- ✅ Includes hover/focus states automatically
- ✅ Maintains consistency with other buttons

## Troubleshooting

### Issue: Component doesn't look right

**Solution:**
1. Check if all colors use CSS variables
2. Verify spacing uses the spacing system
3. Ensure typography follows the scale
4. Compare with similar components in component-library.md

### Issue: Unclear which component pattern to use

**Solution:**
1. Read component-library.md thoroughly
2. Look for similar existing patterns
3. If no pattern exists, create one following brand guidelines
4. Ensure new pattern fits the existing visual language

### Issue: User wants something that breaks brand guidelines

**Solution:**
1. Explain why the guideline exists
2. Suggest an alternative that maintains consistency
3. If truly necessary, document the exception
4. Consider updating guidelines if it's a valid new pattern

## Maintenance

When updating this skill:

1. **Update brand-guidelines.md** when:
   - New colors are added to the palette
   - Typography system changes
   - New spacing values are introduced
   - Brand voice evolves

2. **Update component-library.md** when:
   - New component patterns are established
   - Existing components are refactored
   - New responsive patterns are developed
   - Accessibility patterns improve

3. **Keep examples current** with actual usage patterns from the site

## Summary

This skill ensures all UI work on ZyntroTest.com maintains:
- Visual consistency through the design system
- Professional, scientific brand identity
- Accessible, mobile-first components
- Efficient development through reusable patterns

Always read the reference documents and apply guidelines proactively to maintain the high quality and consistency of the ZyntroTest brand.
