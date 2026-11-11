---
name: website-design
description: "The design foundation for any page of a project: theme polarity per application, the Material-to-Tailwind @theme token bridge, the inline-style ban, WCAG 2.1 AA contrast, keyboard and ARIA rules, purposeful motion and the never-do list. Use when: designing or restyling a website page, a marketing or content page, or any frontend page's colours, theming, accessibility or layout; when the ui-ux-designer agent designs a website page; or when the user says /website-design, 'design this page', 'fix the theme', 'colour contrast', or 'replace this inline style'."
user_invocable: true
---

# /website-design: the design foundation

This skill holds the design foundation: the rules every page of a project obeys, whatever kind of page it is. The rules live in `references/foundation.md` beside this file. A data-dense, always-on product screen is designed with `agentic-auto-improve:application-design`, which loads this foundation first and adds its own layer.

The `ui-ux-designer` agent keeps one step this skill does not repeat: **Step 0, the `ui-evolution` journal lessons.** When you run this skill on its own, do that step first (grep `.claude/registries/JOURNAL.md` and `.claude/registries/JOURNAL/*.md` for `Tags:.*ui-evolution`, apply each lesson whose `Apply when:` matches, treat `recurring-mistake` as load-bearing), exactly as Step 0 of `agents/ui-ux-designer.md` words it.

## Step 1 - Read the project profile (halt on anything unusable)

The profile is `<project root>/.claude/project-profile.md`, where the project root is `CLAUDE_PROJECT_DIR` when set, else the repository holding the files being designed. Never read the plugin's own copy: it is a template. Read the slots `frontend.roots`, `frontend.theme-polarity` and `review.documents`.

| Condition | Outcome | You do |
|---|---|---|
| The project root cannot be determined (no `CLAUDE_PROJECT_DIR`, and no target file yet to locate a repository) | `root-undeterminable` | Halt and ask which project. Do not search. |
| Profile file absent at the project root | `file-missing` | Halt: "no project profile at `<path>`; run `/auto-improve-finish-install`". |
| `frontend.roots`, `frontend.theme-polarity` or `review.documents` row absent | `row-missing` | Halt, naming the slot. |
| Any of the three holds template `*(...)*` prose or is empty | `placeholder` | Halt, naming the slot. Never guess a theme. |
| `frontend.roots` is `none` | `none-authored` | Halt: the project declares no frontend to design for. |
| Target application has no `frontend.theme-polarity` entry | `row-missing` (per app) | Halt, naming the application. |
| Polarity `none` for the target (a library) | `usable` | Use token utilities only. |
| `review.documents` is `none` | `none-authored` | Continue, and say no authoritative documents exist, so the foundation and advisory sources are the only sources. |

No colour class is chosen before the target application is matched to a `frontend.roots` entry and its polarity is read.

## Step 2 - Load the foundation

Read `references/foundation.md` (in this skill's folder) in full and apply it. Then read the paths the `review.documents` slot lists; they are authoritative and win over everything below.

## Step 3 - Design the page

Apply the foundation to the page. The application patterns file (`../application-design/references/application-patterns.md`) does not apply to a website page by default; use one of its patterns only when the page shows live product data. If that file is absent, continue with the foundation alone.

## Advisory sources

- `frontend-design:frontend-design` (a skill from the `frontend-design` plugin): advisory only, for visual direction and distinctive layout on a website page. This plugin's rules and the project's `review.documents` win over it where they conflict. If the plugin is absent, continue without it.
