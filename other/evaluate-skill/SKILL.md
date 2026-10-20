---
name: evaluate-skill
disable-model-invocation: true
description: >-
  Evaluate a Claude Code skill or plugin you just wrote or changed, to find out whether it is any
  good before you ship it. Reads the target, derives per-target success criteria, runs an
  evidence-based battery (structural integrity, triggering accuracy, content quality, behavioral
  lift vs a no-skill baseline), then loops fix → re-run until a 6-point readiness gate passes and
  you confirm. Self-contained: uses skill-creator and plugin-dev only as optional cross-checks,
  never required. Not for writing a skill from scratch (use authoring) or general app code review
  (use ceh-git-workflow:code-review).
effort: xhigh
argument-hint: "[skill-or-plugin-path]"
---

# Evaluate Skill

Produce an **evidence-based verdict** on a Claude Code skill or plugin — one whose quality has been
measured, not asserted. The deliverable is a single living `SKILL_EVAL.md` in the current evaluation
run's folder under `.agents_workspace` (see Output location), revised in place across a fix/re-run
loop until it passes a 6-point readiness gate and the user confirms. Each fresh evaluation gets its
own indexed run folder, so re-running the skill never overwrites a prior run's report or evidence.

### Output location

All output goes under `.agents_workspace/skill-evals/<target-name>/run-<NNN>/` — never next to the
target itself. `<target-name>` is the skill or plugin name (e.g. `evaluate-skill`, `ceh-evaluation`);
`<NNN>` is a zero-padded sequential run index. `.agents_workspace/` is the standard agent-artifacts
directory at the host repo root; create it and any missing parents if absent.

Each fresh evaluation gets a **new run folder** so prior runs are never overwritten: use the next
integer after the highest existing `run-NNN` for this target (`run-001` if none). Within a run, the
fix/re-run loop revises _that run's_ `SKILL_EVAL.md` in place and adds `iteration-<N>/` evidence
subdirs. The run folder holds both the report and the raw run evidence:

```
.agents_workspace/skill-evals/<target-name>/
├── run-001/
│   ├── SKILL_EVAL.md        # the living report for this run — findings only
│   ├── fixtures/            # inputs: trigger battery, competing descriptions, task fixtures
│   └── iteration-<N>/       # raw run outputs per fix/re-run loop
└── run-002/                 # a later re-evaluation — run-001 left untouched
    └── ...
```

**The report holds findings, never inputs.** Trigger prompts, competitor descriptions and task
fixtures go in `fixtures/`, referenced by path; transcripts and generated artifacts go in
`iteration-<N>/`. A reader opening `SKILL_EVAL.md` wants to know whether the target ships, and every
line of test design between them and that answer is a line they scroll past.

The reason this skill exists: a skill that "looks fine" on read often under-triggers, restates what
the model already knows, or makes no measurable difference to outcomes. You only learn which by
running it — firing it against realistic prompts and comparing what happens with and without it.
This skill is that measurement, made disciplined.

The core stance: **derive criteria from the target, then measure against evidence**. There is no
universal metric for "a good skill" — what success means depends on what _this_ target claims to do.
So the first move is always to read the target and extract its own success criteria; everything
after measures against them. The _process and report are fixed; the criteria are derived._

---

## What "golden standard" means here

Two layers, in priority order:

1. **The target's own derived criteria** — what it claims to do, when it should trigger, what
   outcome following it should produce. These are generated per target in Phase 1 and are the
   primary bar.
2. **General authoring principles** — the portable, tool-agnostic rules in
   `references/eval-rubric.md` (triggers on moments not topics, description is the trigger
   mechanism, body is the delta the model doesn't already know, progressive disclosure, explain the
   why over heavy MUSTs, least surprise). These are distilled _from_ the Anthropic skill-creator and
   plugin-dev plugins as reference material — not imported as authority.

If a **host-repo `CLAUDE.md`** exists, fold its conventions in as _additional, lower-priority_
criteria — opportunistic, never required, never the focus. This skill is portable; it must not
depend on any one repo's standards.

