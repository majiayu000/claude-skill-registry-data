---
name: feature
description: Use when driving a feature prompt to a production-ready PR through discovery, definition, design, spec, issues, and dev phases, or when the user runs /feature or /feature resume — orchestrates the A-Team agentic pipeline over a target repo.
---

# feature — A-Team orchestrator

Drives the authorized outcome: discovery, a prototype, an implementation PR,
or a bounded refinement of an existing product. The manifest selects one A/B
arm for the whole run: `harness` runs phase skills on the interactive main
thread; `agent` dispatches role agents across the workflow. Both use
the same deterministic transition CLI, artifacts, gates, and acceptance checks.
The opt-in agent procedure is `agents/TRIAL.md`; read it before any agent-mode
dispatch. The existing instructions below remain the harness-mode procedure.

`PLAN.md` and `CONTRACT.md` in the **harness repo** root hold the full design
rationale. This skill is the executable procedure.

## Preconditions

- You run as the **interactive main thread**. Gates require a human to answer in
  the conversation, and the `discovery` phase is a grill that cannot complete
  without one. If there is no human to prompt (e.g. you are a subagent), do not
  fabricate approval — halt and report.
- You have the `ateam-discovery`, `ateam-definition`, `ateam-design`,
  `ateam-spec`, and `ticket-writer` skills available, and the **runner** — the
  `ateam-runner` CLI, either on `PATH` or as
  `node <harness>/runner/bin/ateam-runner.mjs` (Node 20+, `gh`). If a required
  phase skill is not available, halt and tell the user to install it — do not
  hand-simulate it. If the runner is missing, halt and say where it lives
  (`runner/` in the harness repo) rather than falling back to implementing
  issues yourself: the dev phase's whole value is that an independent session
  judges the diff.

## Invocation

```
/feature "<prompt>" --repo <target>     # start a new feature
/feature "<prompt>" --repo <target> --orchestration-mode agent
/feature resume <slug> --repo <target>  # resume an in-flight feature
```

`--repo` defaults to the current directory if omitted. `<target>` is the git root
you operate on. `--orchestration-mode` accepts `harness` (default) or `agent`.
Record it as `orchestration_mode` in the `init` input. It is immutable for that
feature so an evaluation arm cannot change mid-run.

`ateam-discovery` is also **usable standalone**, without you — a human can invoke
it directly to seed `docs/product/` before any feature exists. When you later run
`/feature`, it reviews and extends those jobs rather than re-deriving them.

## The one rule

**The manifest is the source of truth.** Read it with `feature-cli.mjs show`;
all writes use the validated CLI below. Never assign state, status, approvals,
retry counters, run limits or milestones in JSON by hand. Atomic compare-and-swap
writes and durable event IDs make interrupted operations replayable. `show`
checks actual artifact hashes and conservatively migrates legacy manifests;
legacy `done`, `approved`, or provisional flags do not supply missing evidence.

```sh
node <harness>/runner/src/feature-cli.mjs show --feature <feature-dir>
node <harness>/runner/src/feature-cli.mjs status --feature <feature-dir> --format json
node <harness>/runner/src/feature-cli.mjs <operation> --feature <feature-dir> --expected-revision <revision> --event-id <stable-operation-id> --input '<JSON>'
```

Use `status` for the compact operator view; `--format text` is the default and
`--format html` emits a local preview snapshot. Save HTML outside bound artifact
trees and open it directly in a browser. Both status and `show` revalidate actual
files without writing the manifest. Status distinguishes current phase decisions
from provisional choices and the six independent milestones, and shows the
reason, next action, gate consequence, changed review inputs, assumptions,
outstanding obligations, documents/boards and recorded runtime links. See
`runner/FEATURE-STATUS.md` for the full control and snapshot contract.

Read the entire JSON result. `status: success` and exit 0 permit continuing;
`blocked` includes a persisted concrete reason; `error` includes invalid input or
a revision conflict. Reload on a conflict. Retrying an interrupted identical
command uses its original ID and revision; changed inputs use a new ID. Never
retry a recorded blocked event hoping for a different result. Resolve its cause,
reload, and submit a new event. No CLI operation executes agents, Git, or releases.

**Every manifest write is immediately committed**, so a hard reset or crash can
never lose committed state. Commit messages: manifest-only changes use
`chore(<slug>): <what>` (e.g. `advance to design`); artifact changes use
`docs(<slug>): <phase>`.

**Manifest-only commits stage only the manifest.** A `chore(...)` commit is
`git -C <target> add docs/features/<slug>/feature.json && git -C <target>
commit -m "<msg>"` — never the whole feature or product tree. Mid-phase those
trees hold in-progress artifacts, and a broad add silently sweeps them into a
bookkeeping commit, breaking the chore-vs-docs breadcrumb split (proven in the
2026-07 dry run: a gate-policy chore commit swallowed the PRD).

