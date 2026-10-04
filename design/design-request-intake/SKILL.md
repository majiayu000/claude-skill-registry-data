---
name: design-request-intake
description: Gather Linear + GitHub context and confirm the target platform before generating any brand-new UI screen/design, in Figma or Stitch. Use as the first step whenever a request asks to design, mock up, or generate a new screen — before calling any Figma or Stitch generation tool.
---

# Design Request Intake

Shared first step for any "design/generate a new screen" request, regardless
of destination (Figma via `.claude/rules/figma-design.md`, Stitch via
`.claude/rules/stitch-design.md`). Do this before calling any
destination-specific generation tool (`use_figma`, `create_new_file`,
`generate_figma_design`, `generate_screen_from_text`, ...). It does not
apply to pure edits of a design that already exists and is already open/
identified — those inherit their context and platform from the existing
artifact.

## 1. Linear context

If a Linear ref is linked (`.claude/.linear-link`) or mentioned in the
request, follow `.claude/rules/linear.md` / the `linear-workflow` skill:
call `get_issue` **and** `list_comments` before doing anything else. The
issue title/description alone is often not the full picture — decisions
and scope changes frequently live in the comments.

If no Linear ref exists and the request doesn't reference one, skip this
step — a Linear ref is always optional.

## 2. GitHub/codebase context

Look at:
- Existing screens/components and conventions already in the target
  `apps/<app>/` — don't propose a design that ignores an established
  pattern.
- Relevant open PRs (`gh pr list`, `gh pr view`) that might already be
  touching the same area.
- The target app's `CLAUDE.md` (e.g. `apps/research-hub/CLAUDE.md`) for
  domain model / tech stack context that should inform content and
  structure.

## 3. Platform check

If the request doesn't say which platform/device the screen targets
(mobile app, desktop web, tablet, a specific breakpoint, ...), **ask via
`AskUserQuestion` before generating**. Never default or guess the
platform silently — a wrong guess means regenerating from scratch.

Skip the ask only when:
- The platform is explicitly stated in the request, or
- You're editing/extending an existing screen whose platform is already
  fixed (confirm it — e.g. via Stitch's `get_screen`, or the Figma frame
  size already in place — rather than re-asking).

Map the confirmed platform to whatever the destination tool needs:
- **Stitch**: `deviceType` — `MOBILE` / `DESKTOP` / `TABLET`.
- **Figma**: frame size/breakpoint convention (e.g. a mobile frame vs. a
  desktop web frame) — set this explicitly when creating the frame in
  `use_figma`/`create_new_file` rather than leaving Figma's default.

## 3.5 Color mode

SBSI's design system (`.claude/rules/design-system.md`) defines every
color role for both Light and Dark. If the request doesn't say which
mode(s) to generate for, ask alongside the platform question rather than
defaulting to Light silently — same reasoning as the platform check: a
wrong guess means regenerating from scratch (Stitch in particular needs a
separate design-system asset per mode, see `stitch-workflow`).

## 4. Hand off

Once context (steps 1–2) and platform (step 3) are settled, proceed to
the destination-specific skill:
- Figma: the mandatory `/figma-use` skill, then `use_figma` /
  `create_new_file` / `generate_figma_design`.
- Stitch: `.claude/skills/stitch-workflow/SKILL.md`.
