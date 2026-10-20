---
name: evaluate-skill-lite
description: >-
  A fast, cheap sanity check on a Claude Code skill or plugin while you are still writing or
  iterating on it — not the full ship gate. Runs only the three cheap dimensions — structural
  integrity, triggering accuracy (single pass, no N-run statistics), and content quality against the
  shared rubric — and deliberately SKIPS the expensive behavioral-lift battery (paired with/baseline
  subagents across N runs), reporting the gate as partial (4/6 measured, criteria 5–6 unproven). For
  the full evidence-based verdict with behavioral lift before shipping, use
  ceh-evaluation:evaluate-skill instead. Not for writing a skill from scratch (that is authoring) and
  not for general code review of an application.
argument-hint: "[skill-or-plugin-path]"
---

# Evaluate Skill — Lite

A **fast dev-loop check** on a Claude Code skill or plugin, for use while you are still iterating on
the text — not a ship verdict. It runs the three cheap dimensions and skips the expensive one, so a
loop costs a handful of subagent calls instead of dozens.

This is the deliberately scoped-down sibling of `ceh-evaluation:evaluate-skill`. It shares that
skill's rubric and report schema verbatim — read them rather than re-deriving:

- Rubric: `../evaluate-skill/references/eval-rubric.md`
- Report schema: `../evaluate-skill/references/eval-report-schema.md`

**When to reach for the full skill instead:** before you actually ship. Lite leaves "does this skill
actually help?" unproven by design; only the full skill's behavioral-lift battery answers that.

---

## What lite measures (and what it skips)

| Dimension                   | Lite                                  | Full                       |
| --------------------------- | ------------------------------------- | -------------------------- |
| 1. Structural integrity     | yes (inline, free)                    | yes                        |
| 2. Triggering accuracy      | yes, **N=1** (sanity, not statistics) | yes, N=3                   |
| 3. Content quality (rubric) | yes                                   | yes                        |
| 4. **Behavioral lift**      | **skipped** — left unproven           | yes (paired subagents × N) |

Lite never reports a passing gate. The honest ceiling is **4/6 measured, criteria 5–6 unproven** —
behavioral lift is unmeasured and the user-confirm gate is not a lite concern.

---

## Output location

Same convention as the full skill, with a `mode: lite` marker so a lite report is never mistaken for
a ship verdict. All output goes under
`.agents_workspace/skill-evals/<target-name>/run-<NNN>/` — never next to the target. `<target-name>`
is the skill or plugin name; `<NNN>` is the next zero-padded run index (`run-001` if none). Create
`.agents_workspace/` and any missing parents if absent. A lite run takes its own `run-NNN`; it does
not resume or overwrite a full-eval run.

---

## The loop

```
Phase 0  Intake  → locate & read the target
Phase 1  Derive  → claim, trigger intent, intended outcome; build the trigger battery; draft SKILL_EVAL.md
Phase 2  Run     → structural (inline) + triggering (N=1) + content (rubric)
Phase 3  Report  → fold evidence in; score the 4 measurable criteria; name the highest-leverage gap
Phase 4  Revise  → fix that gap, re-run only the affected dimension, re-score
         ↑________ repeat until the 4 measurable criteria pass, then stop
```

At the end, tell the user plainly: the four measurable criteria are met, and **the path to a real
ship verdict is `ceh-evaluation:evaluate-skill`** (which adds behavioral lift + confirmation).

---

## Phase 0 — Intake

1. **Locate the target.** A skill is a `SKILL.md` plus its directory; a plugin is a directory with
   `.claude-plugin/plugin.json` and one or more `skills/`. If the user names a path, use it; otherwise
   glob for the most recently changed `SKILL.md` / `plugin.json` and confirm in one line.
2. **Read it fully** — body, frontmatter, every `references/` file; for a plugin, the manifest and
   each skill.

For a **plugin** target in lite mode: structural checks on the manifest + the cross-skill collision
check (do two descriptions claim overlapping trigger moments?) + lite triggering/content on the
most-changed skill. Skip the per-skill behavioral sweep.

---

## Phase 1 — Derive criteria

Extract, into the report:

- **Claim** — what does this skill enable, in one sentence?
- **Trigger intent** — when _should_ it fire, and when should it explicitly _not_ (near-misses that
  share keywords but need something else)?
- **Intended outcome** — what an agent following it produces that one without it would not. (Recorded
  for context; lite does not measure it — that is behavioral lift.)

Then build the one battery lite needs:

- **Trigger battery** — 6–8 positive prompts (varied phrasings, including some that don't name the
  skill) and 6–8 genuinely tricky near-miss negatives (share keywords but should not fire). Realistic
  and specific — file paths, real context, lowercase, typos — not abstract. Obvious negatives test
  nothing. (Method detail in the shared `eval-rubric.md`.)

