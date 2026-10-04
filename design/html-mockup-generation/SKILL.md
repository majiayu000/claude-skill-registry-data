---
name: html-mockup-generation
description: Guidelines for generating self-contained HTML mockups that look professional and are easy to iterate on.
---
# HTML Mockup Generation

Guidelines for generating self-contained HTML mockups that look professional and are easy to iterate on.

## Return contract (read first)

When this skill runs inside a subagent (the usual case via `ui-designer` or `/mock`), the subagent's narrative return text is **not shown directly to the user** — the orchestrator surfaces a parseable file list. The last thing the subagent emits MUST be a `<MOCKUP_FILES>` block listing every file written:

```
<MOCKUP_FILES>
.hero/mocks/{slug}/index.html|{Mockup name}|primary
.hero/planning/features/{slug}/spec.md|Spec (Mockups section updated)|spec
</MOCKUP_FILES>
```

One file per line, pipe-separated `path|label|kind`. Include every variant when generating multiple options in one run. Skip this block and the user sees no links. See the `ui-designer` agent definition for full rules.

## When to use

Selection is now driven by `hero spec mock detect` (see `hero spec mock detect --help`). The agent does not decide — the CLI does. This skill is loaded whenever the detect output's `renderer` field is `"html"`, which fires when no Swift signals are detected, when `--renderer=html` was explicit, when `hero.json` `mockups.renderer: "html"` overrides auto-detect, or as a fallback when Swift signals are present but `swiftc` is missing.

## File Structure

```html
<!DOCTYPE html>
<!-- Hero Mock: {slug} | Generated: {date} -->
<!-- Description: {one-line description} -->
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{Title} — Mock</title>
    <style>
        /* All CSS here — no external stylesheets */
    </style>
</head>
<body>
    <!-- All markup here -->
    <script>
        /* All JS here — no external scripts */
    </script>
</body>
</html>
```

## CSS Design System

Use these as defaults. Adjust per-project if the team has brand guidelines.

### Colors
```css
:root {
    --bg: #ffffff;
    --bg-secondary: #f8f9fa;
    --bg-tertiary: #e9ecef;
    --text: #212529;
    --text-secondary: #6c757d;
    --text-muted: #adb5bd;
    --border: #dee2e6;
    --primary: #4a9eff;
    --primary-hover: #3a8eef;
    --success: #28a745;
    --warning: #ffc107;
    --danger: #dc3545;
    --info: #17a2b8;
    --shadow: 0 1px 3px rgba(0,0,0,0.1);
    --shadow-lg: 0 4px 12px rgba(0,0,0,0.15);
    --radius: 6px;
    --radius-lg: 12px;
}
```

### Typography
```css
body {
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    font-size: 14px;
    line-height: 1.5;
    color: var(--text);
    background: var(--bg);
    margin: 0;
    padding: 0;
}

h1 { font-size: 24px; font-weight: 600; margin: 0 0 16px; }
h2 { font-size: 18px; font-weight: 600; margin: 0 0 12px; }
h3 { font-size: 16px; font-weight: 600; margin: 0 0 8px; }
```

### Spacing
Use multiples of 4px: 4, 8, 12, 16, 24, 32, 48, 64.

### Common Components

**Buttons:**
```css
.btn {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    padding: 8px 16px;
    border-radius: var(--radius);
    font-size: 14px;
    font-weight: 500;
    border: 1px solid var(--border);
    background: var(--bg);
    color: var(--text);
    cursor: pointer;
    transition: all 0.15s ease;
}
.btn-primary {
    background: var(--primary);
    color: white;
    border-color: var(--primary);
}
.btn-primary:hover { background: var(--primary-hover); }
.btn-danger { background: var(--danger); color: white; border-color: var(--danger); }
```

**Cards:**
```css
.card {
    background: var(--bg);
    border: 1px solid var(--border);
    border-radius: var(--radius-lg);
    padding: 24px;
    box-shadow: var(--shadow);
}
```

**Tables:**
```css
table { width: 100%; border-collapse: collapse; }
th, td { padding: 12px 16px; text-align: left; border-bottom: 1px solid var(--border); }
th { font-weight: 600; color: var(--text-secondary); font-size: 12px; text-transform: uppercase; letter-spacing: 0.5px; }
tr:hover { background: var(--bg-secondary); }
```

**Forms:**
```css
.form-group { margin-bottom: 16px; }
.form-label { display: block; font-weight: 500; margin-bottom: 4px; font-size: 13px; }
.form-input {
    width: 100%;
    padding: 8px 12px;
    border: 1px solid var(--border);
    border-radius: var(--radius);
    font-size: 14px;
    box-sizing: border-box;
}
.form-input:focus { outline: none; border-color: var(--primary); box-shadow: 0 0 0 3px rgba(74,158,255,0.15); }
```

