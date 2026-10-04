---
name: workstream-start
description: Orient session — preflight, load context, choose work
allowed-tools: ["Read", "Grep", "Glob", "Bash"]
argument-hint: "[task-description]"
---

# Workstream Start — Preflight and Orientation

Orient this agent: verify the environment, load project context, choose work. Multiple agents may
run concurrently on the same repo — this orients ONE, not exclusive access. Contrast with
`/pickup`: this is general orientation; pickup is artifact-first, for a PM already pointing you
at specific work.

---

## Setup-freshness probe

If `state/.repo-setup-just-ran` exists, `/repo-setup` just ran. Delete it immediately (before
printing anything), print one line — `Setup just ran: running orientation once now.` — and
continue with Orient. Orientation runs exactly once per repo on a fresh setup; the sentinel never
suppresses it.

<!-- engine-gap: field=session.setup_just_ran producer=unknown memo=engine-gap-markers-name-a-memo-that-was-never-filed.md -->
Single-shot; race window and lifecycle: wiki.

**Machine profile.** A consumer box: `machine-local get coordinator.machine_profile` prints
`consumer`, or nothing and no `repos.*` path holds a `.coordinator-dev-repo` file. Skip
author-only steps there without comment.

## Orient

The session-cadence orient spine (health, staleness, handoff triage, branch checks, ...) is
computed for you. PowerShell hosts (Shape W,
`${CLAUDE_PLUGIN_ROOT}/snippets/resolve-coordinator-bin.md`):
`& "$env:COORDINATOR_SETTINGS_HOME\bin\orient-assemble.exe" brief --cadence session`. Read the JSON. Every `directives[]` entry names a CLI to run when not
`already_satisfied`; on a consumer box skip any entry that reads fleet state (group-EM watch,
cross-repo memo inbox, fleet registries, cockpit); every `judgment_points[]` entry is an open branch to resolve yourself —
present each with its `dispositions[]`, pick, don't drop any. Don't hand-run what these compute.

**Do NOT load, summarize, or act on any handoff the orient output surfaces** — a `ready-to-fire`
directive naming one is not implicit selection. When the PM asks for one to be picked up, read the
full file and set `HANDOFF_LOADED=true` for Engage — or the PM uses `/pickup`. A markdown in
`state/handoffs/`, `tasks/`, or `archive/` may already be addressed by later commits — verify
before treating it as pending.
<!-- engine-gap: field=handoffs.stale_advisory_reconcile producer=unknown memo=engine-gap-markers-name-a-memo-that-was-never-filed.md -->

**Route-to-baton default:** a memo/finding/triage item inside an active handoff's scope
(`state/handoffs/*.md`, `status: open|claimed`) gets a dated `## Routed from inbox triage
(<YYYY-MM-DD>)` note, committed with pathspec, then closed: `archive-stamp-cli resolve-memo <memo>
--decision accepted --decision-note "routed into <baton>" --realized-by "<baton>"
--in-repo-capture "<baton>"`. Open only if the capture didn't land. Other forks are `/pickup`'s.

**`tasks/`/`archive/` gitignored?** Warn — must track.

### Session residue not covered above

Bin paths below relative to the coordinator settings-home `bin/` directory — resolve per rung 0 /
Shape W in `${CLAUDE_PLUGIN_ROOT}/snippets/resolve-coordinator-bin.md` (PowerShell hosts) or rung 2 (POSIX hosts).

