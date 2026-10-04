---
name: ballot
description: >-
  Use when decisions happen async — reviewer(s) look at it over chat, on a PR,
  on a train, or any time outside the agent session. Triggers: async decision,
  PR review, pull request, remote reviewer, handoff, away-from-keyboard,
  decision ballot, architecture call, architecture decision record, ADR,
  hiring panel, vendor selection, household decision, reconcile, per-reviewer,
  tick box, ballot.
compatibility: claude-code, cursor
license: MIT
metadata:
  author: eins78
  repo: https://github.com/eins78/agent-skills
  version: "1.0.0"
---

# Ballot

Durable decision artefact for decisions that happen async — reviewed over chat, on a pull request, after the agent session ends. Tiered into Must / Should / Could horizons, with an empty checkbox per option. One file per decider (per reviewer when there are several). Reconciliation happens in the sessionlog; the ballot is what survives.

Extracted from the `dossier` skill — pairs with it when SYNTHESIZE produces decisions needing extraction, and stands alone anywhere a decision leaves the immediate session: ADRs, architecture calls, hiring panels, vendor selection, household decisions, PR review handoffs.

## When to Use

- Decider(s) look at the decision outside the agent session — chat handoff, PR review, async sign-off, remote collaboration. Single-decider async is still ballot-worthy; the structure survives 12-hour-later reading and multi-dossier listings. Multiple reviewers get per-reviewer files; a single async decider gets one file.
- The decision has a durable consequence worth capturing in version control — ADRs, architecture calls, hiring panels, vendor selection, PR review, household commitments.
- Decisions have mixed urgency — some block delivery, some are directional, some are informational. The Must/Should/Could tiers encode that.
- The decision surface benefits from a format that reads sensibly on a phone: empty checkboxes, one question per DEC, tiered by urgency rather than time-horizon.

## When NOT to Use

- Decider is in the session right now and the decision fits in chat. Ask and write the outcome in a sessionlog.
- Low-stakes vote with no durable consequence (lunch options).
- Decision surface is not yet framed. Frame first; ballot once options are real.
- Ongoing reconciliation. Ballots are point-in-time; ongoing discussion lives in its own venue (sessionlog, meeting notes).

## Workflow

