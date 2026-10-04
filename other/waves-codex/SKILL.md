---
name: waves-codex
description: WAVES - Workers, Aggregate, Verify, Extend - wave-based orchestration for Codex. Decompose a big goal into independent slices, verify coverage, spawn Codex subagents in parallel as a bounded wave, collect evidence-backed handoffs, verify important claims, synthesize one deliverable, and extend into another wave only when warranted. Bounded by design to avoid runaway token loops; invoke deliberately. Formerly parallel-orchestrate-codex; also fan out, parallelize, spin up multiple agents, orchestrate workers, multi-stream research, audit a repo, split disjoint implementation work.
disable-model-invocation: true
---

# WAVES — Workers · Aggregate · Verify · Extend (Codex)

Run **wave-based orchestration** with Codex subagents. A **wave** is a bounded
round of isolated workers in parallel, then a round that verifies what came back,
then a deliberate decision to build on it — not an open-ended loop. Use this skill
when a task is too broad for one clean linear pass but can be split into
independent slices. You are the manager: discover the problem shape, stage and
verify coverage, decompose it, spawn bounded Codex workers, collect one structured
handoff from each worker, verify important claims, and synthesize the final
deliverable.

**The shape of every wave — WAVE:** Workers fan out across disjoint slices ->
Aggregate their handoffs -> Verify the evidence (the moat) -> Extend into another
wave only when warranted. A loop doesn't know when to stop; a wave does, because
verification is the stop function. (Invoke deliberately - a run spawns more agents
than usual.)

Current Codex docs checked on 2026-07-19: Codex subagents are enabled by default
in current releases, built-in roles include `default`, `worker`, and `explorer`,
custom agents live in `~/.codex/agents/` or `.codex/agents/` (TOML; project
agents load in trusted projects only), and subagent limits live under `[agents]`
in `config.toml`. Official docs no longer enumerate the collaboration tool
names; the current (multi-agent V2) surface exposes `spawn_agent`,
`send_message`, `followup_task`, `wait_agent`, `interrupt_agent`, and
`list_agents`, while threads created before the V2 runtime resume on the legacy
V1 set (`spawn_agent`, `send_input`, `resume_agent`, `wait_agent`,
`close_agent`) — read the live tool registry rather than assuming one set.
Spawning an unknown `agent_type` fails with an error rather than silently
falling back (fallback in Step 2). V2 delegation payloads are encrypted between
model calls, so don't build workflows that inspect spawn prompts from rollout
history. `spawn_agents_on_csv` is documented as experimental; use it when it is
exposed in the active Codex surface, and fall back to normal subagent waves
when it is not. No current Codex doc confirms a general-purpose claim-verifier
or critic hook; use a verifier subagent, CSV verification pass, tests,
validators, or `codex exec --output-schema` instead.

Native delegation on GPT-5.6 (how this skill plugs in): Sol and Terra run the
V2 multi-agent runtime, and the delegation mode is derived from reasoning
effort per turn -- `ultra` means *proactive* (the model spawns on its own
judgment), every other effort means *explicit-request-only*, where the
documented triggers are direct user asks **and "applicable AGENTS.md or skill
instructions"** -- this skill's spawn instructions are that sanctioned
channel, at any effort, no `ultra` required. Avoid `ultra` for wave runs:
proactive spawning happens outside your manifest, and its children inherit the
parent's model and effort (an ultra parent breeds ultra children -- the
runaway-cost failure mode). Native V2 spawns also **fork the parent's history
by default** (`fork_turns` defaults to `all`; filtered, but the child sees
your conversation), and full-history forks inherit the parent's agent type /
model / effort and reject overrides -- so for disjoint wave slices, request
**fresh-context workers** (no history fork), which is also the only spawn
shape that can be routed to a different model or effort. V2 ignores
`agents.max_depth`; its binding limit is concurrent agent slots (4 including
the manager by default; `agents.max_threads + 1` when set) -- batch wider
waves accordingly.

Read these references when using the skill:

- `references/handoff-format.md` for the exact worker handoff contract.
- `references/verification.md` for verification gates and verifier-worker
  playbooks.
- `references/examples.md` for decomposition recipes.
- `references/recommended-config.md` for Codex config and custom agent snippets.
- `references/adaptation-notes.md` for Cursor-to-Codex translation notes.

## When to Use

- The user explicitly asks to use multiple agents, subagents, parallel workers,
  fan-out, or orchestration.
- The task splits into independent slices: data ranges, research streams,
  repo modules, audit dimensions, verification rows, or disjoint code ownership.
