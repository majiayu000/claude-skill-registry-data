---
name: om-auto-write-spec
description: money-tracker.online extension of the installed om-auto-write-spec skill. Repo-specific spec sections and the spec PR's labels; the installed workflow applies unchanged.
---

Extends the installed skill: read `.claude/skills/om-auto-write-spec/SKILL.md` and follow it. On top:

- No label starts this skill (ADR 0029): a person starts the `spec` workflow from the Cezar cockpit. Never add a label outside the Open Mercato taxonomy (`.ai/trackers/github.md`).
- Every spec carries a metadata table directly under its `H1`, before the first section: `Status`,
  `Issue`, `Spec PR`, `Implementation`, in that order, `none` where a value is absent. This skill
  writes it: `Status` is `draft` while the spec PR is open and `ready` once it merges, `Issue` is the
  FR issue driving the run, `Spec PR` is the design PR, `Implementation` is `none` - filling it is
  `om-auto-implement-spec`'s job. A brief-driven run with no issue still needs one before the spec can
  be scheduled; open it rather than leaving `Issue: none` on a merged spec, which is how
  `.ai/specs/implemented/2026-09-08-design-system-plan-reconciliation.md` came to sit unbuilt with nothing to
  schedule it from. New specs land at the root of `.ai/specs/`; `implemented/` and `archived/` are the
  other lifecycle states and belong to later skills. The rules are `.ai/specs/AGENTS.md`.
- Run `pnpm generate-spec-index` before opening the spec PR and commit `.ai/specs/README.md` with the
  spec. The index is generated and the validation gate compares it.
- Every spec under `.ai/specs/` carries two extra sections: **Visual change expected** (routes and states that change on screen, light and dark, desktop and mobile; "none" for backend-only work) and **Copy** (every new user-facing string, as an `en` key name plus text; the implementation lands the key in EN and PL in the same change, per the `i18n-messages` skill).
- Read `CONTEXT.md` for domain vocabulary and `docs/SPEC.md` for the architecture the spec must respect (tenant scoping in `src/server/repos`, Zod on every server-function input, `components/ui` never fetching data, additive D1 migrations). An amount is integer minor units at every layer (`docs/MONEY.md`); cite section numbers rather than restating the arithmetic. Name the owner module of each new concept (`docs/SPEC.md` §8).
- The spec PR is design-only: `Refs #{issueId}`, labels `review`, `documentation`, `skip-qa`, one priority, one risk. Branch `spec/<slug>`.
- Before releasing the claim, post one idempotent comment on the FR issue, marker ``🤖 `om-auto-write-spec` — 🔁 next step``: the spec path (`.ai/specs/<date>-<slug>.md`), the spec PR link, and the sentence that the issue stays open and **is** the implementation ticket - once a human merges the spec PR, starting `issue-autofix` on this issue from the cockpit builds it. Post it whichever path performed the handback (`om-open-pr` or the inline one in `references/claim-pr.md`). The path is not decoration: `om-auto-implement-spec`'s spec resolution scans the issue's comments for a `.ai/specs/` path, and this comment is what makes that step deterministic instead of dependent on a PR link happening to be there.