**Artifact commits stage both artifact layers.** `discovery` writes only to
`docs/product/`; later phases write mainly to `docs/features/<slug>/` but also
touch the durable layer (definition's epics, the pr phase's plan refresh and
product report). When committing a phase's artifact (`docs(...)`), staging only
the feature dir silently drops the durable artifacts — `git add` both paths there.

## The two artifact layers

```
<target>/docs/product/           # DURABLE — outlives any feature
  context.md  jtbd/NN-*.md  epics/NN-*.md  adr/NN-*.md  ateam-plan.md
  research-plan.md
  project-plan.md  ateam-product-report.md  research/  input/<YYYY-MM-DD-label>/
<target>/docs/features/<slug>/   # PER-FEATURE — everything else
  feature.json  prd.md  briefs/  design.md  spec.md  issues.md  lofi/
```

Durable artifacts are cited by feature artifacts and outlive them. You never edit
them yourself — phase skills own them per `CONTRACT.md` (discovery most of the
layer; definition the epics; the pr phase the plan refresh, the project plan,
and the product report), updating in place per the superseding rules there.
One exception you *do* own: the `milestone:` frontmatter key the issues phase
writes back into `epics/NN-*.md`, and nothing else in those files.

## Git and filesystem mechanics

- All file and git operations target the **target repo**, never the harness repo.
- Use absolute paths and `git -C <target>` for every git command. **Never `cd`**
  (CWD resets between calls and `cd` triggers permission prompts).
- The manifest is always the file `<target>/docs/features/<slug>/feature.json`
  (the `manifest-template.json` in this skill dir is only a template — the on-disk
  name is `feature.json`).

## Slug rules

Derive `<slug>` from the prompt deterministically: lowercase, keep `[a-z0-9]`,
replace runs of other characters with a single `-`, trim leading/trailing `-`,
cap at 50 chars, then trim back to the last `-` so no word is cut mid-way (and
strip the trailing `-` that leaves). Example: `"Add saved searches!"` →
`add-saved-searches`; a 50-char cut ending `…-guardians-of-atla` becomes
`…-guardians-of`.

If `<target>/docs/features/<slug>/` already exists on a **new** run, stop and ask
the user (resume it, or pick a different slug) — never silently overwrite.

## Startup

1. Resolve the **target repo** (`--repo`, else CWD).
2. Read `<target>/CLAUDE.md`. Find the `## A-Team Config` block (test command,
   base branch, design-system path, package manager, `github issues`). If the
   block is missing, run the **bootstrap** (below) first. **Base branch
   precedence:** A-Team Config value wins over any default. **`github issues`
   absent → treat as `off`** — an older config predating the key is not
   consent.
   Resolve canonical target/harness paths and Git identities before creating
   output. Refuse a harness target (including the renamed-fork signature below)
   and escaping destinations. Keep harness root/revision, current/product
   context, existing design binding and verification commands in this same config;
   do not create another authority file. A configured harness revision must match
   the invoked checkout; changing its pin is a deliberate upgrade. Consult
   `runner/EXECUTION.md` for executable policy keys and native prerequisites.
3. **New feature:**
   - Compute `<slug>`. Check that neither the feature dir nor the branch
     `feature/<slug>` already exists (`git -C <target> rev-parse --verify
     feature/<slug>`); if either exists, stop and ask the user (resume, or pick a
     different slug) — never silently overwrite.
   - `git -C <target> checkout -b feature/<slug> <base_branch>` (create the branch
     **before** writing artifacts, so they land on the feature branch).
   - Create `<target>/docs/features/<slug>/` and `<target>/docs/product/`.
     Call `feature-cli.mjs init` at expected revision `0` with a stable init event
     and input containing `slug`, `prompt`, `repo`, `base_branch`, `branch`,
     `orchestration_mode`, and the known `run_brief` fields. The template documents the versioned schema;
     the CLI creates the manifest and refuses to replace an existing feature.
   - `git -C <target> add docs/features/<slug> && git -C <target> commit -m "chore(<slug>): init feature manifest"`.
     (`docs/product/` is empty at this point and git cannot stage an empty
     directory — expected; never add placeholder files to the durable layer to
     force it in.)
   **Resume:**
   - Call `feature-cli.mjs show --feature <feature-dir>`. Review stale/unknown
     evidence and outstanding provisional decisions; retain all historical records.
   - Keep the saved `orchestration_mode`. Reject a conflicting explicit mode
     argument; use a separate feature and target checkout for a different arm.
   - If the feature is paused and the human requested resumption, call `resume`
     with that request's concrete reason and a stable event ID, then reload.
     This only clears the scheduling hold. It executes no phase and does not
     retry an uncertain runner action. Inspect exact retained receipts first.
   - Ensure HEAD is on the feature branch: `git -C <target> checkout feature/<slug>`.
4. Enter the phase loop.

## Phase loop

Read `manifest.state` from `show`. The transition functions derive the next
state atomically with completion/approval; there is no separate state bump.

