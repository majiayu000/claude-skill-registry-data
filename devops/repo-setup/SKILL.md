---
name: repo-setup
description: First-time setup for an existing repo, single or --batch.
version: 2.0.0
allowed-tools: ["Read","Write","Edit","Bash","Grep","Glob","Agent","Skill","AskUserQuestion","TaskCreate","TaskUpdate","TaskGet","TaskList"]
---

# Repo Setup

## When to Use

- Starting work in a new project repository for the first time
- `/update-docs` reports `tracker_missing` — the project lacks coordination infrastructure
- PM asks to set up project tracking in an existing repo
- **Marketplace first-run** — new coordinator plugin user setting up their first project
- **Creating a NEW repo from scratch** (not onboarding an existing folder)? → use `coordinator:new-project`, which creates + scaffolds a stack + delegates the onboarding half back to this skill.

**The engine repo is a hard prerequisite** — resolved via `CLAUDE_KLABAUTER_ROOT` / the machine-local
`repos.claude_klabauter` registry entry (in `<settings-home>/machine-local/registry.local.toml`) — for coordinator-claude itself, so it must already
resolve before this skill's own fences will run (private until its OSS release; the maintainer
grants access on request, as for `project-rag`).

**Setup is sufficient — downstream skills add-to, never create-from-scratch.** This skill produces minimum-viable versions of all coordinator artifacts the operator will rely on (`state/orientation_cache.md`, `docs/README.md`, `CLAUDE.md`) — the **skeleton**. Downstream skills (`/update-docs` for ongoing coordination-artifact maintenance, `/workstream-start`) add to them in the same format as content accumulates, and self-gate against fresh substrate — underlying principle: wiki (`produce-not-prescribe`). (`/workday-start` runs unconditionally as session orientation; the produce-not-prescribe axis doesn't apply to it.)

## Lanes

Every invocation fires exactly one of three lanes — `new-project`, `add-existing-project`,
`add-repo` — each a pre-answered round-trip set: `lanes/CONTRACT.md` for the shape,
`lanes/<lane>.yaml` for the canonical values, `residue/<lane>.md` for the rationale a human
reading the flow wants.

Which lane fires is an input to this skill, not a decision it makes: the op parameter (or, until
the engine op lands, the caller's own answer to `p1.repo-classification-ask`) names the lane.
`--batch` is an entry-point mode, not a fourth lane — it drives the
`add-existing-project` lane's answers per repo; see `residue/batch-mode.md`.

## Flag contract

- **Default (no flag) — single-repo, `new-project` or `add-existing-project` lane.** Runs from inside one repo's cwd.
- **`--root <path>` (alias `--target <path>`) — single-repo only, optional.** Onboards a sibling repo by absolute or relative path without cd-ing the session into it; defaults to `$(pwd)`. Orthogonal to `--batch`, which reads paths from `working-repos.yaml` and loops the fleet — `--root`/`--target` names exactly one repo. Resolution mechanic: § Procedure.
- **`--batch` — fleet non-interactive.** See `residue/batch-mode.md`.
- **`--non-interactive` (single repo, valid without `--batch`).** Asks nothing: every judgment point takes the firing lane's `lanes/<lane>.yaml` value, and the unattended-halt set (§ Procedure step 4) returns unresolved to the caller. The name comes from `coordinator.local.md` or the directory name, the type from detection.
- **`--answers <file.json | inline-json>` (single repo).** A JSON object keyed by lane `step_id` (`p2.ask-project-name`, `p2.ask-project-type`, `p2.ask-workstreams`, ...) overriding that step's lane value; every unlisted step takes its lane value. Implies `--non-interactive`; an unknown key fails loud, naming it.
- **`--check-only` is batch-mode-only.** Passed to the default single-repo mode (without `--batch`), the skill exits with the one-line remediation: `"--check-only is only valid with --batch; for a single repo use --non-interactive or --answers."`

## Optional `coordinator.local.md` key: `ceremony_day_anchor`

`ceremony_day_anchor: local|utc` is a flat frontmatter key in `coordinator.local.md`. Absent or `local` anchors the ceremony day on the machine's local date; `utc` anchors it on the UTC date, so collaborators in different timezones share one day label. Repo-setup does not seed it: add the line by hand (or via the flat-key write) only for a repo that wants `utc`.

## Prerequisites

- You are in the project's working directory (not `~/.claude`), or pass `--root`/`--target` (§ Flag contract).
- The firing lane's pre-answered values (`lanes/<lane>.yaml`) or, for `add-repo`, an already-decided classification.

## Procedure

**1. Resolve `$_TARGET_ROOT`** (run before everything else). (shape per `${CLAUDE_PLUGIN_ROOT}/snippets/resolve-coordinator-bin.md`; PowerShell shown) `& "$env:COORDINATOR_SETTINGS_HOME\bin\repo-setup-args-and-register.exe" resolve-target-root`. It validates the resolved path is an existing directory inside a git repo, printing the absolute path to stdout on success or a fail-loud `ERROR: ...` line on stderr with exit 1 on failure — mirror that idiom, never silently fall back to cwd. When an explicit `--root`/`--target` was passed, change the shell's working directory to `$_TARGET_ROOT` as the first action, so every downstream cwd-relative step targets the sibling repo. Absent, `$_TARGET_ROOT` resolves to `$(pwd)`.

**2. Load the firing lane's directives.** Read `lanes/<lane>.yaml` in full: `round_trip_directives[]` supplies every value the procedure below would otherwise prompt for, `terminal_offer_defaults[]` the policy default for every terminal offer, `second_phase_deferred[]` the agent-work steps left unresolved for a later phase. Load once, apply throughout — this skill takes every one of these values as given.

**3. Run the lane-independent mechanical procedure.** Read `residue/mechanics.md` and execute it in full — detection, rendering/scaffolding, substrate seeds, optional tripwire installs, and the Phase 4 report shape run the same way whichever lane fired. Substitute the loaded lane's directive/default values wherever the mechanical procedure names a judgment point; take no value from a prompt.

**4. UNATTENDED-HALT SET.** `p3j.1-test-cmd-detect`, `p3m.verify-reachability`, `tw.windows-console-verify-run`, `batch.hook-respect` are never pre-answered by any lane (`lanes/CONTRACT.md`) — return them unresolved to the calling agent/PM exactly as mechanics.md's own procedure surfaces them.

**5. Roster.** Report the firing lane's `roster_slots[]` verbatim in the Phase 4 output. Materializing the roster into batons is a later skill/ceremony's job.

**5a. Posture overlay.** Read `engagement_posture` from `${CLAUDE_HOME:-$HOME}/.claude/coordinator-identity.yaml`; when set, run `render-posture-overlay <posture> "$_TARGET_ROOT/.claude/em-context.md"` (the same call as `commands/install.md`'s engagement-posture step, including its `.gitignore` check). Absent, skip silently. The op swaps in place, so re-running on a repo that already carries an overlay is safe.

**6. Sentinel — signal that setup just ran.** As the final action, write a session-scoped sentinel so `/workstream-start` (if invoked in this same session) prints its one-line setup notice and then runs orientation once: create the `state/` directory if absent, then touch `state/.repo-setup-just-ran`. The sentinel is single-shot: `/workstream-start`'s Preflight consumes it on first read (`rm -f`). It MUST be gitignored, never committed — see `residue/mechanics.md` for the `.gitignore` line.

## Optional Tripwire Installs

Install steps are mechanical and lane-independent — see `residue/mechanics.md` § Optional tripwire
installs — mechanical half. Whether an offer fires is a value the firing lane's
`terminal_offer_defaults[]` already carries (`tw.windows-console-offer`); this skill
does not decide it inline. A Perforce workspace registers per `contract/p4-provider-fragment.md` § Registration.

## Notes

- **Embedding-class check.** Where this skill's flow touches project-rag indexing setup for a
  repo, ask: "does this corpus need `text`-class embedding?" — project-rag silently defaults prose
  corpora to a code-embedding model otherwise. One question, not a policy section; project-rag
  owns the mechanism, this skill states the question only.
- Any onboarding bug fix needs all three layers to not recur: prevention (fix the install script), reactive repair (`doctor`-style recovery for users who already hit it), searchable docs (a troubleshooting row keyed on the literal error text). Rationale: wiki.
- Extended-substrate seeds and the CLAUDE.md template architecture: wiki.
- Peer-repo citations belong to the workstream record: a peer-repo `file:line` citation lands in
  the relevant `state/workstreams/<id>.yaml` entry's `specs[]` or `deliverables[].text` (free-text
  fields per `coordinator/schemas/workstream.schema.json`) — never in
  `state/orientation_cache.md`, whose `## Active workstreams` heading is name-only, capped at 10
  entries, and schema-forbidden from carrying free-form prose or citations
  (`coordinator/pipelines/workday-start-internals.md:265`, `coordinator/docs/wiki/skills-corpus/tiered-context-loading.md:57`).
