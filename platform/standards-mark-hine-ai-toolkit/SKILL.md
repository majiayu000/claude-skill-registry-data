---
name: standards
description: "Tiered UI design rules for Android, iOS and web, with sources, rationale and platform APIs. Use when building, redesigning or reviewing a screen, component or design system, or when asked about contrast, touch targets, spacing, type scale, screen states, motion, dark mode or UI that looks AI-generated."
argument-hint: "[screen or component] [android|ios|web]"
metadata:
  verified: 2026-09-29
  sources: references/sources.md
---

# Design standards: $ARGUMENTS

The rules live in `~/.claude/rules/design-standards.md`. This skill adds the sources, the reasons and the APIs. If that rule file is missing, grade against the Tier 1 sources in `references/sources.md` only and say so. To improve, redesign or extend a design, or to work on a logo or app icon, use `/design-kit:iterate`. It adds the project's `DESIGN.md` contract, rendered options and the user's pick to these rules.

1. Read the project instructions file, the project's `DESIGN.md` when one exists (SYS-1), then the rule file. Note any T2 rule IDs the project opts in.
2. Name the platform, and the tone and density the screen commits to (DIR-1).
3. Build or review against the rule file one section at a time. Take each API from `references/platform-apis.md`. Do not restate rules from memory.
4. List the states the screen can reach (STA-1) and confirm that the state model has a case for each and the UI renders it.
5. Check accessibility on a device or simulator where you can, at the largest text size, with the screen reader, with reduced motion and in dark mode.
6. Do not fetch a source page to grade a rule. When a rule is disputed, quote its anchor from `references/source-anchors.md`. When the rule and the anchored sentence disagree, follow the source and report the rule ID, the anchor and its confirmed date.
7. Read `references/rationale.md` before overriding or arguing a T2 rule. T2 rules are defaults and grade Nit unless the project opts in.
8. Hand the diff and any labelled screenshots from step 5 to `ui-reviewer` before calling the work done.