- `paused` is a cooperative scheduling hold. Inspect `control.reason` and
  `control.next_state`; do not dispatch another phase or pass a gate. Already
  running work may record completion/failure or issue/milestone receipts without
  lifting the hold. Check the hold again before each new runner dispatch.
- `aborted` is terminal. Preserve all artifacts, accounted branches and history.

- `failed` is terminal until the cause is fixed and a deliberate `revise` command
  records the recovery reason. Preserve completed issue receipts.
- `stale` requires rerunning or revalidating that phase before its gate can pass.
  `start` checks predecessor decisions and clears only its live bindings.
- `complete` at definition/design/pr goes to that phase's gate; other completion
  already selected the next state. `approved` retains its decision history.
- `in_progress` resumes the idempotent phase skill. `pending` starts it.
- `stopped` means the requested stopping point was reached. Report each of the
  six milestones separately; it never means accepted, integrated or released.
- `refinement_review` waits for the named reviews in the saved refinement plan.

| state | action | gate (HITL) | on success → |
|-------|--------|------|--------------|
| `discovery` | `ateam-discovery` | — (grill + in-skill read-back) | `definition` |
| `definition` | `ateam-definition` | ✅ | `design` |
| `design` | `ateam-design` | ✅ | `spec` |
| `spec` | `ateam-spec` | — | `issues` |
| `issues` | `ticket-writer` (batch decomposition) | — | `dev` |
| `dev` | `ateam-runner` (`--source local`) | — | `pr` |
| `pr` | assemble feature branch + open PR | ✅ final review | `stopped` |

`discovery` has **no orchestrator gate**. It is a 🔥 grill: the human is present
throughout and the skill ends with its own read-back of the JTBD set. Adding a
gate would cost a manifest state and a second approval ritual to guard a document
the human has just read. Do not add one.

### Running a phase skill (`discovery`, `definition`, `design`, `spec`)

1. (You only reach here for `status` `pending` or `in_progress` — the dispatch
   rules above handle `complete`/`approved`.)
2. Call `feature-cli.mjs start` with `{"phase":"<phase>","task":{...}}`, then
   commit the resulting manifest. The command selects actual current context
   before dispatch; bootstrap/revalidate a missing or stale index through
   project-context first. A start does not increment retries.
3. Dispatch according to `manifest.orchestration_mode`:
   - **`harness`** — invoke the reserved skill via the Skill tool by name
     (`ateam-discovery` / `ateam-definition` / `ateam-design` / `ateam-spec`).
   - **`agent`** — dispatch `ateam-pm` for discovery/definition and
     `ateam-designer` for design/spec using `agents/TRIAL.md`. Use fresh sessions.

   In every path pass **three** absolute paths — the feature directory, the
   product directory, and the harness `intake/` directory. The worker reads prior
   artifacts plus the manifest and writes only its contract scope. In agent mode,
   specialist work is returned as `requestedDispatches`; this supervisor runs at
   most the declared budget and returns the bounded result to a fresh PM dispatch.
4. In agent mode, process the typed handoff through `agents/TRIAL.md` first.
   Escalation or a specialist request stops this completion path; successful
   output is validated and completed by the supervisor. Then call `show`.
   In harness mode the skill should have called its `complete` command
   successfully, recording its artifacts, stage obligations and blocking flags.
   - Artifact missing OR status not `complete` → treat as **failure** (see below).
   - **Exception — escalation (any phase).** If the skill halted for want of a
     human, it leaves `status = "in_progress"` and says what it is waiting on
     (`discovery` writes an `## Awaiting answers` block into
     `docs/product/context.md`; `definition` halts when its North Star is
     missing and reports that discovery must run first). This is a **defined
     output, not a failure**: do not bump `attempts`, do not retry. Commit,
     surface what is needed to the user, and stop. A later `resume` picks up
     from there.
5. Commit the artifact:
   `git -C <target> add docs/features/<slug> docs/product && git -C <target> commit -m "docs(<slug>): <phase>"`.
   For `discovery`, prefer the skill's own commit message naming what changed and
   why (e.g. `docs(jtbd): 03 reshaped — contract recovery is the job, not search`);
   only fall back to `docs(<slug>): discovery` if it left the work uncommitted.

### Gates (`definition`, `design`, `pr`)

At definition/design, agent mode first runs the cold reviewer in `agents/TRIAL.md`.
Surface its findings with the existing gate report; it cannot grant approval.

Gate behavior is governed by `manifest.gate_policy` — chosen by the **human**
during discovery's independence handoff (never by an agent), default `"block"`:

- **`block`** (default) — the safety valve. Present the artifact inline and
  wait for approve / revise / abort (below).
- **`notify-and-continue`** and **`run-to-pr`** — call `approve` with
  `{"phase":"<phase>","provisional":true}` only when `configure` previously
  stored an explicit human authorization naming that gate. The provisional
  record retains its authorization and exact reviewed artifact hashes. Emit
  the checkpoint and carry this decision forward for the returning human.
  The final PR gate always requires an explicit human decision.

