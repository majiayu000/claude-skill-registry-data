---
name: waves
description: WAVES — Workers · Aggregate · Verify · Extend — wave-based orchestration for Cursor. Decompose a big goal into independent slices, fan them out to isolated parallel subagents via parallel Task tool calls as a bounded "wave", verify each structured handoff, then synthesize, and extend into another wave only when warranted. Invoke explicitly with /waves; bounded by design to avoid runaway token loops. For big research, analysis, audits, and codebase or data exploration where one linear pass is slow. Formerly parallel-orchestrate; also fan out, parallelize, orchestrate subagents, multi-agent.
disable-model-invocation: true
---

# WAVES — Workers · Aggregate · Verify · Extend (Cursor)

Run **wave-based orchestration** inside one local Cursor session. A **wave** is a
bounded round of isolated agents working in parallel, then a round that verifies
what came back, then a deliberate decision to build on it — not an open-ended
loop. You are the **orchestrator**: you discover, decompose the goal into
independent slices, fan them out to parallel **workers** (multiple `Task` tool
calls in one message, backgrounded where the surface supports it), read each
worker's structured **handoff**, verify it, and synthesize one deliverable.
Workers are isolated and return exactly one handoff.

**The shape of every wave — WAVE:**

- **W — Workers.** Fan out isolated workers across disjoint slices (the bounded
  parallel round).
- **A — Aggregate.** Wait for all of them and merge their structured handoffs at
  the synthesize barrier.
- **V — Verify.** The moat: check the evidence behind each handoff before you
  trust it.
- **E — Extend.** Decide — deliberately — whether to launch another wave, or stop.

