---
name: grill-docs
description: Grill the user about a plan (same interview as grilling) and record it — Q→A transcript in grills/, each decision appended to the repo's decisions doc (both under skilleddocs/ by default). Use for "grill me and document it", "grill with docs".
argument-hint: "plan, decision, or doc path [slug]"
---

Call the Skill tool with `"grilling"` and run that interview unchanged. Your addition: write down **each answer as it comes in**, mid-round too, so an abandoned session still leaves a record.

Paths (`skilleddocs/` is at the repo root, per [TRACKING.md](../handoff-auto/TRACKING.md)):
- transcript: `skilleddocs/grills/<local-date>-<slug>.md`. Slug: the argument's last word only when it is kebab-case and follows a doc path or a quoted subject (`docs/plan.md auth-plan`, `"our caching plan" cache-plan`); else 2–4 topic words, and the whole argument is the subject (`should we support e-books` keeps `e-books`).
- register (the decisions doc): the one the repo's `AGENTS.md`/`CLAUDE.md` names (several name one, e.g. a monorepo: the nearest walking up from the working dir to the repo root wins, and say which others you skipped; a path it names is relative to that file's folder); else an existing `docs/decisions.md`; else an ADR folder (`docs/adr/`, `doc/adr/`, `docs/decisions/`); else `skilleddocs/decisions.md`. Same rule as `consult-plan`. An ADR folder gets one new ADR per decision in its own format, carrying the same Source; one that reverses or narrows an old ADR also sets the old one's Status to `Superseded by NNNN` / `Amended by NNNN`, the only edit allowed to an old record. Always name the chosen path in the header's `Register:` field.
- register outside `skilleddocs/` while `skilleddocs/` stays untracked (below) → the transcript goes in `grills/` beside the register file or ADR folder instead (`docs/grills/…` for `docs/decisions.md` or `docs/adr/`), so its Sources ship with it.

Untracked → exclude `skilleddocs/` per [TRACKING.md](../handoff-auto/TRACKING.md) (it also covers the `pip install .` hazard).

## Before round 1

**Resume first.** A transcript for this slug (`grills/<date>-<slug>.md` or its `-2`, `-3`… form below, any date; newest wins, by date then suffix) with `Status: in progress` or `abandoned after Q<n>` → reopen it, never rewrite its header: pass its Q blocks to grilling as settled context (don't re-ask them), re-ask the questions it lists as unanswered, continue `Q<n>` and `D<k>`, set Status back to `in progress`. Otherwise write the header (today's file for this slug already exists, settled → add `-2`, `-3`… to the slug, never overwrite):

```markdown
# Grill: <topic>

Date: <local date> · Subject: <doc path or one line> · Register: <decisions doc path> · Status: in progress

## Rounds
```

## Per answer, before the next question

Transcript, per answered question. `Q<n>` counts across the whole session: continue the numbering across rounds, unique within the file. The heading is exactly `### Q<n>` so its anchor is the lowercase `#q<n>` (a title in the heading would change the anchor); the title goes on the first line:

```markdown
### Q<n>
- Topic: <title>
- Asked: <question + options, one line>
- Recommended: <your rec>
- Answer: <user's choice, verbatim if short; delegated → "(delegated) <rec>">
- Why: <user's reason, else the recommendation's rationale marked "(rec)">
```

Register, one row per settled question, continuing the `D<k>` numbering (an ADR folder: the next ADR number, cited `ADR <n>`). Source is the transcript path, relative to the register, plus the lowercase anchor (`grills/2026-10-16-sync-plan.md#q3` from `skilleddocs/decisions.md`). Called from a `wayfinder` ticket, name the ticket in Source too (`ticket <link>; grills/<file>#q<n>`):

```markdown
| D<k> | <local date> | <decision> | <why> | grills/<file>#q<n> |
```

New register header:

```markdown
# Decisions

Append-only register of decisions from grilling sessions, consult-plan reviews, and orchestrator runs. Reverse a decision with a new row; old rows stay as written.

| # | Date | Decision | Why | Source |
|---|------|----------|-----|--------|
```

Every answer is a decision, delegated ones too: planners, verifiers and consult-plan read the register.

## Close

Frontier empty and the user confirms → `Status: settled`, add `## Summary` (3–8 bullets) and `## Open` (or "none"). Ended early → `Status: abandoned after Q<n>` (n = last answered) and list asked-but-unanswered questions under `## Unanswered` (a resume re-asks them). Print both paths; say they're uncommitted unless the user asks to commit, and that a tracked register's rows need their transcript committed with them or the Sources dangle.