**Tripwire — bad signal closes the valve.** A gate may pass provisionally
**only when the phase's report lists no blocking flags** (per CONTRACT.md:
unlisted-job signals, `TBD`s inside Must scope, failed self-checks,
qualitative criteria whose human run is required at this stage). Pass the actual blocking-flags list in the phase's `complete` command
(empty when none). The CLI validates actual `acceptance.json`, its immutable
history and current artifact snapshots at the claimed stage. Unresolved current
obligations block with their IDs/reasons. Future obligations remain pending. A tripped
gate **blocks and waits regardless of policy**, stating exactly what tripped
it. The human's chosen policy governs the happy path; it never overrides bad
signal.

**Assumption relay.** When a phase's report names assumptions it made, verify
they were appended to `research-plan.md` (phase-tagged, with confidence — the
CONTRACT append exception). If the skill failed to append them, append them
yourself from the report before committing the phase. An assumption that lives
only in a report is a broken promise to the absent human.

On `resume`, if any phase carries `"provisional": true`, present those
artifacts for review **before** continuing past the next gate.

At the `definition` gate (blocking or checkpoint), present `prd.md` **together
with the JTBD set it scopes against** — the PRD's claims are only checkable
against the jobs they trace to.

Blocking-gate responses:

- **pause** → call `pause` with the human's reason and stop dispatching new work.
  This is cooperative control, not suspension or process-tree termination. Native
  macOS detached-child containment (#37) remains explicitly unresolved.
- **approve** → call `approve` with `phase` and `decision: {kind:"human",
  actor:"<human>", authorized:true, reference:"<actual decision reference>"}`.
  This approves that artifact/test plan; it does not record product acceptance.
- **revise** → call `revise` with `phase` and the human's concrete `reason`,
  then start and re-invoke the skill with those notes. Matching artifact bindings
  and dependent phases become stale; unrelated milestone receipts stay current.
  Decision/event history is retained, and revision does not count as failure.
- **abort** → call `abort` with the concrete reason, commit and stop. Leave all
  artifacts and branches; no cleanup or branch deletion follows an abort.

Definition approval binds the PRD and complete briefs tree, including page and
wireflow boards and rendered verification artifacts. Design approval binds its
summary, existing lofi tree and configured accepted token source (or durable
design-system fallback); naming only design.md cannot omit these reviewed outputs.
Spec owns and binds spec.md, with its design/definition dependencies retained.

Definition approval authorizes the definition and its test plan. A prototype
may be created while its planned human study remains pending. Design-stage
checks execute only what is available and due at design; later human acceptance
uses its own milestone and evidence. No blanket human-study flag blocks earlier
work whose required stage has not arrived.

Gates block within the session. Because the manifest persists (and status is
checked on resume), a killed session resumes at the same gate.

### `issues` phase

Agent mode delegates step 1 to `ateam-pm` with `phase: issues` under
`agents/TRIAL.md`. The supervisor retains projection, state writes, and commits.

Two steps, one phase:

1. Invoke `ticket-writer` in **batch decomposition mode** against `prd.md` +
   `spec.md`, with `briefs/` as supporting context (the page briefs carry
   per-page ACs), → `issues.md` — tracer-bullet vertical slices in dependency
   order, each with Gherkin acceptance criteria and its `[[NN]]` job stamp.
2. **GitHub projection (conditional)** — mirror the decomposition into the
   target's GitHub repo. Skipped by default; see the subsection below.

Call `start` for issues before decomposition. When both steps are done, call
`complete` with `{"phase":"issues","artifacts":["issues.md"],"blocking_flags":[]}`.
Only its successful actual-file validation permits advancing to dev. Commit.

**Path mapping (step 1):** the input is `docs/features/<slug>/prd.md` (+
`spec.md`) and the output is `docs/features/<slug>/issues.md`. Pass both
explicitly in the invocation args.

**Acceptance criteria are load-bearing here, not decoration.** The dev phase
refuses any issue without a checkable `### Acceptance criteria` section, because
the reviewer that judges the resulting diff has nothing else to judge against.
An issue that reaches `dev` without them is a decomposition gap, and it costs a
round trip — get them right in step 1.

**Files-touched notes (step 1):** each issue's technical notes must name the
files it expects to touch, so the dev phase can sequence file-colliding issues
up front instead of discovering conflicts at integration.

**Requirement trace (step 1):** each issue must also record the **PRD
requirement IDs** it implements. Ask for it explicitly in the invocation args —
decomposition happens *from* the PRD, so the mapping exists at that moment and
is expensive to reconstruct later. It is what step 2 resolves an issue's epic
through (epics bundle requirement IDs), and what lets a reviewer check coverage:
a requirement no issue claims is a hole in the decomposition.

#### Step 2 — the GitHub projection

**`issues.md` remains the source of truth.** The swarm reads it, not GitHub.
This is a projection: everything downstream keeps working when it is skipped,
which is what lets the skip conditions below be safe.

**Fire it only when all three hold:**

- `## A-Team Config` says `github issues: on`. **Absent or `off` → skip.**
  Silence is not consent to write into a shared repo, and skipping costs
  nothing recoverable.
- The target has a GitHub remote and `gh` is authenticated
  (`gh auth status`). Otherwise skip.
- **Hard guard — the target is not the A-Team's own repo.** Skip if either
  holds: the target's `origin` remote resolves to **`subvisual/the-a-team`**
  (host-agnostic, `.git` suffix and protocol ignored), or the target root
  contains **both `CONTRACT.md` and an `intake/` directory** at its top level —
  the harness's own signature, which also catches a fork or a rename. A
  `/feature` run pointed at the A-Team must **never** create issues in it: it
  is a harness that operates on *other* repos, and dry runs would litter it.
  **Not overridable by config** — `github issues: on` does not lift it.
  The second test can false-positive on an unrelated repo that happens to have
  both. It fails **safe** — the projection is skipped and `issues.md` is
  untouched — and the skip is reported with its reason, so a legitimate
  collision is visible rather than silent.

**What it creates**, in this order:

- **Milestones from epics.** One per `active` epic in `docs/product/epics/`,
  titled from the epic. `done` epics keep any `milestone:` they already have —
  reconcile (close it if still open), never create a new one. `parked` epics
  get no milestone until they go active. Write the returned number back as a `milestone:`
  frontmatter key in the epic file — the one cross-owner write CONTRACT.md
  permits, and what makes re-runs reconcile instead of duplicate. A **re-titled**
  epic still matches by number; a **superseded** epic's milestone is **closed**
  with its description pointing at the replacement, never deleted.
- **Labels from job ids**, `jtbd:NN-slug` (e.g. `jtbd:03-recover-a-mis-filed-contract`)
  — id first, since the id is the stable part and the slug can be re-worded.
  Created if missing. A **superseded** job's label **stays**: closed issues
  wear it, and deleting it would strip their history. New issues use the
  replacement's label.
- **Issues from `issues.md`**, each carrying a label per job it traces to and
  its epic's milestone. **Deriving the epic**: an issue's `[[NN]]` job stamps
  and the PRD requirement IDs it implements resolve to an epic via that epic's
  bundled requirement IDs (`Requirements realized`) — requirement match first,
  job match only as a fallback. An issue resolving to **two** epics means the
  decomposition crosses an epic boundary; assign the requirement-matched one
  and surface the overlap. An issue resolving to **none** gets no milestone,
  which is itself a flag worth reporting.
  An issue tracing to **no job** is a decomposition defect — surface it to the
  human at the next gate rather than creating an untraceable issue.

**Write every returned issue number back into `issues.md`.** Without it the
step is not idempotent, and a revise loop or crash resume silently duplicates
the whole set in GitHub. With the numbers on disk it becomes reconcile-not-create:
re-runs update existing issues and create only what is genuinely new.

**Never fatal, never a blocking flag.** A skipped or failed projection does not
make an artifact wrong, and blocking flags halt the run regardless of
`gate_policy` — that power is reserved for correctness defects. State the skip
and its reason in the phase report and in the PR body, then continue.

### `dev` phase

Both arms use the existing isolated Builder/Verifier sessions described below.
Agent mode must also use this runner: invoking a project Builder agent directly
would bypass the runner's evidence and independent approval boundary.

Invoke the **runner** over `issues.md` — one issue at a time, each in its own
worktree, each gated by an *independent* reviewer session before it counts as
done:

```
ateam-runner run --source local \
  --issues docs/features/<slug>/issues.md \
  --path <target> \
  --base feature/<slug> \
  --branch-prefix "feature/<slug>-issue-" \
  --json
```

`--source local` is the point of the flag: the dev phase never touches GitHub.
Issues come from `issues.md`, verdicts come back in the JSON report, and nothing
is pushed — the `pr` phase owns integration and the single PR. `issues.md` and
`prd.md` are contract artifacts; the runner never edits or deletes either.

**Branch naming:** the orchestrator supplies the prefix, so each issue branch is
`feature/<slug>-issue-<key>` (flat, `<key>` being the slugified issue title).
**Never** `feature/<slug>/issue-<key>` — git refuses a nested ref when
`feature/<slug>` already exists as a branch (ref-as-file vs ref-as-dir conflict).

**Dependencies:** the runner is serial and it *chains* — each approved branch
becomes the next issue's base, so an issue that `depends-on` another is built on
top of its dependency's work without a merge, and two issues touching the same
file cannot conflict by construction. Nothing runs in parallel; that is
deliberate, not a limitation to work around.

**Orchestrator ↔ runner contract (avoids double-counting retries):**

- First preview the exact invocation with `--dry-run --json`. Inspect resolved
  target policy, prerequisites and scope conflicts; the preview creates no
  clones, claims, worktrees, records or GitHub writes. Declare protected work
  with `--scope-path`; only explicit human authorization may supply a narrow
  `--authorization-file`. Do not invent exemptions or relax policy to make a run
  green. Execution requires an existing clone and the native backend described
  in `runner/EXECUTION.md`.
- Parse the **entire stdout** as the version 1 envelope in `runner/CLI.md`.
  Check `schemaVersion`, `status`, `error` and the process exit code. Local
  outcomes are `envelope.result.results`, with reports under
  `envelope.result.report`; diagnostics are stderr. Exit 0 means success/skipped,
  2 means blocked/invalid usage, and 1 means failure. A parsed JSON document alone
  is not completion. Streaming watch is unsupported with JSON or dry-run; use
  `--once` for those modes.
- The runner writes no manifest. Call `start` for dev before dispatch. Record
  each returned outcome through `record-issue` with `issueId`, `status`
  (`complete`, `failed`, `needs-detail`), and `evidence` (`reference`, committed
  `revision`, local receipt `artifacts`). Include the resolved `execution_policy`.
  `complete` requires the verified runner approval receipt described below.
- Before dispatch, include exact adapter repository identities and stable issue
  keys in `run_brief.runner_history` through the existing authorized `configure`
  command. This lets status find interrupted work even before `record-issue` has
  an outcome. Use local target paths for local adapters and `owner/repo` for
  GitHub; never infer associations from matching titles. Keep explicit HTTP(S)
  preview links in `run_brief.runtime_links` with `label` and `url`. Status checks
  link safety and labels runtime availability as not checked.
- Record the returned approval/evidence reference with each approved issue and
  the resolved policy digest in `execution_policy`. Approval must bind valid
  process results, independent review and supervisor checks to committed head.
  Dirty corrections, absent/skipped checks without an applicable explicit
  documentation exemption, source mutation, or changed head/base/criteria
  invalidate evidence. Validate it before using an approved branch; an old
  report or label is insufficient. Later combined-revision checks remain the
  integration phase's responsibility.
- One runner invocation of an issue = **one orchestrator attempt**, whatever the
  runner does internally. Its implement↔review cycles (capped at 3, with an
  early stop when the reviewer's objections stop converging) are part of that
  single attempt — do not count them separately.
- On failure, re-invoke scoped to the failed issue with `--issue <key>`, feeding
  the error back. Never re-run an issue the report marks `approved`. Only
  `record-issue` increments that failed issue's attempts.

**A `needs-detail` outcome is not a failure to retry.** It means the issue
carried no checkable acceptance criteria, so no reviewer could verify it and the
runner refused rather than guessing at requirements. Fix the issue text — that
is a decomposition gap to surface at the next gate, not an implementation error.

**Projected GitHub issue completion:** keep projected issues open while work
exists only on an issue/feature branch or an open PR. After observing integration
into the intended target branch, an authorized projection update may close the
exact mapped issue with its merge receipt. Read the number from `issues.md`;
missing mappings mean projection was skipped. Local runner approval and PR
creation cannot justify closing issues or claiming target integration.

Retry a failed issue up to **2×** (per-issue `attempts`); never skip a failed
issue silently. Issue still failing after 2 retries → record its failed issue outcome and call
`fail` for dev with the concrete reason, commit, and halt (see Failure). Completed issues' branches are **preserved** (not
discarded) for the human to integrate after resolving the failure.

After all scoped issues have current runner approval, call dev `complete` with
its actual code/receipt artifact paths, then record `implementation` separately
with its revision-bound evidence. Completion never infers any other milestone.

### `pr` phase — serialized branch assembly

Agent mode delegates the plan refresh and product report craft to
`ateam-delivery` after branch assembly, under `agents/TRIAL.md`. The supervisor
retains Git operations, verification, PR publication, and the final human gate.

Call `start` for pr. This assembles local feature work and does not authorize
merging into the intended target or deploying.

1. Merge completed+reviewed issues into `feature/<slug>` **one at a time, in
   dependency order** (dependencies before dependents), with plain
   `git merge --no-edit`. **Do not attempt fast-forward merges — they are
   structurally impossible here**: the manifest-commit discipline puts chore
   commits on the feature branch at every issue-status change, so by pr time it
   has always diverged from every issue branch. After each merge run the
   target's test command (if dev introduced a suite the config doesn't yet
   name, run the real suite — and refresh the config in step 3). On conflict or
   red tests, halt and escalate naming the offending issue — never commit a
   broken or conflicted merge.
