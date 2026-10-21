---
name: ui-ux-pro-max
description: Search local UI and UX guidance for styles, palettes, typography, charts, accessibility, and framework patterns. Use for design research or a new design-system draft.
license: MIT; see LICENSE
compatibility: Python 3; standard library only
---

# UI/UX Pro Max for Pi

Read the project's design system, tokens, shared components, and dependencies before searching.
Use existing design decisions as constraints. Search results supply candidates for judgment.

## Run a focused search

Resolve scripts/search.py relative to this skill's directory, as reported by the loader.
Use its absolute path from the project's working directory. Quote paths containing spaces.
The examples use <skill-dir> and <project-root> as placeholders; replace them with resolved absolute paths.

For a new project or a requested redesign:


```sh
python3 "<skill-dir>/scripts/search.py" "museum collection accessible editorial" --design-system -p "Museum" -f markdown
```

For a specific question:


```sh
python3 "<skill-dir>/scripts/search.py" "keyboard focus form errors" --domain ux --max-results 3
```

For implementation guidance, query the project's actual framework:


```sh
python3 "<skill-dir>/scripts/search.py" "form validation" --stack vue --max-results 3
```

Use --help for the installed domains and frameworks.
Design-system mode ignores --stack; run framework searches separately.
Avoid adding a library solely because a result contains its example code.

## Evaluate the results

Check relevance to the product, audience, platform, and current framework version.
Read complete snippets with --full when truncated output hides a needed detail.
When results are empty or unrelated, refine the query once.
If results remain unsuitable, state the search gap and use project evidence and established design principles.
Treat performance, accessibility, and conversion statements as guidance requiring checks in the actual interface.
Select only the recommendations that support the brief.

## Save decisions when useful

Generate recommendations in memory first. Review them against project constraints before saving a draft.
Use --persist only when the task calls for a saved design-system draft.
Always pass --output-dir with the intended project root and -p with the project name.


```sh
python3 "<skill-dir>/scripts/search.py" "museum collection accessible editorial" --design-system -p "Museum" --persist --output-dir "<project-root>"
```

The command writes design-system/<project-slug>/MASTER.md under the output directory.
A --page value adds pages/<page-slug>.md inside that same project directory.
Read those files at their actual paths before implementing a page.
Existing files are preserved by default. Use --force only for an authorized replacement after reading them.
Edit a saved draft to remove incompatible recommendations before adopting it as project guidance.

Scripts and data run locally without network access or third-party Python packages.
Persistence creates files only when requested. See SOURCES.md for the pinned source and packaging changes.
