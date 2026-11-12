---
name: openspec-help
description: Quick-reference card for OpenSpec in the-grid (the 12 wired skills, spec format, CLI). Use when the user asks "how do I use openspec", "how do I add specs to this repo", "what are the openspec commands" or "which openspec skill do I want".
---

# openspec-help

One-shot reference. Not a mode — display and stop.

[OpenSpec](https://openspec.dev) is spec-driven development: proposals get
written and **reviewed before code exists**, and the spec survives the session
that produced it. Upstream is [Fission-AI/openspec](https://github.com/Fission-AI/openspec)
(MIT), tracked at `repos/openspec`.

## The 12 skills

**Normal path — start here:**

| Skill | When |
|---|---|
| `/openspec-explore` | Thinking out loud before committing to a direction. No artefacts written. |
| `/openspec-propose` | You know what you want. Creates the change + all artefacts in one pass. |
| `/openspec-apply-change` | Proposal reviewed and accepted — implement the tasks. |
| `/openspec-verify-change` | Check the implementation actually matches the spec, before archiving. |
| `/openspec-archive-change` | Fold the delta into `openspec/specs/`, move the change to `archive/`. |

**When the normal path doesn't fit:**

| Skill | When |
|---|---|
| `/openspec-new-change` | Step-by-step artefact creation instead of `propose`'s one-shot. |
| `/openspec-continue-change` | Pick up a change someone (or a past session) left half-built. |
| `/openspec-ff-change` | Fast-forward — generate every artefact without stepping through. |
| `/openspec-update-change` | Revise an existing plan and keep its artefacts coherent. **Never edits code.** |
| `/openspec-sync-specs` | Push a delta into main specs *without* archiving the change. |
| `/openspec-bulk-archive-change` | Several parallel changes finished at once. |
| `/openspec-onboard` | Guided first cycle, narrated, on real work in your codebase. |

Related, and **not** an openspec skill: `/spec-scout` audits adoption and
reports spec↔code drift. Survey-only — it never writes specs.

## Layout

```
openspec/
  specs/<capability>/spec.md     current truth — what the system does today
  changes/<change-id>/
    proposal.md                  what & why
    design.md                    how
    tasks.md                     implementation checklist
    specs/<capability>/spec.md   the DELTA — how the spec changes
  archive/                       completed changes
```

The distinction that matters: `openspec/specs/` is present tense.
`openspec/changes/*/specs/` is a diff against it. **Never hand-edit current
truth as part of a change** — write the delta, let `archive` or `sync` fold it
in. That's the failure mode the whole convention exists to prevent.

## Spec format

Plain markdown. No custom syntax.

```markdown
## ADDED Requirements

### Requirement: Theme selection
The app SHALL let users switch between light and dark themes, defaulting to
the system preference.

#### Scenario: User toggles dark mode
- **WHEN** the user clicks the theme toggle
- **THEN** the app switches to dark mode and persists the choice
```

Headers are `ADDED`, `MODIFIED`, or `REMOVED`. Requirements use SHALL. Every
requirement needs at least one WHEN/THEN scenario — one without is untestable
and shouldn't merge.

## Sections
Read a section only when its condition applies; do not preload them.
- sections/adopting.md: read when asked how to adopt OpenSpec in a repo (init, greenfield, brownfield)
- sections/the-grid-specifics.md: read when asked how OpenSpec is wired here, its CLI dependency, stores, or gotchas
