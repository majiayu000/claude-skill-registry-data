---
name: tailwind-config-conformance
description: |
  Validate and refactor Tailwind CSS classes to conform with project's tailwind.config definitions.
  Use this skill whenever: agents or developers generate Tailwind classes without checking the config file;
  you need to enforce consistency with custom theme extensions;
  you want to replace arbitrary or ad-hoc classes with officially configured alternatives;
  you're reviewing code and need to ensure all utility classes match the tailwind.config (colors, spacing, typography, etc.);
  you want to migrate code to use only valid config-defined classes instead of free-form utilities.
  Works with React, Vue, HTML, Svelte, and any code containing Tailwind classes. Automatically discovers tailwind.config.js/ts
  and validates against both built-in Tailwind defaults and custom extensions defined in the config.
metadata:
  author: Ronnasayd Machado - github.com/Ronnasayd
  version: "1.0.0"
---

# Tailwind Config Conformance Validator

## Overview

This skill validates and refactors code to use only Tailwind classes that are explicitly defined in your project's `tailwind.config.js` or `tailwind.config.ts` file.

**The problem it solves:**

- Agents generate classes like `text-red-650`, `p-7.5`, `w-full-minus-1` without checking if they're in your config
- Developers use arbitrary values (`w-[100px]`) when a configured value exists
- Custom theme extensions aren't being utilized, leading to inconsistent styling
- Code review becomes tedious — manually checking which classes actually exist in config

**The outcome:**

- All Tailwind classes are validated against your actual config
- Invalid classes are replaced with valid alternatives from your config
- A summary report shows exactly what changed and why
- Your codebase stays consistent with your design system

---

## How It Works

### Step 1: Understand the Input

You provide:

1. **Code to validate** — Any file containing Tailwind classes (React, Vue, HTML, Svelte, etc.)
2. **Optionally, the config file path** — If not provided, the skill auto-discovers `tailwind.config.js` or `tailwind.config.ts`

### Step 2: Parse Config

The skill reads your `tailwind.config.js/ts` and extracts:

- **Theme values**: colors, spacing, typography, sizing, etc.
- **Extended values**: anything defined under `theme.extend`
- **Corepack values**: all Tailwind built-in defaults (spacings, colors, breakpoints, etc.)

### Step 3: Validate Classes

For each Tailwind class in your code, the skill:

1. **Parses the structure**: `text-red-600` → `text` (utility) + `red-600` (modifier value)
2. **Checks config**: Is `red-600` defined in your config theme?
3. **Accepts valid patterns**:
   - Responsive prefixes: `md:text-red-600`, `lg:p-4`
   - Dark mode variants: `dark:bg-gray-900`
   - State variants: `hover:text-red-600`, `focus:bg-blue-500`
   - Arbitrary values: `w-[100px]` (with caveat — see edge cases)
4. **Flags violations**: Classes not found in config are marked for replacement

### Step 4: Suggest Replacements

When a class doesn't match config, the skill:

1. Finds the **closest valid alternative** from your config (same utility family, nearest value)
2. Suggest the replacement with reasoning ("used `p-7.5` but config only has `p-8`")
3. Applies replacements to the code

### Step 5: Generate Report

Output includes:

- **Refactored code** — All invalid classes replaced
- **Change summary** — List of all replacements with reasons
- **Config violations** — Classes that were invalid and how they were fixed

---

## Input Format

Provide your code and, optionally, the config file path.

**Example 1 (auto-discover config):**

```
Please validate this React component against our Tailwind config:

<code>
  <div className="p-7.5 text-red-650 w-[200px] md:grid-cols-12 dark:bg-navy-new">
    Content
  </div>
</code>
```

**Example 2 (explicit config path):**

```
Validate this with config at apps/web/tailwind.config.ts:

<code>
  <button className="px-custom-lg py-2 bg-primary hover:bg-primary-dark">
    Click me
  </button>
</code>
```

---

## Output Format

ALWAYS use this exact structure:

### Refactored Code

```[language]
[code with all invalid classes replaced with valid ones from config]
```

### Change Summary

| Original Class | Reason                                                                         | Suggested Class               |
| -------------- | ------------------------------------------------------------------------------ | ----------------------------- |
| `p-7.5`        | Not in config. Config has `p-8` and `p-6`. Used `p-8`.                         | `p-8`                         |
| `text-red-650` | Not in config. Config defines `text-red-600` and `text-red-700`. Used closest. | `text-red-600`                |
| `grid-cols-12` | Not in config. Standard Tailwind max is `grid-cols-12` but check if extended.  | ⚠️ Recommend extending config |

### Config Validation Report

- **Config file found**: `tailwind.config.ts` (root)
- **Total classes validated**: 15
- **Valid classes**: 12
- **Invalid classes**: 3
- **All violations fixed**: ✅ Yes

---

## Edge Cases Handled

### 1. Arbitrary Values

Arbitrary values like `w-[100px]` are allowed but flagged:

- ✅ Allowed if there's a legitimate reason (truly custom, not covered by config)
- ⚠️ Flagged if a similar config value exists (e.g., if config has `w-96`, don't use `w-[100px]`)

### 2. Responsive & Dark Mode Variants

All of these are validated:

- `md:p-4` → validates `p-4`, ignores `md:` prefix
- `dark:bg-gray-900` → validates `bg-gray-900`, ignores `dark:` prefix
- `hover:text-red-600` → validates `text-red-600`, ignores `hover:` prefix
- Combinations: `lg:dark:hover:text-red-600` → validates `text-red-600` only

### 3. CSS-in-JS & Object Syntax

Handles multiple formats:

- JSX className strings: `className="p-4 text-red-600"`
- Tailwind function calls: `import { cn } from '@/utils'; cn('p-4', { 'text-red-600': isActive })`
- CSS modules with Tailwind: `@apply p-4 text-red-600;`
- Tailwind directives in CSS: `@layer components { .btn { @apply px-4 py-2; } }`

### 4. Plugins & Presets

If your config uses plugins (e.g., `@tailwindcss/forms`, `daisyui`), the skill:

- Notes the plugin in the report
- Validates core classes and plugin-provided utilities separately
- Flags any conflicts between plugin utilities and core Tailwind

---

## Important Notes

### Arbitrary Values Policy

- **Allowed**: `w-[200px]` if no config spacing covers this exact need
- **Discouraged**: `w-[96px]` when config already has `w-96`
- **Recommendation**: If frequently needed, extend `tailwind.config.ts` instead

### Config Extensions

This skill validates against your config **as-is**. If you find patterns that are missing:

- Note them in the report
- Consider extending your `tailwind.config.ts`
- Re-run the skill after extending config

### Responsive Breakpoints

The skill uses breakpoints from your config:

- Standard: `sm`, `md`, `lg`, `xl`, `2xl`
- Custom breakpoints: validated from your `theme.screens` config

### Dark Mode

Validates `dark:` prefix if:

- `darkMode: 'class'` is set in your config (most common)
- Dark mode is enabled in your config

---

## Walkthrough Example

**Input Code:**

```jsx
export function Card({ isActive }) {
  return (
    <div className="p-7.5 rounded-2xl bg-gradient-blue shadow-lg">
      <h2 className="text-xl font-bold text-navy-new">Title</h2>
      <p className="text-sm text-gray-500 mt-12 md:mt-6">Description</p>
      <button className="px-custom-lg py-2 bg-primary hover:bg-primary-dark">
        Action
      </button>
    </div>
  );
}
```

**Config (tailwind.config.ts):**

```ts
export default {
  theme: {
    extend: {
      colors: {
        primary: "#007AFF",
        "primary-dark": "#0051D5"
      },
      spacing: {
        "custom-lg": "18px"
      }
    }
  }
};
```

**Output:**

Refactored Code:

```jsx
export function Card({ isActive }) {
  return (
    <div className="p-8 rounded-xl bg-blue-500 shadow-lg">
      <h2 className="text-xl font-bold text-slate-900">Title</h2>
      <p className="text-sm text-gray-500 mt-10 md:mt-6">Description</p>
      <button className="px-custom-lg py-2 bg-primary hover:bg-primary-dark">
        Action
      </button>
    </div>
  );
}
```

Change Summary:

| Original                | Reason                                                   | Replacement             |
| ----------------------- | -------------------------------------------------------- | ----------------------- |
| `p-7.5`                 | Not in config. Used `p-8` (closest).                     | `p-8`                   |
| `rounded-2xl`           | Not in config. Max is `rounded-xl`.                      | `rounded-xl`            |
| `bg-gradient-blue`      | Not in config. No matching gradient. Used `bg-blue-500`. | `bg-blue-500`           |
| `text-navy-new`         | Not in config. Used `text-slate-900` (dark neutral).     | `text-slate-900`        |
| `mt-12`                 | Not in config. Max is `mt-10`.                           | `mt-10`                 |
| `px-custom-lg`          | ✅ In config (extended). Kept as-is.                     | `px-custom-lg`          |
| `py-2`                  | ✅ Valid Tailwind. Kept as-is.                           | `py-2`                  |
| `bg-primary`            | ✅ In config (extended). Kept as-is.                     | `bg-primary`            |
| `hover:bg-primary-dark` | ✅ Valid. Kept as-is.                                    | `hover:bg-primary-dark` |

---

## When NOT to Use This Skill

- **Intentional arbitrary values**: If you're deliberately using `w-[calc(100%-10px)]` for a specific calculation, explain that and the skill will preserve it with a note.
- **Not a Tailwind project**: This skill is Tailwind-specific. Regular CSS projects need different validation.
- **No config file**: If your project doesn't have a `tailwind.config.js/ts`, this skill can't validate. Set one up first.

---

## Tips for Best Results

1. **Provide the config path** if it's not in the standard location (root or `src/`). E.g., `apps/web/tailwind.config.ts`
2. **Include context** if your code uses custom utilities from plugins. E.g., `This project uses @tailwindcss/forms`
3. **Review the summary** before applying changes — the suggestions are smart but your intent is the source of truth
4. **Extend config strategically** — if the skill frequently suggests the same replacements, consider extending your `tailwind.config.ts` to include those values
