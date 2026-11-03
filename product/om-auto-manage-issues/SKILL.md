---
name: om-auto-manage-issues
description: money-tracker.online extension of the installed om-auto-manage-issues skill. Human-hold labels, category mapping, the readiness verifier and the hand-on to afk-triage.
---

Extends the installed skill: read `.claude/skills/om-auto-manage-issues/SKILL.md` and follow it. On top:

- Human-hold labels (skip the issue entirely): `blocked`, `do-not-close`, `do-not-merge`.
- Category comes from the issue form (`.github/ISSUE_TEMPLATE`): a bug report is `bug`, an enhancement is `feature`, a maintenance item is `refactor`; Dependabot is `dependencies`.
- The Definition of Ready is in `SDLC.md`; the not-ready comment names the missing ticket-level items and points at the issue form section that holds each.
- **Run the readiness verifier before recording `not-ready`.** When step 6 of the installed
  skill (`references/enrich-existing-issue.md`) finds a ticket-level item missing, follow
  `.ai/skills/om-auto-fix-issue/SKILL.md` § Readiness verifier: `READINESS: VERIFIED` records
  `READY_STATUS=ready` and posts the `readiness verified` comment instead of the not-ready one;
  a `NEEDS_HUMAN` row that is a decision is settled through `.ai/skills/afk-decide/SKILL.md` (see "Settle, do not ask" below); only a row nobody but the reporter can answer records `not-ready`, and the not-ready comment lists only those rows.
  A verified issue is ready for every rule below.
- **Hand on by doing nothing.** In the `issue-groom` workflow `afk-triage` runs right after this
  skill, in the same run (ADR 0029), and turns a ready groom into an Agent Brief and a not-ready one
  into a brief or a `blocked` hold. Add no label to hand the issue on: the Open Mercato labels are
  the whole vocabulary (`.ai/trackers/github.md`). On `READY_STATUS=not-ready` the not-ready comment
  is the whole output of this step.
- **Never groom a Sentry issue.** A body with a `<!-- sentry-issue:` marker was filed from production error data, and the maintainer's login on it does not make it trusted, so the author gate does not stop it. Stop with `NO_ACTION_NEEDED` before any mutation: no automation grooms, briefs or implements it (ADR 0029, `.ai/scripts/backlog-status.mjs`).
- **A spec parent needs no brief.** An issue whose body starts with `Spec: .ai/specs/` is a parent:
  `afk-to-tickets` slices it into tickets that carry their own Agent Brief, and `afk-triage` stops
  on it. Groom it for labels and readiness as usual, and never leave that decision to a human in the
  report or a comment.
- **Settle, do not ask.** Grooming runs unattended, so the installed skill's "the not-ready comment
  names what a human must add" is narrowed here to what only the reporter knows (a repro, a
  version, what they expected). Everything else is settled in this run through
  `.ai/skills/afk-decide/SKILL.md` and never makes the issue `not-ready`:
  - A missing **Out of scope** section is written by this run: ask the product owner specialist for
    it, append it to the issue body with **update-issue** under an `## Out of scope` heading marked
    as agent-written, and record the verdict as a Resolved assumptions row in the groom comment.
  - An open question (product, design, scope, naming) is put to the fitting specialist and
    recorded as a non-blocking Resolved assumptions row (`# | Question | Applied default | Why`) in
    the groom comment. It is never addressed to the issue author and never makes the issue
    `not-ready`.
  - "A human's call", "decided by a maintainer" or similar wording copied into a ticket from a spec
    or an earlier comment is an open question like any other, never a blocker: settle it the same
    way.
- Implementation notes must name the owner module for each concept (`docs/SPEC.md` §8) and warn when the change would touch a protected surface in `BACKWARD_COMPATIBILITY.md`. An issue whose ask is listed in `docs/agents/out-of-scope.md` is reported as out of scope with the row's ADR, never groomed into a ticket.
