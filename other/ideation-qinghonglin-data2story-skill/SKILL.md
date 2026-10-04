---
name: ideation
description: "Front stage for /data2story-pro when the reader has no dataset — only a vague idea. Converges the idea into a concrete, data-backed topic through a sparring-partner dialogue (anti-sycophantic, feasibility-pressure-tested), then acquires a REAL dataset through find-data, with a user checkpoint after each. Returns a validated DATA_DIR for the main pipeline. Not a newsroom role — runs upstream of Detective, before any dataset exists. Real data only; never a reason to synthesize data."
argument-hint: "<free-text idea> <DATA2STORY_ROOT>"
allowed-tools: Skill, Read, Write, Bash(*), Glob, Grep, AskUserQuestion
---

# Ideation — from a vague idea to a data-backed topic + a real dataset

The `/data2story-pro` orchestrator routes here in **IDEA MODE**: the reader handed over a hunch, a
question, or a half-formed angle instead of a dataset. Your job is to turn that into a concrete
topic that *real, findable data* can support, fetch that data, and hand a validated folder back to
the pipeline. You do this WITH the reader, not for them — two real checkpoints, no railroading.

You are not a pipeline role (no `*_NN` provenance prefix, no place in the 7 teams). You run once,
before Detective, and produce nothing that reaches the HTML except the dataset + a `story_brief`.

## Inputs
- `$1` = the reader's raw idea text (may be empty → open by inviting it).
- `$2` = `DATA2STORY_ROOT` (resolved by the orchestrator; where `data/<slug>/` will live).

## Return contract (how the orchestrator continues)
- **Success:** emit a final line `DATA_DIR=<absolute path to the validated dataset folder>`. The
  `story_brief.json` sits at `<DATA_DIR>/meta/story_brief.json`. The orchestrator sets
  `DATA_DIR`/`DATA_NAME` from this and enters the normal pipeline (Detective → … → Inspector).
- **Abort:** emit `IDEATION_ABORTED: <one-line reason>` (reader stopped, or no real dataset supports
  the idea after the bounded loop). The orchestrator halts honestly and runs NO pipeline. Never
  fabricate data to manufacture a success.

## The flow — 3 steps, 2 checkpoints

**Interaction style — let the reader CHOOSE, don't make them compose.** Drive the convergence
and BOTH checkpoints with `AskUserQuestion`: frame the angles / scope / data-forks as options the
reader clicks, not paragraphs they must write — picking is far lower-friction and each question
doubles as a micro-checkpoint. ALWAYS keep the **Other / free-text** escape open: the menu is your
framing, and the reader's own off-menu angle is often the best one, so never let it cage the
brainstorm. (This is NOT the cold opening questionnaire `sparring-partner` warns against — it is
choice-driven convergence *after* you have framed the space: lead the very first turn with
substance + an open invite, then switch to options.)

### Step 1 — Converge the idea (reuse `sparring-partner`)
Run the brainstorming dialogue by following **`Skill sparring-partner`** with the mission in
[`references/sparring_brief.md`](references/sparring_brief.md): drive the reader from a vague idea to
ONE concrete data-story topic. Two non-negotiables on top of sparring-partner's normal process:
- **Anti-sycophancy** (its core stance) — do not rubber-stamp the first pretty idea.
- **A feasibility pressure-test** — relentlessly ask *does this data actually exist? at what
  granularity? who publishes it? for which years/places?* A beautiful idea with no obtainable data
  is a **failure** of this step, not a success. Steer toward a nearby idea the data CAN support.

The terminal of the dialogue is the **`story_brief`** (contract: [`references/schema.json`](references/schema.json)) —
topic, angle, audience, the questions the data must answer, a structured `data_needs` spec, any
**real** candidate sources surfaced, and the exact `find_data_invocation.query`. Reply in the
reader's language (sparring-partner's rule).

### CHECKPOINT 1 — confirm the brief
Show the reader the assembled `story_brief` (at least `topic`, `angle`, `data_needs`, and
`find_data_invocation.query`). Use `AskUserQuestion` (approve · edit · abort) or a plain confirm.
Loop back into Step 1 on edits. Do not proceed until the reader approves the brief. On abort →
return `IDEATION_ABORTED: reader stopped at brief`.

### Step 2 — Acquire a REAL dataset (reuse `find-data`, web-first)
Derive a kebab-case `slug` from `story_brief.topic`; set `OUT_DIR` to the ABSOLUTE path
`$2/data/<slug>` (resolve `$2` to an absolute path first). Then follow **`Skill find-data`** with the
brief's query and ALWAYS pass that explicit `--out OUT_DIR` — never rely on find-data's bare default
(its default is `DATASETS_ROOT/<name>`, a DIFFERENT root: `./datasets/<name>`, not `data/<slug>`).
An explicit `--out` always wins, so the dataset is guaranteed to land at the path ideation chose:

```
Skill find-data "<story_brief.find_data_invocation.query>" --out OUT_DIR [--mode <single|theme>] [other flags]
```

find-data searches (web-first on an open-source machine with no local corpora), fetches, and runs
its 4 completeness gates, writing `OUT_DIR/validate.json`. Read that file back for the verdict. The
dataset files land directly under `OUT_DIR`, and the `DATA_DIR` returned to the orchestrator (the
success line below) is exactly that absolute `OUT_DIR` — not find-data's default location.

**Bounded acquisition loop (≤ 2 attempts).** If find-data returns BLOCKED / no adequate dataset:
1. Surface honestly what was and wasn't found (the failing gates).
2. Offer the reader: **(a)** re-enter Step 1 to pivot/narrow the topic (often the data exists only
   at a coarser granularity — adjust the brief), **(b)** try an alternate real source/query, or
   **(c)** abort.
3. Never invent a dataset, a source URL, or a license to "succeed."

After 2 failed attempts with no path forward → return `IDEATION_ABORTED: no real dataset supports
this idea (closest gap: <gate>); suggested pivot: <one line>`.

### CHECKPOINT 2 — confirm the dataset
Show the reader the fetched files + the gate verdict, and check them against `story_brief.acceptance`
(does it actually have the entities / metric / coverage you agreed on?). `AskUserQuestion`
(use it · send back to Step 2 · abort). Do not proceed until approved.

### Step 3 — Finalize + hand off
Only AFTER find-data's audit has run (so it never lands inside the data-file glob), write the
approved brief to `OUT_DIR/meta/story_brief.json`:

```bash
mkdir -p "OUT_DIR/meta" && # write story_brief.json there (valid JSON matching references/schema.json)
```

It carries the reader's intent into provenance; the Detective MAY read it for human-intent context
(loose coupling — not required). Then emit the success line:

```
DATA_DIR=OUT_DIR
```

## Guardrails
- **Real data only.** No synthesis, no simulated rows, no fabricated source URLs or licenses — that
  would break the whole verifiability premise. "Can't find data" is an honest `IDEATION_ABORTED`,
  not a reason to invent it.
- **Checkpoints are real stops.** The reader drives; you converge with them, not at them.
- **Portability.** No hardcoded machine paths — derive everything from `$2` and the resolved skill
  dir. Works on a fresh open-source clone with no local data corpora.
- **Stay in your lane.** You write only inside `OUT_DIR` (the dataset folder). You do not build HTML,
  run the pipeline, or touch any role artifact — that's the orchestrator's job after you return.

## Reference files
- [`references/schema.json`](references/schema.json) — the `story_brief` contract (annotated example).
- [`references/sparring_brief.md`](references/sparring_brief.md) — the specialized mission handed to
  `sparring-partner`, with the feasibility pressure-test and a worked vague-idea → brief example.
