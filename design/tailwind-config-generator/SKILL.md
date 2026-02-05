---
name: tailwind-config-generator
description: Generate Tailwind CSS configuration files with custom themes, plugins, and content paths. Triggers on "create tailwind config", "generate tailwind configuration", "tailwind setup", "tailwindcss config".
---

# Tailwind Config Generator

Generate Tailwind CSS configuration files with custom themes, colors, and plugins.

## Output Requirements

**File Output:** `tailwind.config.js` or `tailwind.config.ts`
**Format:** Valid Tailwind CSS configuration
**Standards:** Tailwind CSS 3.x

## When Invoked

Immediately generate a complete Tailwind configuration with content paths, theme customizations, and plugins.

## Configuration Template

```javascript
/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ['./src/**/*.{js,ts,jsx,tsx}'],
  theme: {
    extend: {
      colors: {
        primary: '#3b82f6',
      },
    },
  },
  plugins: [],
};
```

## Example Invocations

**Prompt:** "Create tailwind config with custom color palette"
**Output:** Complete `tailwind.config.js` with extended theme.
