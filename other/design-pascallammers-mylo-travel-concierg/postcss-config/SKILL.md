---
name: postcss-config
description: PostCSS configuration template and validation logic for Tailwind CSS processing with Autoprefixer. Includes 4 required standards (required base plugins, critical plugin order with tailwindcss first and autoprefixer last, file naming as postcss.config.js, required dependencies). Use when creating or auditing postcss.config.js files to ensure correct CSS build pipeline.
---

# PostCSS Configuration Skill

This skill provides postcss.config.js template and validation logic for CSS processing configuration.

## Purpose

Manage postcss.config.js configuration to:

- Configure Tailwind CSS processing
- Set up Autoprefixer for browser compatibility
- Ensure consistent CSS build pipeline
- Maintain correct plugin order

## Usage

This skill is invoked by the `postcss-agent` when:

- Creating new postcss.config.js files
- Auditing existing PostCSS configurations
- Validating PostCSS against standards

## Template

The standard PostCSS template is located at:

```
templates/postcss.config.template.js
```

## The 4 PostCSS Standards

### Rule 1: Required Base Plugins

Must include both required plugins:

- `tailwindcss` - Tailwind CSS processing
- `autoprefixer` - Browser prefix automation

### Rule 2: Plugin Order (CRITICAL)

Plugins must be in this exact order:

1. `tailwindcss` - FIRST
2. `autoprefixer` - LAST

✅ **ALWAYS**: Use Tailwind first, Autoprefixer last (reversed order causes CSS processing errors)

### Rule 3: File Naming

Must be named exactly `postcss.config.js`:

- ALWAYS use `.js` extension (not `.ts` or `.mjs`)
- Vite expects `postcss.config.js`

### Rule 4: Required Dependencies

Must have in package.json devDependencies:

```json
{
  "devDependencies": {
    "postcss": "^8.4.0",
    "tailwindcss": "^3.4.0",
    "autoprefixer": "^10.4.0"
  }
}
```

## Validation

To validate a postcss.config.js file:

1. Check that file exists at workspace root
2. Read package.json for dependencies
3. Parse config and check plugin array
4. Verify plugin order (tailwindcss first, autoprefixer last)
5. Check all required dependencies exist
6. Report violations

### Validation Approach

```javascript
// Rule 1: Check required plugins
const hasTailwind = plugins.some(
  (p) => p === "tailwindcss" || p.includes("tailwindcss"),
);
const hasAutoprefixer = plugins.some(
  (p) => p === "autoprefixer" || p.includes("autoprefixer"),
);

// Rule 2: Check plugin order
const tailwindIndex = plugins.findIndex(
  (p) => p === "tailwindcss" || p.includes("tailwindcss"),
);
const autoprefixerIndex = plugins.findIndex(
  (p) => p === "autoprefixer" || p.includes("autoprefixer"),
);

if (tailwindIndex > autoprefixerIndex) {
  errors.push("Rule 2: autoprefixer must be last plugin (after tailwindcss)");
}

// Rule 4: Check dependencies
const deps = packageJson.devDependencies || {};
if (!deps.postcss) errors.push("Rule 4: Missing postcss in devDependencies");
if (!deps.tailwindcss)
  errors.push("Rule 4: Missing tailwindcss in devDependencies");
if (!deps.autoprefixer)
  errors.push("Rule 4: Missing autoprefixer in devDependencies");
```

## Repository Type Considerations

- **Consumer Repos**: Must strictly follow all 4 standards unless exception declared
- **Library Repos**: May have additional plugins for component library needs (e.g., postcss-import)

### Exception Declaration

Consumer repos may declare exceptions in package.json:

```json
{
  "metasaver": {
    "exceptions": {
      "postcss-config": {
        "type": "custom-plugins",
        "reason": "Requires postcss-import for component library structure"
      }
    }
  }
}
```

## Best Practices

1. Place postcss.config.js at workspace root (where package.json is)
2. Use template as starting point
3. Keep plugin order: tailwindcss → autoprefixer
4. Include PostCSS in devDependencies
5. Re-audit after making changes
6. Minimal configuration - only what's needed

## Integration

This skill integrates with:

- Repository type provided via `scope` parameter. If not provided, use `/skill scope-check`
- `/skill audit-workflow` - Bi-directional comparison workflow
- `/skill remediation-options` - Conform/Update/Ignore choices
- `tailwind-agent` - Tailwind CSS configuration coordination
