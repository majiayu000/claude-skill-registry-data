---
name: markdown-authoring
description: Markdown style patterns to use when writing documents.
---

When writing Markdown files:

* **Start with an H1 as the first heading.**
  The first heading in the file should be a top-level `# Heading` (not `##` or deeper).

* **Use ATX headings only.**
  Headings must use leading `#` characters (`#`, `##`, `###`, …), not Setext (`Heading` + `====`).

* **Unordered list marker is flexible.**
  You may use `-`, `*`, or `+` for bullet lists (no enforcement).

* **Indent nested unordered lists by 2 spaces.**
  When a list item contains a nested list, indent the nested list by **2 spaces**.

* **Blank lines are allowed more freely.**
  Extra consecutive blank lines are permitted (no “single blank line only” restriction).

* **Line length limit is effectively very high; but follow sembr**
  For prose, follow the Semantic Line Breaks convention,
  described in `<path-to-skill>/reference/sembr.md`.
  Table rows are **not** checked for line length.

* **Headings must be surrounded by blank lines.**
  Put a blank line **before and after** each heading (where applicable).

* **Duplicate headings are allowed.**
  Reusing the same heading text in multiple places is acceptable.

* **Lists must be surrounded by blank lines.**
  Put a blank line **before** a list and a blank line **after** a list.

* **Inline HTML is allowed.**
  HTML (like `<br>`, `<details>`, etc.) is permitted in Markdown.

* **Add Table of Contents.**
  If there are more than 4 sections, add a table of contents by adding this (if not already present):

```markdown

## Contents

<!-- toc -->
<!-- tocstop -->

```

- Run command `just -g toc [path-to-file.md]` when complete. The just recipe is configured with `[no-cd]`, so `markdown-toc` will run from the working directory you call the just command with.