A loop doesn't know when to stop; a wave does, because verification is the stop
function. (Invoked explicitly with `/waves`: a run spawns more agents than usual,
so it's opt-in, not auto-triggered.)

Waves runs **in place of** cloud orchestration. It adopts the principles the
Cursor team proved out in their cloud `orchestrate` plugin — planners plan,
workers hand off up, no cross-talk — but runs them on local subagents with zero
setup: no separate cloud agents, no API keys, no runtime. Local subagent runs
are the whole story here.

## When to use

- A large goal that splits into **independent** slices (research areas, data
  chunks, files/modules, audit dimensions).
- The work is mostly **read / research / analysis** — the safest thing to
  parallelize locally (see "Parallel writes" for why).
- A single linear pass would be slow and you want real speedup from concurrency.

## When to skip

- Small or linear tasks (just do them — fan-out overhead isn't worth it).
- Work needing tight back-and-forth or shared mutable state between steps.
- Parallel **edits to the same files** — local workers share one filesystem.

## Core principles

Adapted from `orchestrate`. These keep the run converging without coordination.

1. **Orchestrator plans and synthesizes; it does not do the heavy lifting.**
   Discovering, decomposing, reading handoffs, and writing the final deliverable
   are your job. The bulk reading/research/analysis is delegated to workers.
2. **Workers are isolated.** A subagent has **no access to the user's message,
   your prior steps, or sibling workers.** Every worker prompt must be fully
   self-contained: goal context, its exact slice, where to look, what to return.
3. **One worker, one slice, one handoff.** The worker's final message is the
   only thing you read back. Define its exact shape (see `references/handoff-format.md`).
4. **Parallelism is for reading, not writing.** Local workers share the
   workspace; concurrent writes to overlapping paths corrupt each other.
5. **Continuous motion.** A handoff can reveal new work. Spawn a second wave
   (driven by a handoff gap *or* a new user request). Stop only when every slice
   is terminal and the synthesis is complete.
6. **Verify before you trust.** A worker's `Status: success` is a claim, not
   evidence. Check each handoff against something re-openable before folding it
   into the synthesis. See "Verification" below and `references/verification.md`.
7. **Decomposition is entropy reduction.** A vague goal is high-entropy — many
   plausible plans still fit it. Your first job is to shrink that space (dig
   locally, then pull from attached resources, then ask the user only if it
   pays) *before* you slice it; slicing a high-entropy goal yields overlapping,
   mis-sized slices. See "Entropy-first decomposition."

## Entropy-first decomposition

Before you fan out, treat the goal as an **entropy-reduction** problem: shrink
how many plausible interpretations and plans still fit what you know. A vague,
high-entropy request ("build a Flappy Bird game", "make my app faster") doesn't
slice cleanly yet — reduce the uncertainty first, then decompose the
low-entropy version. Name what's uncertain, because the two kinds resolve
differently:

- **Specification uncertainty** — what the *user* wants (ambiguous goal, missing
  acceptance criteria, unstated constraints). Resolve by stating an explicit
  assumption and proceeding — or, only when a wrong guess is expensive, by
  asking.
- **Environment / knowledge uncertainty** — facts you don't have yet but *can*
  get (repo shape, schema, API behavior, current docs, data size). Resolve by
  gathering, not by asking.

Spend the cheapest action that buys the most certainty first — an
**information-gain ladder** — and aim each probe at the unknown whose answer
eliminates the most plans: the highest-information question is the one that
splits the surviving interpretations roughly in half, not the one easiest to
look up.

1. **Dig locally first (cheap).** Tool calls in the main session (list, read the
   schema/README, grep, sample data). This *is* Step 0, framed as entropy
   reduction; it often collapses most of the uncertainty for free.
2. **Then pull from attached resources.** If the environment doesn't hold the
   answer, spawn a small **scouting wave** of research workers to fetch it (web,
   Exa/Ref MCP, docs) — route these read-heavy slices to the cheap, fast model
   (see "Picking the model per slice").
3. **Ask the user last, and only when it pays.** Ask only when residual
   *specification* uncertainty is high and the question's expected information
   gain clearly beats its cost. Most requests carry enough to proceed on a
   stated assumption; over-asking is its own failure mode.

Then **cascade**: one high-level request becomes a **decomposition wave**
(understand → locate unknowns → draft the plan) → verify → an **execution wave**
that builds the ordered subtasks, with more scouting sub-waves wherever entropy
stays high. Order the plan least-to-most — do the first-order subtasks first and
let each verified result lower the uncertainty for the next. Keep the living
plan in `TodoWrite`, and stop reducing when entropy is low enough to act: the
verification gate doubles as "is the uncertainty low enough to commit?" One
caution: a plan-then-execute pass fixes *missing steps*, not a *misread goal* —
only the specification check above catches wrong framing, which is why it comes
before planning. (Worked example + wave shape + paper grounding:
`references/examples.md`.)

## The loop

Track it with `TodoWrite` so the waves stay visible.

### Step 0 — Discover first (serial, in the main session)

Do **not** fan out blind. Spend a few cheap tool calls in the main session to
learn the shape of the problem: list the directory, read the schema, sample the
data, confirm coverage/size. This is what tells you the *natural* decomposition
(how many chunks, which workstreams). Skipping discovery produces overlapping or
mis-sized slices.

### Step 0.5 — Stage the data (when it's remote or messy)

`explore` workers are **read-only by design, and read-only mode blocks all MCP
tools** (Cursor staff-confirmed), so they can't reach databases or MCP-backed
sources. If the source is remote or wrapped in noise, the orchestrator must
stage clean inputs **before** fanning out:

- **Pull remote → local.** SSH/`rsync`/export the relevant data to a local
  scratch dir so read-only workers can read it (e.g. query a remote SQLite
  read-only, export the rows, `rsync` the markdown).
- **Clean + normalize once, centrally.** Strip wrappers, boilerplate, and binary
  blobs (base64, logs); fix timestamps. Doing this once beats making every worker
  re-derive it (and keeps noise out of their context).
- **Pre-chunk for the workers.** Split into the exact per-worker files/ranges so
  each prompt can point at one path.
- **One scratch dir per run.** Keep staged inputs, worker artifacts, and
  between-wave syntheses in one place (e.g. `.waves/<run>/` with `staging/`,
  `handoffs/`, `synthesis-wave-N.md`) so prompts cite paths instead of pasting
  content and later waves re-read files, not chat history.
- **Verify before you spawn.** Print counts and per-slice bounds; confirm the
  partition sums to the total (e.g. 8 chunks × ~388 = 3,097) so no slice is a
  silent blind spot. Fix anomalies (bad sort, dups) centrally, then re-check.
  (Details: `references/verification.md` §1.)

In practice this serial prep is often the *largest* phase; the parallel fan-out is
fast once inputs are clean.

### Step 0.7 — Triage: size the run, then classify each slice

**Size the run first, out loud.** Weigh breadth (how many independent slices),
depth (how much reasoning each needs), ambiguity (how well-formed the goal is —
see "Entropy-first decomposition"), and stakes (how costly a wrong answer is —
this sets verification tiers), then state the chosen shape in one line before
spawning — e.g. `Run shape: one wave, 4 workers (3 research + 1 data chunk);
second wave only if handoffs expose gaps.` On the fence between two shapes,
pick the smaller and say so. And if triage says no wave is needed, do the task
inline and say that — never present inline work as wave coverage.

Then classify each slice on **three axes** — this is the classify-and-act
pattern, routing the right work to the right handler:

- **Worker type** — read-only (`explore`) / web-research (`generalPurpose`) /
  shell / competing-attempt (`best-of-n-runner`) / specialized review (`bugbot`,
  `security-review`). (See the table under "Choosing `subagent_type`".)
- **Dependencies** — which slices (if any) this one needs verified output from.
  Most slices should have none; a real dependency edge is what separates waves.
- **Verification tier** — how much checking the slice's stakes justify:
  `auto-accept` (low-stakes, corroborated) → `single verifier` (medium) →
  `multi-model panel` (high-stakes) → `debate` (contested, no ground truth).
  Spend the verification budget where a wrong claim is expensive, not uniformly.

Record the triage as a **wave manifest** — one row per slice, written before
you spawn (in `TodoWrite` or `.waves/<run>/manifest.md`):

| slice | scope | worker type | model | depends_on | verification tier |
|---|---|---|---|---|---|
| 1 | msgs 1–500 | explore | (default fast) | — | auto-accept |
| 2 | voice-stack research | generalPurpose | (default) | — | single verifier |
| 3 | voice build spike | generalPurpose | (default) | 2 | single verifier |

`depends_on` defines the wave boundaries: a wave is every not-yet-run slice
whose dependencies are all met — and a dependency is **met only when its
handoff has been verified** (Step 3), not merely returned. Launch wave 1 (no
dependencies) in parallel; launch each dependent slice with the distilled,
verified findings (or their `.waves/<run>/` path) folded into its
self-contained prompt — and unrelated slices stay parallel. The manifest is
also your **completion gate**: N rows spawned means N handoffs collected and
checked off before synthesis — a wave with a missing handoff has a silent
hole in it (Step 3).

### Step 1 — Decompose into independent slices

Split along whichever axis makes slices independent:

- **Data chunks** — partition large data and give each worker a disjoint range
  (e.g. messages 1–500, 501–1000, …).
- **Workstreams** — separate research/analysis areas (e.g. "research voice
  stack", "research the Notion SDK", "audit auth code").
- **Files / modules** — disjoint, non-overlapping path sets.

Each slice needs: a one-line scope, what to look at, and a defined output. For a
big wave (roughly 5+ workers), state the decomposition plan to the user before
spawning so they can redirect cheaply. If you have many slices, fan out in
**waves** (launch a batch, let it complete, launch the next) rather than all at
once, so you stay within practical concurrency limits.

### Step 2 — Fan out in parallel

Send **one message with multiple `Task` tool calls** — one per slice whose
dependencies are met (handoffs verified, not just returned) — that is what
makes them run concurrently (this is the officially documented parallelism
mechanism). Pick `subagent_type` per slice (table below). Give each a 3-5 word
`description` and a self-contained `prompt` ending with the required handoff
format.

Backgrounding is surface-dependent: the documented switch is the
`is_background: true` frontmatter field on custom subagents; a per-call
`run_in_background: true` parameter exists on some surfaces but is
**undocumented** (and absent on others, e.g. cloud agents) — pass it when the
schema exposes it, and don't rely on it elsewhere. Background workers include
their final message in the completion notification. (`/multitask` is a separate
user-facing Agents Window command, not this skill's mechanism.)

When workers run in the background, **end your turn.** You are notified as each
completes — do **not** `AwaitShell`, poll, or read output files in a loop. The
`Task` call itself confirms the launch. When the surface runs Task calls
synchronously, the batch still executes concurrently and returns together.

### Step 3 — Collect and synthesize

**Completion gate first:** check off every handoff against the wave manifest —
N spawned means N accounted for. A worker that never returns, errors out, or
comes back `partial`/`blocked` is a hole in the wave, and synthesizing around
it silently drops a slice. **Worker failure ladder:** (1) re-task once,
narrower — resume the same worker (each `Task` returns an agent ID that
resumes with context preserved; completed subagents persist checkpoints, so a
resume restores prior context even after the worker finished) when the slice
just needs continuation, or re-spawn fresh with a narrower scope and a note
about what came back. Resume only for *continuation of the same slice* — a
resumed worker carries its old slice's context, which contaminates an
unrelated assignment; (2) if
it fails again, do that slice yourself in the main session; (3) if it stays
blocked, carry the slice into the synthesis explicitly as `not-covered` —
never average over a missing slice as if coverage were complete.

As handoffs arrive, read each one: note `Status`, extract `Key findings`, and
mine `Open questions` / `Suggested follow-ups` — each bullet may become a
second-wave task. Reconcile conflicts across workers.

**Don't trust a handoff because it says `success`.** Verify each finding's
evidence (cited file:line / URL / metric resolves and says what's claimed),
recount headline numbers from the source, and route low-confidence,
conflicting, or citation-heavy claims to a verifier (Step 3.5). See
"Verification" below. A wave's handoffs count as **verified** only when these
checks pass *and* every claim whose manifest tier demands a verifier has its
verdict back — cheap checks alone don't clear a `single verifier` or higher
tier.

Only then **compress at the barrier**: write the distilled synthesis to
`.waves/<run>/synthesis-wave-N.md` and work from that file — next-wave prompts
cite paths into the scratch dir, never re-paste raw handoffs. This file is
what dependent slices and later waves consume, so nothing unverified enters it
as a finding: a claim still awaiting its verdict is carried only as an
explicit `pending-verification` line.

**Pin the constraints through the compression.** The wave manifest, the stop
conditions/budget, and any safety or scope rules are carried *verbatim* into
every synthesis file and every between-wave summary — never paraphrased or
summarized away. Compaction silently drops in-context constraints (measured:
violation rates rise from 0% to 30–59% after compaction; pinning restores 0% —
arXiv 2606.22528), and a run whose stop conditions got compressed out is a run
that loops or quits at random.

### Step 3.5 — Verifier pass (when the tier demands it)

Before writing the wave synthesis, spawn dedicated verifier workers for every
claim whose manifest tier is `single verifier` or higher — and for anything
that arrived contested, surprising, single-sourced, or low-confidence. Give
each verifier the claim + its cited sources, no generator reasoning, no
authorship labels (see "Verification"). Verifiers can run while you draft
around them, but their verdicts gate the wave synthesis itself, not just the
final deliverable: until its verdict returns, a claim may sit in
`synthesis-wave-N.md` only as an explicit `pending-verification` line — never
as a settled finding, and never in a dependent slice's prompt (Step 0.7's
met-only-when-verified rule).

### Step 4 — Second waves (continuous motion)

If handoffs exposed gaps or follow-ups — or verified handoffs just unblocked
dependent manifest slices — spawn another parallel wave the same way. Repeat
until no slice is `pending` and nothing new surfaced. Stopping early while
genuine follow-ups remain is the failure mode this skill guards against; the
stop function is the manifest plus the stated budget (see "Bounded waves"),
never "we've already done a wave or two."

Skipping a follow-up wave is legitimate in exactly three cases — name which
one applies when you decide: the remaining open items are
**primary-source-verified** (a verifier can't improve on the evidence),
**time-gated** (unresolvable until an external event, carry them as explicit
open items), or **genuinely contested** (independent quality sources disagree;
more sampling won't settle taste — record the disagreement instead).

### Step 5 — Deliver

Synthesize all handoffs into the single artifact the user asked for (roadmap,
report, summary, plan). Cite which worker produced which finding when it helps,
and carry each claim's confidence through (`verified / single-sourced /
unverified`) — never launder a `low` into a confident sentence.

Then write any code/files yourself, or spawn a dedicated implementation wave
(mind "Parallel writes"). **Verify the deliverable**, not just the handoffs:
re-run/`curl`/validate served artifacts, regression-check sibling routes, and
re-read the critical files you wrote (see `references/verification.md` §6).

## Bounded waves — size, budget, and the stop function

A wave is bounded on purpose — but bounded by **completion and budget, not by a
wave count**. "Loop-until-done" unbounded burns tokens for little gain:
candidate *generation* is cheap, *selection* plateaus, and extra rounds are
non-monotonic — more iterations can *lower* quality, not just cost. Equally
real is the opposite failure: **stopping while the manifest still has open
slices.** Bounded waves keep the exploration, drop the runaway, and never
abandon un-terminal work.

- **Width: N = 3–8 workers per wave.** Size N so you can *fully verify all N*.
  Go wider only when a cheap automatic check (tests, schema, exec) gates the
  results. (Grounding: homogeneous-agent teams plateau around N≈4–8 — added
  workers contribute redundant evidence, and *diversity*, not head count, is
  what escapes the ceiling — arXiv 2606.02646, 2602.03794. Practically, Cursor
  staff confirm no fixed subagent cap but that ~40 concurrent workers can
  overwhelm the extension host: batch into waves.)
- **Depth: the manifest is the stop function.** Keep extending while any
  manifest slice is non-terminal *and* the last wave added verified progress.
  Stop only on one of three conditions: **completion** (every slice terminal
  and the synthesis done), **stagnation** (a wave surfaces nothing new and its
  outputs near-duplicate the last, or quality dropped), or **budget
  exhaustion**. State the budget up front in the run-shape line — a worker or
  token budget, not a wave count (e.g. `budget: ~20 workers`). Do not stop
  because a round number of waves has passed; a realistic run is often
  `12 + 3 + 1` workers across three waves, and a decomposition cascade on a
  vague goal legitimately runs more. (Grounding: verification-driven replan
  loops that stop on completeness thresholds, diminishing returns, and token
  budgets — not fixed iteration caps — arXiv 2603.11445; convergence-based
  stopping beats a fixed `max_iterations` at parity quality, arXiv 2606.27009.)
- **Scouting is cheap — don't let it eat the budget.** Entropy-reduction waves
  (scouting, decomposition) run on cheap models and count separately from the
  execution budget. Never end a run "out of waves" when the caps were consumed
  by discovery before execution started.
- **Budget split: ~60% generation / 40% verification.** Selection is the scarce
  resource; spend there.
- **Match width to difficulty:** easy → 1 + a light refine; medium → 3–5;
  hard/open-ended → 5–8 for approach diversity; hardest/novel → don't loop,
  escalate the model.
- **Anti-poisoning handoff:** carry only a *distilled, verified* handoff (the
  winner + a short critique) into the next wave — never raw transcripts or losing
  candidates. Long, irrelevant context measurably degrades reasoning.

**Loop-until-done is justified only when ALL hold:** a cheap, reliable
~ground-truth verifier exists; the signal is crisp and actionable (a failing
test, not "try harder"); each iteration shows measurable progress; the work is
easy–medium difficulty; and it stays hard-capped. That fits code-with-tests and
exec-feedback pipelines; it misfits open-ended research/writing/design (verify in
bounded waves instead).

## Verification

The orchestrator's highest-leverage job. You can't make a worker smarter at
inference time, but verifying a handoff is far cheaper than producing it, and in a
multi-wave run one unchecked bad handoff compounds into the synthesis.

- **Gate before spawn** — counts, coverage, partition-sums (Step 0.5).
- **Cheap checks every handoff** — evidence present + resolves, scope match,
  contradiction skim, citations actually support the claim.
- **Self-checks in the prompt** — cite-or-drop, confidence tags, "read
  COMPLETELY", live sources, flag-unverified. (Don't rely on freeform
  "double-check yourself"; give an oracle or a separate verifier.)
- **Dedicated verifier worker** for high-stakes / contested / citation-heavy
  claims — give it the claim + sources but **not** the generator's reasoning nor
  any authorship label (judges favor output marked as their own; blind them),
  and have it reason against a rubric/reference before its verdict
  (reference-guided + CoT is the cheapest reliable judge upgrade). Never show
  the generator the verifier's rubric (anti-gaming). For the highest-stakes
  calls, a multi-model panel + synthesis checks harder still (see "Multi-model
  fan-out").
- **Measure & cross-check** — re-run the oracle, recount from source, require ≥2
  independent sources that actually *entail* the claim (a citation being present
  ≠ the claim being supported).
- **Escalate** low-confidence / conflicting findings (re-task with a tighter
  prompt → dedicated verifier → ask the user, who may choose a stronger model)
  instead of folding them in.

Strongest on objective, checkable work (counts, code, facts-with-sources); on
taste/judgment, verify the sub-claims, don't fake a grade. Keep claims honest:
isolation **reduces error propagation / path dependency**, but don't claim a
quantified "prevents poisoning" — there's no isolation-only ablation. Full
playbook: `references/verification.md`.

## Choosing `subagent_type`

| Slice is… | Use | Notes |
|---|---|---|
| Read-only code/data exploration | `explore` | Fast, **read-only by design** — and read-only mode **blocks all MCP tools**. Pass thoroughness: "quick" / "medium" / "very thorough". |
| Research needing web / MCP (Exa, Ref, docs) | `generalPurpose` | Multi-step; can use available web/MCP tools. Do **not** set `readonly: true` (read-only blocks all MCP). |
| Multi-step work mixing read + light reasoning | `generalPurpose` | The general workhorse. |
| Shell/git heavy investigation | `shell` | Command execution specialist. |
| Browser testing / UI verification | `browser-use` | Navigates and screenshots. **Stateful: auto-resumes one shared instance, so don't fan out `browser-use` in parallel** — use a single serial UI slice. Needs agent mode (not `readonly`). |
| Competing attempts at the same task | `best-of-n-runner` | Each runs in an **isolated git worktree/branch** — safe from shared-checkout clobbering; you then compare attempts and merge the winner. |

**Naming drift across surfaces.** Cursor's docs describe the built-ins as
`explore`, `bash`, and `browser`, while Task-tool schemas expose
surface-dependent values (`generalPurpose`, `explore`, `shell`, `browser-use`,
`best-of-n-runner`, review specialists…). Read the live `subagent_type` enum
off the Task tool rather than assuming this table's names — the roles are
stable, the labels drift.

**Custom subagents and the missing-type fallback.** Custom subagents (project
`.cursor/agents/`, user `~/.cursor/agents/`, or plugin-provided) show up as
their own `subagent_type` values — worth defining when a role repeats across
runs (a verifier, a docs researcher) so its prompt, pinned `model`, `readonly`,
and `is_background` defaults live in one file. Two verified gotchas
(staff-confirmed on the forum, not in docs): new agent files register only
after a Cursor restart, and a type missing from the enum is **not** permission
to skip the role — run it as `generalPurpose` with the role's instructions
inlined in the worker prompt (passing the intended `model` on the call)
instead. Nesting note: the platform itself now allows the main agent *and its
direct subagents* to launch subagents (one extra level, no deeper — the SDK
docs state the same cap); this skill still keeps fan-out orchestrator-only as
policy, because nested fan-out hides work from the manifest and the
verification gate.

### Picking the model per slice (cost / speed routing)

Model choice is a cost/speed lever — route it, don't put every slice on a
frontier model:

- **Scouting / decomposition / read-heavy exploration → the cheap, fast model.**
  Cursor's built-in `explore` and search subagents already default to the
  Composer fast family (e.g. `composer-2.5-fast`) for exactly this: fast, cheap,
  and tuned for codebase understanding and tool use — so read waves are cheap by
  default and you often need not set `model` at all. To pin it, pass
  `model: "composer-2.5"` on the `Task` worker, or set the `model` field
  (`inherit` | a model ID) on a custom `.cursor/agents/` subagent. For
  lightweight short-context slices on the GPT side, `gpt-5.6-luna` at a higher
  effort is the cost-per-unit-of-work champion — but never give Luna
  long-context reads (its recall collapses on 256K+ contexts per OpenAI's own
  MRCR tables; route big-file slices to a stronger tier or chunk smaller).
  This is the entropy-reduction workhorse.
- **Per-model options ride in brackets on the model ID** (documented syntax):
  `gpt-5.6-sol`, `claude-opus-4-8[effort=high,context=300k]`,
  `composer-2.5[fast=false]`, `composer-2.5[]` (empty brackets pin the
  standard, non-fast variant). Use `[effort=…]` instead of guessing separate
  "thinking" slugs.
- **High-stakes verification, synthesis, or a multi-model panel → stronger
  reasoning, chosen deliberately** (e.g. a frontier tier at `effort=high`,
  escalating effort only for a slice that stays unresolved). For a
  user-requested or high-stakes multi-model panel, **ask which models to use;
  don't guess slugs** (see "Multi-model fan-out").
- Otherwise honor a model the user named; if a requested model is unavailable,
  say so rather than silently substituting.

Caveats: availability varies (Max Mode, plan, or admin restrictions can force a
fallback to a compatible model; legacy request-based plans without Max Mode run
subagents on Composer regardless of `model` configuration); slugs drift, so
read them off Cursor's model picker rather than hardcoding volatile ones;
`inherit` can be unreliable in some surfaces (omit `model` to inherit). When a
custom agent's model matters, pin it in the frontmatter **and** pass the
matching `model` on the `Task` call — the field has been ignored under some
conditions (documented fallbacks plus confirmed bug reports), so if a worker's
output quality looks off, consider that the intended model may not have run.
Respect the user's cost and model preferences over any default here.

For review/audit slices, Cursor also exposes specialized subagents when available
(e.g. `bugbot`, `security-review`, `ci-investigator`, `ci-watcher`) — prefer them
for those slice types.

## Multi-model fan-out (panel + synthesize)

The default fan-out runs each *slice* on one model. A **high-stakes** slice —
an architecture/design call, a risky correctness question, a security or audit
pass, or a key research synthesis — fan the **same** slice out to a **panel of
different models**, then act as judge and synthesizer.

Reconcile; don't concatenate. Label **CONSENSUS** (2+ models agree) vs
**lone-model** findings, resolve contradictions, dedupe overlap, and carry each
claim's confidence into one answer. The synthesis is where most of the value
lives — per OpenRouter's Fusion research, roughly three-quarters of the gain
comes from the synthesis step, not the model diversity — so invest there rather
than stapling outputs together. Evidence: a panel of independent models + a
judge + a synthesizer matched and surpassed a single top-tier model on hard,
deep-research problems (OpenRouter, *Surpassing Frontier Performance with
Fusion*, openrouter.ai/blog/announcements/fusion-beats-frontier/).

Run it in Cursor: pass a **different `model`** to each sibling `Task` worker on
the same slice, launch them in **one message** (parallel; backgrounded where
the surface supports it), then synthesize. This is the **high-stakes** end of model routing —
the orchestrator picks frontier models only when the user asks for a multi-model
pass or the slice is explicitly high-stakes — so **ask which models to use;
don't guess slugs.** (The cheap end — routing scouting and read-heavy waves to
Composer 2.5 — is under "Picking the model per slice.")

Caveat: a panel multiplies token cost (you pay every worker) and adds latency —
reserve it for high-stakes slices, not routine ones. The adversarial multi-model
review (a panel of reviewer models + one synthesized verdict) is this same
pattern applied to code review. For *grading* panels specifically, judges drawn
from **disjoint model families** beat a single frontier judge on human agreement
while cutting self-preference bias and cost (PoLL) — the family diversity, not
the head count, is what does the work.

## Generate-and-filter & tournaments

For open-ended ideation or "produce the single best X", generate several
candidates and **filter** — don't trust one attempt:

- **Cheap filter first.** Gate candidates through a near-ground-truth check
  (tests, schema/exec, dedup/clustering) *before* spending judge tokens —
  generation is cheap, judging is not. (AlphaCode's shape: generate many → filter
  ~99% by tests → cluster → submit a few.)
- **Selection ladder, not all-pairs.** Dedup/cluster → shortlist → pairwise-judge
  only among finalists. A naive O(N²) tournament spends most of its tokens
  comparing also-rans.
- **Use `best-of-n-runner`** for competing *implementation* attempts (each in its
  own git worktree), then inspect/test/merge the winner yourself.
- For high-stakes *judgment* calls, the multi-model panel (above) is the
  generate-and-filter of verification.
- **Budget check.** At equal cost, k independent attempts + a majority vote or
  cheap filter usually beats critique/debate loops — benchmark any iterative
  loop against that baseline before paying for it.

## Worker prompt = the contract

A worker cannot ask follow-up questions. Under-specified prompts drift silently.
Write each as if you get one shot. Every worker prompt includes:

1. **Overall goal** (context only — "don't try to own the whole goal").
2. **This worker's exact slice** (the disjoint range / area / paths).
3. **Where to look** (dirs, files, data ranges, which MCP/tools to use).
4. **What to return** — the structured handoff from `references/handoff-format.md`.
5. **Self-verify rules** — cite-or-drop every claim, tag confidence
   (`high|med|low`), and state what you could **not** verify. Analysis workers:
   "read COMPLETELY (N lines) and report the count." Research workers: "use live
   sources, not training data."
6. **Scope boundaries** — what's explicitly OUT of scope (so it doesn't overlap a
   sibling worker).
7. **Return only the handoff, and keep it a digest.** The worker's entire final
   message becomes your context — tell it to return *only* the structured
   handoff, capped at roughly 15 findings with one-line evidence each, and to
   write any large artifact (tables, logs, full lists) to a file and cite the
   path instead of pasting it inline.
8. **Edit workers: you are not alone.** For implementation slices, warn the
   worker that siblings may be active: own only the listed paths, don't revert
   others' changes, and **never spawn its own subagents** (only the orchestrator
   fans out).

See `references/handoff-format.md` for the copy-paste worker handoff template and
`references/examples.md` for a full worked run (the health-coach research job in
the screenshots) plus reusable decomposition recipes.

## Parallel writes (the local gotcha)

**Local subagents share one working directory.** Concurrent writes to overlapping
files clobber each other.

- Parallel **reads/research/analysis**: always safe. This is the default use.
- **Disjoint edits you keep all of**: use regular workers only when path sets are
  strictly disjoint, or do the edits serially after the research waves finish.
- **Competing attempts at the same task**: use `best-of-n-runner` (each in its
  own git worktree/branch), then **inspect, test, and merge the chosen result
  yourself** — worktrees prevent clobbering, not the merge.

## Waves instead of cloud orchestration

Waves is deliberately the **replacement** for cloud fan-out, not a stepping
stone to it. Local subagent runs cover the whole workload this skill targets —
research, audits, data analysis, exploration, and bounded implementation — with
isolation, parallelism, resume, and verification, and none of the cloud setup
(separate VMs, API keys, runtimes). The lessons worth keeping from the Cursor
team's cloud `orchestrate` plugin are already folded into this skill: planners
plan, workers hand off up, no cross-talk, disk/git as the durable medium. Do
not spawn cloud agents for a waves run; if a run truly outgrows one machine
(days-long fleets, PR-per-task pipelines), that is a different tool choice for
the user to make — say so and let them decide.

> Cursor subagent mechanics here were checked on 2026-07-19 against current
> docs, changelogs, and staff forum replies: parallel Task calls in one message
> are the documented fan-out; `is_background` frontmatter is the documented
> background switch while per-call `run_in_background` is live but undocumented
> and absent on some surfaces; completed subagents persist resume checkpoints
> (CLI release 2026-07-06); nesting is capped at one extra level; read-only
> mode blocks all MCP; there is no documented concurrency cap, but staff report
> ~40 concurrent workers can overwhelm the extension host — batch into waves.
> The details most likely to drift: Task parameter names, the `subagent_type`
> enum, and model-ID bracket options. Re-verify those if they matter to your
> run.

## Checklist

- [ ] Discovered the problem shape before decomposing.
- [ ] Reduced entropy before slicing (dug locally → pulled from attached
      resources → asked the user only if it paid); sliced the low-entropy goal.
- [ ] Stated the run shape in one line before spawning (on the fence → the
      smaller shape); never presented inline work as wave coverage.
- [ ] Triaged each slice (worker type + dependencies + verification tier).
- [ ] Routed scouting / read-heavy waves to the cheap fast model (Composer 2.5,
      or `gpt-5.6-luna` for short-context slices only); reserved frontier /
      panel models for high-stakes slices; never gave Luna-class models
      long-context reads.
- [ ] Slices are independent (disjoint data/areas/paths), or their `depends_on`
      edges are recorded in the manifest.
- [ ] Wrote the wave manifest (slice / worker type / model / depends_on /
      verification tier) before spawning; launched dependent slices only after
      their dependencies' handoffs were verified (distilled findings fed into
      their prompts).
- [ ] Each worker prompt is fully self-contained (no reliance on chat history).
- [ ] Each wave's `Task` calls sent in one message; backgrounded where the
      surface supports it (`is_background` / `run_in_background`).
- [ ] Ended turn to await background completions — no polling loop.
- [ ] No two parallel workers write the same paths.
- [ ] Verified coverage before spawning (counts/bounds/partition-sum).
- [ ] Checked every manifest row off at collection (completion gate); ran the
      failure ladder on missing/blocked slices — no slice silently dropped.
- [ ] Read every handoff; spawned follow-ups for open questions.
- [ ] Waves bounded by the manifest + stated budget (width ≈3–8; scouting
      waves counted separately): continued while slices were non-terminal and
      progress was verified; stopped only on completion, stagnation, or budget
      — and named which of the three no-second-wave cases applied when
      skipping a follow-up.
- [ ] Carried only distilled handoffs forward; manifest, stop conditions, and
      budget pinned verbatim through every synthesis/compaction.
- [ ] Verified each handoff's evidence (not just its `Status`); escalated
      low-confidence / conflicting / uncited findings; wrote
      `synthesis-wave-N.md` only from verdict-cleared findings (pending claims
      tagged `pending-verification`, never fed to dependent slices).
- [ ] Verified the final deliverable (re-ran/validated; re-read critical writes).
- [ ] Synthesized one deliverable from the handoffs.