2. **Plan refresh** (the PM's keep-artifacts-live duty — a locked decision):
   invoke `discovery-plan` once to fold every phase-appended assumption and
   open question into current `ateam-plan.md` + `research-plan.md` — the v0
   ships with plans that reflect what was actually built, not what discovery
   predicted. The same step writes **`docs/product/project-plan.md`**: the plan
   for the **project after v0** — what is left undone, what the epics say comes
   next, what the research plan's open questions imply for the roadmap. Durable
   rules apply.

   Keep the three plans distinct; conflating them is what made this file
   necessary. `ateam-plan.md` is the plan to **reach** v0 (the agents' own
   plan) · `research-plan.md` is the honest disclosure **shipping with** v0 ·
   `project-plan.md` is the plan for what happens **after** v0, for the human
   team. Keep it separate from `ateam-product-report.md` too: the report is
   backward-looking and code-grounded, the project plan is forward-looking and
   necessarily speculative, and mixing verified claims with speculation is how
   a report loses its authority. Commit.
3. **Config refresh** (keep-artifacts-live, extended to config): update any
   `## A-Team Config` fact the run invalidated — e.g. dev introduced a test
   suite, so `test command: none` becomes the real command. Commit as `chore`.
4. **Product report** (durable): invoke `product-report`. It reads the run's
   artifacts — `context.md`, jobs, epics, the ADRs, `ateam-plan.md`,
   `research-plan.md`
   (post-refresh), `prd.md`, `design.md`, `spec.md`, `issues.md` — **and the
   final v0 code** on `feature/<slug>`, and writes
   `docs/product/ateam-product-report.md`: the PRD for the product — product
   framing, the epics on the MoSCoW scope, and what actually shipped. Durable
   rules apply (update in place, supersede — never silently replace). Commit as
   `docs(<slug>): product report`. This runs **before** the PR opens so the
   report ships inside it and the final human review covers it.
5. When all issues are integrated and the full suite is green, open one PR
   `feature/<slug> → <base_branch>` (via `gh`). Body assembled from `prd.md` +
   `design.md` + the issue list — and link `research-plan.md` as the run's
   honest disclosure. If the GitHub projection ran, reference the milestone;
   if it was **skipped**, say so and why, so nobody assumes issues exist.
6. Save a local PR receipt containing its URL and reviewed revision. Call pr
   `complete` with the report and receipt paths, then present the PR for its
   blocking `approve` gate. The requested PR stopping point becomes `stopped`
   after approval. Record `verification` with actual combined-revision results.
   PR creation or approval records no target integration, release, human
   acceptance or product validation. No automatic merge or deployment follows.

## Failure handling

A phase "fails" when its skill errors, produces no artifact, or leaves an
incorrect status. `attempts` counts **failure-retries only** (starts at 0).

- On a failed phase invocation, call `fail` with `phase` and concrete `reason`;
  this persists the failed state and increments its failure counter. Under the
  existing two-retry allowance, record a `revise` reason and restart the phase
  after fixing the cause. At two retries, stop and surface the error.
- Dev retries are counted only by failed `record-issue` results. Never change
  counters by hand or count the runner's internal review cycles twice.
- A blocked stage obligation or missing human answer is not an execution
  failure. Preserve the concrete reason and resume after its resolution.
- **An environment-killed subagent is not a phase failure.** If a subagent dies
  on an infrastructure error (session limit, API outage) rather than failing
  the work itself: verify its workspace is clean, resume or re-dispatch it, and
  do **not** bump `attempts` (proven recovery path, 2026-07 dry run).

## Bootstrap (missing target config)

If the target `CLAUDE.md` lacks `## A-Team Config`:

1. If no `CLAUDE.md` at all, generate one **for the target repo**: apply the
   `/init` skill's analysis to `<target>` (read the target's files, write
   `<target>/CLAUDE.md`). The bare `/init` command analyzes the session's CWD —
   never rely on it when `--repo` points elsewhere.
