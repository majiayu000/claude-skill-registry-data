---
name: forge
description: Take raw idea notes and adversarially decide whether each should become a skill — fold into an existing one, add as new, or drop — with an in-principle rating. Trigger on:- forge, assess skill ideas, review skill-ideas, should this be a skill, model a skill from an idea.
argument-hint: "dir to scan (default docs/skill-ideas/), or prose describing a revision to an existing skill"
allowed-tools: Read, Grep, Glob, Write, Edit, Bash
disable-model-invocation: true
model: claude-opus-5
---

# Forge

Turns raw ideas into skill decisions. For each idea it models the strongest version of
the skill implied, runs an internal Proposer/Skeptic debate, and renders a verdict plus
a rating. This is `notice`'s "Reviewing" step, done properly instead of skipped.

## When to use this

- `docs/skill-ideas/` has accumulated candidates and you want them triaged.
- Pointed at someone else's skill directory to assess that set.
- **Revision mode** — a prose argument (not a scan dir) naming a change to what an
  existing skill *does*: its procedure, triggers, tools, or a mis-calibration surfaced
  by `/notice`. No new idea file needed — skill management is the point.
- Skip only for a pure wording fix to an existing skill — just make it.

## Procedure

1. **Read `.specify/memory/constitution.md` and `skills/README.md`** (the authoring
   standard, the registry, and the **Overlap check**).

2. **Resolve the input** — if the argument is prose describing a change to an existing
   skill rather than a path, this is **revision mode**: skip the scan. Model the target
   skill as it stands and the proposed change, run steps 3–5 on *the change* (does it
   earn its place in that skill, should it fold into a different one, does it bloat an
   always-loaded `description`), write the report section (step 7), and on confirm apply
   the `Edit` directly — no idea file to archive. Otherwise, scan: the argument as a
   dir, else `docs/skill-ideas/`. `Glob` `*.md` (non-recursive; the `_` dirs are
   skipped). Note whether this is **local mode** (`docs/skill-ideas/`) or **external
   mode** (any other path). Process each file in order:

3. **Proposer pass** — model the strongest skill the idea implies: name, one-line
   purpose, trigger phrases, the procedure it would run, the artifact or outcome it
   produces, and the recurring need it serves. Steelman it. In external mode the input
   may already be a `SKILL.md` draft — model from that, don't reinvent it. Write this
   case into the report before starting the Skeptic pass.

4. **Skeptic pass** — assume the skill should *not* exist; make the idea earn its place.
   Attack on four axes:
   - **Overlap** — apply the Overlap check against every `skills/*/SKILL.md`. Name any
     skill it duplicates or heavily shares discipline with.
   - **Realness** — is the need recurring or a one-off? Cite evidence: `docs/notice.md`,
     `git log`, the idea file itself.
   - **Skill-shaped** — is this a reusable *procedure*, or a preference / fact /
     one-time task that belongs in memory or `CLAUDE.md`?
   - **Context cost** — does an always-loaded `description` for this pay for itself?

5. **Synthesis** — reconcile the two passes, citing named Proposer and Skeptic points
   (a named overlap must be addressed, not waved past). Apply the rule:
   - Distinctness ≤ 2 → **fold into `<existing>`** — unless Recurrence ≥ 4 *and* folding
     would push the host skill past ~120 lines, then **add**.
   - Skill-fit ≤ 2 **or** Recurrence ≤ 2 → **drop** (say which axis, and where the
     content should go instead if anywhere).
   - Otherwise → **add as new**.

6. **Rating, in principle** — score independent of the verdict (a strong idea can still
   be `fold`). Five axes, 1–5, one line of justification each:

   | Axis | 1 | 5 |
   |---|---|---|
   | Recurrence | seen once | arises weekly |
   | Distinctness | ~duplicate | no neighbour |
   | Skill-fit | belongs in memory | clearly a repeatable procedure |
   | Scope tightness | vague / broad | single crisp trigger→outcome |
   | Context cost | heavy for niche value | cheap or high-value |

7. **Write the report** to `docs/skill-ideas/_assessments/<YYYY-MM-DD>.md` — one file per
   run, each idea a section: modeled skill, Proposer case, Skeptic case, verdict, rating.

8. **Act on confirm — local mode only, per item:**
   - **add** — write `skills/<name>/SKILL.md` to the authoring standard, append a
     registry row to `skills/README.md`.
   - **fold** — show the exact Edit (target skill, section, added text); apply on yes.
   - **drop** — record the reason.
   Then move every processed idea file to `docs/skill-ideas/_processed/` with the verdict
   appended. External mode stops after step 7 — report only.

## Constraints

- Proposer's full case is written to the report before the Skeptic pass begins.
- The Skeptic argues from "this should not exist"; a weak defence is a finding, not a
  pass.
- Synthesis must address every overlap the Skeptic named.
- External mode never writes outside this repo and never archives the scanned files.
- Never delete an idea file — `_processed/` only.
- Don't design the skill in depth here — `add` produces a first draft; a real design
  pass is `/designit`.

## Done criteria

- Every `*.md` in scope has a verdict and a 5-axis rating in the report.
- Confirmed `add` / `fold` actions applied; registry updated.
- Processed idea files moved to `_processed/` (local mode).
