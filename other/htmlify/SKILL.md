---
name: htmlify
description: |
  Offline HTML rendering of superpowers-gstack Markdown artefacts (design docs,
  handoffs, plans) and per-directory dashboards, in the plugin's house style.
  Prefer the Artifact tool when it is available.
---

# /htmlify

Renders a Markdown artefact to a styled HTML companion, and a dashboard page per
directory. Since 3.0.0 this is the **offline fallback**: when the Artifact tool is
available, publish the artefact as a page with it instead (load the `artifact-design`
skill first) — it is hosted, theme-aware, shareable and supports comments. Reach for
htmlify when there is no Artifact tool, or when the user explicitly asks for a local
HTML file.

`styles/companion.css` is the canonical implementation of the plugin's visual style
(Liquid Glass surfaces, gradient-mesh backgrounds, dual theme). Reuse its tokens when
building an Artifact page for one of these artefacts.

## How to invoke

The skill directory is the "Base directory for this skill" shown when the skill loads.
The wrapper `bin/htmlify` self-locates and runs from any cwd:

```bash
"$SKILL_DIR/bin/htmlify" <path-to-md>            # → <dir>/.superpowers-html/<name>.html
"$SKILL_DIR/bin/htmlify" <path-to-md> --open     # also open it in the default browser (macOS)
"$SKILL_DIR/bin/htmlify" dashboard <dir>         # → <dir>/.superpowers-html/index.html
```

First run per install location: `cd "$SKILL_DIR" && bun install` (the wrapper prints
this exact command and exits 5 if deps are missing; exit 5 also means `bun` is absent).

The open flag opens the file in the user's default browser and touches nothing else.
It never closes windows.

### Flags

- `--plan <plan.json>` — richer layout driven by a rendering plan (see below)
- `--no-clobber` — skip the render if the HTML is newer than the MD
- `--force-rebuild` — render even under `--no-clobber`

## Rendering plan (optional)

Without `--plan` the default template renders the Markdown as structured cards. With a
plan you can map sections to components: `comparison-matrix`, `flowchart-svg`,
`pullquote`, `callout-box`, `stats-bar`, `two-column`, `expandable`, `diff-card`, and a
`feedback_panel` whose answers copy to the clipboard as a prompt for the next session.
Write the plan in this session (no API call), then pass it with `--plan`.

```json
{
  "version": 1,
  "sections": [
    {"heading": "Approaches Considered", "treatment": "comparison-matrix",
     "data": {"items": [{"title": "Option A", "pros": ["…"], "cons": ["…"], "effort": "1d", "risk": "low"},
                        {"title": "Option B", "pros": ["…"], "cons": ["…"], "highlighted": true}]}},
    {"heading": "Architecture", "treatment": "flowchart-svg",
     "data": {"orientation": "LR",
              "nodes": [{"id": "a", "label": "Input"}, {"id": "b", "label": "Process", "emphasis": true}],
              "edges": [{"from": "a", "to": "b", "label": "transform"}]}}
  ],
  "pullquotes": [{"text": "…", "attribution": "…", "after_section": "Problem Statement"}],
  "feedback_panel": {"enabled": true, "premises": ["P1"], "approaches": ["A1"],
                     "custom_questions": [{"id": "q1", "label": "Did this layout help?", "type": "radio", "options": ["yes", "no"]}]}
}
```

| Treatment | Data |
|---|---|
| `comparison-matrix` | `{items: [{title, summary?, pros?, cons?, effort?, risk?, highlighted?}]}` |
| `flowchart-svg` | `{nodes: [{id, label, shape?, emphasis?}], edges: [{from, to, label?}], orientation?: "TB"\|"LR"}` |
| `pullquote` | `{text, attribution?}` |
| `callout-box` | `{level?: "info"\|"warn"\|"insight"\|"danger", title?, body}` |
| `stats-bar` | `{items: [{label, value, delta?, trend?}]}` |
| `two-column` | `{left: {heading?, body}, right: {heading?, body}}` |
| `expandable` | `{summary, body, open?}` |
| `diff-card` | `{title?, before: {label?, content}, after: {label?, content}}` |

Section headings in the plan match the Markdown H2s case- and whitespace-insensitively;
a plan section with no matching H2 renders as a new section.

## Frontmatter types

`type: design-doc` (office-hours), `type: handoff` (context-handoff), `type: plan`
(autoplan); anything else renders through the generic template with a banner.

## Exit codes

0 success · 1 usage error · 2 schema validation failure · 3 Markdown parse error ·
4 I/O error · 5 setup error (bun or deps missing)

## Development

```bash
cd skills/htmlify && bun install && bun test
```