2. Append (never overwrite) an `## A-Team Config` block with detected values;
   ask the user for any you cannot detect:
   ```
   ## A-Team Config
   - test command: <cmd>
   - base branch: <default branch>
   - design system path: <path>
   - package manager: <from lockfile>
   - harness root: <canonical installed harness checkout>
   - harness revision: <invoked committed SHA; upgrade only deliberately>
   - target remote: <canonical target origin>
   - current context: docs/product/context.md
   - product context: docs/product/
   - read paths: ["."]
   - write paths: ["."]
   - output paths: ["docs/features", "docs/product"]
   - github issues: <on|off — ask; write the literal word, not the choice list>
   ```
   **`github issues` must be asked, never detected.** Creating issues is an
   outward-facing write to a shared repo, and bootstrap is the one moment a
   human is reliably present — under `notify-and-continue` or `run-to-pr`
   nobody is there when the issues phase runs, so an interactive prompt then
   would either hang or defeat the policy. This line is that consent, given
   once and recorded durably. If you cannot ask, write `off`.
3. Commit the new/updated `CLAUDE.md` to the **base branch, before the feature
   branch is created** (`git -C <target> add CLAUDE.md && git -C <target>
   commit -m "chore: bootstrap A-Team Config"`). Config is repo infrastructure
   every future run needs — not feature work riding a deletable branch.
