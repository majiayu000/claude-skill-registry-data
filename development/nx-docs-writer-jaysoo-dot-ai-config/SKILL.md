---
name: nx-docs-writer
description: Documentation writing and editing for nx.dev docs. Use when adding, editing, or polishing documentation, migrating Markdoc to Starlight, debugging content transformations, or fixing documentation site issues. Triggers on "docs", "documentation", "nx.dev", "Markdoc", "Starlight", "astro-docs".
---

# Nx Documentation Writer

## Repository Structure

### nx-dev/ (Next.js Site)
Main documentation site - Next.js with sub-packages:
- `nx-dev/feature-search/` - Algolia search
- `nx-dev/ui-blog/` - Blog components
- `nx-dev/ui-common/` - Shared UI
- `nx-dev/data-access-documents/` - Document processing

### astro-docs/ (Starlight)
Standalone docs using Astro/Starlight framework.

## URL Generation

**Rule**: Lowercase + replace special chars with dashes + remove extension

| File Path | URL |
|-----------|-----|
| `features/CI Features/split-e2e-tasks.mdoc` | `/docs/features/ci-features/split-e2e-tasks` |
| `concepts/mental-model.mdoc` | `/docs/concepts/mental-model` |

## Markdoc Syntax

### Component Names
Use underscores: `side_by_side` NOT `side-by-side`

### JSON in Tags
```markdown
{% graph %}
```json
{"nodes": [...]}
```
{% /graph %}
```
- Use code fences for JSON (never inline with escaped quotes)
- JSON available in `data-code` attribute
- Never escape template blocks: `{% %}` not `\{% %\}`

## Markdoc to Starlight Migration

| Markdoc | Starlight |
|---------|-----------|
| `{% tabs %}...{% /tabs %}` | `#### Tab Label` headers |
| `{% callout type="note" %}` | `:::note` |
| `{% callout type="warning" %}` | `:::caution` |
| `{% callout type="check" %}` | `:::tip` |
| `{% callout type="error" %}` | `:::danger` |
| `{% graph %}` | Remove (not supported) |

**Before transforming**: Validate balanced tags first!

```javascript
const content = fs.readFileSync('file.md', 'utf-8');
const open = (content.match(/\{% tabs %\}/g) || []).length;
const close = (content.match(/\{% \/tabs %\}/g) || []).length;
if (open !== close) console.error(`Unbalanced: ${open} open, ${close} close`);
```

## Frontmatter Rules

- **Frontmatter title = h1** - NEVER duplicate with content h1
- **Sidebar labels** can differ from page title
- **Code blocks are not headings** - `#` in shell scripts isn't markdown h1

## Testing Documentation

### Build & Serve
```bash
nx run PROJECT:build
npx serve dist -p 8000  # Use -p not --port
```

### Verification
```bash
# Check rendered HTML
curl -s http://localhost:8000/path | grep "pattern"

# Clear cache between tests
rm -rf .astro dist

# Find duplicate h1s
grep -r "^#\s" --include="*.md" docs/
```

**Search only works in production builds**, not dev server.

## Common Mistakes

- Don't duplicate theme switcher in mobile menu (Starlight handles it)
- Don't assume all UI elements are in Header.astro
- Don't use `lg:hidden` when you mean `xl:hidden`
- Don't override entire Starlight components for simple style fixes
- Don't assume markdown files are well-formed - validate first
- Don't create complex regex for malformed input - fix the source
- Don't use inline JSON in Markdoc tags with escaped quotes

## Best Practices

- Check what Starlight provides by default FIRST
- Prefer CSS fixes in global.css over component overrides
- Clear Astro cache (`.astro`) when transformations aren't reflecting
- Test individual files with Node scripts before full integration
- After file changes, wait 5-10 seconds for rebuild before verification
- Use `[data-theme='dark']` selector for dark mode styles
- Use Tailwind theme colors `theme('colors.slate.600')` for consistency

## Related Files

When making documentation changes, check:
- `redirect-rules-docs-to-astro.js` - Redirect mappings
- `next.config.js` - Rewrites and redirects
- `map.json` - Routing configuration
