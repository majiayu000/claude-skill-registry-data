---
name: adversarial-planning
description: Two genuinely different models debate a plan before anything is built — Claude (Fable) drafts, Codex/OpenAI challenges, capped at 3 rounds, Codex executes the converged plan, the planner reviews the real diff. Use when a wrong plan is expensive to discover late — rigging/animation pipelines, architecture decisions, schema or infra migrations. Do NOT use for small obviously-correct changes (just do them), and do NOT use it after the work exists — grading a finished artifact is adversarial-verification.
---

# Adversarial Planning

## The problem

A single model planning alone has one blind spot: its own. It can catch its own typos,
not its own bad assumptions — the plan sounds coherent because the same reasoning that
wrote it is the reasoning checking it.
[`adversarial-verification`](../adversarial-verification/SKILL.md) solves this for "did
the fix work"; this skill solves it one step earlier, for "is the plan sound before
anyone spends an hour building the wrong thing."

```
Plan (Fable)  →  Debate (Fable vs Codex, ≤3 rounds)  →  Execute (Codex)  →  Review (Fable)
```

## When to use

Use it when the cost of a late-discovered wrong plan is hours, money, or a rebuild:

- new rigs / animation pipelines (`.wolf/buglog.json` bug-198 / 214 / 215 are exactly
  the "plan looked fine, three hours in it wasn't" pattern on the mascot rig)
- architecture decisions with downstream lock-in — storage layout, agent topology,
  dependency-flow changes
- migrations: schema, framework major, deploy-path swap
- any plan whose steps you cannot state a per-step check for; the debate exposes that

Do **not** use it:

- for small, obviously-correct changes. Two models arguing about a one-line fix burns
  real money for no information. Do the thing, then verify cheaply.
- after the work exists. Debating a finished diff is
  [`adversarial-verification`](../adversarial-verification/SKILL.md)'s job.
- when Codex is unreachable. A "debate" that silently degrades to one model is a solo
  plan with extra latency — surface the failure, do not fall back.

## Inputs

| Required | How to confirm | If absent |
|---|---|---|
| A task statement concrete enough to plan against — files, surface, success condition | Written out before dispatch | **Stop.** A vague brief produces a plan that cannot be challenged specifically, and the debate degenerates into style notes. |
| `codex` CLI installed and authenticated | `codex --version` → `codex-cli 0.144.1` (observed 2026-07-29) | **Stop.** Do not substitute a second Claude instance and call it adversarial — different weights are the whole mechanism. |
| A **confirmed** Codex model string | `grep '^model' ~/.codex/config.toml` → `model = "gpt-5.6-sol"` (observed 2026-07-29) | **Stop.** Never hardcode a guessed model. This string already moved once (`gpt-5.5` → `gpt-5.6-sol`). |
| Provider reachability | `codex doctor` → `0 fail` | **Stop and surface it.** `codex doctor` has caught a real "required provider endpoint unreachable" despite valid auth. Do not silently retry. |
| Founder `y` on the spend | STOP-AND-SHOW manifest: model + max rounds + est. cost | **Do not launch.** Every challenge round and the execution turn is a paid Codex call. One manifest → one `y` → one run. |

## Procedure

1. **Pre-flight the CLI** — `codex --version`, `grep '^model' ~/.codex/config.toml`,
   `codex doctor`. Record the actual strings; do not carry them from memory.
2. **STOP-AND-SHOW the launch**: model, round cap, estimated cost. Wait for `y`.
3. **Round 1 — proposal + challenge.** Planner (Fable) drafts a real plan: steps, files
   touched, per-step verification, risks. Challenger (Codex, `-s read-only`) attacks the
   assumptions and must name specifically what would change its mind — a missing edge
   case, an untested assumption, a step whose stated check cannot actually fail.
4. **Round 2 — revision + recheck.** Planner addresses that *specific* challenge, not a
   full rewrite. Challenger rechecks. Satisfied → stop; do not burn round 3 on agreement.
5. **Round 3 — mandatory, no more argument.** If rounds 1-2 did not converge, stop
   debating in the abstract and **execute**: the real build is the tie-breaker. Lock in
   whichever plan exists and hand it to the executor.
6. **Execute with the strongest coding model for the job** (here Codex,
   `-s workspace-write` — and only this turn gets write sandbox).
7. **Planner reviews the real executed result** — the actual diff/output, not the plan in
   the abstract. `REVIEW_SCHEMA` forces a ship/no-ship boolean plus named deviations.
8. **Relay Codex verbatim.** A Claude paraphrase of Codex's judgment defeats the entire
   mechanism; the script preserves it in `codex_verbatim`.

### Codex is not reachable via `agent()`'s `model` option

`agent()` (Workflow tool) only spawns Claude models (`sonnet`/`opus`/`haiku`/`fable`),
and a Workflow script has no shell access, so it cannot invoke `codex` directly. **Fix:**
dispatch a Claude subagent whose entire job is to shell out to `codex exec` via Bash and
relay the raw output verbatim.

```bash
codex exec -m <MODEL> -s <read-only|workspace-write> --json -o /tmp/out.json < prompt.txt
```

`-m` explicit model · `-s` sandbox (read-only for challenge/review, `workspace-write`
**only** for the execution turn) · `--json` machine-readable event stream · `-o` final
message to a file. Pipe the prompt over **stdin** as shown — never interpolate plan JSON
into the shell command.

### Running it

The full loop lives in
[`scripts/adversarial-planning.wf.js`](scripts/adversarial-planning.wf.js). `PLAN_SCHEMA`
forces structured steps (action / files / per-step check / risks) so each revision has
something concrete to diff. `CHALLENGE_SCHEMA` returns `{ codex_verbatim, satisfied,
specific_challenge }`. `REVIEW_SCHEMA` forces ship/no-ship + deviations.