4. Continue startup.

## Manifest

See `manifest-template.json` for schema version 2. The CLI owns validation,
revision increments, event identities, phase statuses, approval bindings,
selective staleness, retries and all state transitions. Discovery passes the
human's existing instructions to `configure`; changes to scope/policy require
a concrete existing authorization reference, never invented approval.

The six independent keys under `milestones` are `implementation`, `verification`,
`human_acceptance`, `integration`, `release`, and `product_validation`. Record
each through `record-milestone` with `milestone` and `evidence` containing
`reference`, `revision`, and local `artifacts`. Human acceptance additionally
requires a human `decision`. Integration requires `merged:true` and `target`
equal to the manifest's intended `base_branch`; an issue branch or open PR is
not that evidence. A milestone records one observed fact; outstanding obligations
remain visible and other milestones do not advance automatically.

### Refinement from current context

For a bounded existing-product delta, reuse the existing feature artifacts and
canonical acceptance ledger. Call `configure-refinement` with the structured
`change` described in `runner/REFINEMENT.md`. The command runs the actual
`planRefinement` validator, retains context/source revisions, and invalidates
only affected bindings. A ready plan permits scoped dev without marking earlier
phases approved. Required discovery reopens discovery; security/domain/design/
architecture/migration reviews block implementation until revision-bound receipts
are supplied and the route is recomputed. Every dev start revalidates the route.
After implementation and verification have their own current milestone records,
call `finish-refinement` with `completion` in the schema documented by
`runner/REFINEMENT.md`. The command reruns scope/current-head checks and the
existing supervisor approval validator against actual stored evidence; a supplied
`passed` flag cannot finish the run. Only a freshly verified result is recorded.
Finishing this requested delta does not record human acceptance, integration,
release or product validation. No replacement orchestrator, permanent agent,
automatic merge or deployment is introduced. Keep review/verification results
linked to the change. Explicit start `task.paths` are target-relative.

