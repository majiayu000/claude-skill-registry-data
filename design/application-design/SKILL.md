---
name: application-design
description: "The data-dense product-screen layer of the design method: density, the trading typography scale, metric grids, status badges, metric cards, loading skeletons, empty states, real-time value flashes, live regions and the sidebar-plus-content app shell, on top of the design foundation. Use when: designing or polishing an application screen, dashboard, data table or real-time panel; when the ui-ux-designer agent designs an application screen; or when the user says /application-design, 'make it denser', 'trading terminal look', 'metric card', 'status badge', 'loading skeleton' or 'price flash'."
user_invocable: true
---

# /application-design: dense, always-on product screens

This skill holds the application layer of the design method. It builds on the design foundation owned by `agentic-auto-improve:website-design` (`references/foundation.md`) and never restates it. A marketing or content page is designed with `website-design` alone.

The `ui-ux-designer` agent keeps one step this skill does not repeat: **Step 0, the `ui-evolution` journal lessons.** When you run this skill on its own, do that step first (grep `.claude/registries/JOURNAL.md` and `.claude/registries/JOURNAL/*.md` for `Tags:.*ui-evolution`, apply each lesson whose `Apply when:` matches, treat `recurring-mistake` as load-bearing), exactly as Step 0 of `agents/ui-ux-designer.md` words it.

## Project Context

**App type**: Real-time algorithmic trading terminal — data-dense, always-on
**Stack**: Angular 21 + Angular Material 21 (MDC) + TailwindCSS 4
**Users**: Power traders who need maximum information density and zero cognitive friction

This is trading-terminal guidance. For a project that is not a trading one, keep the density and always-on posture and read the trading wording as the project's own domain.

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

## Step 2 - Load the foundation (halt if absent)

Read `../website-design/references/foundation.md`, the sibling skill's file, in full. If that file is absent, say which path you looked for (resolved against this skill's folder) and halt. Do not continue with the application layer alone. Then read the paths the `review.documents` slot lists; they are authoritative.

## Step 3 - Load the application patterns

Read `references/application-patterns.md` (in this skill's folder) and apply it on top of the foundation: density, the typography scale, metric grids, badges, cards, skeletons, empty states, value flashes, live regions and the app shell.

## Advisory sources

- `dataviz` (a host built-in skill, not from a plugin): advisory only. Covers chart form heuristic, colour formula and validator, mark specs, stat tiles, dashboard layout, light/dark and accessibility. This plugin's rules and the project's `review.documents` win over it where they conflict. If it is absent, continue without it.
