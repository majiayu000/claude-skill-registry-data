---
name: component-scaffold
description: Scaffold and conventions to create a new UI component following project patterns (no Shadow DOM, static stylesheet registration, pixEngine templates). Use when adding a new custom element to the app.
license: MIT
metadata:
  author: AI Agents
  version: "1.0"
---

## When to use this skill

Use this skill when you need to add a new Custom Element-based UI component to the app following repository conventions (no Shadow DOM, register styles, use `pixEngine` templates).
Use this skill when you need to create a new reusable UI component following project conventions. This skill covers component structure, lifecycle management, and code organization patterns.

## Quick start

1. Create a component directory with `ComponentName.js`, `ComponentName.css`, and `ComponentName.template.html`.
2. Register styles via `registerStylesheet()` in the static block and define the custom element.

For detailed examples, patterns, and quality checklist see [references/REFERENCE.md](references/REFERENCE.md).

For project-specific conventions (naming, bundling, templating), see the project's `.context/` directory.
