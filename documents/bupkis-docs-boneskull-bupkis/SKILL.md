---
name: bupkis-docs
description: How to create & maintain TypeDoc site documentation and the README for Bupkis
metadata:
  category: documentation
---

# Bupkis Documentation

## Overview

This skill provides guidance for creating and maintaining the Bupkis documentation site, which uses TypeDoc with custom plugins for automated redirect generation and media file management.

## When to Use

Invoke this skill when:

- Updating the TypeDoc site documentation
- Modifying README.md structure or content
- Adding new assertion implementations that need documentation
- Building or validating the documentation site
- Fixing documentation build issues
- Working with custom JSDoc tags (`@bupkisAnchor`, `@bupkisAssertionCategory`, `@bupkisRedirect`)

## Important: Do Not Edit

**CHANGELOG.md is auto-generated** from commit messages and should never be manually edited. All changelog updates happen automatically during release.

## Architecture Overview

**Key Components:**

- **TypeDoc** - API documentation generator
- **Custom Plugin** (`.config/typedoc-plugin-bupkis.js`) - Handles media files and dynamic redirects
- **Site Structure** (`site/`) - Hand-written documentation pages
- **Assertion Implementations** (`src/assertion/impl/`) - Source code with JSDoc tags
- **Generated Output** (`docs/`) - Built site (ignored by git)

## Building Documentation

**Build Command:**

```bash
npm run docs:build
```

This runs TypeDoc with the strict configuration and generates the full documentation site in `docs/`.

## Custom JSDoc Tags System

Bupkis uses three custom JSDoc block tags to generate redirects for assertion documentation:

### `@bupkisAnchor`

**Purpose:** Specifies the anchor ID in the generated documentation page.

**Format:** `@bupkisAnchor <anchor-id>`

**Example:**

```typescript
/**
 * @bupkisAnchor unknown-to-be-a-string
 */
```

This creates an anchor like `#unknown-to-be-a-string` in the generated docs.

### `@bupkisAssertionCategory`

**Purpose:** Maps the assertion to a documentation category/document.

**Valid Categories:**

- `primitives` → `Primitive_Assertions`
- `strings` → `String___Pattern_Assertions`
- `numeric` → `Numeric_Assertions`
- `equality` → `Equality___Comparison_Assertions`
- `collections` → `Collections_Assertions`
- `object` → `Object_Assertions`
- `function` → `Function_Assertions`
- `error` → `Error_Assertions`
- `date` → `Date___Time_Assertions`
- `promise` / `async` → `Promise_Assertions`
- `snapshot` → `Snapshot_Assertions`
- `other` → `Other_Assertions`

**Example:**

```typescript
/**
 * @bupkisAssertionCategory primitives
 */
```

### `@bupkisRedirect`

**Purpose:** (Optional) Provides a custom redirect path when it differs from the anchor.

**Format:** `@bupkisRedirect <custom-path>`

**Example:**

```typescript
/**
 * @bupkisAnchor function-to-throw-any
 * @bupkisAssertionCategory function
 * @bupkisRedirect to-throw
 */
```

This creates a redirect from `assertions/to-throw/` → `documents/Function_Assertions#function-to-throw-any`.

## How Redirects Work

The custom plugin (`.config/typedoc-plugin-bupkis.js`):

1. **Listens** to `Converter.EVENT_CREATE_DECLARATION` during TypeDoc processing
2. **Inspects** JSDoc block tags on variable declarations with assertion types
3. **Validates** that the category exists in `CATEGORY_DOC_MAP`
4. **Registers** redirects using `typedoc-plugin-redirect`
5. **Format:** `assertions/<redirect-name>/` → `documents/<Category_Document>#<anchor>`

**Example Flow:**

```typescript
// In src/assertion/impl/sync-basic.ts
/**
 * @bupkisAnchor unknown-to-be-a-string
 * @bupkisAssertionCategory primitives
 */
export const stringAssertion = ...
```

**Generated Redirect:**

- Path: `assertions/unknown-to-be-a-string/`
- Target: `documents/Primitive_Assertions#unknown-to-be-a-string`

## Updating Assertion Documentation

When adding or modifying assertions in `src/assertion/impl/`:

**Required Steps:**