1. **Frame the decisions.** For each DEC, one decision surface, one time-horizon, at least two real options. Tag Must / Should / Could.
2. **Create one ballot file per decider.** Filename: `DOSSIER-<slug>-BALLOT-<Reviewer>.md`. Multiple reviewers → one file each. Single async decider → one file (the reviewer field holds that decider's name). The `DOSSIER-` prefix keeps the ballot next to any companion context doc in a file listing even when the ballot is standalone — see §Standalone vs. Dossier-invoked.
3. **Prose-recommend per DEC, but leave checkboxes empty.** A pre-ticked box is pressure, not a recommendation.
4. **Hand off the ballot.** Post the link in the channel the decider(s) will see it; commit the file so it survives the session.
5. **Reconcile in the sessionlog.** Walk each DEC, note where decider(s) ticked or where reviewers split, record the decided outcome. Reconciliation is a session output, not a third ballot file.

Template: `${CLAUDE_SKILL_DIR}/templates/ballot-per-reviewer.md`.

## Conventions

These rules are empirical — each came from a concrete ballot that went wrong before it was fixed. Full rationale: `${CLAUDE_SKILL_DIR}/references/ballot-conventions.md`.

- **One file per decider.** Do NOT create a single-file multi-column ballot. For multi-reviewer ballots, scrolling past peer columns on a phone is cramped. For single-decider async, a multi-column layout is just noise. Enforced by `ballot-filename.sh` — the filename must end `-BALLOT-<Reviewer>.md`.
- **Clean cover block.** Reviewer, role, (peer-ballot link if multi-reviewer), dossier/context link. Nothing else. No "updated 2026-04-18" paragraph, no changelog, no "changes since previous version". Archaeology belongs in the commit log and sessionlog.
- **Recommended-but-not-pre-ticked.** A DEC can have a prose recommendation (`*Recommended: Option B — one-line why.*`), but checkboxes stay empty. The reviewer's tick is the decision.
- **One DEC = one decision surface = one time-horizon.** Do not mix "launch-day channels" with "next year's CFP commitments" in a single multi-select.
- **No anti-options.** If you added an option labelled "not recommended" or "for completeness", either add a `<!-- justify: ... -->` comment (e.g. the option has political visibility) or delete it. Anti-options cost reviewer ticking-time without changing outcomes.
- **Must / Should / Could tiers.** Must blocks delivery. Should blocks only if reviewers disagree (or a single async decider flags dissent). Could is informational. If the Must tier has unresolved disagreement at delivery time, flag in the sessionlog — the ballot skill does not ship a hard gate for this (too fragile to parse).
- **Reconciliation in the sessionlog.** Not in a third file. Ballots are durable; reconciliation is session-scoped.

## Use Cases

Each is a 2-3 line sketch of how the template adapts.

- **ADR voting.** Senior engineers approve an architectural decision. Must tier = the chosen architecture; Could tier = migration preferences. Dossier optional; the ADR itself can be the context doc.
- **Architecture call reconciliation.** Whiteboard session ended contested. Ballot captures the surviving options per sub-decision, each reviewer ticks over the following week, reconciliation at the next standup.
- **PR review handoff.** Agent session produces a change set; reviewer will look at the PR after hours. Ballot captures the decision surfaces (approve / request-changes per thread, merge strategy, release-note wording). Reviewer ticks on the train; reconciliation lands in the sessionlog once the PR merges.
- **Hiring panel.** Must = ship offer / reject / more-interview. Should = role scoping (seniority band, onboarding pairing). Could = onboarding prefs. Compensation stays out of the ballot body — keep it in the offer doc.
- **Vendor selection.** Must = which vendor (one option per vendor). Should = contract term, payment schedule. Could = optional add-ons. Dossier provides the comparison table; ballot captures commitments.
- **Household decision.** Max + partner choosing among options (holiday, appliance, move-date). Low-stakes but the ballot mechanism scales down — two Must items is plenty.

## Reviewing a ballot

Ballots are reviewed against `${CLAUDE_SKILL_DIR}/references/review-checklist.md`. The checklist covers filename pattern, cover-block cleanliness, anti-options, time-horizon-per-DEC, recommended-but-not-pre-ticked, tier discipline, async-readability, and reconciliation location.

**One mechanical gate.** `ballot-filename.sh` fires PostToolUse on `Write|Edit` for files matching `DOSSIER-*BALLOT*.md` and fails on anything not matching `DOSSIER-<slug>-BALLOT-<Reviewer>.md`. Alerting level, not true blocking — the file is already on disk when the hook fires; exit 2 feeds stderr back to Claude, which usually corrects. Everything else is reviewed by checklist, not by grep: the other concerns (cover-block archaeology, anti-options, dated claims, scope coherence) don't generalize cleanly across dossier styles, and a judgement-capable reviewer catches them more reliably than a pattern match.

Must-tier "blocks delivery" is a convention, not a gate. A ballot-state parser to detect final-status-with-unticked-Must would be too fragile (requires reconstructing reviewer intent). Flag in the sessionlog if a Must item is unresolved at delivery time.

## Standalone vs. Dossier-invoked

**Standalone.** For ADRs, architecture calls, hiring, vendor selection, household decisions. The `DOSSIER-` filename prefix stays — it keeps ballots grouped with any companion documents and makes the gates fire. No dossier file needs to exist; the cover-block "Full dossier" link can point to a meeting notes doc, an ADR markdown file, or be omitted.

**Dossier-invoked.** When a `dossier` SYNTHESIZE surfaces decisions needing per-reviewer sign-off, the dossier skill points at this skill's template and conventions. The dossier owns the research; the ballot owns the decision surface. See `skills/dossier/SKILL.md` §SYNTHESIZE.

## Related Skills

| Skill | Integration |
|-------|-------------|
| `dossier` | Primary caller. Dossier research produces decisions; ballot extracts them. |
| `bye` | Reconciliation lives in the sessionlog — same sessionlog `/bye` builds at session end. |
| `commit-notation` | `D:` prefix for ballot commits when delivered with a dossier; otherwise commit-intention matches the parent artefact (e.g. `F:` for an ADR, `D:` for a hiring decision doc). |

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Single-file ballot with two reviewer columns | One file per reviewer — `DOSSIER-*-BALLOT-<Reviewer>.md` |
| Cover block with "updated 2026-…" or changelog paragraph | Commit log holds history; cover block holds reviewer/role/links only |
| Pre-ticked checkbox as "recommendation" | Use prose: `*Recommended: Option B.*` Checkboxes stay empty |
| Mixing time-horizons in one DEC | Split into two DECs (e.g. DEC-003 launch-day, DEC-004 next-year) |
| Anti-option listed for completeness | Either justify (`<!-- justify: ... -->`) or delete |
| Reconciliation as a third file | Reconciliation lives in the sessionlog, not a `DOSSIER-*-RECONCILE.md` |
| Must-tier item unresolved, delivery called complete | Flag in sessionlog; no gate enforces this |
