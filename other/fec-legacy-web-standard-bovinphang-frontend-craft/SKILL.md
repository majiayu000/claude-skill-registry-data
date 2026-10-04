---
name: fec-legacy-web-standard
description: "Use when maintaining or safely modifying existing non-framework frontend code: vanilla JavaScript, jQuery, HTML/CSS, MPA pages, server-rendered templates, legacy plugins, or long-lived code that should stay in its current stack. Use migration skill when planning a move to React/Vue/TypeScript; Chinese triggers include traditional frontend, native JS, jQuery."
---

# Traditional front-end project specifications (JS + jQuery + HTML)

## Purpose

Safely maintain vanilla JS, jQuery, HTML/CSS and server-side template projects without rewriting the technology stack.

## Procedure

1. First confirm whether this change is to maintain the old stack or migrate; switch to the modern migration workflow when migrating to React/Vue/TypeScript.
2. Use the existing architecture and coding style, prioritize fixing problems, and do not introduce multiple modernizations in one change.
3. JavaScript uses IIFE/namespace to reduce global pollution, and event binding is delegated to reasonable containers first.
4. DOM updates cache selectors, batch operations, and escapes user input; Ajax must handle loading, error, empty status, and prevention of repeated submissions.
5. HTML/CSS maintains semantics, label, alt, BEM/existing naming and low selector depth.
6. Key security checks: `.html()`, `innerHTML`, URL parameter rendering, CSRF token and file upload.

## Detailed reference

Load [references/legacy-patterns.md](references/legacy-patterns.md) when it comes to jQuery namespaces, event binding, Ajax, XSS escaping, file organization, and maintenance checklist examples.

## Constraints

- Improve within the existing architecture and do not introduce modern frameworks that are incompatible with the project.
- Progressive enhancement is better than reinventing the wheel.
- Disable using `innerHTML` / `.html()` to directly insert user input.
- Avoid global variable pollution.
- Focus on one maintenance point at a time to avoid rebuilding the entire module.

## Expected Output

The changes are consistent with the style of the old project, no global variables are leaked, events and DOM operations are maintainable, Ajax state is intact, user input has been escaped, and incremental improvements do not destroy existing functionality.
