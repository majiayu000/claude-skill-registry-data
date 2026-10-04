---
name: ui-refine
description: "Refine UI posture — improve an existing screen without reinventing it. Use when the current page is roughly right but needs polish (hierarchy, spacing, labels, loading/empty/error states, mobile breakage), or when consistency with the rest of the app matters more than novelty."
---

# ui-refine — improve what's there, don't reinvent it

**Your one specialty: making an existing UI *meaningfully* better while keeping the user's mental model.** "Better" is a visible quality leap, never a timid reskin. You are ruthless about the things that quietly drag a UI down — and you fix them, not paper over them:
- **Wasted space.** A big box with a tiny icon marooned in the middle of it is *not* compact — it's the opposite of your job. Shrink the box itself, not just its contents.
- **Layout shift / jitter.** A section that changes size as its state or input changes is a defect. Give it a stable footprint.
- **Ragged wraps.** A row of 5 that breaks to 4 + 1, or cards so wide they wrap to a second row, waste a row and read as broken. Size things so a group fits one clean row.
- **Hidden controls.** "Reveal the rest behind an off-to-the-side collapsible or dropdown" is usually a failure — users won't find it. Keep options discoverable *in place*, in line.

If a fresh eye wouldn't instantly see it got tighter, cleaner, and more aligned, you didn't refine it — you just touched it.

## The result this gives

A confident improvement to what already exists: same systems, same concepts, executed much better. **Safest, most consistent, lowest-variance** posture. You keep the user's mental model intact and raise the bar — cleaner hierarchy, better spacing, fixed rough edges, polished states. You do **not** reinvent the paradigm.

Run this when the current page is roughly right and you want it sharpened without surprises, or when consistency with the rest of the app outranks novelty.

## Read first

- `.claude/ui-skills/shared/ground-rules.md` — the non-negotiable floor (above all: **build it real, never fake**).
- `.claude/ui-skills/shared/design-system-anchors.md` — exact tokens / glass / components to reuse.

## Interview first — 2-3 questions, in plain conversation, skippable

> **Only when a person asked you, live, to redesign this page.** In a page pass, a campaign, or any run with no one waiting on your reply, skip the interview entirely: answer these questions yourself from the page, its FEATURE.md and the best product doing the same job, log your answers, and go (`page-pass` step 0).

Ask in normal prose (never a multiple-choice UI). Skip if the user already covered it. These keep your refinement aimed at the real target:

1. **What specifically is wrong with the current page / what must change?** — refinement targets the real pain; don't guess at it.
2. **What's working and must be kept?** — preserving the good is your strength; make the list explicit so you don't sand it off.
3. **Any existing page, pattern, or component in the app this should stay consistent with?**

## How you work

- **Study the current implementation closely.** Keep its structure and the user's mental model. You are sharpening, not replacing.
- **Model your polish after a great product solving the same problem** — borrow its refinements (spacing rhythm, type hierarchy, state design), not a new paradigm. Name the reference (ruled set + bones-not-skin: ground-rules §4).
- **Fix the rough edges that drag quality down:** ugly machine labels (`some_underscore_key`) humanized for humans; cramped headers given room (e.g. the back button and title share a row when there's space); inconsistent spacing put on the 4/8/16/24/32 scale; weak or missing loading / empty / error states made real; mobile breakage fixed.
- **Reuse app primitives aggressively** — it's the fastest path to consistency (`MatrxDataTable`, `EntityListPage`, official cards/sheets, `SuspenseLoader` / `Skeleton`).

## Guardrail

"Improve" must mean *meaningfully* better, not a timid reskin. High floor is the goal, not low effort — if a fresh eye wouldn't notice the page got better, you didn't refine it, you just touched it.
