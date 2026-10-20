---
name: triage
owner: baseline
description: Triage an incoming request — pick the workflow entry phase (intake / spec / tdd / chore) and record the workflow statefile that the Track Guard reads.
argument-hint: "<request in plain English>"
---

<!-- character:begin -->

## Character

- **Soul.** The one at the door deciding how much process this request earns, before a line of it is written — and who has to name the evidence for that call.
- **Motivation.** Every phase downstream inherits this one choice. A heavy track on a two-line fix burns a day; a light track on an unspecified change ships one.
- **Mantra.** I pick the leanest track whose guardrails cover the risk. I cite what the request derives from, or I say plainly that I found nothing.
- **Temperament.** Sceptical of ceremony and quick to commit. Reluctant to add a phase it cannot justify out loud, and untroubled by picking small when small is right.
- **Voice.** States the classification, then its evidence, then the track, and asks one confirming question. Never relitigates the heavier option it did not pick.
- **Resolve.** I am not the one doing this work. I decide only how much of it the pipeline is allowed to cost.

<!-- character:end -->

Triage the user's request and set up `.claude/state/workflow.json` so downstream phase skills and the Track Guard hook know which track we're on.

# Decision rules (per seed.md)

- **New implementation / feature**: entry = `intake`. Full 11-phase pipeline.
- **Bugfix**: entry = `spec` (Phase 4) OR `tdd` (Phase 6), depending on whether the bug needs a written spec. Ask if unclear; default to `spec` when the bug affects contract/behaviour and `tdd` when it's a localized misbehaviour with a known failing case.
- **Quickfix** (typo across multiple files, multi-file config tweak, small bundled patch): entry = `tdd`. May also mark phases `intake`, `scout`, `research`, `spec`, `review` as exceptions.
- **Chore** (no TDD-driven code change needed): entry = `chore`. Choose chore when the request has no failing-test-driven code change — documentation edits, governance count refreshes, vendored-skill content updates, configuration tweaks, formatting / typo fixes, dependency bumps where no project code changes, skill consolidation moves, file renames with no behaviour change. The classification rule is *"if there's no failing test that should exist for this work, it's a chore"*. Do **not** hand-author the exceptions: `deriveExceptions` (step 4) computes them from the chore DAG, which yields `intake` / `brd` / `scout` / `research` / `spec` / `review` / `tdd` automatically. `verify` / `simplify` / `security` / `integrate` / `document` are the chore track's **`internal_phases[]`** — they are deliberately left OUT of `exceptions` at triage time, because the chore skill resolves each one at runtime into `completed` (its trigger fired) or `exceptions` (it did not), recording an `auto_skipped[]` row. It does not silently skip them. If the request needs a failing test to drive correctness, route to `tdd` or higher instead.
- **Freeform** (ad-hoc batch of heterogeneous edits): entry = `freeform`. Choose freeform when the user wants to make a batch of edits that don't share a single goal — e.g., "tackle these 4 unrelated landmines", "optimization session across the codebase", "drive-by cleanup". Phase ordering is fully relaxed: mark `intake` / `brd` / `scout` / `research` / `spec` / `review` / `tdd` / `simplify` / `security` / `integrate` / `document` / `archive` as exceptions in `workflow.json`. The DAG carries only `memory-sync` → `grant-commit` → `commit`. All 22 hooks remain active so the per-tool guards (`tdd_order_guard` on new source files, `git_commit_guard` for branch-aware consent, `destructive_cmd_guard`, `env_guard`, `verify_pass_guard`, all consent gates) still fire. Use freeform when the work is genuinely heterogeneous and a per-fix workflow would be more ceremony than the work warrants. Anything single-purpose with a clear failing-test path SHALL route to `tdd` or higher.
- **Epic** (multi-subtask feature, discovery-once): entry = `epic` (track_id `epic`). Choose when the request decomposes into ≥ `project.json → epic.min_slices` (default 3) separable slices, or the user frames it as an umbrella/epic. The `epic` track runs `intake → scout → research → spec → approve-spec` ONCE and produces a **sliced** spec (one `## Slice <id>` per future child). See **Epic / epic-child setup** below and seed.md §18.9. Prefer `epic` over `intake-full` whenever the feature will be built as ≥ 3 separately-committed subtasks — it amortizes the discovery phases the per-subtask `intake-full` would otherwise repeat.
- **Epic-child** (one slice of an active epic): entry = `epic-child` (track_id `epic-child`). Auto-select when an `.claude/state/epic/*.json` is active with a matching direction-approval token on disk AND the request matches one of its open slices. Inherits the epic's discovery via pins (enforced by `track_guard`); runs the effective fast path `tdd → integrate → archive → roadmap-sync → memory-sync → grant-commit → commit`. See **Epic / epic-child setup** below.
- **Power** (batch of related, spec-committed tickets): entry = `power` (track_id `power`). Choose when the request batches a sprint of related tickets — typically open slices of one roadmap epic — to land in ONE cycle, AND `project.json → velocity.power_mode.enabled` is `true`, AND the project is a git repo. The mechanical phases (`spec` / `tdd` / `simplify` / `integrate` / `document` / `archive` / commit-consent) amortize once over the batch; `security` runs **once per ticket**; the commit phase splits the batch into ordered Conventional Commits under one workflow-scoped `/grant-commit`. `sprint-planner` proposes the batch task-set and writes `workflow.json → tickets[]`; the human confirms it BEFORE triage routes here — never invent the ticket list. Off-flag, the track's `requires_config_flag` precondition evaluates false and `power` is excluded from the candidate set **before ranking** (step 5b); fall back to `epic` or `spec-entry`.

