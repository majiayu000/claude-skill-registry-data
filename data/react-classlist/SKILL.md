---
name: react-classlist
description: Organize long or disorganized className attributes in React components into semantic groups using cn() or className
---

# React ClassName Organizer

Organize className attributes in React components for readability and maintainability.

## When to trigger

Refactor className when:
1. Single-line className exceeds 80-100 characters
2. Disorganized `cn()` or `classList()` calls exist
3. User explicitly requests className organization

## Instructions

1. **Choose utility function:**
   - Use `cn()` if already imported in the file
   - Otherwise, use standard `className`

2. **Break into multiple lines:**
   - Each line should be semantically grouped
   - Lines should not exceed ~80 characters
   - Keep responsive modifiers with their base class

3. **Group classes in this order:**
   - Layout (flex, grid, position type)
   - Spacing (gap, padding, margin)
   - Sizing (width, height, min/max)
   - Display & visibility
   - Typography (font, text-*)
   - Colors & backgrounds
   - Borders & effects
   - Positioning values (top, left, z-index)
   - Transitions & animations
   - Responsive variants (keep with base class)

4. **Format:**
   ```jsx
   // Before:
   className="overflow-y-auto max-h-[50vh] md:max-h-auto flex-col gap-4 md:gap-2 pt-2 w-full md:w-auto"

   // After:
   className=cn(
     'flex-col gap-4 md:gap-2 pt-2',
     'w-full md:w-auto max-h-[50vh] md:max-h-auto',
     'overflow-y-auto scrollbar-hide'
   )
   ```

5. **Keep together:**
   - Responsive modifiers with base: `'w-full md:w-auto'`
   - Related utilities: `'flex items-center justify-between'`

## Tool access
allowed-tools:
  - Read
  - Edit
  - Grep

## Notes
- Preserve all existing classes
- Maintain semantic grouping over strict alphabetical order
- Each line should be readable and cohesive