**One shell call** for the three independent, non-gating probes below (order doesn't matter among
them — none reads another's output):

- **Safety commit**, non-negotiable, don't ask, silent no-op if nothing to commit:
  `coordinator-safe-commit --blanket --invoking-command workstream-start "chore:
  workstream-start sweep — pre-orientation capture"`.
- **Setup-state self-heal**, silent: `coordinator-setup-state auto-record-if-source-is-live`.
- **Outbox drafts** (inbound staleness is already in the orient output):
  `workday-start-cross-repo-memo-outbox-surface` — non-empty → surface verbatim; empty → skip.

**Branch detection** stays its own call — it gates everything that follows: main is read-only.
Stay on a non-main branch if on one (this covers an environment-designated day branch, recorded as
`coordinator.dayBranch`). On main, run `sync-main --quiet` (report divergence
first), then — author box only — create the default `work/{machine}/{date}` (`-2` on collision),
superseded by the branch-day-span directive when present. A consumer box stays on the branch it
is on and cuts nothing. Diverged from `main` >2 days → recommend
`/merging-to-main`, wait for the PM; ≤2 days → continue silently.

### Context load — not part of the shared spine

**Lessons.** Enumerate `state/lessons/*.yaml` (`query-records --type lesson`); read `CONTEXT.md`
if present. Note the count — `CLAUDE.md` is already in context.

**Action items / roadmap.** Skip if `state/.workday-start-marker` has today's date.
Otherwise read whichever of `ACTION-ITEMS.md`, `ROADMAP.md` (or their `docs/` variants) exist,
first match wins; it gets a brief active/blocked/ready summary feeding the Engage menu.

**Orientation check.** SessionStart already injected orientation context — don't re-read it. No
fresh cache → point at `/workday-start` or `/update-docs`. Review-trail: glob
`state/review-trail/**/*.json` and `archive/review-trail/**/*.json`, sort by basename, surface the
last path (a frozen corpus — a historical stopping point, not a live gap).

**Doc index / fan-out.** `docs/README.md` present → note wiki/research/plan counts; without an
index → note `/update-docs` builds one. Use `fan-out-dispatch.py` for parallel executor prompts.

**Delegation (game-dev, author box only).** `project_type: game-dev` + `unreal` in `project_subtypes`
→ dispatch `Agent(subagent_type='example-game-repo-control:ue-{domain}')` for single-domain work.

**Project-RAG (author box only).** `project-rag` MCP available → call `project_subsystem_profile()`,
report the count; prefer `project_subsystem_profile("<name>")` over Explore.

---

## Engage

Choose work and load task-specific context.

### Work selection

**CRITICAL — handoff loaded?** If `HANDOFF_LOADED=true`: **the handoff IS the work order.** No
menu, no "what should this agent work on?", no listing items and waiting, no "want me to proceed?"
Read any referenced files not yet in context, then **dispatch the first action item — dispatch IS
running**, per pickup's dispatch-economics checklist (`skills/pickup/SKILL.md`). Multiple next
steps → execute in order unless the PM redirects.

> **Do not ask whether to dispatch** — invoking this skill IS the request for the dispatch this
> step names; it dissolves no gate this skill's own body names.

**If no handoff loaded — fresh-install branch — fires ONLY when ALL hold:** no handoff loaded
(established above), AND `$HOME/.claude/.coordinator-fresh-install` exists. Consume (delete) the
sentinel BEFORE emitting anything, so this never re-fires on a later no-handoff session, then emit
the fresh-install message: `~/.claude` is the live install to evolve, the onboarding handoff if
present, fallback first steps (co-write `CLAUDE.md`, `/repo-setup`, `/workday-start` daily).

**Otherwise, the standard work menu** — each option loads its own context once picked:

1. **Implementing** — find/read the relevant plan doc; summarize the first step.
2. **Fixing a bug** — identify the failing test/error/repro; read the relevant source.
3. **Reviewing** — identify the target (commits/files/PR); load review criteria.
4. **Research / exploration** — ask what to explore; no ceremony.
5. **Maintenance** — daily health check, weekly audit, or debt triage.
5a. **Strategy/ceremonies** — `/shape`, `/goal-setting`, `/roadmap-planning`, `/spike` (mechanism
    derisking; PM-gated, never EM/subagent-initiated — gating: `spike/SKILL.md` § Invoke Gating,
    pipeline position: wiki)
6. **Work the backlog** — central (`coordinator-state-root.py --central`) and local
   `state/improvement-queue/*.yaml`, surface depth; `state/bug-backlog/*.yaml` ≥10 open P1/P2, or
   any `status: open` in `state/cross-repo-commitments/`, → advocate `/bug-blitz` (skip silently
   if absent/empty).

   **Red-suite predicate — independent of backlog depth.** Read `state/test-red/<machine-local get
   coordinator.machine_slug>.yaml` if present (absent/malformed → skip silently, no error). Per
   tier, compute the delta against the comparison baseline (`acknowledged.baseline` when live and
   unexpired, else `previous.failing`), and advocate `/bug-blitz` — **naming the tier and
   surfacing the delta counts, never a bare "the suite is red"** — when `new` is non-empty, the
   acknowledgement is null/void/expired with `failing[]` non-empty, the acknowledged owner is
   closed while `failing[]` remains, or `failing` is `null` (never read as clean). Message
   wordings per case: wiki. An acknowledged, unexpired, all-`persistent` set advocates nothing.
   Never runs the test tier, never blocks — only reads the engine's record.
   <!-- engine-gap: field=test_red.advisory producer=unknown memo=engine-gap-markers-name-a-memo-that-was-never-filed.md -->
7. **Other** — ask the user to describe it; load relevant context.

`$ARGUMENTS` provided → use it directly, skip the menu. Surface the tracker's ready/executing
items and plan docs (`docs/`, `tasks/`, `tasks/plans/`) as concrete options. A fresh backlog item or ad-hoc ask with no sizing-object yet routes through
`coordinator:sizing` first.

### Status report

Two lines: repo state (uncommitted changes may be a peer's), current branch.
<!-- engine-gap: field=session.repo_status_summary producer=unknown memo=engine-gap-markers-name-a-memo-that-was-never-filed.md -->
