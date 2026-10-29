---
name: subagent-eval
description: Empirically evaluate and optimise a Claude Code sub-agent via a blinded head-to-head against the production baseline, then pick its model on data. Use when tuning a sub-agent's prompt, choosing or re-checking its model (e.g. a new model release), proving an agent change before committing, or testing whether a specialist beats native Explore. To author a new agent first, read AUTHORING.md.
effort: xhigh
---

# Sub-agent eval & optimise

Prove a sub-agent change with evidence before shipping it. Run three times to date (`codebase-*`, `thoughts-*`, `docs-*`) — reproduce that loop. **Quality is the deciding metric; cost/latency break ties only.**

## When to use

- **Optimise** — a sub-agent's prompt is being edited and the change needs proving.
- **Re-validate** — a new model (or effort level) shipped; re-check which model **and effort** each agent should run.
- **Compare** — does a specialist actually beat the native `Explore` baseline?
- **Create** — authoring a new agent: read **[AUTHORING.md](AUTHORING.md)** first, then enter this loop.

This is a multi-agent `Workflow` (opt-in — it spends real tokens). Say "use a workflow" / confirm before launching.

## Workflow

1. **Frame & pick entry mode.** State the agent(s) under test and the decision to make (ship this prompt? which model?). For create, do AUTHORING.md first.
2. **Build the benchmark.** Per archetype the agent serves (e.g. locate / analyze):
   - Mine real prompts: `python3 .claude/eval/mine_subagents.py --print` → pull from `.claude/eval/mined/corpus.jsonl` (shape rows into tasks with `shape_tasks.py`). Read-only context? `shape_tasks.py` writes YAML into the repo by default — pass `--dry-run`, or read `corpus.jsonl` rows directly (count by exact `agent ==` field, not a substring `grep -c`, which over-counts routing fields).
   - Add a **golden** task (hand-written, clear oracle) and an **adversarial** task (zero-match / trap).
   - Write a **verified oracle** for each — confirm every expected path/value against the tree *now*.
   - ☐ Include at least one HARD task with headroom. Near-ceiling tasks don't discriminate — a well-curated repo makes even `Explore@haiku` score ~1.0 (see `docs-*` example).
3. **Run the head-to-head.** Adapt **[harness-template.js](harness-template.js)** and launch via `Workflow`. Candidates per task: native baseline (`Explore` @ its production model, usually haiku), specialist @ `sonnet`, specialist @ `opus`.
   - ☐ **Effort is a second axis, but not a per-spawn candidate.** Unlike `model`, there is **no per-spawn `effort` override** (see REFERENCE.md § Model & effort decision), so you can't add effort cells to `CANDS` and sweep them in one run. To test effort *today*, run the head-to-head once per `effort:` frontmatter value — edit `.claude/agents/<name>.md`, restart to re-register, re-run — then compare the recorded per-run JSON (Path 2; mind the mid-run file-mutation/provenance caveat). The per-spawn `effort` opt that would let effort mirror the model sweep in one run is filed as a prerequisite.
   - ☐ **Variance-control the deciding axis**: ≥3 runs × ≥2 judges per cell for any model decision. 1 run scouts a locate, but never flip a model from a single-run cell — a lone run can fabricate (the `ln` incident) and swing the mean; the harness now flags an n<3 promotion as inconclusive. Set the harness `DECIDING_KINDS` to THIS agent's archetype — **not literally `analyze`**; a third archetype (e.g. `pattern`) also needs per-agent **contract discriminators** added to the judge (REFERENCE.md "Scoring a new agent's contract").
   - ☐ Judges are **blinded** (no candidate id) and **verify every claimed path/Status/citation against the tree** before scoring. See REFERENCE.md.
   - ☐ Registry gotcha: a just-created agent is NOT in the session's hot registry — either restart to register, or use the harness's adopt-on-disk bootstrap. See REFERENCE.md.
   - ☐ Script placement: paste the harness inline (or keep it in `/tmp`); never save an adapted copy under `.claude/eval/` — its top-level `return` trips Biome and blocks the husky pre-commit. See REFERENCE.md.
   - ☐ **Dry-run first (zero agents)**: validate the harness logic with stubbed hooks before launching — see REFERENCE.md "Validate the harness before launch". Re-run after every harness edit; it's free and catches syntax + aggregation bugs.
4. **Decide each model and effort quality-first.** Default `sonnet` at the model's tier-default effort. Adopt a costlier cell — a higher model class, or a higher effort level — ONLY if it clears the same bar: `mean(candidate) ≥ mean(incumbent) + 0.05` AND it isn't dragged by over-templating. Among cells within 0.05 of the best, pick the **cheapest**: cost ranks by model tier first, then effort level. Model and effort choices are **task-shaped, not class-shaped** — see REFERENCE.md § Model & effort decision.
5. **Wire routing** (if creating/changing an agent's role). Add it to the command fan-outs (`write-plan.md`, `brainstorm.md`, `iterate-plan.md`) and tighten reciprocal when-not redirects in sibling agents' descriptions.
6. **Verify + safety.**
   - ☐ `make check` via **@agent-codebase-verification** (never run `make` directly).
   - ☐ **After any multi-agent run**: review the FULL `git status` + `git diff`; confirm the agent roster count is unchanged (`ls .claude/agents/*.md | wc -l`); `git restore` anything outside the intended seam. Verify provenance before blaming a sub-agent — git state that shifts mid-run is usually the operator's own concurrent commits/branch switches (check `git reflog` + author), not a stray `Bash` call.
7. **Record.** Write `thoughts/research/<YYYY-MM-DD>-<family>-agent-headtohead.md`, mirroring an existing example: TL;DR → Setup → Results → Decisions applied → Key findings → Per-run JSON → Caveats → Fast follow. Be honest — a tie or a null result is a real finding.

## References

- **[REFERENCE.md](REFERENCE.md)** — §6.3 rubric, §6.4 aggregation, model & effort decision rule, judge-prompt pattern, registry/bootstrap gotcha, safety checklist, lessons from the runs.
- **[AUTHORING.md](AUTHORING.md)** — how to write a new agent before validating it.
- **[harness-template.js](harness-template.js)** — parameterized `Workflow` head-to-head for the **§6.3 execution** pass; fill the tasks/oracles/candidates and launch.
- **[routing-harness-template.js](routing-harness-template.js)** — the **§6.2 routing** pass: scores `description`s with no candidate execution — blinded judges route probes among the on-disk descriptions and rate scope-clarity + verbosity. See REFERENCE.md §6.2.
- **System of record:** `thoughts/designs/2026-04-21-sub-agent-eval-pipeline.md` (§6.2 routing, §6.3 execution, §6.4 aggregation, §14.1 model floor).
- **Worked examples** (copy one): `thoughts/research/2026-06-02-codebase-agent-headtohead.md`, `…/2026-06-03-thoughts-agent-headtohead.md`, `…/2026-06-03-docs-agent-headtohead.md`.
- **Corpus tooling:** `.claude/eval/{mine_subagents,shape_tasks,harvest_hook}.py`.