## Concurrency

One feature at a time (v1). Do not start a second feature while one is in flight.

## Strict artifact gate

The feature CLI validates real wireflow/page-brief sources at definition and
later stages, and component state declarations from spec onward. Follow
`<harness>/runner/ARTIFACTS.md`. A permissive render, stale SVG or receipt alone
cannot advance a phase. Repair invalid IDs or missing criteria in the owning
source, then rerun completion; do not weaken the canonical obligation ledger.

## Combined delivery checks

Before recording `verification` or completing/approving `pr`, run the supervisor's
`runner/src/combined-cli.mjs verify` against the current feature branch and the
project's `deliveryVerification` binding. Follow `runner/COMBINED-VERIFICATION.md`.
Include every current `issues.md` entry and its actual supervisor approval; all
approved heads must be ancestors of the combined SHA. Record the returned path as
`evidence.combinedVerification` with the same `evidence.revision`. The feature CLI
rechecks that proof against the actual issue file, branch and policy. A moved
branch or changed criteria requires fresh evidence. Keep failed and unexecuted
checks, substitutions and baseline dispositions visible; a later pass retains
prior failures. This milestone does not claim integration or human acceptance.

## Research decisions before dependent commitment

Follow `runner/ASSUMPTIONS.md`. Existing research stays in the product research
plan's single versioned `ateam-assumptions` block, with source digests and retained
`assumptions-history/<revision>.json` snapshots. `run_brief.assumptions` contains
actual ASM IDs. Do not invent demand, ownership, validation or authorizations to
make a gate pass. Legacy prose is preserved and indexed when present; routine
refinement reuses existing records and needs no full discovery rerun.

The command layer validates current research on phase entry, completion and
approval, and on refresh of prior phase evidence. A due load-bearing assumption
names the missing evidence or existing authorized deferral. A prototype before a
later study remains allowed with uncertainty and unresolved owners visible; its
synthetic results cannot become observed human validation. Updates to later-stage
research preserve earlier valid approvals. Prior source/version/result provenance
cannot be overwritten, even through an intermediate revision.

For a supported no-go or reshape, use `record-research-decision` with
`{"assumptionIds":["<actual ASM ID>"]}`, the current `--expected-revision` and a
stable `--event-id`. The command consumes the current recorded decision, returns
success, and stops dependent work. It preserves implementation, verification,
human acceptance, integration, release and product-validation records; stopping
research is not failed delivery. Resuming this direction requires a retained,
authorized research revision and an explicit `revise` of the affected phase.
Separate observed implementation/merge/release facts remain recordable; a claim
of human or product validation still requires its own due evidence.
These validation claims include earlier unresolved research deadlines and the
effective deadline of any authorized deferral. Unrelated later studies remain
pending without invalidating earlier milestones. Recording a valid stop decision
does not require completing work being stopped; other pending research remains
visible, while source, decision and history integrity must still validate.

### Harness evaluation evidence

For harness maintenance, use the versioned synthetic evaluation corpus in `runner/EVALUATION.md` alongside ordinary tests. Preserve outcome records independently from traces, exact source and skill-bundle hashes, and the declared model/configuration/input/rubric identifiers for any separately authorized trials. Never infer human acceptance or model capability from synthetic deterministic passes. Retain grader disagreements and revised rubrics rather than averaging them away. Issue #37 remains an unsupported, release-ineligible dependency until independently resolved; passing existing native controls cannot waive that limitation.