1. Add JSDoc comment with `@bupkisAnchor` and `@bupkisAssertionCategory`
2. Verify the category matches one of the valid categories
3. (Optional) Add `@bupkisRedirect` if the URL path should differ from the anchor
4. Run `npm run docs:build` to regenerate docs
5. Check build output for redirect registration logs
6. Verify the redirect works in the generated site

**Validation:**

- Plugin logs: `Registered redirect for <name>: <path> ➡️ <target>`
- Warning for unknown categories: `Unknown category "<category>" for assertion <name>`

## Testing Documentation

**Validate Redirects:**

After adding or modifying assertions, validate that redirects work correctly:

```bash
node .claude/skills/bupkis-docs/scripts/validate-redirects.js --build
```

This script:

1. Builds the documentation
2. Parses build logs to extract registered redirects
3. Validates redirect structure and format
4. Reports any invalid redirects

**What it checks:**

- ✓ Redirect paths start with `assertions/`
- ✓ Document paths start with `documents/`
- ✓ Anchors are present when using `#` syntax
- ✓ All registered redirects follow expected format

**Integration with Playwright:**

The script is designed to work with Claude Code's Playwright MCP server for end-to-end testing. When invoked by Claude, it can:

- Serve documentation locally
- Navigate to redirect URLs
- Verify redirects resolve to correct target pages
- Check that anchors exist on target pages

**See:** `references/testing-redirects.md` for complete testing guide.

## Site Structure

**Hand-Written Content** (`site/`):

```
site/
├── about/          - About pages
├── assertions/     - Assertion documentation
├── guide/          - User guides
├── media/          - Images, logos (copied to docs/media/)
└── reference/      - Reference documentation
```

**Generated Output** (`docs/` - gitignored):

```
docs/
├── assets/         - TypeDoc-generated CSS/JS
├── documents/      - Generated API documentation
├── media/          - Copied from site/media/
└── [other pages]   - Generated HTML pages
```

## Media Files

The plugin automatically copies all files from `site/media/` to `docs/media/` after rendering completes.

**Log Output:**

```
Will copy all files in site/media/ to docs/media/
Copied site/media/logo.png to docs/media/logo.png
```

## Troubleshooting

**Problem:** Redirect not generated

- **Check:** JSDoc tags are present and correctly formatted
- **Check:** Category name matches `CATEGORY_DOC_MAP` entries
- **Check:** Variable is exported and has an assertion type
- **Review:** Build logs for warnings about unknown categories

**Problem:** Build fails

- **Check:** Run `npm run docs:build` for detailed error output
- **Check:** TypeDoc configuration in `typedoc.json` or package.json
- **Check:** Plugin is loaded correctly in TypeDoc config

**Problem:** Media files not copied

- **Check:** Files exist in `site/media/`
- **Check:** Build completed successfully (copy happens at `RendererEvent.END`)
- **Review:** Build logs for copy confirmation messages

## Bundled Resources

**scripts/** - Automation utilities for documentation tasks

- `validate-redirects.js` - Validates documentation redirects by testing structure and optionally using Playwright

**references/** - Detailed reference documentation

- `jsdoc-tags.md` - Complete reference for custom JSDoc tags
- `build-process.md` - Documentation build process guide
- `testing-redirects.md` - Guide for testing redirects (see below)
- `README.md` - Index of available references

## Examples

```
User: "Add documentation for the new isEmpty assertion"
Claude: I'll help you add the JSDoc tags for documentation. Based on the assertion
        implementation, I'll add:
        - @bupkisAnchor array-to-be-empty
        - @bupkisAssertionCategory collections
        Then rebuild the docs to verify the redirect is registered correctly.
```

```
User: "The redirect for 'to throw' isn't working"
Claude: Let me check the JSDoc tags in the assertion implementation. I'll verify:
        1. The @bupkisRedirect tag is set to "to-throw"
        2. The @bupkisAnchor matches the expected anchor
        3. The category is valid in CATEGORY_DOC_MAP
        Then rebuild and check the logs for redirect registration.
```

```
User: "Update the README to add the new feature section"
Claude: I'll update README.md following the existing structure. After making changes,
        I'll run `npm run docs:build` to ensure the documentation site builds correctly
        with the updated content.
```
