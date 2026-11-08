---
name: design-setup
description: >
  Interviews the owner, one topic at a time, and writes `.claude/rules/design.md` — the
  design system, per-platform settings, how to reach a screen, and the design rules the
  design commands need. Detects what it can from the repository first and offers that as
  the default; the owner answers or keeps the current value. Owner-invoked only — no
  command or agent may reach it.
when_to_use: >
  Reach for this right after `/init-project` ships the file unfilled, whenever a design
  command stops naming an unfilled field of `.claude/rules/design.md`, or any time the
  owner wants to change what the file says. Not for reading the file (any agent does that
  directly).
disable-model-invocation: true
allowed-tools: Read, Write, Edit, Bash, Glob, Grep, AskUserQuestion
---

# design-setup

`.claude/rules/design.md` is owner-governed: how this product is designed is the owner's
policy, not something a model should guess at. This skill is the only way it gets written
or changed — running it IS the owner's approval, so there is no separate confirmation step.

## When it applies

- A new project, right after `/init-project` copies the template unfilled.
- A design command stopped because a field of the file is unfilled.
- Any time the owner wants to change what the file says, filled or not.

## Inputs

| Input | Where it comes from |
|---|---|
| The current file | `.claude/rules/design.md`, or `template.md` (this skill's own directory) when absent |
| The current shape | `template.md` — the shipped template |
| Repo signals | `package.json` (dependencies, scripts), `tailwind.config.*`, `tokens` or theme files, component folders, route folders, Storybook config, `.claude/verification-notes.md`, `CLAUDE.md` |
| Installed detectors | `tooling-detector`, `framework-detector`, whichever exist under `.claude/skills/` in this project — used when present, never assumed |
| Environments and credentials | `.claude/rules/verification.md` §1 and §3 — referenced, never copied |

## Topics

One `AskUserQuestion` call per topic, in the file's own order:

1. **§1 Design system** — artifact link and namespace, source of truth, build command, and
   whether the product's build may run to bundle components.
2. **§2 Per platform** — for each platform: board component kind (real or parts), tokens
   source, component library paths, viewport sizes.
3. **§3 How to reach a screen** — route list, seed data, capture command, where current
   screenshots live. Sign-in is never asked for a value: the file points at
   `verification.md` §3.
4. **§4 Design rules** — reuse, accessibility floor, process rules. Each field has a stated
   default:
   - **Reuse** — default: "the design system's components and tokens; a new component needs
     a reason. How far a layout departs from today's screen is §5's departure latitude."
     Offer this default even when the current file still carries the old wording ("an
     existing view beats a new one"): that wording made every layout change a reuse
     violation, and layout departure is now §5's departure latitude, not a reuse rule.
   - **Accessibility floor** — see "Accessibility floor" below.
   - **Process rules** — free text; default: keep the current value, or leave blank.
5. **§5 Design direction** — brand, style pack, references, departure latitude. Run
   `node .claude/lib/design-map.js direction --dir .` first when the file is filled; its
   `available_packs` are the style packs to offer. Each field has a stated default:
   - **Brand** — free text; default: keep the current value, or leave blank.
   - **Style pack** — one of `available_packs`, or none; default: none, so the product's own
     design system leads.
   - **References** — every product or site to draw toward, in one field (this replaces the
     old competitor-references line); default: keep the current value, or leave blank.
   - **Departure latitude** — `keep` (change only what the brief items require), `refine`
     (keep information architecture and navigation; layout, spacing, hierarchy and visual
     treatment may change) or `rethink` (layout, navigation placement and composition may
     change entirely). Default: `refine`.

Each call offers, in this order: the detected value (marked as detected, with its source),
then the file's current value where it differs, then "keep". An answer of "keep", or
skipping the topic, leaves that section untouched. Re-running on a filled file asks only
what is missing or what the repository now contradicts.

**Accessibility floor.** The question offers contrast 4.5:1 and 44 px touch targets as the
default and says it is a default. `design.md` records the owner's answer, whatever it is —
not the default unless the owner chose it. It is written in the form
"contrast <n>:1, targets <n> px" so `design-map.js direction` can read the two numbers.

## Writing

Once every topic has an answer, the whole file is written at once in the template's shape.
No preview and no second confirmation. A section the interview did not change keeps its
content verbatim.

## Never

- **Write a credential's value.** Sign-in goes by reference to `verification.md` §3.
- **Contact or probe an environment.** Detection reads files already in the repository.
- **Edit any file other than `.claude/rules/design.md`.**
- **Start a design command, or any other command.** The owner's next invocation does that.

## Readout

Ends with the framework's four-section readout (STATE / DECISIONS / ISSUES / NEXT,
`.claude/rules/command-status.md`), then the `═══ COMMAND COMPLETE: /design-setup ═══`
banner and a call to `.claude/hooks/notify-complete.sh design-setup complete "<one-line summary>"`.