Show the user the derived criteria and the battery in one line — _"here's what I'll check and the
trigger prompts; adjust?"_ — then write the draft `SKILL_EVAL.md` (shared schema) with
`eval_gate: 0/6`, `mode: lite`, and proceed.

---

## Phase 2 — Run the three cheap dimensions

Put raw outputs in the run folder's `iteration-<N>/` subdirectory.

### 1. Structural integrity (deterministic, inline)

Check directly — no subagent. Frontmatter parses; `name` present and matches the directory;
`description` present and non-trivial; body more than a stub; `references/` holds only schemas or
templates. For a **plugin** also: `plugin.json` present and valid, `name` matches directory, `version`
is semver, and (if the repo uses one) the marketplace entry exists with a matching version. Record
each as pass/fail with the specific evidence. If a repo `validate.py` exists, run it as a cross-check.

### 2. Triggering accuracy (cold subagents, N=1)

Use the **exact cold-invocation protocol** in `../evaluate-skill/references/eval-rubric.md` Part 2
("Running it"), but run each prompt **once** (N=1) instead of N=3 — lite changes only the repetition
count, never the protocol. In particular: hand each fresh subagent **only the user prompt** and
observe whether the skill fires while it handles the task; **do not** ask it which skills it would
load — that priming inflates the positive rate and is precisely what makes a lite number diverge
from a full run. Report positive trigger rate and near-miss false-positive rate separately. N=1 is a
sanity read, not a statistic — say so; if a result looks borderline, or disagrees with a prior full
run, note it as worth an N=3 re-check in the full skill rather than trusting the single run.

> Triggering note: the model only consults a skill for tasks it can't trivially handle alone. Make
> positive prompts substantive enough that consulting the skill is plausibly worthwhile — a one-step
> "read this file" won't fire any skill regardless of description quality.

### 3. Content quality (LLM-judged against the shared rubric)

Judge the body against `../evaluate-skill/references/eval-rubric.md`: is it the _delta_ the model
doesn't already know, or a restatement? Framed as a moment (verb/context) or a topic? Within size
norms and using progressive disclosure? Does it explain _why_ rather than pile on ALL-CAPS MUSTs?
Cite specific lines as evidence — quotes, not vibes.

---

## Phase 3 — Report & score the measurable criteria

Fold the run evidence into `SKILL_EVAL.md` following the shared schema
(`../evaluate-skill/references/eval-report-schema.md`) — one question-headed section per dimension
measured, written for a reader who has never heard of the target. Score the four criteria lite can
measure (definitions in the same file):

1. **Structurally valid** — all deterministic checks pass.
2. **Triggers on intent** — positive trigger rate ≥ threshold (single-pass).
3. **Doesn't over-trigger** — near-miss false-positive rate ≤ threshold.
4. **Content is delta + moment-framed** — rubric pass, within size norms.

Criteria **5 (behavioral lift)** and **6 (user confirms)** stay **unproven** — answer them
**Not measured** in the gate table, never **Yes**. Set `eval_gate: N/6` counting only criteria 1–4
as potentially met (max `4/6`).

A criterion is **met by evidence** — a trigger count, a cited line — never by assertion. **Do not
emit a fabricated composite score.** Tell the user the current count and the single
highest-leverage gap among criteria 1–4; that gap drives Phase 4.

---

## Phase 4 — Revise

Fix the named gap (a sharper description for a triggering miss, cutting restated content, adding the
missing delta). Re-run **only the affected dimension** into a new `iteration-<N+1>/`, re-score, and
report what moved (e.g. _"description tightened — positive trigger rate 5/8 → 7/8; lowest now is
content restating general knowledge in lines 40–55"_). Return to the new lowest of criteria 1–4.

When criteria 1–4 are met, **stop and hand off**: state that structure, triggering, and content are
clean, and that behavioral lift remains unproven — run `ceh-evaluation:evaluate-skill` for the full
ship verdict. Leave `status: draft` (lite never sets `passed`).

---

## Stop Conditions

- **The target's claim is incoherent or duplicates an existing skill** — say so directly; the fix is
  upstream of evaluation (rewrite or delete, not measure).
- **A plugin has two skills whose trigger moments collide** — flag the collision; per-skill tuning
  won't fix overlapping descriptions.
- **The user actually wants a ship verdict** — behavioral lift is the point and lite can't provide
  it; hand off to `ceh-evaluation:evaluate-skill` rather than stretching lite.

---

## Edge Cases

**Brand-new skill with no usage:** the normal case — derive criteria from the text and measure via
simulation.

**Borderline triggering at N=1:** report it honestly and recommend an N=3 re-check in the full skill;
don't silently treat one run as conclusive.

**No subagents available (e.g. Claude.ai):** run triggering inline yourself one prompt at a time —
less rigorous (you carry the skill's context), but a useful sanity check. Say so and lower confidence
on that dimension.
