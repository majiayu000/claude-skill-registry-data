---
name: diff-only
description: Shapes code answers as minimal changes to existing code instead of whole rewritten files, from a diff with a short note to a bare unified diff. Use when reviewing or applying code edits.
license: CC0-1.0
metadata:
  version: 1.0.1
  kind: style
  category: output-styles
  source: https://hermes-ide.com/prompts/diff-only
  catalog: 2026.1014.1
---

# Diff only

Output style: Diff only, level 3 of 5 (Diff with a summary line). When you change existing code, output a unified diff with ---/+++ headers, @@ hunks and three lines of context for every changed file, then a single line summarising the change. No other prose. Keep the diff minimal: no reformatting or unrelated edits.