External tools (`skill-creator`, `plugin-dev:*`, a repo's `validate.py`) are **optional
cross-checks** — invoke them only if detected, treat their output as evidence, and when they
disagree with your finding, investigate the disagreement rather than deferring. Never auto-fail or
auto-pass on their say-so. The evaluation runs to completion with built-in tools alone.

---

## The Loop

```
Phase 0  Intake     → locate & read the target; detect optional cross-check tools
Phase 1  Derive     → extract claims; build the trigger battery, behavioral tasks, and assertions;
                      draft SKILL_EVAL.md
Phase 2  Run        → measure all four dimensions; subagents for triggering & behavioral, N runs,
                      capture variance
Phase 3  Report+Gate→ aggregate evidence into the report; score the 6-point gate; name the ONE
                      highest-leverage gap
Phase 4  Revise     → fix that gap; re-run only the affected dimension; re-score
         ↑__________ repeat Phase 2–4 (affected dimension only) until gate passes AND user confirms
Phase 5  Validate   → flip status: passed; hand off remaining advisory findings
```

Like a good interview, **the lowest-scoring dimension picks the next fix** — never a fixed checklist
march. Each loop closes one gap.

---

## Scoped run — behavioral lift only

The full loop measures all four dimensions; `ceh-evaluation:evaluate-skill-lite` measures the three
cheap ones (structural + triggering + content). The one dimension neither cheap path gives you is
**behavioral lift** — so that is the only thing worth scoping here.

When the user asks "just check if it actually helps" (and doesn't want the full battery), run
**dimension 4 only** — 1 task, with-skill vs baseline, N=1 (~2 subagent calls + grading). Report the
assertion delta and say so in the report. This is a sanity read, not the gate: N=1 is noise, re-run
at N≥3 before trusting it, and it never sets `status: passed`.

For triggering, structure, or content in isolation, use `evaluate-skill-lite` rather than this skill.
For all four dimensions with variance and the full 6-point gate, run the loop above.

---

## Phase 0 — Intake (read before measuring)

1. **Locate the target.** A skill is a `SKILL.md` plus its directory; a plugin is a directory with
   `.claude-plugin/plugin.json` and one or more `skills/` (and possibly `agents/`, `hooks/`). If the
   user names a path, use it; otherwise glob for the most recently changed `SKILL.md` /
   `plugin.json` and confirm the target in one line.
2. **Read it fully** — the `SKILL.md` body, frontmatter, every `references/` file, and for a plugin
   the manifest and each skill/agent.
3. **Detect optional cross-checks** (do not require any): a `validate.py` / validation script in the
   repo, the `skill-creator` skill, the `plugin-dev:*` agents. Note which are available; you will
   run them as confirmation in Phase 2 only where cheap.
4. **New run vs. resume.** Default to a **new run folder** (next `run-NNN`) so a re-evaluation never
   overwrites prior evidence. Only resume the latest existing run — reusing its folder instead of
   creating a new one — when its `SKILL_EVAL.md` is still `status: draft` and the user is continuing
   an interrupted loop; then read it, re-score the gate, and resume at the lowest-scoring dimension.
   A re-evaluation of an already-passed (or otherwise completed) target always starts a fresh run.

For a **plugin** target, the evaluation is: manifest/structural checks + run the per-skill
evaluation for each skill + a cross-skill collision check (do two descriptions claim overlapping
trigger moments such that the wrong one fires?). Evaluate the riskiest/most-changed skill in depth;
sample the rest.

---

## Phase 1 — Derive criteria (the open-ended part)

Read the target and extract, in the report:

- **Claim** — what does this skill enable, in one sentence?
- **Trigger intent** — when _should_ it fire, and when should it explicitly _not_ (the near-miss
  cases that share keywords but need something else)?
- **Intended outcome** — what does an agent that follows this skill produce that one without it
  would not?

From those, generate the three test inputs the run phase needs:

1. **Trigger battery** — 8–10 positive prompts (varied phrasings, casual and formal, including ones
   that don't name the skill) and 8–10 near-miss negatives (share keywords/concepts but should not
   fire). Make them realistic and specific — file paths, real context, typos, lowercase — not
   abstract. Obvious negatives ("write a fibonacci function" for a PDF skill) test nothing; the
   negatives must be genuinely tricky. (Method detail in `references/eval-rubric.md`.)
2. **Behavioral tasks** — 2–3 realistic tasks that exercise what the skill claims to improve.
3. **Assertions** — per task, objectively verifiable statements that are true only if the skill
   genuinely worked (not surface compliance). A discriminating assertion passes when the skill
   succeeds and fails when it doesn't.

Show the user the derived criteria and the batteries: _"Here's what I'll measure and the test
prompts — do these match your intent, or adjust?"_ Bad test inputs produce a worthless evaluation,
so this checkpoint matters. Save the batteries and fixtures to the run folder's `fixtures/`, then
write the draft `SKILL_EVAL.md` (schema in `references/eval-report-schema.md`) to the current run
folder (`.agents_workspace/skill-evals/<target-name>/run-<NNN>/`) with `eval_gate: 0/6` and proceed.

---

## Phase 2 — Run the battery

Put raw run outputs in the current run folder's `iteration-<N>/` subdirectory
(`.agents_workspace/skill-evals/<target-name>/run-<NNN>/iteration-<N>/`) so the report stays readable
and the evidence stays auditable. Measure four dimensions.

### 1. Structural integrity (deterministic, inline)

Check directly — no subagent. Frontmatter parses; `name` is present and matches the directory;
`description` is present and non-trivial; body is more than a stub; `references/` holds only schemas
or templates (not prose dumps). For a **plugin** also: `plugin.json` present and valid, `name`
matches directory, `version` is semver, and (if the repo uses one) the marketplace entry exists and
its version matches. Record each as pass/fail with the specific evidence. If a repo `validate.py`
exists, run it as a cross-check and reconcile any disagreement.

### 2. Triggering accuracy (cold subagents)

Run each battery prompt through a **fresh subagent** that has the skill available, and record
whether the skill fired. Cold subagents matter — they have none of your context, so they reflect
real triggering. Run each prompt **N=3 times** (triggering is probabilistic) and record the trigger
rate. Report positive trigger rate and near-miss false-positive rate separately.

> Triggering note: the model only consults a skill for tasks it can't trivially handle alone. Make
> behavioral and positive-trigger prompts substantive enough that consulting the skill is plausibly
> worthwhile — a one-step "read this file" won't fire any skill regardless of description quality.

### 3. Content quality (LLM-judged against the rubric)

Judge the body against `references/eval-rubric.md`: is it the _delta_ the model doesn't already
know, or a restatement of general knowledge? Framed as a moment (verb/context) or a topic? Within
size norms and using progressive disclosure? Does it explain _why_ rather than pile on ALL-CAPS
MUSTs? Cite specific lines as evidence for each judgment — quotes, not vibes.

### 4. Behavioral lift (with-skill vs baseline, the expensive one)

For each behavioral task, spawn **two subagents in the same turn**: one with the skill available,
one with no skill (the baseline). Instruct each subagent to write **any code or files it produces
only under this run's `iteration-<N>/generated/` folder** — never in the host repo or next to the
target — so the working tree stays clean and the generated artifacts remain auditable evidence.
Save both transcripts to the workspace. Then **grade** each output
against that task's assertions — pass/fail with a cited quote from the transcript or output as
evidence; a file that exists but has wrong content is a fail. Run each task **N times** and report
the spread, because a single run is noise. The finding is the _difference_: does with-skill clear
assertions the baseline misses, and is that difference stable across runs?

> This is noisy and the costliest dimension. Report variance honestly. "Helps 3/4 runs, no
> regression on the 4th" is a real, reportable result — do not collapse it to a single number.

---

## Phase 3 — Report & score the gate

Fold the run evidence into `SKILL_EVAL.md` following `references/eval-report-schema.md` — which
carries the section order, the gate table, and the seven rules that keep the report readable. Write
it for **someone who has never heard of the target**: say what the target does before reporting
anything about it, head each dimension with the question it answers, state what every number is out
of, and quote the failure rather than only counting it. That reader is the point; an evaluation
nobody reads has measured nothing.

Then score the **6-point readiness gate** (full definition in the schema):

1. **Structurally valid** — all deterministic checks pass.
2. **Triggers on intent** — positive trigger rate ≥ threshold across runs.
3. **Doesn't over-trigger** — near-miss false-positive rate ≤ threshold.
4. **Content is delta + moment-framed** — rubric pass, within size norms.
5. **Behavioral lift** — with-skill beats, or at minimum does not regress, baseline on the derived
   assertions, with acceptable run-to-run variance.
6. **User confirms.**

All six go in the report's gate table, each carrying its formal name, the plain question, the
answer (**Yes** / **No** / **Not measured**), the measurement in words, and a remark. The remark is
`—` unless the criterion is qualified — proxied, inherited from an earlier run, waived, or passed
against a loosened threshold. A remark records a _qualified_ Yes; a criterion that fails outright is
a **No**, not a Yes with an excuse.

A criterion is **met by evidence** — a trigger count, a cited line, a with/baseline delta — never by
assertion. **Do not emit a fabricated composite score** (no "Quality: 87/100"). The gate count
(`eval_gate: N/6`) is the only summary number; everything else is evidence and pass/fail. A
plausible-looking number you can't defend is worse than an honest "criterion 5 is unproven."

Tell the user, in one or two lines, the current gate score and the **single highest-leverage gap** —
the one fix that would move the most. That gap drives Phase 4.

---

## Phase 4 — Revise

Fix the named gap — either you propose and apply the fix (a sharper description for a triggering
miss, cutting restated content, adding the missing delta) or the author does. Then **re-run only the
affected dimension** into a new `iteration-<N+1>/`, re-score the gate, and report what moved
(e.g. _"Description tightened — positive trigger rate 6/10 → 9/10, false-positives still 0. Lowest
now is criterion 5: behavioral lift is unproven. Re-running that next."_).

Return to the new lowest-scoring dimension. This is the loop the goal demands: measure → fix →
re-measure, until the gate is satisfiable.

### When a dimension can't be measured

Behavioral lift on a niche skill may be hard to simulate cheaply. Don't stall the loop: state the
limit honestly in the report, run the cheapest meaningful proxy you can, and mark the criterion as
**unproven** rather than passing it on faith. An honest "unproven" beats a fabricated pass.

---

## Phase 5 — Validate & hand off

When all 6 criteria are met **and** the user confirms:

- Flip frontmatter `status: passed`, set `eval_gate: 6/6`, stamp `updated`.
- Give a one-paragraph verdict: what the skill does, the evidence it triggers and helps, and the one
  change that would most improve it next.
- List remaining **advisory** findings (non-blocking improvements) so the author has a backlog.

**Do not flip to passed to end the loop early.** If the user wants to stop before the gate passes,
leave `status: draft`, record the open criteria honestly, and say plainly which dimensions are
unproven — an honest draft beats a report claiming a quality it didn't measure.

---

## Stop Conditions

- **The target's claim is incoherent or the skill duplicates an existing one** — say so directly; the
  fix is upstream of evaluation (rewrite or delete, not measure).
- **A plugin has two skills whose trigger moments collide** — flag the collision; no amount of
  per-skill tuning fixes overlapping descriptions.
- **Behavioral simulation is impossible to make meaningful** for this target — report it as a limit,
  evaluate the other three dimensions, and mark criterion 5 unproven rather than faking it.

---

## Edge Cases

**Target is a brand-new skill with no usage:** that's the normal case — derive criteria from the
text and measure via simulation. No history is needed.

**Plugin with many skills:** evaluate the most-changed/riskiest skill in full, sample the others for
structural + triggering, and always run the cross-skill collision check.

**No subagents available (e.g. Claude.ai):** run triggering and behavioral checks inline yourself
one prompt at a time — less rigorous (you have the skill's context), but a useful sanity check.
Say so in the report and lower confidence on those dimensions accordingly.
