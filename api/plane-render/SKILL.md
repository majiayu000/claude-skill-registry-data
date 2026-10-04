---
name: plane-render
description: >
  Generate properly formatted HTML for Plane issues, comments, sprint reports,
  and pages. Plane requires HTML — plain text creates unformatted walls of text.
  Use this skill whenever writing content that goes into Plane via the API:
  issue descriptions, progress comments, sprint cycle reports, architecture pages.
  Triggers on: "write to plane", "create plane issue", "plane description",
  "plane comment", "sprint report", "plane page", "plane html", "render for plane".
---

# Plane Content Renderer

Plane's API accepts and renders HTML. Always produce HTML — never plain text.

## Supported Templates

Four content types. Load the matching reference file before writing:

| Content Type | When | Reference |
|---|---|---|
| Issue description | Creating a new Plane issue | `references/issue-description.md` |
| Comment | Progress, review, decision updates on a Plane issue | `references/comment.md` |
| Sprint report | End-of-cycle summary posted to a Plane cycle | `references/sprint-report.md` |
| Page | Architecture docs, requirements, ADRs in Plane pages | `references/page.md` |

## Core Rules

1. **All output is HTML.** Wrap every content block in valid HTML tags.
2. **No raw Markdown.** Plane does not render Markdown — it renders HTML.
3. **Keep it scannable.** Use `<h2>`, `<h3>`, `<ul>`, `<table>` to structure; avoid long `<p>` walls.
4. **Links must be `<a href="...">`.** Plane does not parse bare URLs.
5. **Code goes in `<pre><code>`.** Inline code uses `<code>`.
6. **Bold emphasis: `<strong>`.** Italic: `<em>`.

## Quick Reference — Common HTML Patterns

```html
<!-- Section heading -->
<h2>Context</h2>

<!-- Bullet list -->
<ul>
  <li>Item one</li>
  <li>Item two</li>
</ul>

<!-- Numbered list -->
<ol>
  <li>First step</li>
  <li>Second step</li>
</ol>

<!-- Link -->
<a href="https://example.com">Label</a>

<!-- Code block -->
<pre><code>some_command --flag value</code></pre>

<!-- Inline code -->
<code>variable_name</code>

<!-- Table -->
<table>
  <thead><tr><th>Column A</th><th>Column B</th></tr></thead>
  <tbody>
    <tr><td>Value 1</td><td>Value 2</td></tr>
  </tbody>
</table>

<!-- Horizontal rule (section separator) -->
<hr>

<!-- Agent footer -->
<p><sub>{agent_name} · <a href="{task_url}">{task_short_id}</a></sub></p>
```

## How to Use

1. Identify the content type needed.
2. Read the matching reference file from `references/`.
3. Fill the template placeholders (all `{placeholder}` style).
4. Deliver the HTML string as the `description`, `comment`, or `body` field in your API call.

## API Field Mapping

| Plane surface | API field | Endpoint |
|---|---|---|
| Issue description | `description_html` | `POST /api/v1/issues/` |
| Issue comment | `comment_html` | `POST /api/v1/issues/{id}/comments/` |
| Cycle (sprint) description | `description_html` | `PATCH /api/v1/cycles/{id}/` |
| Page content | `description_html` | `POST /api/v1/pages/` |

> Exact endpoints vary by Plane version; confirm against local `api/openapi.json` when in doubt.
