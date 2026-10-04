---
name: staff-session
description: "PM-GATED, never from a subagent. Agent Teams review for architecture calls."
allowed-tools: ["Agent", "Read", "Write", "Bash", "Glob", "Grep", "TaskCreate", "TaskUpdate", "TaskList", "TaskGet", "SendMessage"]
argument-hint: "--mode plan|review --tier standard|full [--members \"the Staff Engineer,the Director of Engineering,...\"] <input>"
---

# Staff Session — Agent Teams Planning and Review Driver

**`standard`/`full` tier requires agent teams** — `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1` in
`settings.json`'s `env`, applied at SESSION START and not toggleable mid-session. Without it every
named `Agent` call here is an ordinary background subagent and no team forms. `--tier lightweight`
does not depend on this — see Step 2.

The EM scopes the work, selects the team, spawns all teammates, and is **freed**; the team then
debates and synthesizes autonomously. Roles, models and counts: `pipelines/staff-session/
team-protocol.md` § Team Roles — read there, don't re-derive.

**Lightweight tier falls through to single-reviewer dispatch via `/review` (plan) or
`/review-code` (code) — no team created.**

## Arguments

`$ARGUMENTS`:
- `--mode plan|review` — required.
- `--tier lightweight|standard|full` — required. `lightweight` → single-reviewer dispatch.
  `standard` = 2 debaters. `full` = 3-5 debaters.
- `--members "persona-a,persona-b,..."` — optional override of auto-selection.
- `<input>` — required. Plan mode: objectives document/text. Review mode: artifact path.

## Step 1 — Parse Arguments and Setup

Parse `--mode`, `--tier` (both required — fail with usage message if missing), `--members`
(optional), remaining text as `<input>`.

Generate run ID (`YYYY-MM-DD-HHhMM`), spawn timestamp, topic slug from input. Create
`docs/research/{run-id}-workdir/` (shared paper-trail convention with
`/coordinator:notebooklm-research` — detail: wiki). Set output path: plan mode →
`docs/plans/YYYY-MM-DD-{topic-slug}.md`; review mode →
`state/review-findings/YYYY-MM-DD-{topic-slug}-staff-review.md`. Advisory path:
`{scratch-dir}/advisory.md`.

Announce: "Running `/staff-session --mode {mode} --tier {tier}` on '{topic}'."

## Step 2 — Tier Routing

**`--tier lightweight`:** do NOT create a team. Route to `/review` (plan artifacts) or
`/review-code` (code artifacts) with the specified member (default `the Staff Engineer`). Announce and
**STOP — the rest of this command does not execute.**

**`standard`/`full`:** forms a team. `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS` is `"1"` by default and
this skill forms one on that default — every named `Agent` call anywhere becomes a teammate that
returns no result. Continue to Step 3.

## Step 3 — Scope (EM Direct)

Write `{scratch-dir}/scope.md` per the template in `pipelines/staff-session/templates-and-fields.md`
§ Step 3. Plan mode: EM writes objectives and constraints only — never the plan. Review mode: EM
provides artifact path and focus areas only — never pre-formed findings.

## Step 4 — Select Team Composition

`--members` specified → those exact slugs are the debater list.

Not specified → match topic + scope to a domain category (the one piece of genuine judgment this
step retains). For `--tier full`, judgment-select 1-3 additional personas and append to an
explicit override list.

**Resolve the roster via the CLI, not a hand-maintained table:**

Shape W (rung 0) — ladder and shapes: `${CLAUDE_PLUGIN_ROOT}/snippets/resolve-coordinator-bin.md`.
    `& "$env:COORDINATOR_SETTINGS_HOME\bin\staff-session-assemble.exe" --session-mode <plan|review> (--domain-signal "<category>" | --slug <slug> [--slug <slug> ...]) --json`

Returns `{personas: [{slug, agent_file, subagent_type}, ...], narration, source}`. Fails loud
(usage exit) on an unresolvable domain signal, unknown slug, or `the Director of Engineering` as a debater — surface that
error to the PM verbatim. `the Director of Engineering` is never a valid debater slug — fixed synthesizer identity
(`coordinator:eng-director`), spawned separately in Step 6. Resolver mechanics: wiki.

Debater count from the resolved roster: `standard` = 2 (default pair), `full` = 3-5 (default pair
+ judgment-selected additions).

Announce composition to PM before creating the team, using the resolved `personas[].slug`:
> "I'll run this with **{Persona A}** and **{Persona B}** [+ **{Persona C}**...] debating, plus a
> staff synthesizer. Proceeding."

## Step 5 — Create Tasks

Order matters — earlier task IDs are referenced in blocking-chain setup.