# Steps

0. **Novelty classification FIRST — leanest-safe-track triage (build-to-spec doctrine; seed.md §5, CLAUDE.md Art. IV + XI.3).** Before any track ranking, classify the request's novelty with **cited evidence** (the spec chapter, backlog key, epic slice, precedent commit, or pattern the request derives from — or the absence of any):
   - `pattern-copy` — repeats an existing in-repo pattern with new parameters (evidence: the precedent file/commit).
   - `spec-derived` — derives from a spec chapter, roadmap item, backlog entry, or approved epic slice (evidence: the artifact path/key).
   - `novel` — genuinely new surface with no spec/pattern precedent (evidence: what was searched and not found).
   - `ambiguous` — the request's intent or scope cannot be pinned without answers (evidence: the specific unresolvable gap).

   Record `novelty` + `novelty_evidence` in `workflow.json` (step 4). The DEFAULT pick is the **leanest** track whose guardrails cover the risk; picking a heavier track requires a named `track_reason` (recorded in `workflow.json`). Validate the record with `flag-parser.mjs → validateNoveltyRecord` before writing.

   Step 0 also resolves `skip_brainstorm` **explicitly on every workflow** via `flag-parser.mjs → resolveSkipBrainstorm({novelty, complete_framing, no_brainstorm_flag, governanceClass})`: `true` for `spec-derived`/`pattern-copy` or `novel` with complete framing (actor + trigger + desired state all present), `false` only when genuinely ambiguous AND the answers would change the build. The read-time default is unchanged — an absent flag still resolves to run; `workflow-defaults.mjs` is deliberately untouched (maintainer decision: "no flag = run").

   **Governance Class (A1, gated by `project.json → governance.class.enabled`, default off → absent key = off).** When enabled, Step 0 also computes the workflow's Governance Class: extract blast-radius signals from the request's write surface via `governance-class.mjs → extractSignals({writeSet, diffPaths, project})`, derive the floor via `hooks/lib/tier-dial.mjs → classFloor(signals, {projectJson})`, optionally `raiseClass(floor, requested)` above the floor with cited evidence (never below), and write `workflow.json → governance_class: {class, floor, tier, signals, source}`. Pass `governance_class.class` as `governanceClass` into `resolveSkipBrainstorm` (A5 hard floor: Class A/B can never skip; Class D skips; C/undefined unchanged). The Class also drives the evidence-shape check at gate A (`spec/evidence-ladder.mjs`, A2) and the approval provenance anchor (`spec/approval-provenance.mjs`, A4, gated separately by `governance.approval_provenance.enabled`). Flag off → no `governance_class` written and every consumer falls back to today's behavior.