**Badges/Tags:**
```css
.badge {
    display: inline-block;
    padding: 2px 8px;
    border-radius: 12px;
    font-size: 12px;
    font-weight: 500;
}
.badge-success { background: #d4edda; color: #155724; }
.badge-warning { background: #fff3cd; color: #856404; }
.badge-danger { background: #f8d7da; color: #721c24; }
.badge-info { background: #d1ecf1; color: #0c5460; }
```

## Layout Patterns

### App Shell (sidebar + content)
```html
<div style="display: flex; min-height: 100vh;">
    <nav style="width: 240px; background: var(--bg-secondary); border-right: 1px solid var(--border); padding: 24px 16px;">
        <!-- sidebar nav -->
    </nav>
    <main style="flex: 1; padding: 32px;">
        <!-- main content -->
    </main>
</div>
```

### Dashboard Grid
```html
<div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 24px;">
    <div class="card"><!-- metric card --></div>
    <div class="card"><!-- metric card --></div>
    <div class="card"><!-- metric card --></div>
</div>
```

### Header with Actions
```html
<div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 24px;">
    <div>
        <h1>Page Title</h1>
        <p style="color: var(--text-secondary); margin: 0;">Brief description</p>
    </div>
    <div style="display: flex; gap: 8px;">
        <button class="btn">Secondary</button>
        <button class="btn btn-primary">Primary Action</button>
    </div>
</div>
```

## Interactivity Patterns

Keep JS minimal. Common patterns:

**Tab switching:**
```javascript
document.querySelectorAll('[data-tab]').forEach(tab => {
    tab.addEventListener('click', () => {
        document.querySelectorAll('[data-tab]').forEach(t => t.classList.remove('active'));
        document.querySelectorAll('[data-panel]').forEach(p => p.style.display = 'none');
        tab.classList.add('active');
        document.querySelector(`[data-panel="${tab.dataset.tab}"]`).style.display = 'block';
    });
});
```

**Modal toggle:**
```javascript
function toggleModal(id) {
    const modal = document.getElementById(id);
    modal.style.display = modal.style.display === 'flex' ? 'none' : 'flex';
}
```

**Dropdown:**
```javascript
function toggleDropdown(id) {
    const dd = document.getElementById(id);
    dd.style.display = dd.style.display === 'block' ? 'none' : 'block';
}
document.addEventListener('click', (e) => {
    if (!e.target.closest('.dropdown')) {
        document.querySelectorAll('.dropdown-menu').forEach(d => d.style.display = 'none');
    }
});
```

## Realistic Data

Use realistic-looking placeholder data:

- Names: "Sarah Chen", "Marcus Johnson", "Aisha Patel" (diverse, realistic)
- Emails: "sarah.chen@example.com"
- Dates: Use relative dates ("2 hours ago", "Yesterday", "Mar 15")
- Numbers: Use realistic ranges (not round numbers — "$12,847" not "$10,000")
- Status values: Use the actual statuses from the spec if available

## What NOT to Do

- Don't use CDN links or external resources
- Don't use Lorem Ipsum — write realistic placeholder text
- Don't use icon fonts — use simple inline SVG or Unicode characters (▶ ● ✓ ✕ ⋯ ↓ →)
- Don't add complex animations
- Don't use canvas or WebGL
- Don't make it pixel-perfect — it's a prototype for discussion, not production code
- Don't include more than 2-3 screens in one file — keep it focused

## Spec write-back

When invoked against a spec slug (not free-text), after saving the mockup, link it back from the originating spec so delivery agents can find it.

1. Locate the spec. Try in order:
   - `.hero/planning/features/{slug}/spec.md`
   - `.hero/planning/bugs/{slug}/spec.md`
   - `.hero/specs/{slug}/spec.md` (archive fallback)
2. If a `## Mockups` section does not exist, append one near the end of the spec body. Place it before `## Validation` if that section exists; otherwise at the end of the file.
3. Add an entry in this format:

   ```markdown
   - [{Mockup name}](.hero/mocks/{slug}/index.html) — YYYY-MM-DD — one-line description of what the mockup shows
   ```

   - Default the name to a humanized slug (e.g. `Hero landing page`). Use something more specific when the spec has multiple mockups or iteration variants (e.g. `Hero landing page — dense variant`).
   - Use today's date in ISO format.
   - Keep the description to one line — what's shown, not why.

### Iteration semantics

On `--iterate`, match the existing entry by path. If the path is unchanged (the common case — overwriting `index.html`), update the date in place and rewrite the description only if the iteration meaningfully changed what's depicted. Don't append a duplicate row. If the iteration produces a new file (e.g. `dense.html` alongside `index.html`), append a new entry instead.

### Free-text exception

When `/mock` is invoked with free-text rather than a spec slug, there is no spec to write back to. Save the mockup under `.hero/mocks/_adhoc/{kebab-case-summary}/index.html` and skip the write-back step entirely. This keeps the `.hero/mocks/` root clean — slug-keyed dirs match real specs; `_adhoc/` clearly doesn't.
