---
name: ui-case-studies
description: >
  Case studies for common product screens — defaults, required content, and
  anti-patterns. Use when designing or reviewing Settings, Profile, Auth,
  Empty states, Dashboard, or similar screens, or when the user asks what
  content belongs on a page by default.
---

# UI case studies

Short, opinionated inventories of **what a screen usually ships with** and **what content belongs there**. Use before mockup/implement (`frontend-mockup-first`, `hallmark`). Prefer the product’s real domain language over generic labels.

Load the matching file under [cases/](cases/):

| Screen | File |
|--------|------|
| Settings | [cases/settings.md](cases/settings.md) |
| Profile / account | [cases/profile.md](cases/profile.md) |
| Sign-in / sign-up | [cases/auth.md](cases/auth.md) |
| Empty / first-run | [cases/empty-state.md](cases/empty-state.md) |
| App dashboard / home | [cases/dashboard.md](cases/dashboard.md) |

## How to use

1. Identify the screen type (or closest match).
2. Read that case study.
3. Adapt labels to this product; drop sections that don’t apply (YAGNI).
4. Keep the existing app palette (`frontend-mockup-first`).
5. Run `hallmark` for visual structure — these cases cover **content**, not look.

Do not copy filler copy into the UI unless the user asked for placeholder text.
