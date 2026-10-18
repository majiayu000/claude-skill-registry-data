---
name: clink-masteragent
description: What a master agent owns and can never delegate, and how to pick the model for a delegation from measured scores instead of memory. Use before any clink delegation, and whenever choosing between models, efforts, or clients — including "which model should review this", "is the cheap one good enough", "should I escalate the effort". Carries the full per-axis score table for every reachable model+effort inline, generated from the structured source, so the choice is made against data rather than recollection. Pairs with clink-subagents (handing out work), clink-brainstorm (convening judgment), and clink-debug (hunting a bug).
---

# clink-masteragent

> **Requires [PAL MCP server](https://github.com/BeehiveInnovations/pal-mcp-server)** with `clink` configured. This skill is the selection and ownership layer under [`clink-subagents`](../clink-subagents/SKILL.md), [`clink-brainstorm`](../clink-brainstorm/SKILL.md) and [`clink-debug`](../clink-debug/SKILL.md) — it decides *who* and *what you keep*, they decide *how*.

## Why this exists

**A master agent picks the model for a delegation from memory, because there is nowhere to look it up.** That is demonstrated, not theorised: during the work that produced this skill, the orchestrating agent chose a model for a review panel from a recollection of an earlier failure rather than from any score. Checked afterwards against the data, the model it picked was **weaker on the axis the task actually needed** — it won on hallucination-resistance, which the prompt had already neutralised by forbidding tool use, and lost by 3.6 points of composite intelligence and nearly 2× on agentic ability, which was live.

So the score table is **in this file**, below the guidance, rather than in a document you would have to decide to open. Falling from a recommendation to the evidence is a scroll, not a decision.

## What the master owns and can never delegate

| Kept | Why it cannot be handed out |
|---|---|
| **Decomposition** | Choosing what the leaves *are* is the design. A worker given the wrong leaf does it perfectly. |
| **Integration** | Only the master holds the whole change; a worker sees its own diff. |
| **Final verification** | The buck stops here. A subagent's report is a hypothesis until checked — a worker in this repo's own history claimed a merged PR that did not exist, and `git` disproved it. |
| **Security and trust boundaries** | Auth, secrets, permissions, entitlement paths. Blast radius, not diff size, decides. |
| **Anything you cannot check** | If you cannot verify the output, delegating it converts an unknown into a false confidence. |
| **Building the delegation contract** | The `BrainstormRequest v1` states the objective, the scope the worker may not leave, and what is fact versus assumption. Handing that authoring to the worker asks it to decide what it was supposed to be constrained by. Shape: [`clink-brainstorm/references/request-v1.md`](../clink-brainstorm/references/request-v1.md). |

**A delegated green is not a green.** Two failures seen in this repo, both from workers that did good work otherwise: a test that pinned message *wording* rather than behaviour (the suite passed either way; only reading it found the problem), and a suite in which no test had ever been observed to fail, because the prompt asked for "the function and its tests" in one pass. **Ask for the RED first, and require the failing output back before the implementation exists.** Then mutate: mutation is what converts a delegated green into evidence.

**And a delegated RED is not a red.** That advice was followed exactly on 2026-08-05 and was still not enough. Two leaves went out **at the same moment**, to `gpt-5.6-luna` at `high`, same prompt shape, both asked for the red only. The code leaf came back with a good test. The prose leaf came back with **11 assertions**, each a `grep` for a sentence the worker had *invented* — it ran, exited 1, and **reproduced on the orchestrator's machine exactly as reported.** The result was real; the test was worthless, because the fix it demanded was *"paste these strings into the file"*, and it would have gone green on a change that added the sentences and nothing else.

So **re-running a delegated red is not the check — reading what the assertion is anchored to is.** A reproducing red proves only that the assertion fails today; it says nothing about whether the assertion is *about* anything. Demand anchors that are **facts a reader can check against reality** — a real flag, a measured count, a returned value — never a wording the worker chose. This repo's own `tests/skills/test-agy-effort-flag.sh` is the standard: it asserts on `--effort`, its three rungs, and the measured `446`.

Two more tells, both shipped in that same file:

- **A "control" that is trivially true forever.** Its two passing checks were `[ -f "$FILE" ]` on files months old. A real control asserts a *behaviour* that holds before **and** after, so an over-broad fix breaks it.
- **Positive assertions with no negative check.** It defined a `hasnt` helper and never called it, so a partial edit adding the new wording *beside* the old, wrong wording would pass.

**And a delegated detector is neither.** When what comes back *reports on* something rather than *doing* something — a linter, a scanner, a coverage report, an audit, a review — the green/red rules do not bite, because such a thing can run, exit 0, and produce a report in which **nothing is false and nothing is useful.** Two checks, both measured 2026-08-05:

- **Are the findings over-broad?** A delegated audit called **30 of 32** suites defective — it flagged suites with *no assertions at all*, and every anchor containing no space, which condemns `446`: a measured token count and one of the best anchors in that repo. Corrected, **the real number was 11**. A reviewer trusting the count would have been sent to 19 healthy suites. **False positives are not the safe direction** — a critic that cries wolf **gets switched off**, and its true findings go with it.
- **Was the clean result probed?** The corrected detector then reported **0 findings**, which reads as good news and is worth nothing alone: it is **indistinguishable from a detector that stopped working**. So **make it dirty on purpose** — feed it one known defect, watch the count go `0 → 1`, delete the probe. A scan you have not seen find something has not been shown to find anything.

**The second occurrence was self-inflicted**, and that is the part to keep: the replacement detector, written by the agent that had just criticised the first, repeated the same over-broad flagging one layer down. **Over-broad flagging does not respect who is writing.**

## Choose the axis before the model

**Never rank candidates by the composite Intelligence Index alone.** Measured from Artificial Analysis' own methodology page (Index v4.1):

| Category | Weight | Uses tools |
|---|---|---|
| Agents | 34% | ✓ |
| Coding | 24% | ✗ |
| Scientific Reasoning | 24% | ✗ |
| General | 18% | ✗ |

**Only 34% of the composite is measured with tools in the loop.** The other 66% is single-shot question answering. A delegation is an agentic task, so ranking candidates by the composite imports a two-thirds majority signal about something the delegation is not.

Two consequences worth holding:

- **Hallucination enters the composite at 4%** (as `1 − hallucinationRate` inside AA-Omniscience, itself 12%). So models can differ ~4× on non-hallucination while their composites differ by ~2 points. **Read that column; never infer it from the index.**
- **A high non-hallucination score can mean the model simply does not know.** It is a refusal-to-invent measure, not a knowledge measure. Rank on the composite *and* the axis, never the component alone.

**Different models lead different axes.** In the table below the leaders are not one model — Claude Opus 5 leads Index, Agentic and GDPval; GPT-5.6 Sol leads Coding and Terminal-Bench; GLM-5.2 leads non-hallucination; **Kimi K3 at `low` effort** leads τ-Banking. Any document naming one "best model" is wrong for most tasks.

**Enumerate every row that clears the bar before choosing.** Taking the first model over the line is how a far cheaper equal gets missed — that is what the `$/pt` column is for.

## Instrument constraints come first

The three instrument skills filter which routes are eligible **before** any general preference here applies, because their selection functions differ in kind:

- [`clink-brainstorm`](../clink-brainstorm/SKILL.md) — a panel's choice depends on which round it is and whether positions have converged. The small model has no place on a panel; the deliverable is reasoning.
- [`clink-subagents`](../clink-subagents/SKILL.md) — buying throughput on verifiable leaves, so the cheap tier is usually right.
- [`clink-debug`](../clink-debug/SKILL.md) — **provenance is a hard exclusion**: never ask the lineage that proposed a hypothesis to falsify it.

A cheap general preference never overrides a specific prohibition.

## Delegation lifecycle

Applies whichever instrument you chose. Each item is marked **[D]** discipline you must keep yourself, or **[T]** a tool capability — with the issue where it does or does not yet exist.

| | Step | |
|---|---|---|
| A | **Acceptance** — write the success criterion before the call. Exploratory work gets required questions and evidence standards instead of pass/fail tests. | [D] |
| B | **Feasibility** — a read-heavy delegation takes 400–530s against a real repo. Under a 60–120s transport ceiling that is **infeasibility, not latency**. | [D] |
| C | **Ops preflight** — which quota lane does this spend? Prefer each client's house lane. | [D] |
| D | **Containment** — an isolated workspace, not a shared tree; two subagents can otherwise mutate one checkout. | [T] `pal#20` — **does not exist yet** |
| E | **Selection** — axis → harness → context → model+effort → right-size to the cheapest point that clears the bar. Escalate only after a real failure. | [D] |
| F | **Prompt and output contract** — the worker has zero conversation context. Absolute paths, the exact I/O contract, "return ONLY X". | [D] |
| G | **Dispatch safety** — run id, idempotency key, process-tree ownership, bounded I/O. A retry without an idempotency key double-launches. | [T] `pal#20` — **does not exist yet** |
| H | **Recovery** — a timeout is not a death certificate; the child may still be running. | [T] `pal#20` |
| I | **Promotion** — derive what changed from the workspace; an agent-authored manifest is not authoritative. | [D] |
| J | **Master verification** — yours, always. Mutate a delegated core. | [D] |

**The [T] rows are the honest part of this table.** Those protections are described in `pal-mcp-server#20` and are *not implemented*. Until they are, treat them as discipline you keep manually and state that you did — do not read the row as a guarantee.

A related gap worth knowing while you delegate: the model catalog is enforced by reading the command PAL builds, and codex also takes a model from `~/.codex/config.toml` and `--profile`. So a model can arrive with nothing on the argv (`pal-mcp-server#39`).

## Case list

**Not yet written.** #74 specifies narrow cases entered by conjunction — at least three literally-true conditions, an explicit exclusion, ranked fallbacks — and names task verbs as forbidden in case names because a verb matches everything.

Authoring those against this table is the next slice. **Until then the instruction is the fall-through one, which is designed to be the common path anyway: read the table and choose on the axis this task actually needs.** An empty case list is honest; a thin one would be worse, because a tier list that looks complete stops an agent from questioning a case that only nearly matches.

## Evidence — every reachable model and effort

Regenerated by `docs/research/scripts/generate_masteragent.py` from the structured source; `tests/skills/test-figures-sourced.sh` fails if any figure here is not in that file. **Do not edit this block by hand.**

Coverage gaps, stated: AA publishes only the top 25 per axis, so blanks are "not published", never zero. **Nobody benchmarks `antigravity` or `claude-9arm`** — two of five clients have no third-party data at all. Harness choice moves scores about as much as model choice (the same model, same effort, has scored 54.4 via Codex against 46.1 via Cursor CLI), and this table is per-model, not per-harness.

<!-- figures:start source=docs/research/data/aa-models-augmented.csv -->

84 reachable model+effort rows. **Sorted by name — position implies no ranking.**
★ marks the leader of that column. Cost is AA's cost to run the whole Index suite;
**$/pt** is that divided by the index, so a low number is capability per unit spend.

| Model | Index | Agentic | Coding | Non-halluc. | TermBench | τ-Banking | GDPval | Ctx | Cost | $/pt |
|---|---|---|---|---|---|---|---|---|---|---|
| Claude 4 Sonnet (Non-reasoning) | 25.5 | — | — | 0.592 | — | — | — | 1,000,000 | — | — |
| Claude 4 Sonnet (Reasoning) | 28.9 | 16.6 | 37.6 | 0.715 | 0.363 | 0.138 | 0.186 | 1,000,000 | — | — |
| Claude 4.5 Sonnet (Non-reasoning) | 29.3 | — | — | 0.493 | — | — | — | 1,000,000 | — | — |
| Claude 4.5 Sonnet (Reasoning) | 36.4 | 24.6 | 52.1 | 0.526 | 0.558 | 0.190 | 0.276 | 1,000,000 | 1132.85 | 31.11 |
| Claude Fable 5 (Adaptive Reasoning, Max Effort, Opus 4.8 Fallback) | 59.9 | 52.8 | 76.5 | 0.451 | 0.846 | 0.268 | 0.623 | 1,000,000 | 5630.52 | 94.06 |
| Claude Opus 4.5 (Non-reasoning) | 34.7 | — | — | 0.246 | — | — | — | 200,000 | — | — |
| Claude Opus 4.5 (Reasoning) | 40.8 | — | — | 0.402 | — | — | — | 200,000 | — | — |
| Claude Opus 4.6 (Adaptive Reasoning, Max Effort) | 43.7 | — | — | 0.387 | — | — | — | 1,000,000 | — | — |
| Claude Opus 4.6 (Non-reasoning, High Effort) | 37.8 | — | — | 0.240 | — | — | — | 1,000,000 | — | — |
| Claude Opus 4.7 (Adaptive Reasoning, Max Effort) | 53.5 | 44.4 | 73.6 | 0.638 | 0.831 | 0.289 | 0.495 | 1,000,000 | 3737.82 | 69.83 |
| Claude Opus 4.7 (Non-reasoning, High Effort) | 42.7 | — | — | 0.481 | — | — | — | 1,000,000 | — | — |
| Claude Opus 4.8 (Adaptive Reasoning, Max Effort) | 55.7 | 47.2 | 74.3 | 0.641 | 0.846 | 0.276 | 0.545 | 1,000,000 | 3752.55 | 67.38 |
| Claude Opus 5 (Adaptive Reasoning, High Effort) | 58.9 | 52.1 | 76.5 | 0.481 | 0.876 | 0.328 | 0.620 | 1,000,000 | 1973.77 | 33.53 |
| Claude Opus 5 (Adaptive Reasoning, Low Effort) | 50.6 | 39.8 | 66.9 | 0.451 | 0.764 | 0.233 | 0.477 | 1,000,000 | 556.06 | 10.99 |
| Claude Opus 5 (Adaptive Reasoning, Max Effort) | 60.7 ★ | 55.3 ★ | 78.0 | 0.499 | 0.891 | 0.303 | 0.679 ★ | 1,000,000 | 3835.51 | 63.20 |
| Claude Opus 5 (Adaptive Reasoning, Medium Effort) | 56.3 | 47.1 | 74.3 | 0.479 | 0.861 | 0.287 | 0.566 | 1,000,000 | 1114.96 | 19.81 |
| Claude Opus 5 (Adaptive Reasoning, Xhigh Effort) | 60.1 | 54.5 | 77.0 | 0.498 | 0.880 | 0.315 | 0.664 | 1,000,000 | 2909.91 | 48.44 |
| Claude Sonnet 4.6 (Adaptive Reasoning, Max Effort) | 47.2 | 40.8 | 63.0 | 0.539 | 0.712 | 0.305 | 0.438 | 1,000,000 | 3355.85 | 71.08 |
| Claude Sonnet 4.6 (Non-reasoning, High Effort) | 35.9 | — | — | 0.341 | — | — | — | 1,000,000 | — | — |
| Claude Sonnet 4.6 (Non-reasoning, Low Effort) | 34.3 | — | — | 0.404 | — | — | — | 1,000,000 | — | — |
| Claude Sonnet 5 (Adaptive Reasoning, High Effort) | — | — | — | — | — | — | 0.450 | 1,000,000 | — | — |
| Claude Sonnet 5 (Adaptive Reasoning, Low Effort) | — | — | — | — | — | — | 0.357 | 1,000,000 | — | — |
| Claude Sonnet 5 (Adaptive Reasoning, Max Effort) | 53.4 | 46.7 | 71.5 | 0.627 | 0.805 | 0.282 | 0.551 | 1,000,000 | 4010.12 | 75.17 |
| Claude Sonnet 5 (Adaptive Reasoning, Medium Effort) | — | — | — | — | — | — | 0.401 | 1,000,000 | — | — |
| Claude Sonnet 5 (Adaptive Reasoning, Xhigh Effort) | — | — | — | — | — | — | 0.504 | 1,000,000 | — | — |
| Claude Sonnet 5 (Non-reasoning, High Effort) | 41.7 | 33.7 | 66.4 | 0.499 | 0.753 | 0.140 | 0.436 | 1,000,000 | 427.33 | 10.24 |
| Gemini 3 Flash Preview (Non-reasoning) | 27.4 | — | — | 0.098 | — | — | — | 1,000,000 | — | — |
| Gemini 3 Flash Preview (Reasoning) | 37.8 | — | — | 0.078 | — | 0.175 | — | 1,000,000 | — | — |
| Gemini 3.1 Pro Preview | 46.5 | 21.4 | 68.8 | 0.501 | 0.738 | 0.165 | 0.232 | 1,000,000 | 815.11 | 17.54 |
| Gemini 3.5 Flash (high) | 50.2 | 37.4 | 70.1 | 0.393 | 0.787 | 0.254 | 0.421 | 1,000,000 | 1040.88 | 20.73 |
| Gemini 3.5 Flash (medium) | 45.4 | — | — | 0.397 | — | — | — | 1,000,000 | — | — |
| Gemini 3.5 Flash (minimal) | 34.9 | — | — | 0.266 | — | — | — | 1,000,000 | — | — |
| Gemini 3.6 Flash (high) | 50.1 | 38.7 | 69.2 | 0.465 | 0.775 | 0.245 | 0.462 | 1,000,000 | 726.70 | 14.51 |
| GLM-5.2 (max) | 51.1 | 43.1 | 68.8 | 0.719 ★ | 0.779 | 0.268 | 0.505 | 1,000,000 | 1061.18 | 20.77 |
| GLM-5.2 (Non-reasoning) | 34.1 | 34.8 | 46.5 | 0.665 | 0.517 | 0.157 | 0.444 | 1,000,000 | — | — |
| GPT-5 mini (high) | 25.3 | 19.4 | 15.6 | 0.459 | 0.037 | 0.146 | 0.216 | 400,000 | 130.43 | 5.15 |
| GPT-5 mini (medium) | 30.9 | — | — | 0.576 | — | — | — | 400,000 | — | — |
| GPT-5 mini (minimal) | 14.3 | — | — | 0.116 | — | — | — | 400,000 | — | — |
| GPT-5.1 (high) | 36.9 | 21.0 | 49.4 | 0.487 | 0.524 | 0.140 | 0.244 | 272,000 | 779.10 | 21.13 |
| GPT-5.1 (Non-reasoning) | 20.4 | — | — | 0.098 | — | — | — | 400,000 | — | — |
| GPT-5.2 (medium) | 38.0 | — | — | 0.394 | — | — | — | 400,000 | — | — |
| GPT-5.2 (Non-reasoning) | 26.0 | — | — | 0.392 | — | 0.120 | — | 400,000 | — | — |
| GPT-5.2 (xhigh) | 42.2 | — | — | 0.203 | — | — | — | 400,000 | — | — |
| GPT-5.3 Codex (xhigh) | 44.3 | — | — | 0.131 | — | — | — | 400,000 | — | — |
| GPT-5.4 (low) | 39.1 | — | — | 0.189 | — | — | — | 1,050,000 | — | — |
| GPT-5.4 (Non-reasoning) | 27.7 | — | — | 0.168 | — | — | — | 1,050,000 | — | — |
| GPT-5.4 (xhigh) | 51.4 | 41.1 | 71.1 | 0.114 | 0.783 | 0.303 | 0.446 | 1,050,000 | 2185.46 | 42.52 |
| GPT-5.4 mini (medium) | 29.8 | — | — | 0.108 | — | — | — | 400,000 | — | — |
| GPT-5.4 mini (Non-Reasoning) | 16.6 | — | — | 0.047 | — | — | 0.144 | 400,000 | — | — |
| GPT-5.4 mini (xhigh) | 40.0 | 30.2 | 56.1 | 0.102 | 0.592 | 0.214 | 0.335 | 400,000 | 1095.43 | 27.40 |
| GPT-5.4 nano (medium) | 30.2 | — | — | 0.496 | — | — | — | 400,000 | — | — |
| GPT-5.4 nano (Non-Reasoning) | 17.6 | — | — | 0.391 | — | — | — | 400,000 | — | — |
| GPT-5.4 nano (xhigh) | 38.2 | 27.5 | 56.1 | 0.264 | 0.607 | 0.210 | 0.301 | 400,000 | 277.68 | 7.26 |
| GPT-5.5 (high) | 53.1 | 43.5 | 71.6 | 0.143 | 0.794 | 0.295 | 0.483 | 922,000 | 1719.16 | 32.36 |
| GPT-5.5 (low) | 43.5 | 30.4 | 60.9 | 0.140 | 0.655 | 0.212 | 0.343 | 922,000 | 375.23 | 8.63 |
| GPT-5.5 (medium) | 50.4 | 37.8 | 71.5 | 0.137 | 0.805 | 0.258 | 0.436 | 922,000 | 935.77 | 18.56 |
| GPT-5.5 (Non-reasoning) | 35.4 | 25.8 | 56.5 | 0.088 | 0.610 | 0.138 | 0.311 | 922,000 | 211.11 | 5.97 |
| GPT-5.5 (xhigh) | 54.8 | 44.9 | 74.9 | 0.145 | 0.843 | 0.313 | 0.495 | 922,000 | 2777.91 | 50.66 |
| GPT-5.6 Luna (high) | 46.1 | 40.1 | 63.3 | 0.105 | 0.697 | 0.223 | 0.484 | 1,000,000 | 61.13 | 1.33 |
| GPT-5.6 Luna (low) | 33.3 | 25.4 | 44.2 | 0.123 | 0.434 | 0.120 | 0.327 | 1,000,000 | 16.02 | 0.48 |
| GPT-5.6 Luna (max) | 51.2 | 45.6 | 71.4 | 0.099 | 0.809 | 0.272 | 0.541 | 1,000,000 | 190.87 | 3.73 |
| GPT-5.6 Luna (medium) | 38.1 | 31.0 | 50.7 | 0.115 | 0.532 | 0.153 | 0.388 | 1,000,000 | 23.77 | 0.62 |
| GPT-5.6 Luna (Non-reasoning) | 26.6 | 22.0 | 39.3 | 0.265 | 0.390 | 0.091 | 0.286 | 1,000,000 | 14.16 | 0.53 |
| GPT-5.6 Luna (xhigh) | 49.1 | 42.9 | 68.6 | 0.099 | 0.779 | 0.243 | 0.515 | 1,000,000 | 106.08 | 2.16 |
| GPT-5.6 Sol (high) | 55.9 | 48.5 | 77.2 | 0.120 | 0.873 | 0.306 | 0.563 | 1,000,000 | 1159.45 | 20.75 |
| GPT-5.6 Sol (low) | 49.4 | 40.0 | 69.7 | 0.127 | 0.768 | 0.244 | 0.472 | 1,000,000 | 400.42 | 8.10 |
| GPT-5.6 Sol (max) | 58.9 | 54.0 | 77.4 | 0.112 | 0.880 | 0.330 | 0.616 | 1,000,000 | 3442.81 | 58.46 |
| GPT-5.6 Sol (medium) | 53.6 | 44.5 | 76.3 | 0.129 | 0.861 | 0.265 | 0.528 | 1,000,000 | 697.25 | 13.01 |
| GPT-5.6 Sol (Non-reasoning) | 41.2 | 34.9 | 65.1 | 0.087 | 0.742 | 0.161 | 0.438 | 1,000,000 | 299.27 | 7.26 |
| GPT-5.6 Sol (xhigh) | 57.7 | 51.8 | 78.3 ★ | 0.110 | 0.895 ★ | 0.326 | 0.595 | 1,000,000 | 1862.64 | 32.31 |
| GPT-5.6 Terra (high) | 49.0 | 41.3 | 67.1 | 0.125 | 0.757 | 0.223 | 0.505 | 1,000,000 | 469.44 | 9.59 |
| GPT-5.6 Terra (low) | 40.5 | 30.6 | 58.1 | 0.122 | 0.625 | 0.161 | 0.377 | 1,000,000 | 154.79 | 3.83 |
| GPT-5.6 Terra (max) | 55.0 | 47.4 | 76.7 | 0.148 | 0.880 | 0.318 | 0.541 | 1,000,000 | 1607.93 | 29.26 |
| GPT-5.6 Terra (medium) | 45.6 | 37.0 | 64.7 | 0.121 | 0.723 | 0.194 | 0.451 | 1,000,000 | 222.71 | 4.89 |
| GPT-5.6 Terra (Non-reasoning) | 34.0 | 29.3 | 52.3 | 0.065 | 0.562 | 0.134 | 0.371 | 1,000,000 | 131.46 | 3.87 |
| GPT-5.6 Terra (xhigh) | 51.6 | 44.7 | 70.6 | 0.133 | 0.801 | 0.243 | 0.537 | 1,000,000 | 705.36 | 13.67 |
| gpt-oss-120b (high) | 23.8 | 13.2 | 30.4 | 0.088 | 0.262 | 0.120 | 0.151 | 131,072 | 96.28 | 4.04 |
| gpt-oss-120b (low) | 14.9 | 1.0 | 21.2 | 0.219 | 0.139 | 0.029 | 0.000 | 131,072 | 24.20 | 1.62 |
| Grok 4.5 (high) | 53.8 | 45.7 | 72.4 | 0.465 | 0.816 | 0.326 | 0.514 | 500,000 | 639.87 | 11.89 |
| Kimi K2.7 Code | 41.9 | 29.6 | 60.8 | 0.197 | 0.674 | 0.181 | 0.343 | 256,000 | 544.15 | 12.97 |
| Kimi K3 (low) | 46.6 | 37.0 | 72.0 | 0.258 | 0.824 | 0.340 ★ | 0.385 | 1,048,576 | 283.30 | 6.08 |
| Kimi K3 (max) | 57.1 | 50.1 | 76.2 | 0.491 | 0.850 | 0.334 | 0.594 | 1,048,576 | 2437.41 | 42.68 |
| Qwen3.6 35B A3B (Non-reasoning) | 24.2 | 19.1 | 28.1 | 0.073 | 0.416 | 0.052 | 0.261 | 262,144 | 495.84 | 20.52 |
| Qwen3.6 35B A3B (Reasoning) | 31.6 | 21.4 | 41.9 | 0.503 | 0.449 | 0.087 | 0.277 | 262,144 | 333.53 | 10.54 |

<!-- figures:end -->

## At session end — record what actually happened

Every defect found in these skills so far came from a session going wrong and somebody reconstructing it afterwards from a transcript. `clink-brainstorm` alone produced three that way (a leading prompt manufacturing convergence, an agentic agent told not to read files, a stop condition skipped without disclosure) — and none of them was recorded by the session that caused it.

**Before the session ends, report each rule that did not hold** as a `skill-feedback` issue on `xenodeve/xeno-skills`, whichever repo you were working in. Search `--state all` first and **comment on the existing issue rather than opening a second** — one issue per rule, so the comment count is the frequency. Pass `--repo xenodeve/xeno-skills` on every call; `gh` defaults to the repo you are standing in. It records which skills fired, which rules did not hold, and which rule was followed and still produced the wrong thing — **including the embarrassing cases, especially those.** A log of only the memorable sessions is a failure-selected sample and no rate can be read from it.

The rules, the skeleton and the read-trigger live in **`t4-agent-memory`** — load it rather than working from this paragraph. If you cannot reach the tracker, say so in the session report instead of skipping quietly.
