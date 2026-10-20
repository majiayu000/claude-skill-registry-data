---
name: orchestrate
disable-model-invocation: true
description: >-
  Enter thin-orchestrator mode for a large, multi-step task with several heterogeneous or
  investigation-heavy parts — decompose and delegate rather than execute directly, capping
  context/token cost by keeping the main session lean and pushing all file I/O and execution into
  cheap isolated subagents. Not for mechanical single-pass changes where a scripted edit plus a
  typecheck is cheaper than delegating (e.g. a repo-wide rename), nor for a single one-off subagent
  dispatch. Stays in effect for the rest of the session once entered.
argument-hint: "[goal]"
---

# Orchestrate

Enter **thin-orchestrator mode**: the main session plans and delegates, and never
executes directly. Hold this posture for the rest of the session unless told
otherwise.

## Why this exists (the cost model)

The dominant cost lever in agentic work is **context isolation**, not model
choice. In a single agentic loop every tool result accumulates in one window and
is re-billed on every subsequent turn, so cost grows roughly quadratically with
task length. Routing to cheaper models is a second-order saving stacked on top.

One line: **the orchestrator's window is the expensive thing — guard its size,
keep its prefix stable, and let cheap isolated workers absorb all the volume.**

The main session is the orchestrator (not a file). Workers run as subagents —
each in a fresh, isolated context, only its final message returning to the
parent, so raw file contents and tool spew never land in the priciest,
most-rebilled window. Read-only exploration goes to the **built-in `Explore`
agent**; the `executor` and `verifier` workers ship with this plugin.

## Your job as orchestrator

- Restate the goal in one line, then produce a plan and a dependency-ordered list
  of subtasks.
- Dispatch each subtask to the matching subagent and wait for its summary.
- Maintain a compact **ledger** of results — one or two lines per completed
  subtask. Record outcomes, not contents.
- Synthesize, adjudicate ambiguity, and decide what to dispatch next.

## Hard rules

- **Do not read files, grep, glob, edit, or run tools directly.** All I/O and
  execution go to subagents. Raw file contents, search output, and tool spew must
  never enter your window.
- Hand each worker a tightly-scoped spec naming only the files/area in scope.
- Keep the ledger compact. If you need detail again, re-dispatch a worker to
  fetch it — re-deriving from a cheap worker beats carrying the raw output.
- Never re-read a worker's output yourself to check it. Verify against explicit
  acceptance criteria with the verifier.

## Delegation map

Launch the matching subagent for each subtask (set `subagent_type` to one of
these):

- **Explore** (built-in) — locating code, mapping call sites, summarizing how
  something works. Use before planning when the layout is unknown. Prefer the
  built-in over a custom agent here: it is read-only, reads excerpts rather than
  whole files, takes a breadth hint (`medium` / `very thorough`), and — unlike
  custom subagents — does **not** inherit `CLAUDE.md`, so it carries the least
  context tax of any worker. It starts without repo conventions, so put any
  convention the search needs into the spec.
- **executor** (Sonnet) — all code changes, edits, and multi-step
  implementation. Use instead of editing in the main session.
- **verifier** (Haiku) — checking an executor's output against acceptance
  criteria. Dispatch after every executor run.

> Gotcha: subagents run in the **background by default**, and a background
> subagent keeps only these built-in tools — `Read`, `Grep`, `Glob`, `Bash`,
> `PowerShell`, `Edit`, `Write`, `NotebookEdit`, `WebFetch`, `WebSearch`,
> `TodoWrite`, `Skill`, `ToolSearch`, `EnterWorktree`, `ExitWorktree`, `Monitor`,
> `TaskStop`, `SendMessage`, `Artifact`. Everything else is stripped whether
> inherited or named in `tools:`, and the removal is silent. `AskUserQuestion` is
> removed from _every_ subagent, foreground or background, so a worker can never
> stop to ask you something — put the answer in the spec or keep that step in
> this session.

## Resuming a worker vs. dispatching a fresh one

