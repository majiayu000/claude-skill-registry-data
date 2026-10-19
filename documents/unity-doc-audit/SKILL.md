---
name: unity-doc-audit
description: Audit and improve the documentation of Unity C# scripts and project onboarding without changing behaviour - Inspector usability (Tooltip, Header grouping), XML summary, param and returns comments that explain why, magic numbers, manager and singleton lifecycle notes, a custom developer tools listing, entry scene and Unity version in the README. Use when asked to document, comment or onboard on a Unity folder or script.
license: Unlicense
metadata:
  tags: "Unity, Documentation, Onboarding, Code Quality"
  category: "implementation"
---

# Unity documentation audit

Constraint: comments, attributes and markdown only. No behaviour change. Scope to the first-party folder; never
touch vendor packages.

## Part 1: repository and onboarding

1. Exact Unity version (`ProjectSettings/ProjectVersion.txt`) and the entry scene a developer presses Play on.
2. Custom developer tools: scan for `[MenuItem(` and `: EditorWindow`; list each with its menu path and what it
   solves in a "Custom Developer Tools" section.
3. Architecture in one paragraph: the core pattern (service locator, singleton facade, ECS, ...) and the entry
   classes; keep it in the canonical agent/developer instructions file, not duplicated.

## Part 2: script documentation

For each script in scope:

1. **Inspector usability**: every `public` or `[SerializeField]` field gets a `[Tooltip]` (or the project's
   equivalent, e.g. Odin `[InfoBox]`); group related fields with `[Header]` (or `[Title]`); follow the file's
   existing attribute style.
2. **XML docs**: `/// <summary>` on public classes and members explaining why the member exists, when to use it
   and its side effects; not a restatement of the name; `<param>` and `<returns>` documented.
3. **Magic numbers and vector maths**: inline comments with the intent, or a named constant when reused (a
   constant is a code change: keep it local and mention it in the review).
4. **Managers and singletons**: a class-level comment with the lifecycle (where it lives, when `Instance` is
   available, DontDestroyOnLoad) and how other scripts should access it.
5. **Legacy markers**: while touching a file, mark only edited lines that carry a legacy pattern with the
   project's migration marker; do not migrate during a documentation pass.

## Output

- Edited scripts (comments and attributes only), compile checked (an EditMode test run is enough).
- A summary table in the review: file, tooltips added, summaries added, notes.
- Proposed updates to design documents when the code contradicts them (do not rewrite design docs silently).