```js
Workflow({
  scriptPath: "<skill-dir>/scripts/adversarial-planning.wf.js",
  args: { task: "<the plan/task to debate>", codexModel: "gpt-5.6-sol" /* CONFIRMED */ },
});
```

It returns `{ rounds, converged, plan, transcript, execution, review }`. Read
`review.ship` and `review.deviations` against `execution.codex_verbatim` before trusting
the result.

## Verification

Pre-flight gates — all four run **before** the paid launch.

```bash
codex --version
```

**PASS:** prints a `codex-cli <version>` line. Observed 2026-07-29: `codex-cli 0.144.1`.
A "command not found" is a stop, not a fallback. `[repro]`

```bash
grep -n '^model' ~/.codex/config.toml
```

**PASS:** prints exactly one model line, and that string is what you pass as
`args.codexModel`. Observed 2026-07-29: `1:model = "gpt-5.6-sol"`. If your intended
string differs from the file, resolve it before spending — never silently substitute.
`[repo]`

```bash
codex doctor | tail -3
```

**PASS:** the summary line ends `0 fail`. Observed 2026-07-29:
`16 ok · 1 idle · 3 notes · 1 warn · 0 fail degraded`, with
`✓ reachability active provider endpoints are reachable over HTTP`. Any `fail` count
above zero is a stop — surface it, do not retry into a paid call. `[repro]`

```bash
grep -cE '^(const|let) (PLAN|CHALLENGE|REVIEW)_SCHEMA' \
  .claude/skills/adversarial-planning/scripts/adversarial-planning.wf.js
grep -c 'codex_verbatim' \
  .claude/skills/adversarial-planning/scripts/adversarial-planning.wf.js
```

**PASS:** first command prints `3` (all three schemas present — observed 2026-07-29),
second prints a non-zero count (the verbatim relay survives). A script missing
`codex_verbatim` is paraphrasing Codex, which voids the debate. `[repo]`

**Do not run `node --check` on the Workflow script.** It is not a plain module: it
combines `export const meta` with a top-level `return`, and `node --check` reports
`SyntaxError: Illegal return statement` at line 198 (observed 2026-07-29) on a file that
is perfectly valid under the Workflow runner. Treating that as a real failure would send
you fixing a non-bug; the grep gates above are the honest structural check. **This aspect
has no CLI syntax gate — that is a SKIP, closed by the Workflow runner itself at launch.**

**Post-run:** the loop is only verified when `review.ship` is backed by
`execution.codex_verbatim` containing the real diff/output. A `ship: true` whose evidence
is the plan restated is `[inferred]`, not `[repro]`, and carries no severity.

## Worked example

Pre-flight for a debate on the Love Hurts Girl retarget plan, this worktree, 2026-07-29.

```bash
$ codex --version
codex-cli 0.144.1

$ grep -n '^model' ~/.codex/config.toml
1:model = "gpt-5.6-sol"

$ codex doctor | tail -3
  ✓ reachability   active provider endpoints are reachable over HTTP
      ChatGPT base URL   https://chatgpt.com/backend-api/ reachable (HTTP 403)
16 ok · 1 idle · 3 notes · 1 warn · 0 fail degraded

$ grep -cE '^(const|let) (PLAN|CHALLENGE|REVIEW)_SCHEMA' \
    .claude/skills/adversarial-planning/scripts/adversarial-planning.wf.js
3
```

All four pre-flight gates green `[repro]`. Note what the third one bought: `codex doctor`
reports `auth mode chatgpt` and a base URL that answers **HTTP 403** — which is the
*expected* reachable-but-unauthenticated response for that probe, and is why the gate
reads the summary's `0 fail` rather than eyeballing status codes.

The launch itself is a paid call and did **not** fire here — no founder `y` was in scope
for this session, so the run stops at the manifest:

```
STOP — Confirm before proceeding:

Action : adversarial-planning debate + execute
Model  : gpt-5.6-sol   (confirmed from ~/.codex/config.toml)
Rounds : ≤3 challenge + 1 execute + 1 review
Cost   : ~4-5 paid Codex calls

Proceed? [y/N]
```

That is the correct terminal state for an unapproved run — pre-flight verified, spend
gated, nothing invented about what the debate "would have" concluded.

## Failure modes

| Symptom | What is really happening | Bug |
|---|---|---|
| Debate ran, both sides are Claude | `agent()` cannot spawn Codex. Without the Bash relay you got one model arguing with itself. | — |
| The challenge reads like a Claude summary of Codex | The relay paraphrased. `codex_verbatim` must carry Codex's exact words or the second model contributed nothing. | — |
| Model string errors mid-run, the script "falls back" | Silent substitution. Confirm the string in pre-flight and name which model actually ran. | — |
| `codex doctor` warns, run proceeds anyway | Fail-open. A degraded provider mid-debate produces truncated challenges that read as agreement. | bug-230 |
| Round 3 is another round of argument | Round 3 is execution-only by construction; without it the loop has no exit condition and burns rounds on rhetoric. | — |
| `node --check` on the `.wf.js` reports a syntax error, someone "fixes" the script | Workflow scripts legally use top-level `return`. The error is the tool's, not the file's. | — |
| Plan approved, execution deviates, review says ship | The review graded the plan, not the diff. `review.deviations` must be derived from `execution.codex_verbatim`. | — |
| Whole loop launched without a manifest | Every round is a paid call. One manifest → one `y` → one run; approval never carries forward. | — |
| Three hours into the build the plan turns out wrong anyway | The per-step checks in `PLAN_SCHEMA` were unfalsifiable ("looks correct"). A step whose check cannot fail is an unplanned step. | bug-198/214/215 |