1. **Synthesizer task** (created first, blocked by all debaters below): subject "Synthesize all
   debater positions into final {plan|findings}"; description points to reading
   `{scratch-dir}/*-position.md`, writing `{output-path}` + `{scratch-dir}/synthesis.md`, and
   `{scratch-dir}/advisory.md` if warranted. Save as `{synthesizer-task-id}`.
2. **Debater tasks** (one per persona, no blockers on creation): subject "{Persona Name}:
   {mode} session on {topic}"; description points to `{scratch-dir}/scope.md`, the mode-specific
   research/debate/write instruction, output to `{scratch-dir}/{persona-slug}-position.md`, DONE
   to synthesizer. Collect all IDs.
3. `TaskUpdate(taskId: "{synthesizer-task-id}", addBlockedBy: [<all debater task IDs>])`.

## Step 6 — Spawn All Teammates

Read the planner/reviewer/synthesizer prompt templates from
`${CLAUDE_PLUGIN_ROOT}/pipelines/staff-session/`. For each debater, read the persona identity
excerpt from `personas[].agent_file` (Step 4's roster), injected at `[PERSONA_IDENTITY]`. Fill all
`[BRACKETED_FIELD]` placeholders — see `pipelines/staff-session/templates-and-fields.md` § Step 6
for the full field list.

**Spawn ALL teammates in a single message (parallel):** one `Agent(name: "{persona-slug}", model:
"opus", subagent_type: "{personas[i].subagent_type}", prompt: <filled prompt>)` per debater
(subagent_type from Step 4's roster, never hardcoded — e.g. game-dev personas use `game-dev:`,
not `coordinator:`), followed by `TaskUpdate(taskId: "{debater-id}", owner: "{persona-slug}")`;
then `Agent(name: "synthesizer", model: "opus", subagent_type: "coordinator:eng-director", prompt:
<filled synthesizer prompt>)` + its `TaskUpdate`.

## Step 7 — EM Is Freed

After spawning, announce:

> "Staff session running on '**{topic}**' with **{N} debaters** ({names}) + **1 synthesizer**.
> Debate phase: floor 3 min, ceiling {MAX_MINUTES} min. Synthesizer unblocks when all debaters
> complete. I'm available for other work — I'll be notified when the synthesizer completes."

**You are now free to continue with the PM.** Do not poll, monitor, or send WRAP_UP — the team
self-governs via `team-protocol.md`.

## Step 8 — On Completion Notification

1. Read `{output-path}`; verify substantive content (not just headers/a stub).
2. Mode-specific verification: plan mode → `## Implementation Plan` section with
   tasks/files/steps, and the marker `**Review:** Staff session ({participants}) — debated and
   synthesized. Ready for enrichment.` present byte-exact (this line is the single authoritative
   producer copy `enrich-and-review`'s gate matches against — never hand-type a second copy).
   Review mode → findings structured with severities/persona attributions, `## Verdict` line
   present.
3. Check for advisory: `test -f {scratch-dir}/advisory.md`; read if present.
4. Commit the output artifact (scoped): `git add -- {output-path}` then `git commit -m
   "staff-session: {mode} — {topic-slug}" -- {output-path}`. Then commit the paper trail as an
   explicit file list, not the whole workdir: `git add -- {scratch-dir}/scope.md
   {scratch-dir}/*-position.md {scratch-dir}/synthesis.md {scratch-dir}/advisory.md` then
   `git commit -m "staff-session: paper trail — {topic-slug}" -- {scratch-dir}/scope.md
   {scratch-dir}/*-position.md {scratch-dir}/synthesis.md {scratch-dir}/advisory.md` (omit
   `advisory.md` from both commands when the synthesizer wrote none) — the archive op in item 5
   cannot archive an untracked workdir; detail: wiki.
5. Archive-and-cleanup: invoke `fleet.archive_paper_trail` with `run_id={run-id}`,
   `topic_slug={topic-slug}`, `dry_run=false`. Moves `{scratch-dir}` to
   `docs/research/archive/YYYY-MM-DD-{topic-slug}/`, lands one scoped commit, removes the source
   tree. Safe no-op on re-run. Mechanics and CLI-trampoline caveat: wiki.
6. Team auto-cleans on session exit — no explicit teardown.
7. Present to PM: mode-specific framing ("ready for `/enrich-and-review`" / "synthesized
   findings"), 2-3 bullet executive summary, output path, and — if advisory exists — a pointer to
   the archived advisory.

## Error Handling

See `pipelines/staff-session/templates-and-fields.md` § Error Handling Matrix for the full
failure-mode → action table (debater crash, synthesizer failure, DONE-not-received, debate loops,
unknown slug, missing output).