A completed worker can be resumed with `SendMessage` (its ID or name as `to`); it
auto-resumes in the background with its full prior context and needs no new
`Agent` call. This is a real lever, but it is **conditional, not a default** —
resuming re-sends the worker's entire accumulated transcript as input.

- **Resume** when the follow-up genuinely continues that worker's task _and_ its
  context was expensive to build (wide exploration, many files read), and it
  finished recently enough that the prompt cache is likely still warm. On a cache
  hit this is overwhelmingly the cheaper path.
- **Dispatch fresh** when the next task is independent, or when the worker's
  transcript has grown large relative to what the next step actually needs. On a
  cache miss you pay full input price for that whole transcript, which can exceed
  the cost of a fresh worker's much smaller prefix. Repeated resumes compound,
  since each one re-sends everything before it.
- **Never** resume merely to save re-reading one file — a cheap fresh worker is
  correct there.

`Explore` and `Plan` are one-shot: they return no agent ID and cannot be resumed.
Use `executor` or a custom agent when you expect to continue the work. A worker
also needs `SendMessage` in its `tools:` to message a sibling.

## Model routing

Route to the cheapest model that clears the bar (Opus → Sonnet → Haiku). Routing
matters most on the **output** side — workers generate the bulk of output tokens.

- **Opus** — orchestration, decomposition, synthesis, anything ambiguous (this
  session).
- **Sonnet** — most real execution: coding, transformation, multi-step work.
- **Haiku** — mechanical work only: extraction, classification, routing,
  single-file edits with an unambiguous spec, and verification. (Read-only
  exploration goes to the built-in `Explore` agent, not a Haiku worker.)

> Gotcha: the env var `CLAUDE_CODE_SUBAGENT_MODEL` takes highest precedence and
> forces _every_ subagent onto one model, overriding per-agent `model:` fields.
> Leave it unset to keep per-agent routing (useful only as a global cost ceiling).

## Spec discipline

- Calibrate spec detail to the worker's model: tight and explicit for Haiku,
  terser for Sonnet (let it reason).
- Don't over-specify trivial tasks — a cheap retry beats an expensive, exhaustive
  spec. Opus output is the most expensive token in the system.
- Give the verifier explicit acceptance criteria and the exact checks to run.

## Cost levers, ranked by dollar impact

1. **Keep the orchestrator's window flat.** Delegate all I/O; hold plan +
   summaries only. Biggest lever.
2. **Prompt-cache the stable prefix** (≈90% off cached input — automatic in
   Claude Code). The job is to keep the prefix lean and stable.
3. **Route to the cheapest model that clears the bar.**
4. **Trim what every subagent inherits** — a lean root `CLAUDE.md` is a tax paid
   by every worker on every turn. Push locality-specific detail into nested
   `CLAUDE.md` files (loaded on demand only when a file in that subtree is read)
   and on-demand conventions into `.claude/rules/` or skills. Splitting a root
   `CLAUDE.md` with `@imports` does **not** reduce context — imports load at
   launch into every session and subagent.
5. **Calibrate spec verbosity to executor capability** — bias toward cheap
   retries over exhaustive specs.
6. **Verify without re-importing** — check against acceptance criteria with the
   Haiku verifier, never by having the orchestrator re-read worker output.

Not cost levers: **parallelism** is a wall-clock lever (same total tokens, and it
can raise cost if it triggers redundant exploration); the **Batch API** discount
applies only to latency-tolerant offline jobs, not interactive sessions.

## Subagents, not Agent Teams

For a cost goal, prefer **subagents** (hierarchical fan-out/fan-in, isolated
context, only the final message returns). **Agent Teams** — peers communicating
via a shared mailbox/task list — use roughly **7× the tokens of a single
session** because they deliberately break the context isolation that drives the
savings. Reserve teams for tasks where mid-task peer communication is
unavoidable (cross-cutting refactors, multi-module features with
interdependencies); they buy wall-clock time and coordination quality, not cost.

Begin by restating the goal in one line, then produce the plan.
