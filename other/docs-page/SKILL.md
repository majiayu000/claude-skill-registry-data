---
name: docs-page
description: |
  Technical documentation page with sidebar navigation, search, code blocks,
  and table of contents. Use for "docs", "documentation", "API docs", "guide".
triggers:
  - "docs"
  - "documentation"
  - "api docs"
  - "guide"
  - "readme"
  - "reference"
df:
  mode: prototype
  platform: desktop
  scenario: content
  preview:
    type: html
    entry: index.html
  design_system:
    requires: true
---

# Docs Page Skill

Produce a documentation page with navigation and content.

## Layout
- **Left sidebar** (260px, sticky): logo, search input, nav tree with
  expandable sections. Active page highlighted with accent.
- **Main content**: max-width 75ch.
  - Breadcrumb at top.
  - Title + last-updated badge.
  - Body with heading anchors.
  - Code blocks with copy button (no JS — use `user-select: all` + hint).
  - Tables, callout boxes (info/warning/tip), inline code.
- **Right TOC** (200px, sticky): auto-generated from H2/H3 headings.

## Rules
- Sidebar scrolls independently from content.
- Code blocks: dark theme, syntax tokens via CSS classes.
- Callouts: left border + icon prefix.
- `data-df-id` on each section heading.
- Responsive: sidebar collapses to hamburger below 1024px.

## Output
Single `index.html`, inline CSS.