- The main value is speed, context hygiene, and verification discipline: keep
  noisy exploration out of the manager thread, then check the claims that matter.
- A second or third wave may be useful after first-wave handoffs expose gaps,
  conflicts, narrowed scope, or high-stakes claims needing verification.

## When to Skip

- The task is small, linear, or easy to do locally.
- The slices require constant cross-talk or shared mutable decisions.
- The next action is blocked on one immediate investigation; do that locally.
- Parallel code edits would overlap heavily and no worktree/isolation strategy is
  available.

## Core Principles

1. The manager plans, verifies, and synthesizes. Workers do heavy reading,
   research, tests, audits, bounded edits, or focused claim checks.
2. Worker prompts are self-contained. Do not assume workers can infer the user's
   original request, your scratch reasoning, or sibling work unless you
   intentionally pass or fork that context. (On GPT-5.6's V2 runtime, native
   spawns fork parent history *by default* -- request fresh-context workers
   for disjoint slices, and keep prompts self-contained either way: a forked
   child sees a filtered history, not your reasoning, and fork behavior is
   version-sensitive.)
3. One worker owns one slice and returns one handoff.
4. Verify before you trust. A worker's `Status: success` is a claim, not
   evidence.
5. Parallel reads are the default safe case.
6. Parallel writes require disjoint ownership or isolated worktrees. Codex is
   safer than a shared local-only model when workers run in separate sandboxes or
   worktrees, but write conflicts are still a coordination problem.
7. Continuous motion (within the stated budget). Handoffs reveal new work; treat
   each open question or suggested follow-up as a candidate second-wave task and
   spawn it. Keep going until every slice is terminal and the synthesis is
   complete -- stopping early while genuine follow-ups remain is the failure
   mode this skill guards against. (The manifest plus the stated budget is the
   stop function; see "Bounded Waves.")
8. Decomposition is entropy reduction. A vague goal is high-entropy: many
   plausible plans still fit. Shrink that space -- dig locally, then pull from
   attached resources, then ask the user only if it pays -- before you slice it.
   See "Entropy-First Decomposition."

## Bounded Waves - Size, Budget, and the Stop Function

A wave is bounded on purpose - but bounded by **completion and budget, not by a
wave count**. Unbounded "loop-until-done" burns tokens for little gain:
candidate generation is cheap, selection plateaus, and extra rounds are
non-monotonic (more iterations can lower quality, not just cost). Equally real
is the opposite failure: stopping while the manifest still has open slices.
Keep the exploration, drop the runaway, never abandon un-terminal work.

- Width: 3-8 workers per wave (and within the concurrency limit: V2 allows 4
  concurrent agent slots including the manager by default, or
  `agents.max_threads + 1` when set -- with `max_threads = 6`, that is 7
  slots; batch wider waves). Size the wave so you can fully verify all of it.
  Go wider only with a cheap automatic check (tests,
  `codex exec --output-schema`, schema/exec) gating results.
  (Grounding: homogeneous-agent teams plateau around N~4-8 - added workers
  contribute redundant evidence, and diversity, not head count, escapes the
  ceiling - arXiv 2606.02646, 2602.03794.)
- Depth: the manifest is the stop function. Keep extending while any manifest
  slice is non-terminal AND the last wave added verified progress. Stop only on
  one of three conditions: completion (every slice terminal, synthesis done),
  stagnation (nothing new + outputs near-duplicate the last wave, or a quality
  drop), or budget exhaustion. State the budget up front in the run-shape line
  - a worker or token budget, not a wave count (e.g. `budget: ~20 workers`). A
  realistic run is often `12 + 3 + 1` workers across three waves, and a
  decomposition cascade on a vague goal legitimately runs more. (Grounding:
  verification-driven replan loops stop on completeness thresholds, diminishing
  returns, and token budgets, not fixed iteration caps - VMAO, arXiv
  2603.11445; convergence-based stopping beats fixed `max_iterations` at parity
  quality - arXiv 2606.27009.)
- Scouting is cheap - don't let it eat the budget. Entropy-reduction waves
  (scouting, decomposition) run on cheap models/low effort and count separately
  from the execution budget. Never end a run "out of waves" when the budget was
  consumed by discovery before execution started.
- Budget ~60% generation / 40% verification; selection is the scarce resource.
- Match width to difficulty: easy -> 1 + light refine; medium -> 3-5;
  hard/open-ended -> 5-8 for diversity; hardest/novel -> escalate reasoning/model,
  don't loop.