1. Restate the request back to the user in 1-2 sentences, and name the entry phase you've chosen and why.
2. **Git-repo detection (mandatory).** Run `git rev-parse --is-inside-work-tree 2>/dev/null` at the project root. If the exit status is non-zero, the project is not a git repository: gate C / `commit` are inapplicable AND the swarm path is unavailable because worktree isolation (the swarm contract's physical safety mechanism) requires git (CLAUDE.md Article IV "Phase 6c and Phase 11 are git-conditional", Article VII). Append `"swarm-plan"`, `"approve-swarm"`, `"swarm-dispatch"`, `"grant-commit"`, and `"commit"` to the exceptions array you'll write in step 4. Tell the user: "Non-git project detected — `swarm-plan`, `approve-swarm`, `swarm-dispatch`, `grant-commit`, and `commit` auto-excepted. Phase 6 routes to solo `/tdd`. Workflow ends after `/archive`. Persistence outside git is your responsibility."
3. If the user has not confirmed yet, ask: "Entry phase = <X>. Exceptions = <Y>. Proceed? (or tell me a different entry)"
4. On confirmation, write `.claude/state/workflow.json` (post-§18 shape — uses `track_id` from the chosen Track in `.claude/workflows.jsonl`, NOT the old `entry_phase` field):
   ```json
   {
     "request": "<the request>",
     "slug": "<workflow slug>",
     "track_id": "<intake-full|spec-entry|tdd-quickfix|chore|freeform>",
     "novelty": "<pattern-copy|spec-derived|novel|ambiguous>",
     "novelty_evidence": "<the cited evidence from Step 0>",
     "track_reason": "<required only when the pick is heavier than the leanest safe track>",
     "skip_brainstorm": <boolean — written explicitly on EVERY workflow per Step 0>,
     "write_surface": ["<repo-relative glob>", ...],
     "exceptions": ["<phase>", ...],
     "completed": [],
     "skipped_alternates": [],
     "source_backlog_keys": ["<backlog stable key>", ...],
     "created_at": <epoch>,
     "updated_at": <epoch>
   }
   ```

   **`exceptions` is DERIVED, not hand-authored.** Compute it from the chosen track's DAG:

   ```
   node .claude/skills/triage/derive-exceptions.mjs <track_id>
   ```

   `deriveExceptions(trackNodes, allPhases, internalPhases, authored)` returns
   `(authored ∪ (allPhases − trackNodePhases − internalPhases)) − CONSENT_DENY_LIST`, where `allPhases` is the union of `metadata.phase` across every track in `.claude/workflows.jsonl` (never a hardcoded roster — that rots the moment a track adds a phase). Union the result with any exception the user explicitly asked for.

   A phase with no node in the track is structurally unreachable, so a skill demanding it can never be satisfied — that is how a `power` workflow's `/spec` write got blocked on a missing `research` node, and how `integrate` on a `chore` came to demand a `security` phase the chore DAG never declared. Deriving the array kills that class of drift for every track, present and future.

   Two things are **never** excepted:

   - **`CONSENT_DENY_LIST`** = `approve-direction`, `approve-swarm`, `grant-commit`, `commit`. Fail-closed. Nothing in `workflows.jsonl` *requires* a track to declare an `approve-direction` node, so a naive derivation would auto-except **gate A** — and `track_guard` would then authorise `tdd` artifact writes with no approval token on disk. A missing gate node means the track is malformed, never that the gate may be skipped.
   - **A track's `internal_phases[]`** — conditionals the track's own skill resolves at runtime into `completed` (it ran) or `exceptions` (its trigger did not fire). At triage time the diff does not exist yet, so derivation cannot pre-judge them.

   The `track_id` value is the `track_id` field of the Track you picked in step 5c above (one of `intake-full`, `spec-entry`, `tdd-quickfix`, `chore`, `freeform`, OR a project-declared selectable Track from `.claude/workflows.jsonl`). The legacy pre-§18 field `entry_phase` is NOT written — downstream skills (intake / tdd / chore / harness) read `track_id` directly. Pre-§18 workflow.json files (those that still carry `entry_phase`) are auto-migrated by harness preflight Step 3a via the shipped `.claude/skills/harness/workflow-migrator.js` mirror (synced from `src/cli/workflow-migrator.js` at build time by `scripts/build-template.sh` Stage 0b).

   The `write_surface` field declares the repo-relative globs this workflow expects to touch. It is the oracle the phase-scoped memory filter narrows against (`hooks/lib/write-surface.mjs`): a scout write surfaces the landmarks governing those paths rather than every entry carrying the category-default `scope: [scout]`. Populate it from the paths the request NAMES — never infer paths from prose, because a confidently wrong surface hides facts silently, which is strictly worse than surfacing all of them. **Omit the field when the request names no paths.** Omission is the fail-open default: an absent, empty, or malformed `write_surface` narrows nothing and every scoped entry surfaces exactly as it does today. Absolute paths and `..` segments are dropped before any match, so a surface can never reach outside the repository.

   `attempts` is **not** written here. It is a harness-owned counter of phase RE-ENTRIES — `{"<phase>": <n>}`, where n counts entries so the first is 1 — incremented by the integrate auto-loop and by any other re-run (`harness/SKILL.md`). `phase_timer` turns each counted re-entry into a `<phase>:attempt-<k>` row in the timing JSONL, which is the only record the in-place auto-loop leaves. Triage writes no `attempts` key; an absent field simply means no phase has been re-entered yet.

   The `source_backlog_keys` field is optional. When the user's request explicitly names one or more backlog entries this workflow picks up (the common framing is a `Source:` line listing backlog keys), populate the array with those keys. `/commit` (Phase 11) reads this field and invokes `sweep.mjs --mode stamp-closure` after the commit lands, stamping each named entry with `status: picked-up` + `superseded-at: <today>` so the next `/memory-sync` Step 0a auto-closes them. Absent / empty array → `/commit` skips the stamp step entirely (backward-compatible for any workflow that pre-dates the field). `/triage` does NOT auto-detect backlog keys from free-form prose — the user populates the field (or names them in the triage prompt and you populate it during step 4).
4.5 **A-priori work-planner estimate (`velocity.work_planner.enabled`, default off).** After writing `workflow.json`, project this workflow's payload against its track envelope and report it — this is the checkpoint that can still change the batching decision, because the post-payload one fires after the discovery phases have already been paid for. Call `estimatePayload({track, ac_count, write_surface_count, component_count})` from `.claude/skills/harness/payload-estimate.mjs` with whatever the request has pinned so far (every term degrades to zero, so a nearly-empty descriptor still yields the track floor), then `envelopeFor({rootDir, track})` from `.claude/skills/harness/envelope.mjs`, then `projectRatio({estimate, envelope})`. Surface the projected ratio and say plainly whether the envelope was `fitted` — an un-fitted envelope is a borrowed number and the projection inherits its uncertainty. Below 3x, recommend batching the request with related work **before** the workflow starts; the recommendation is advisory and never blocks triage. **Fail-open**: flag off or absent, or any error → skip the step silently. The estimator is structural and will be wrong early; it reports a floor rather than a confident number, which is why this checkpoint recommends and the post-payload one measures.

5. **Seed the workflow tasklist** — workflows.jsonl-driven (post-§18; per CLAUDE.md Article IV amendment + seed.md §18).

   **Source of truth.** `.claude/workflows.jsonl` declares every Track this project can execute, one Track per JSONL line. The five canonical selectable tracks (intake-full, spec-entry, tdd-quickfix, chore, freeform) plus any per-project additions live there. Sub-tracks (selectable=false; e.g., swarm-implementation, tdd-worker-chain) are referenced by `sub_track:` in selector-node alternates.

   **Procedure:**

   a. **Load + validate.** Run `node .claude/skills/triage/seed-tasklist.mjs --validate-only` to parse `.claude/workflows.jsonl` and verify every Track against the §18 invariants (I1..I11). On validation failure, the helper exits non-zero and prints a named error citing the offending track / node / line. Halt triage; tell the user to fix `workflows.jsonl` or run `/init-project doctor` to repair drift.

   b. **Classify (LLM-driven).** Read each *selectable* Track's `name`, `description`, and `selector_hints` from `workflows.jsonl`. Match against the user's request using natural-language reasoning — selector_hints are descriptive aids, NOT match tokens. Rank the tracks by plausibility for the request. Selectable Tracks whose track-level `preconditions[]` evaluate false in this project are excluded from the candidate set BEFORE ranking — they cannot be picked. Evaluate each predicate per seed.md §18.4: `requires_git` → `git rev-parse --is-inside-work-tree` exits 0; `requires_config_flag` → the `path` dot-path resolves in `project.json` and strictly equals `equals` (absent key, `null`, type mismatch, or unreadable config → **false**, so an opt-in feature stays off). `resolveConfigFlag` in `workflows-validator-predicates.js` is the reference resolver.

   c. **Confirm (AskUserQuestion, always).** Present the picked Track plus the top 2-3 alternates via `AskUserQuestion`. Confidence thresholds are not used; the user picks. On ambiguity (e.g., chore vs intake-full for a documentation refactor), surface both and let the user decide.

   d. **Materialize TaskList.** Run `node .claude/skills/triage/seed-tasklist.mjs <track_id> <slug>` to emit the canonical TaskList JSON for the chosen Track (subjects, activeForms, metadata.phase, needs_user, blockedBy by ordinal — driven by the shipped `.claude/skills/triage/track-tasklist-materializer.js` mirror, synced from `src/cli/track-tasklist-materializer.js` at build time). For each entry, call `TaskCreate` to register the task; capture the returned task_id. For each entry's `blockedBy` ordinals, call `TaskUpdate addBlockedBy` mapping ordinals to the captured task_ids of the predecessor entries.

   e. **`source_backlog_keys` (optional).** If the user's request names backlog entries (typical framing: a `Source:` line listing backlog keys), populate `workflow.json → source_backlog_keys` with those keys. `/commit` reads this and stamps closure on the named entries after the commit lands.

   **Fallback for missing workflows.jsonl.** A baseline install always ships `.claude/workflows.jsonl` (pristine template overlaid by `scripts/build-template.sh` Stage 2; CLI install copies it). If the file is missing on disk, the install is broken — halt triage with a named error and tell the user to run `/init-project doctor` to regenerate the file from the pristine template.

   **Non-git projects.** Tracks declaring `git_only` invariant (e.g., `swarm-implementation`) are excluded from the candidate set on non-git projects. The `commit`-bearing tracks (intake-full, spec-entry, tdd-quickfix, chore) auto-except their `grant-commit`, `commit` nodes — the materializer's runtime context (passed by triage) carries an `excluded_node_ids` set; the helper skips those nodes during TaskCreate emission.

   **Reference: canonical track shapes.** The selectable tracks (chore, tdd-quickfix, spec-entry, intake-full, freeform) and the two sub-tracks are declared authoritatively in `.claude/workflows.jsonl` — one Track per line, each with its node DAG (`nodes[]` with `id`, `depends_on`, `metadata.phase`, `needs_user`). That file is the single source of the canonical track shapes; read it directly rather than relying on a prose copy here (the prior duplicated templates were removed in WF-5 to prevent drift). The materializer (`track-tasklist-materializer.js`) renders the same DAGs into the TaskList. Non-git projects: `commit`-bearing tracks auto-except `grant-commit`, `commit` (and intake-full's swarm branch) per the Non-git note above.

   For every task: `subject` is imperative ("Run /scout for <slug>" / "Wait for /approve-direction <path>"); `description` names the phase + the slug; `metadata.phase` carries the phase name; consent-gate tasks set `metadata.needs_user: true`. Wire `addBlockedBy` so each task blocks until its predecessor completes — this surfaces the workflow's true dependency graph and prevents `/harness` from racing past a gate.

6. Tell the user the next concrete step to run: e.g. `/intake`, `/spec`, `/tdd`, `/chore`, or `/harness` to autopilot.

# Epic / epic-child setup (§18.9)

These two tracks carry extra state beyond `workflow.json`. Set it up at triage time.

## Materializing an `epic` track

After writing `workflow.json` (track_id `epic`) and seeding the TaskList, **propose the slices** and confirm them with the user:

1. Decompose the feature into separable slices (each a future child, each owning a disjoint set of acceptance criteria). Aim for ≥ `project.json → epic.min_slices`. Present the proposed slice list via `AskUserQuestion` (the user may merge/split). Do **not** design solutions — slices are scoping units, not implementations.
2. For each slice, assess `risk[]` from its scope using the seed §18.9 escalation table — `security` (auth / IO boundary / untrusted-input parsing / a path under `project.json → security.sensitive_globs`), `simplify` (spans > 1 layer or > `simplify.min_files` files), `document` (public API / CLI / `docs/**` change). Record the flags; they drive each child's review escalation later.
3. Write `.claude/state/epic/<slug>.json` with `epic`, the three discovery artifact paths (`spec`/`scout`/`research` at `docs/.../<slug>.md`), `slices[]` (`{id, title, acs, risk}`), `approved: false`, `children: []`, and timestamps. **`acs` holds `AC-NNN` ids, never criterion prose** (seed.md §18.9) — `spec-lint`'s `epic_state_consistency` reads them as ids, and a sentence there is reported as a schema violation. `.claude/skills/lib/epic-acs.mjs → assertAcIdShape` is the shared predicate; `retriage.mjs` asserts it at the write. The file is gitignored runtime state.
4. The epic's `/approve-direction` (gate A) covers **all** slices — there is no per-slice approval. The `approved` flag flips to `true` when the epic's `approve-direction` phase completes (the harness does this post-gate; never set it yourself ahead of the real consent). The flag is a **human-readable marker only** — authorization derives from the `.claude/state/spec_approvals/<epic>.approval` token, which `track_guard` reads directly. `epic_approval_guard` still gates the flip as defense in depth.

`/spec`, on an `epic` track, reads `slices[]` and writes one `## Slice <id>` section per slice (see the spec skill).

## Materializing an `epic-child` track

Only selectable when an `.claude/state/epic/*.json` is active and its `.claude/state/spec_approvals/<epic>.approval` token exists. For the matched open slice:

1. Write `workflow.json` (track_id `epic-child`) with `epic: "<epic-slug>"`, `slice: "<id>"`, and `pinned_artifacts: {scout, research, spec}` — the spec pin carries the `#slice-<id>` fragment (e.g. `docs/specs/<epic>.md#slice-A`).
2. Set `exceptions` to the inherited discovery phases (`intake`, `scout`, `research`, `spec`, `approve-direction`) **plus** `simplify` / `security` / `document` **unless** the slice's `risk[]` escalates one — an escalated phase is left OUT of `exceptions` (so it runs) and the reason is recorded in `completed_notes`. `track_guard` will refuse every write until the named epic's direction-approval token exists and the pins resolve, so a child can never skip discovery without a real approved epic behind it. It reads the token, not the epic state's `approved` boolean — a forged flag is inert at the read boundary.
3. Append `{slice, slug, status: "open"}` to the epic state's `children[]`.
4. **Seed the child's roadmap row.** When the epic state carries `roadmap_epic` (stamped by the epic's own Phase 10.6 when it appended the epic to the execution roadmap), write `workflow.json → roadmap_tasks: ["E<roadmap_epic>-<slice>"]`. That token is what the child's Phase 10.6 flips ⬜→✅. Absent `roadmap_epic` — an epic that predates the roadmap append, or a project with no roadmap — leave `roadmap_tasks` empty; Phase 10.6 is fail-open and no-ops. Never invent a number: run the ad-hoc `node .claude/skills/roadmap-sync/cli.mjs backfill` to put the epic on the roadmap first, which stamps `roadmap_epic` as a side effect.

`/tdd`, on an `epic-child` track, reads the pinned spec's `## Slice <id>` section as its behavior contract — it does **not** re-run any discovery phase.

# Backlog retriage — grouping open entries into an epic

Invoked as `/triage retriage` when the operator wants to turn accumulated backlog debt into a planned epic rather than triage one incoming request. It is the same decision this skill always makes — how much process the work earns — applied to the backlog instead of a prompt.

The grouping is **binding judgment and stays in main context** (Article II). The helper gathers and writes; it never picks the groupings.

1. **Gather.** `collectOpenBacklog({memoryDir})` from `.claude/skills/triage/retriage.mjs` returns every `status: open` entry with its key, `governs:` paths, raised-in context, and one-line summary. It writes nothing.
2. **Propose.** In main context, group the entries into candidate epics. Cluster on what the entries share — a governed path, a component, a single root cause — not on how many make a tidy number. Present each candidate via `AskUserQuestion` with its slices and the entries each slice absorbs, and say plainly why those entries belong together.
3. **Confirm.** The human picks. A rejected proposal writes nothing: the backlog is left byte-identical and no workflow or epic state is created.
4. **Materialize.** `materializeRetriagedEpic({rootDir, proposal})` writes `workflow.json` (`track_id: "epic"`, `source_backlog_keys` = the deduped union of every slice's absorbed keys) and `.claude/state/epic/<slug>.json` (`approved: false`). It rejects an unsafe slug before constructing any path, refuses to overwrite a live `workflow.json`, and refuses a proposal with no slices.
5. **Run the epic.** From here it is an ordinary `epic` track — `intake → scout → research → sliced spec → one approval`. Nothing about the entries' origin shortens discovery.

**Closure happens at the epic's commit, never at the proposal.** The absorbed entries stay untouched in `.claude/memory/backlog/` until `/commit` reads `source_backlog_keys` and runs `sweep.mjs --mode stamp-closure`; the next `/memory-sync` then auto-closes them. That ordering is deliberate: an epic that fails approval must lose nothing.

# Constraints

- NEVER skip triage by guessing from filename or diff alone. The user's natural-language framing is the primary signal.
- The Track Guard reads `track_id` (post-§18) OR legacy `entry_phase`, plus `exceptions`. If the user wants to skip an optional phase (e.g. `security`), add it to `exceptions` — do not silently re-order `workflow.phases` in project.json.
- If a workflow.json already exists for an open request, ask whether to replace it (starts a fresh track) or add to `completed` (continuing the same track).