- Anti-poisoning: carry only a distilled, verified handoff (winner + short
  critique) into the next wave, never raw transcripts or losing candidates.
  Exception: constraints are pinned, never summarized - the manifest, stop
  conditions/budget, and safety/scope rules travel verbatim through every
  synthesis and compaction (compaction measurably drops in-context constraints;
  arXiv 2606.22528).

Loop-until-done is justified only when ALL hold: a cheap reliable ~ground-truth
verifier exists; the signal is crisp/actionable (a failing test, not "try
harder"); each iteration shows measurable progress; easy-medium difficulty; still
hard-capped. Fits code-with-tests/exec-feedback; misfits open-ended
research/writing/design.

## Entropy-First Decomposition

Before you fan out, treat the goal as an entropy-reduction problem: shrink how
many plausible interpretations and plans still fit what you know. A vague,
high-entropy request ("build a Flappy Bird game", "make my app faster") does not
slice cleanly yet -- reduce the uncertainty first, then decompose the
low-entropy version. Name what is uncertain, because the two kinds resolve
differently:

- Specification uncertainty -- what the user wants (ambiguous goal, missing
  acceptance criteria, unstated constraints). Resolve by stating an explicit
  assumption and proceeding, or -- only when a wrong guess is expensive -- by
  asking.
- Environment / knowledge uncertainty -- facts you do not have yet but can get
  (repo shape, schema, API behavior, current docs, data size). Resolve by
  gathering, not by asking.

Spend the cheapest action that buys the most certainty first -- an
information-gain ladder -- and aim each probe at the unknown whose answer
eliminates the most plans (the highest-information question splits the
surviving interpretations roughly in half):

1. Dig locally first (cheap): inspect local state in the manager thread (list,
   read schema/README, grep, sample data). This is Step 0; it often collapses
   most of the uncertainty for free.
2. Then pull from attached resources: if local state lacks the answer, spawn a
   small scouting wave of `explorer`/research workers to fetch it (docs, MCP,
   web) on a fast low-cost configuration (`gpt-5.6-terra` or short-context
   `gpt-5.6-luna` at `low`/`medium`; see Step 2).
3. Ask the user last, and only when it pays: when residual specification
   uncertainty is high and a question's expected information gain beats its cost.
   Most requests carry enough to proceed on a stated assumption.

Then cascade: one request becomes a decomposition wave (understand -> locate
unknowns -> draft the plan) -> verify -> an execution wave that builds the
subtasks least-to-most (each verified result lowering uncertainty for the next),
with more scouting sub-waves wherever entropy stays high. Track the living plan
with `update_plan`; stop reducing when entropy is low enough to act -- the
verification gate doubles as "is the uncertainty low enough to commit?" (Worked
example: `references/examples.md`.)

## The Loop

Track the run with Codex's plan mechanism (`update_plan`) whenever the workflow
has more than a couple of moving parts.

### Step 0 - Discover Serially

Do not fan out blind. First inspect enough local state to learn the natural
shape of the work:

- List directories or data sources.
- Read schemas, manifests, READMEs, package boundaries, or route maps.
- Sample representative records/files.
- Count rows, files, modules, routes, messages, or scope size.
- Identify likely independent slices and risky overlap.

This manager-side discovery prevents duplicate worker scopes, blind spots, and
mis-sized chunks.

### Step 0.5 - Stage and Verify Coverage

Codex subagents inherit the current sandbox, approvals, MCP, and tool access, so
remote or messy data does not always need to be staged locally first. Still stage
data when it reduces risk or repeated work:

- Export remote/database data once if credentials, rate limits, or query cost
  would make every worker redo the same setup.
- Normalize noisy inputs once: strip wrappers, binary blobs, boilerplate, and
  irrelevant logs.
- Pre-chunk huge corpora into exact per-worker files or ranges.
- Keep one scratch dir per run (e.g. `.waves/<run>/` with `staging/`,
  `handoffs/`, `synthesis-wave-N.md`) so prompts cite paths instead of
  pasting content and later waves re-read files, not chat history.

Then run a pre-fan-out gate:

- Total rows, files, messages, modules, routes, or records.
- One line per slice with ID/range/path/date bounds and item count.
- Partition-sum check: slice counts add back to the total.
- Duplicate/gap check: no overlapping ranges, missing IDs, bad sort, or empty
  chunks.
- Central fix-and-recheck if any anomaly appears.

This serial prep is often the largest phase. The parallel fan-out is fast once
inputs are clean and coverage is proven.

### Step 1 - Decompose into Independent Slices

Size the run itself first, out loud: weigh breadth (how many independent
slices), depth (reasoning per slice), ambiguity (see "Entropy-First
Decomposition"), and stakes (this sets verification tiers), then state the
chosen shape in one line before spawning -- e.g. `Run shape: one wave, 4
workers; second wave only if handoffs expose gaps.` On the fence between two
shapes, pick the smaller and say so. If no wave is needed, do the task in the
manager thread and say that -- never present inline work as wave coverage.

Choose the split axis that gives each worker clear ownership:

- Data chunks: disjoint ID ranges, date ranges, files, or CSV rows.
- Workstreams: separate technologies, product areas, research questions.
- Repo modules: non-overlapping path sets or package boundaries.
- Audit dimensions: security, performance, correctness, tests, maintainability.
- Verification rows: one claim, citation group, or metric per verifier task.
- Code edits: disjoint file/module ownership, preferably in worktrees for
  heavier changes.

For a large wave, usually 5 or more workers, state the decomposition plan and
the pre-fan-out coverage gate to the user before spawning so they can redirect
cheaply.

Respect `agents.max_threads`. Current Codex docs say it defaults to `6` when
unset. If you need more slices than available threads, batch them into waves.

Then triage each slice on three axes (classify-and-act): the **Codex role**
(table in Step 2), its **dependencies** (which slices it needs verified output
from -- most have none; a real dependency edge is what separates waves), and a
**verification tier** - `auto-accept` (low-stakes, corroborated) ->
`single verifier` -> `multi-model/multi-pass panel` (high-stakes) -> `debate`
(contested, no ground truth). Spend verification where a wrong claim is expensive,
not uniformly.

Record the triage as a **wave manifest** - one row per slice (`slice | scope |
role | effort | depends_on | verification tier`), written to the plan or
`.waves/<run>/manifest.md` before spawning. `depends_on` defines the wave
boundaries: a wave is every not-yet-run slice whose dependencies are all met,
and a dependency is met only when its handoff has been **verified** (Step 3),
not merely returned. Launch wave 1 (no dependencies) in parallel; launch each
dependent slice with the distilled, verified findings (or their
`.waves/<run>/` path) folded into its self-contained prompt, and keep
unrelated slices parallel. The manifest doubles as the **completion gate**: N
rows spawned means N handoffs collected and checked off before synthesis
(Step 3). It is also the **spawn-plan audit**: V2 delegation payloads are
encrypted after dispatch, so the manifest review before spawning is the only
point where a human (or the manager) can inspect what each worker was asked
to do.

### Step 2 - Fan Out with Codex Subagents

Spawn all workers whose dependencies are met (handoffs verified, not just
returned) in the same manager turn when possible. In Codex, the stable
interaction is explicit: "spawn one agent per
slice, wait for all of them, then summarize/synthesize." When the active tool
surface exposes direct subagent tools, use those. On the current (V2) surface
the names are `spawn_agent`, `send_message`, `followup_task`, `wait_agent`,
`interrupt_agent`, and `list_agents`; threads resumed from before the V2
runtime instead expose the legacy V1 set (`spawn_agent`, `send_input`,
`resume_agent`, `wait_agent`, `close_agent`). Read the live registry and use
whichever set is present.

Pick the smallest capable role:

| Slice | Codex role | Notes |
| --- | --- | --- |
| Read-heavy code/data exploration | `explorer` | Best for targeted codebase questions and evidence gathering. Use `gpt-5.6-terra` (or short-context `gpt-5.6-luna`) with low reasoning for fast file reads and scans. |
| General research, docs, MCP/web work | `default` or custom docs researcher | Codex workers inherit available MCP/tooling. Use a custom agent when the research shape repeats. |
| Implementation or fixes | `worker` | Give explicit ownership of files/modules and warn that other workers may be active. |
| Review/security/test-risk audit | custom reviewer | Use read-only sandbox and higher reasoning for correctness/security work. |
| Browser/UI investigation | custom browser debugger | Give browser tooling and ask for evidence, not broad edits. |
| Verification of important claims | custom verifier | Give claim + cited sources, not the generator's reasoning. |
| Many row-shaped tasks | `spawn_agents_on_csv` | Experimental; use one CSV row per work item and require `report_agent_job_result`. |

A missing role is not permission to skip it. Spawning an unknown `agent_type`
fails with an error rather than falling back, and `.codex/agents/` roles load
only in trusted projects -- so when a custom role you want is unavailable in
the active surface, spawn `default` (or `worker`/`explorer`) with that role's
instructions inlined in the worker prompt instead of dropping the role.

On GPT-5.6's V2 runtime, **inlined role instructions are the primary pattern,
not the fallback**: custom TOML role routing has been unreliable on Sol/Terra
(roles resolving to null, model/sandbox pins ignored -- openai/codex #31814,
#32587, #32782; per-spawn `model`/`reasoning_effort` overrides return in
0.145+, honored only when the user, AGENTS.md, or skill instructions
explicitly request them -- which this skill's routing instructions do). V2
also exposes `agent_type` only when custom agents are registered. So: put the
role in the prompt, state the intended model/effort explicitly per spawn, and
treat TOML as optional tuning to re-verify per release rather than required
setup.

Route both the model tier and the reasoning effort per slice. The GPT-5.6
family (GA 2026-07-09) is the current default: `gpt-5.6` (alias for
`gpt-5.6-sol`, the flagship) for the manager, verifiers, synthesis, and hard
slices; `gpt-5.6-terra` for lighter/faster subagent work (the official Codex
guidance) and balanced long-context reads; `gpt-5.6-luna` as the cheapest
option for lightweight, short-context slices -- classification, row-shaped
work, small-chunk reads -- but never long-context reads (Luna's recall
collapses on 256K+ contexts per OpenAI's MRCR tables; note Codex clients
currently treat GPT-5.6 context as 272K anyway, so keep chunks well under
that). Spawn caveat: Luna is still on the V1 runtime, so **Sol/Terra V2
parents currently cannot spawn Luna children** -- Terra is the cheap tier for
spawned workers; use Luna from the main thread, `codex exec` fleets, or
CSV fan-out surfaces instead. Terra-vs-Luna is contested among independent
evals; the poles are not: lightweight -> Luna, hard/agentic -> Sol. `gpt-5.3-codex-spark` (research
preview) remains the near-instant text-only option, and `gpt-5.5` /
`gpt-5.4-mini` remain available as older fallbacks.

Effort ladder (model-dependent at both ends): `none`, `minimal`, `low`,
`medium`, `high`, `xhigh`, `max`, plus `ultra` as a Codex product setting (not
an API effort) that runs `max` with proactive multi-agent (~4 parallel agents,
roughly 3-4x single-agent cost; Plus+ plans; Codex warns about its
concurrency). Use `low`/`medium` for scouting and all-around research, `high`
for coding and verifying, `xhigh`/`max` for orchestration, deep problem
solving, and pre-fan-out synthesis; escalate a stuck high-stakes slice to Sol
at `max` before considering `ultra` (which also flips delegation to proactive
-- see the native-delegation note above). The live per-spawn field is
`reasoning_effort`; the config / custom-agent TOML key is
`model_reasoning_effort` -- set effort on each worker, not only in config. On
0.144.x the V2 per-spawn `model`/`reasoning_effort` overrides were hidden
(children silently inherited the parent's model and effort); 0.145+ exposes
them by default, honored when the user, AGENTS.md, or skill instructions
explicitly request routing. Overrides work only on fresh-context spawns --
full-history forks always inherit. **Verify what actually ran**: children
inheriting the wrong model/effort was the top July-2026 failure mode, so
check each worker's reported model/effort (or judge by output quality)
instead of trusting the requested settings. Speed tier is a user preference:
honor `/fast` / `service_tier` if the user enabled it and don't force it;
honor any model/effort the user named, and if a requested model is
unavailable, say so rather than substituting.

### Step 3 - Collect and Verify Handoffs

Codex handles spawning, routing follow-ups, waiting, and closing in the manager
workflow. Current docs say when many agents are running, Codex waits until all
requested results are available and returns a consolidated response.

**Completion gate first:** check every handoff off against the wave manifest -
N spawned means N accounted for. A worker that never returns, errors out, or
comes back `partial`/`blocked` is a hole in the wave. **Worker failure
ladder:** (1) re-task once, narrower -- steer or continue the same worker
(V2: `send_message` to pass info without triggering a turn, `followup_task` to
assign a new turn; legacy V1 threads: `send_input`, `resume_agent`) when the
slice just needs continuation, or re-spawn fresh with a narrower scope and a
note about what came back. Re-task the same worker only for continuation of
its own slice -- it keeps its prior context, which contaminates an unrelated
assignment; (2) if it fails again, do that slice in the manager thread; (3) if
it stays blocked, carry the slice into the synthesis explicitly as
`not-covered` - never average over a missing slice as if coverage were
complete.

Avoid manual polling loops. Continue non-overlapping local work while workers
run; wait only when synthesis is blocked on their results. For each handoff:

- Check `Status`.
- Check `Coverage` against the assigned slice.
- Extract `Key findings`, evidence, confidence tags, and source paths/URLs.
- Preserve `Sources` and `Confidence & verification`.
- Treat each `Open questions` and `Suggested follow-ups` bullet as a candidate
  second-wave task: accept, reject, or consolidate it. Spawning a focused
  follow-up wave for real gaps is the normal path, not an exception.
- Reconcile contradictions across workers before presenting claims as settled.

Run cheap checks on every important finding:

- Evidence is present.
- Cited path/URL/range resolves.
- Evidence actually supports the claim.
- Scope matches the assigned slice.
- Headline counts can be re-counted from source.
- Confidence labels are preserved.

Accept only evidence-backed, scope-correct, non-contradicted findings. Demote,
re-task, or verify the rest. Then **compress at the barrier**: write the
distilled synthesis to `.waves/<run>/synthesis-wave-N.md` and work from that
file - next-wave prompts cite paths, never re-paste raw handoffs. Pin the
constraints through the compression: the manifest, stop conditions/budget, and
safety/scope rules are copied verbatim into every synthesis file, never
paraphrased (see "Bounded Waves" anti-poisoning note).

### Step 3.5 - Spawn Verifier Passes When Needed

Verification is the manager's highest-leverage job: checking a claim is usually
cheaper than generating it, and unchecked errors compound across waves.

Use a dedicated verifier when a claim is high-stakes, contested, surprising,
citation-heavy, single-sourced, or low-confidence. Give the verifier:

- The atomic claim.
- The cited source paths/URLs/commands.
- The acceptance question.
- No generator reasoning, and no authorship labels (judges favor output marked
  as their own; blind them).

The verifier returns `supported`, `partly-supported`, `unsupported`, or
`source-not-found` per claim. For many claims, prefer `spawn_agents_on_csv` when
available: one claim per row, fixed JSON result via `report_agent_job_result`.
If the CSV tool is unavailable, spawn normal verifier subagents in waves under
`agents.max_threads`.

### Step 4 - Second Waves (continuous motion)

Multi-wave is the normal shape, not an exception: a realistic run is often
`12 + 3 + 1` workers across three waves rather than one giant burst. Spawn
another wave whenever first-wave handoffs expose:

- Missing coverage.
- Conflicting findings.
- A specialized follow-up that was out of scope.
- A verification task that can run while you synthesize.
- A dependent manifest slice whose `depends_on` handoffs just verified.
- A bounded implementation task after research converged.
- A new user request that narrows or redirects the scope.

Repeat until no slice is pending and nothing new surfaces, within the stated
budget (see "Bounded Waves" - the manifest is the stop function, not a wave
count). Skipping a follow-up wave is legitimate in exactly three cases -- name
which one applies when you decide: the remaining open items are
**primary-source-verified** (a verifier can't improve on the evidence),
**time-gated** (unresolvable until an external event; carry them as explicit
open items), or **genuinely contested** (independent quality sources disagree;
record the disagreement instead of sampling more).

Sequential second and third waves are spawned by the manager at depth 1 and are
encouraged -- they are NOT what `max_depth` limits. `agents.max_depth` (default
`1`) governs *recursion* only: a worker spawning its own sub-workers. Keep
recursion off by default and raise `agents.max_depth` deliberately and tightly
only if a recursive subplanner is truly needed; manager-driven waves need no
such change.

### Step 5 - Deliver One Synthesized Artifact

Do not forward raw handoffs as the final answer. Produce the user's requested
artifact: report, roadmap, code patch, audit, decision memo, or implementation
plan. Cite worker evidence when it helps, especially file paths, line numbers,
data ranges, URLs, and unresolved uncertainties. Carry confidence into the final
output: `verified`, `single-sourced`, or `unverified`. Never turn a
low-confidence handoff into a confident sentence.

If implementation is required after the research wave, either:

- Make the edits yourself in the manager thread after reading all handoffs.
- Spawn a bounded implementation wave with disjoint file ownership.
- Use Codex app worktrees or `codex exec` in separate git worktrees for heavier
  parallel code attempts.

Verify the deliverable itself:

- Run tests, validators, `curl`, screenshots, parsers, or smoke checks as
  appropriate.
- Regression-check sibling routes/files touched by the work.
- Re-read or grep critical files you wrote before relying on them.
- For generated artifacts, prefer a deterministic validator script or schema.

## Worker Prompt Contract

Every worker prompt includes:

1. Overall goal as context only.
2. The worker's exact slice and ownership.
3. Where to look: paths, data ranges, URLs, MCP/docs sources, commands, or repo
   modules.
4. Coverage rule: read the assigned slice completely when feasible, report
   counts read such as `388/388`, and call out skipped files/ranges.
5. Evidence rule: cite-or-drop every important claim, tag confidence
   (`high|med|low`), and say what would change the conclusion.
6. What not to do: avoid owning the whole task, avoid sibling scopes, avoid
   editing unless explicitly assigned.
7. The required handoff format from `references/handoff-format.md` - and keep
   it a digest: roughly 15 findings max with one-line evidence each; large
   artifacts (tables, logs, full lists) go to a file, cite the path.

End every worker prompt with the copy-paste ending for its worker type
(generic, research, implementation, or verifier) from
`references/handoff-format.md` § "Prompt endings per worker type".

## CSV Fan-Out

Use `spawn_agents_on_csv` when the work is naturally one row per worker: files,
incidents, packages, PRs, migration targets, messages, customer records, or
claims to verify.

Manager responsibilities:

- Create a CSV with a stable `id_column`.
- Put enough per-row context in columns for a self-contained prompt.
- Provide an `instruction` template with `{column_name}` placeholders.
- Provide an `output_schema` when downstream synthesis needs machine-readable
  results.
- Require each worker to call `report_agent_job_result` exactly once.
- Set `output_csv_path`; use `max_concurrency` below or equal to
  `agents.max_threads`.

For a verifier pass, build `claims.csv` with `claim_id`, `claim`, `sources`,
`acceptance_question`, and optional `stakes`. Require JSON fields: `verdict`,
`evidence`, `source_status`, `correction`, `confidence`, and `gaps`.

If the CSV tool is unavailable in the active Codex surface, split the CSV into
normal worker or verifier slices and use the handoff format.

## Generate-and-Filter and Tournaments

For open-ended ideation or "produce the single best X", generate several
candidates and filter rather than trusting one attempt:

- Cheap filter first: gate candidates through a near-ground-truth check (tests,
  `codex exec --output-schema`, schema/exec, dedup/clustering) before spending
  judge tokens. Generation is cheap; judging is not.
- Selection ladder, not all-pairs: dedup/cluster -> shortlist -> pairwise-judge
  only among finalists. A naive O(N^2) tournament wastes tokens on also-rans.
- Competing implementations: use Codex app Worktree mode or `git worktree` plus
  one `codex exec` per attempt, then inspect/test/merge the winner.
- Budget check: at equal cost, k independent attempts plus a majority vote or
  cheap filter usually beats critique/debate loops -- benchmark any iterative
  loop against that baseline before paying for it.

## Parallel Writes in Codex

Codex subagents are a good fit for parallel write work when you use worktrees,
separate sandboxes, or disjoint ownership. Still treat write coordination as a
real merge problem:

- Read/research/test/log analysis: safe default.
- Disjoint edits in one checkout: acceptable when ownership is explicit and
  paths do not overlap.
- Overlapping edits: avoid. Have workers propose handoffs, then implement
  serially.
- Competing implementations: use Codex app Worktree mode, or plain
  `git worktree` plus one `codex exec` run per attempt.
- Always inspect and test the merged result in the manager thread.

## Native Verification Surfaces in Codex

Use these where they fit:

- Tests, validators, type checks, linters, browser checks, and direct source
  recounts are the strongest verification signals.
- Custom `verifier` agents are the Codex-native replacement for a dedicated
  verifier worker.
- `spawn_agents_on_csv` is ideal for a verifier-per-row pass when exposed.
- `codex exec --output-schema` gives machine-readable verification in scripted
  fleets.
- Codex `/review`, GitHub code review, and reviewer custom agents help for code
  risk review.
- `approvals_reviewer = "auto_review"` is an approval/security reviewer only; it
  is not a general claim-verification hook.
- Lifecycle hooks exist in config, but current public docs do not confirm a
  general eval/critic hook for arbitrary worker findings.

## Escalating Beyond One Interactive Thread

Use this skill for interactive, bounded fan-out inside one Codex task.

### Coordinator Thread Mode (long-horizon, Desktop only)

Codex Desktop threads can receive `codex_app.*` thread-management tools
(`create_thread`, `list_threads`, `read_thread`, `send_message_to_thread`,
`fork_thread`, `handoff_thread`, `set_thread_title`, `set_thread_pinned`,
`set_thread_archived`). When present, a long-lived **coordinator thread** can
run waves whose workers are *visible, durable Desktop threads* instead of
subagents -- useful when a run outlives one task, needs user-clickable worker
threads, or maintains persistent per-module "lanes."

Write it defensively; the tools are undocumented and gated (checked
2026-07-19):

- Availability: Desktop-local threads only, behind a feature flag. Remote,
  mobile, and CLI-started threads miss the tools; threads created before the
  tools existed resume without them. **Probe before fan-out** (`tool_search`
  for `create_thread`); if absent, fall back to normal subagent waves -- never
  fake thread orchestration.
- The coordinator must be a fresh, Desktop-local thread. `codex exec`-created
  threads don't appear in the sidebar or `list_threads`.
- Same handoff discipline as subagents: message a worker thread and require the
  structured handoff back via `send_message_to_thread`; **never `read_thread` a
  full worker transcript into the coordinator** -- that is the context
  pollution this skill exists to prevent. Threads accumulate context forever,
  so reuse a worker thread only for its own lane, never for an unrelated slice.
- Run a heartbeat loop instead of busy-polling: on a fixed cadence check worker
  status, collect handoffs, re-task or replace stalled workers, and spawn
  follow-up threads until the manifest is terminal.
- Worktree hygiene: one branch + worktree per worker thread; pin the
  coordinator; archive workers when merged. Codex keeps ~15 managed worktrees
  and auto-deletes on archive; the sidebar hydrates only ~50 recent threads,
  so title workers consistently and track them in the manifest, not the
  sidebar.

For scripted or CI-style fleets, use `codex exec` with explicit sandbox and
model settings, often one process per git worktree. `codex exec --json` and
`--output-schema` are useful when another script needs stable events or
machine-readable results.

For always-on, team-scale orchestration, use the Symphony pattern: an issue
tracker or queue as the control plane, one agent workspace per item, bounded
concurrency, retries, observability, and human review. Treat Symphony as a
reference/spec pattern, not a drop-in replacement for this interactive skill.

## Checklist

- [ ] Used `update_plan` for multi-wave work.
- [ ] Discovered the shape of the problem before decomposing.
- [ ] Reduced entropy before slicing (dug locally -> pulled from attached
      resources -> asked the user only if it paid); sliced the low-entropy goal.
- [ ] Stated the run shape AND the budget (workers/tokens, not a wave count)
      in one line before spawning (on the fence -> the smaller shape); never
      presented inline work as wave coverage.
- [ ] Staged or normalized inputs when it materially helps.
- [ ] Verified coverage before spawning: counts, bounds, partition-sum,
      gaps/duplicates.
- [ ] Slices are independent (or their `depends_on` edges recorded) and sized
      to `agents.max_threads`.
- [ ] Wrote the wave manifest (slice / role / effort / depends_on /
      verification tier) before spawning; launched dependent slices only after
      their dependencies' handoffs were verified; checked every row off at
      collection (completion gate); ran the failure ladder on missing/blocked
      slices.
- [ ] Each worker prompt is self-contained and ends with the handoff contract.
- [ ] Picked `explorer`, `worker`, `default`, custom agents, verifier agents, or
      `spawn_agents_on_csv` deliberately.
- [ ] Routed scouting / read-heavy waves to a fast low-cost configuration
      (`gpt-5.6-terra`, or `gpt-5.6-luna` for short-context slices only, at
      `low`/`medium`); reserved Sol + high/max effort for coding, verification,
      and synthesis; never gave Luna long-context reads.
- [ ] Avoided manual polling loops; waited only when synthesis was blocked.
- [ ] Read every handoff and resolved conflicts.
- [ ] Preserved per-finding confidence labels.
- [ ] Carried only distilled, verified syntheses between waves (no raw
      transcripts or losing candidates); pinned the manifest, stop conditions,
      and budget verbatim through every synthesis/compaction.
- [ ] Treated each open question / follow-up bullet as a candidate second-wave
      task; spawned waves for the ones that change the deliverable, coverage,
      or confidence; stopped only on completion, stagnation, or budget -- and
      named which of the three no-second-wave cases applied when skipping a
      follow-up.
- [ ] Verified high-stakes, conflicting, low-confidence, or uncited findings
      before synthesizing.
- [ ] Verified the final deliverable: re-ran/validated and re-read critical
      writes.
- [ ] Produced one synthesized deliverable.
- [ ] For edits, verified disjoint ownership or used worktrees.
