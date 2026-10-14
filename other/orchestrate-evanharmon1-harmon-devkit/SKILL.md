---
name: orchestrate
description: >-
  Standing mode for policy-resolved, worktree-isolated Dev flow runs. It
  dispatches scoped roles, owns run records and adjudication, monitors durable
  events, and schedules a merge queue without making product or safety choices.
  Use when coordinating one or more Dev Loop lanes. Invoke as /orchestrate.
---

# Orchestrate

**Runtime assets travel with the skills.** Every executable this skill names is
vendored by `task sync:skills`, never fetched from a repository-root `scripts/`
path (harmon-devkit#974): a consumer that installed the skill has no such
directory, so a root-relative dependency installs a skill that cannot run. Two
shorthands are used below and resolve the same way in harmon-devkit's source
tree and in a consumer's flattened `.claude/skills/` one:

- `assets/<name>` — this skill's own asset, i.e. `${CLAUDE_SKILL_DIR}/assets/<name>`.
- `<package>/assets/<name>` — a sibling package's asset. **Resolve
  `${CLAUDE_SKILL_DIR}` physically first**, then append:

  ```sh
  skill_dir="$(cd "${CLAUDE_SKILL_DIR}" && pwd -P)"
  support_dir="$skill_dir/../dev-flow-support/assets"
  ```

  The `cd`/`pwd -P` is load-bearing, not ceremony: where the skills directory
  is reached through a symlink — harmon-devkit's own `.agents/skills/<name>`
  entries are symlinks into `ai/skills/<category>/` — a **logical**
  `${CLAUDE_SKILL_DIR}/../` splits by resolver. `ls` follows the link and
  succeeds; Node collapses `..` with `path.resolve()` before touching the
  filesystem and fails with `MODULE_NOT_FOUND`. Resolving physically first
  makes both agree. This is the same rule `dev-flow-support`'s own `SKILL.md`
  states for asset-to-asset calls; see it for the canonical wording.

  The shared dev-flow v2 runtime (`devflow-policy.mjs`,
  `validate-result-schemas.mjs`, `render-dev-flow.{sh,mjs}`,
  `dev-flow-exit.{sh,mjs}`) lives in `dev-flow-support/assets/`.

A missing sibling package is a blocker, not a fallback: vendor the `universal`
category as a unit rather than resolving a runtime path some other way.

Resolve and announce policy with `dev-flow-support/assets/devflow-policy.mjs`; record resolved
rigor, rounds, breadth, roles, strategy, and disclosures in the run. That
reader operates under `schema_version = 2` and under nothing else: a legacy,
v1, mixed, or unknown `.devflow.toml` is refused with one actionable message
(`copier update` against the harmon-init release shipping the version-2
template, and hold `.skills-sync.yaml` at the last pre-v2 skills release until
it has migrated). Report that message as a blocker and start no run; never
hand-decode an older shape, invent caps, or advance the pin to get past it
(harmon-devkit#604). `assets/consumer-pin-audit.sh` is the standing check
that a repository's vendored-skill pin and its policy shape agree. Runtime
isolation is optional; its absence alone is not a dispatch blocker. Every role
still stays within its declared scope. Use one worktree and branch per lane,
record ownership, scope, dependencies, and the complete file overlap.
Before dispatching overlapping scopes, either serialize them or record the
explicit merge dependency in both lane briefs.

Before tier resolution, bind `$repo` from the canonical target issue URL and
retain the validated target remote name as `$remote` in that lane's checkout.
Validate it with `gh repo view "$(git remote get-url "$remote")" --json url
-q .url`, requiring the result to equal `https://$host/$repo`
(case-insensitively), where `$host` is the canonical issue URL's host, as
`implement` step 1 does; `nameWithOwner` alone would accept a same-named
mirror on another host. A missing remote, failed lookup or mismatched target
is a blocker. This binding belongs to the target repository, which may differ
from the writable fork remote; pass it unchanged to step 0.

**Resolve each issue's Tier before you dispatch its lane, never by eye.**
Follow `dev-flow-support`'s § "Resolving an issue's Tier":
- Read the issue's `tier:<value>` label on every owner type, plus
  `tier:pinned`, its `tier:<role>:*`/`rigor:*`/`strategy:*` labels, and its
  Risk and Complexity, with the repository's owner type as `owner_type`: on
  an organization repository Risk and Complexity come only from issue
  fields, never a same-named label.
- Translate them with `dev-flow-support/assets/tier-inputs.mjs --policy
  .devflow.toml`, which
  reconciles label conflicts *before* the reader runs. A `tier:pinned` with
  more than one unqualified `tier:<value>` is an ambiguous pin: no
  `pinnedTier` is passed, a warning names both values, and
  the pin rung is dropped, so resolution continues through the remaining
  rungs.
- Pass the result to `devflow-policy.mjs resolve`. That is how the reader
  receives the issue as `issueTier` (Risk × Complexity, plus the stored Tier
  as a cache) and the pin as `pinnedTier`. When the Tier label is absent,
  the reader computes the Tier from Risk and Complexity.

Every resolution, at dispatch or any later re-resolution, runs the full
procedure, step 0 included. When the lane's working tree (committed,
staged, unstaged or untracked) differs from its merge base in
`.devflow.toml`, `agent-registry.json`, or the reader,
`toml-lite` or `tier-inputs.mjs` assets, the **merge-base** helper and reader
resolve it instead of the branch's
(the procedure's step 0). Decide that with `step0_probe "${remote:-}"`,
passing the `$remote` validated against the lane's target `$repo` above;
when it returns 2 (indeterminate), stop
rather than dispatching. A merge base that predates `tier-inputs.mjs` needs
an operator-pinned reader supplied outside the branch; without one the Tier
is indeterminate, never resolved by the branch copy. On a `strategy:*`
conflict an interactive orchestrator asks the operator, and unattended
dispatch takes `default_strategy` with the warning.
Label provenance is checked before translation, under § "Nothing here arms
anything" in `AGENTS.md`. Every `rigor:*`, `strategy:*` and `tier:<role>:*`
label you honor goes into the helper's `authorized_labels`. An unlisted one
is dropped with a warning (fail-closed). The pin's marker and value are
verified separately. Risk, Complexity and the stored Tier are ungated (ADR
2026-09-30 D3). Record the resolved implementer tier
and its source in the run and in the lane brief's `{{role-tiers}}`. Put the
`tier-inputs.mjs disclose` lines into the PR-body disclosure. They name:
- the tier source (pinned, rigor, derived, default);
- any pin-caused invariant break;
- any overridden role label;
- every warning.

In a repository whose `.devflow.toml` has no `[tier.matrix]`, a classified
issue whose Tier the **derived rung would decide** resolves indeterminate
(exit 3) and keeps its profile tier. That means no operator tier, no honored
pin, no `tier:implementer:*` label and no chosen rigor. When one of those
decides instead, it applies with exit 0; do not stop that run. This includes
harmon-devkit until its template update to the release carrying
harmon-init#1475. Disclose it; never guess a Tier.

## Planning

Before provisioning or dispatching a slate, turn its milestone or explicit
issue list and the resolved policy into a durable plan at
`<git-common-dir>/dev-flow-v2/slates/<slate-id>/plan.json`. Resolve the common
Git directory with `git rev-parse --git-common-dir`; a linked worktree's `.git`
path is a file and is never the shared-state root. Planning is orchestrator
judgement written down, not a new autonomous planner: the schema, validator,
and append-only recompute rule make its deterministic parts checkable.
A second writer of the same `plan.json` is a blocker: the slate lock in
§ "Durable orchestrator state" refuses it, by slate id and by the work itself.

Build and publish the plan in this order:

1. **Graph.** When `.foreman.toml` exists and the slate is milestone-backed,
   consume `task foreman:plan -- --milestone <n>` for dependencies, waves, and
   the ready set instead of reimplementing Foreman's graph. Otherwise read
   native blocked-by edges and the fixed `Blocked by:` fallback lines from
   `breakdown` §4. For an explicit issue list in a Foreman repository, include
   its containing milestone in the graph input or stop if no authoritative
   Foreman graph can cover the list.
2. **Re-verify.** Check every ready issue read-only against the live target
   tree. Record `valid`, `partial`, or `done` and a complete candidate-file
   list; issue-body line numbers are hints, never evidence. Remove `done`
   issues from dispatch waves without erasing their verified verdict. An
   issue labelled `human` — a `(HUMAN):`/`(QA):` collector or other
   human-only work — is never dispatched, so drop it from the slate before
   re-verifying, together with every slate issue it blocks: none of them
   enters `plan.issues`, a wave, or a lane (the plan schema has no verdict
   for them, and a dependent kept without its blocker would either dangle or
   dispatch early). The dependents re-enter a later plan once a human closes
   the precondition, and the run's human-work summary names all of them.
3. **Overlap.** Compare every pair of dispatchable candidate-file lists. Record
   the complete shared-path intersection for each overlapping pair, choose
   `serialize` or `split`, and record the resulting merge dependency. A split
   also becomes the ownership fence in both lane briefs; an overlap absent
   from the plan is not safe to dispatch.
4. **Cap.** Record which dispatcher applies and the cap it actually uses. An
   interactive orchestrator uses the resolved
   `[breadth].max_parallel_agents` directly. Only when Foreman is the dispatcher
   is that policy cap intersected with `.foreman.toml`'s `max_parallel`; a
   configured Foreman limit never lowers an interactive run's cap.
5. **Project.** In a complete revision `plan`, record the resolved policy
   snapshot; re-verified issues and candidate files; pairwise overlaps and
   resolutions; waves; and lane, issue, branch, run id, and fence assignments.
   Each lane fence uses exactly the `brief.envelope.schema.json` `fence` item
   shape. Later authorized expansions append `{path, at, reason}` entries to
   that lane's `expansions` array instead of rewriting its original fence. An
   accepted expansion is a recomputation reason: before the lane edits the
   expanded path, publish a complete new revision through the candidate,
   validate, rename, and canonical-readback sequence in step 7.
   **Persist lane profiles at dispatch.** Write each lane's complete resolved
   profile as `{lane, policy}` in `plan.lane_profiles` in the validated
   revision before dispatch, including its caps, breadth, all five role tiers, sources and
   operator pins. `plan.policy` is the slate baseline; `lane_profiles` is a
   complete projection, not a partial override.
   A recorded lane profile is immutable for its run; changing it requires a new run.
   When the array is present it
   must cover every planned lane and name no unknown lane. On resume, read
   the last validated revision's lane profile for the lane brief and stage
   gates; never substitute the slate's global role tiers. Older plans without
   the array remain valid: before resuming dispatch, resolve every lane through
   the full tier procedure (step 0 included) and append a validated revision
   containing `lane_profiles`. Do not infer past lane refinements from the
   global baseline. If inputs cannot be recovered, stop as indeterminate.
6. **Reserve, emit and validate.** Before writing `plan.json` at all, take the
   slate lock with its explicit issue set:
   `dev-flow-support/assets/run-record.mjs lock acquire --slate <slate-id>
   --session <session> --issues <n,n,…>`, adding `--milestone <n>` for a
   milestone-backed slate (the milestone exists only in the lock). A second
   orchestrator naming the same work is refused here, before it can publish a
   plan or dispatch anything. Then write the closed record and validate it with
   `node dev-flow-support/assets/validate-result-schemas.mjs plan <plan.json>`. Refuse dispatch
   on a structural error, a broken revision digest, an incomplete overlap set,
   a graph/projection mismatch, an ownership error, or a cap violation. Both
   writers refuse while the canonical plan names an issue outside the
   reservation, so a later revision that adds issues widens the reservation
   with `lock acquire --issues` first.
   Immediately before each lane dispatch, compare the live target head with the
   last revision's `plan.base_sha`; when they differ, recompute and validate the
   plan before dispatching.
7. **Recompute after every external merge.** Re-read the new default-branch
   head, release newly unblocked dependents, rebuild waves, and repeat live
   re-verification and pairwise overlap checks. Append the next `revisions[]`
   entry with the complete new `plan` plus `seq`, `prev_digest`, `digest`, `at`,
   and `reason`, using the same canonical-JSON SHA-256 chain convention as
   `run.schema.json`; the digest covers the complete sorted-key `plan` and the
   chain fields. The last revision is current, and earlier revisions remain
   reconstructable without a second top-level projection. As the slate's single
   writer, write the complete candidate beside `plan.json`, validate that
   candidate with the `plan` kind, rename it over the canonical record, then
   validate the canonical readback. Either validation or rename failure is a
   blocker; dispatch and merge-queue mutation remain paused.
   The mechanical half of a base move — bump `base_sha`, retire done issues
   and their lanes, extend the chain — is
   `dev-flow-support/assets/plan-revise.mjs base-move`, which runs exactly
   that sequence. It refuses, naming the paths or issues, whenever the move
   needs judgment: the new commits touch a live lane's fence or candidate
   files, or a done issue releases a dependent. Fence expansions, overlap
   choices and wave changes stay yours; write them as a complete revision.

## Durable orchestrator state

Everything you need in order to resume lives under the Git common directory,
never in the session scratchpad. A scratchpad does not survive a session
restart, and one that was wiped mid-slate took every dispatch file, ruling
and watcher script with it (harmon-devkit#1296). The scratchpad is for
throwaway work only.

- **Run records:** `<git-common-dir>/dev-flow-v2/runs/<run-id>/run.json`,
  beside `monitor.json`.
- **Slate plan:** `<git-common-dir>/dev-flow-v2/slates/<slate-id>/plan.json`.
- **Your own working files** — dispatch files, rendered briefs, ruling files,
  watcher state:
  `<git-common-dir>/dev-flow-v2/slates/<slate-id>/orchestrator/<run-id>/<attempt-nonce>/`,
  keyed by run id and attempt nonce the way lane reports are.
  `assets/dev-flow-monitor.sh orchestrator-dir --slate-id ID --run-id ID
  --nonce NONCE` prints the path.

Use `dev-flow-support/assets/run-record.mjs` for the run-record operations
it supports, never a hand edit:

- `transition`, which also appends the matching transition receipt;
- `intervention`;
- `bind-pr`;
- `close`.

Promotion is decided out of the readiness gate by the session that owns
integration — the orchestrator in an orchestrated run, the `/integrate`
session in a solo run — and that session records it with `run-record.mjs
promote`.

A run belongs to exactly one slate. Its first helper write needs the run to be
a lane in some revision of that slate's plan, and records the slate in
`runs/<run-id>/owner-slate`; every later write must name the same slate. Each write builds
a candidate, validates it with `validate-result-schemas.mjs run --receipts`
plus every adjudication document in the run directory, renames it over
`run.json` and validates the readback. A refused edge, a promotion dated
before the last transition, a promotion over an unsettled deferred finding,
or any entry written after the run has ended — promoted, capped, escalated or
abandoned — therefore never lands. The rest of the
record keeps its existing writers:

- the kickoff record — this skill, at activation;
- pass receipts, evidence registrations, splits and stage-advance
  transitions — `/review`'s own write recipe;
- settlements — `/integrate`.

Each of those writers runs the same candidate, validate, rename and readback
sequence. Point an intervention that rests on a ruling file at it with
`--ruling FILE`: the note records the file's SHA-256. That digest identifies
the bytes you relied on. It does not protect them: the note lives in a
lane-writable record and nothing verifies it automatically, so an edit is
caught only by someone who re-hashes the file and compares. `close` records a non-promotion outcome if
the run is still open, then moves the run's orchestrator directory into
`runs/<run-id>/orchestrator/`, so a stale dispatch file can never mislead a
later session. Files under `.git/` never show in `git status`.

Both writers take the **slate lock** (`run-record.mjs lock
acquire|release|status`), recorded under `<git-common-dir>/dev-flow-v2/locks/`
with the slate's milestone and issue set. While another session holds the
same slate, the same milestone, or any of the same issues — under any slate
id — every write is refused. Take it before publishing the plan (§ Planning
step 6), with `--issues` and, for a milestone-backed slate, `--milestone`: an
implicit lock taken at a first write records no milestone, and a plan
published before its reservation can overwrite another session's plan. Release it when the slate
ends. `--force
--reason` breaking a dead session's lock is an operator decision; name it in
the handoff.

Durable means *this clone*: the common directory survives restarts, `/clear`
and worktree removal, but not a fresh clone, a rebuilt devcontainer without a
persistent volume, or an ephemeral cloud session. GitHub evidence stays the
cross-machine record. Every worktree shares the directory, so a lane *can*
edit these files; re-hashing a ruling file against its recorded digest is the
only check that an edit happened.

## Lane briefs

Lane briefs consume the validated plan's last revision assignments, fences,
overlap choices, and merge dependencies rather than reconstructing them from
session prose.

### File-scope fences

A file-scope fence is the closed list of paths and globs a lane may write. Derive
it from the issue's named surface, every repository test that asserts on those
files, and the consumers reported by
`assets/validator-dependency-scan.sh <path>...` for each manifest, schema, or
registry in that surface. The scan is a read-only, grep-based inventory of
consumers under `scripts/`, `ai/skills/**/assets`, `taskfiles/`, and
`Taskfile.yml`; it finds file names and hard-coded keys, not YAML/TOML scalar
values. Inspect its candidates and add the validators and tests that would
reject the lane's change. Release-please's `CHANGELOG.md` is never
lane-owned and never belongs in a fence; lockfiles are ordinary fence entries.

Across live lanes, enforce one writer per file. When an overlap is unavoidable,
name the shared file and disjoint sections in both lane briefs' overlap lists
and record the branch-update or merge dependency that serializes them. A worker
has one bounded self-expansion route: a validator or test that rejects its
change and that no other live lane touches, recorded once for that file as
`YYYY-MM-DD fence expansion: path:line[-line] — reason` in its lane report.
Verify the dated entry and line scope, reject it if another live fence owns the
file, and record the accepted expansion as a `run.json` intervention with `kind: asked`.
The Planning section owns recording the same fact in `plan.json`.
Every other expansion requires an ownership check and an attributed re-brief
before the worker edits the file.

Before evaluating the readiness gate, run
`assets/fence-check.sh --brief <rendered.md>`.
It derives the comparison base from the brief's default branch, then reports
whether both sides of every changed path are covered by the rendered envelope
fence or a labelled expansion in the envelope's `report_path`. Its advisory
refusal is visible to the orchestrator.
This pre-gate subset check is not a readiness-gate condition.

The source catalog below is the complete render contract. It deliberately lives
in this procedure rather than in the dispatched template: substituting free-form
values into a catalog inside the output would duplicate them into a Markdown
table before their intended sections.

| Placeholder | Source |
| --- | --- |
| `{{brief-envelope-json}}` | JSON serialization of the exact `brief.envelope.schema.json` fact fields; `body` is omitted from the block because the validator derives it from all Markdown outside the delimiters |
| `{{lane-name}}` | Orchestrator lane plan |
| `{{run-id}}` | Active run's `run.json` |
| `{{branch}}` | Lane plan and `git branch --show-current` |
| `{{default-branch}}` | Target repository default branch |
| `{{base-sha}}` | Lane creation record |
| `{{worktree-path}}` | `git rev-parse --show-toplevel` in the lane |
| `{{harness}}` | Selected implementer's registry harness |
| `{{effort}}` | Reasoning effort the lane is expected to run at — the value its status line is checked against |
| `{{codex-model-id}}` | Model id the Codex pane was launched with, or `n/a` for a non-Codex harness |
| `{{codex-launch-flags}}` | The approval and sandbox policy the Codex pane was launched with. Default: `-a never -s workspace-write -c sandbox_workspace_write.network_access=true`. `--dangerously-bypass-approvals-and-sandbox` is a per-dispatch override, disclosed on the profile line; `n/a` for a non-Codex harness |
| `{{report-path}}` | Nonce-scoped path under the common Git directory, or a path whose worktree exclusion the orchestrator has installed and verified |
| `{{scratch-dir}}` | Per-lane subdirectory of the scratchpad, for throwaway files only — nothing needed to resume lives there; never the scratchpad root |
| `{{repo-tier}}` | `light`, `standard`, or `heavy` — resolved by the base template's strongest-signal-wins procedure, never by matching a row's description |
| `{{gate-bounds-override}}` | Repository's own measured gate bounds, or `None — use the base template's table.` |
| `{{gate-commands}}` | The repository's actual gate invocations, one per line |
| `{{generation}}` | Active pointer generation |
| `{{active-state-path}}` | `assets/dev-flow-monitor.sh active-path` |
| `{{record-directory}}` | Active run record directory |
| `{{policy-projection}}` | Resolved policy projection recorded at kickoff |
| `{{file-scope-fence}}` | Orchestrator's lane ownership plan |
| `{{live-lane-overlaps}}` | Orchestrator's complete live-lane overlap map |
| `{{issue-number}}` | Claimed GitHub issue number |
| `{{issue-title}}` | Fresh canonical-target `gh issue view` result |
| `{{issue-url}}` | Canonical target-repository issue URL |
| `{{unit-kind}}` | `implementation` or `proposal-only` — a proposal-only lane still runs every gate, commits, pushes and opens the draft PR; it stops there |
| `{{claim-handoff}}` | Transaction-refreshed claim for the provisioned lane branch: authenticated comment ID, author ID, `updated_at`, expected assignees, and expected claim labels |
| `{{verified-facts-and-rulings}}` | Orchestrator verification and attributed decisions |
| `{{git-sandbox-note}}` | Harness-specific sandbox policy, or `Not applicable.` |
| `{{known-environmental-failure}}` | Verified run exception, or `None.` |
| `{{rigor}}` | Trusted policy resolution |
| `{{rigor-source}}` | Policy resolver disclosure |
| `{{challenge-cap}}` | Selected rounds policy |
| `{{review-cap}}` | Selected rounds policy |
| `{{integration-cap}}` | Selected rounds policy |
| `{{remediation-cap}}` | Selected rounds policy |
| `{{min-rounds}}` | Selected rounds policy |
| `{{wall-clock-min}}` | Selected rounds policy |
| `{{deadline}}` | Active `run.json.started_at` plus `wall_clock_min` |
| `{{max-agent-runs}}` | Selected breadth envelope |
| `{{max-parallel-agents}}` | Selected breadth envelope |
| `{{strategy}}` | Trusted policy resolution |
| `{{strategy-source}}` | Policy resolver disclosure |
| `{{role-tiers}}` | Resolved five-role tier projection, including the implementer's tier source (pinned, rigor, derived, default, or operator) and every `dev-flow-support/assets/tier-inputs.mjs disclose` line — a pin-caused invariant break, an overridden role label, a rejected role label (with the reader's reason), a tier warning, or a derived Tier left indeterminate |
| `{{operator-pins}}` | Attributed operator pins, or `None.` |
| `{{pr-title}}` | Orchestrator's release-title-compliant proposal |
| `{{ready-sentinel}}` | Orchestrator-generated per-lane sentinel prefix |
| `{{handoff-sentinel}}` | Orchestrator-generated draft-handoff sentinel prefix |
| `{{blocked-sentinel}}` | Orchestrator-generated per-lane sentinel prefix |
| `{{attempt-nonce}}` | Fresh nonce for this dispatch attempt |

Every local PR-owning lane brief MUST carry the active run identity so the lane worker can
route confidence stages through `/review` and publish a draft with v2 evidence;
the supervising orchestrator then invokes `/integrate` and retains every
finding disposition, PR-body edit, thread reply, readiness decision, and
promotion. (`retro-run-report.mjs` exit 10 `no-run-record` is the failure this
routing prevents.) The required fields are: run id, branch, generation,
active-state path, record directory, and policy projection. Without them the
lane worker falls back to the inline `task challenge` / `task review` procedure,
which produces no run record and no adjudication evidence.

Before draft publication, a confidence-stage finding uses the template's
decision handshake: the lane records a decision request and waits for a durable
orchestrator-authored disposition. With a compatible `/review`, a confirmed code
fix is performed by the fresh bounded implementer dispatched after the
orchestrator reserves its agent run. The inline fallback has no such dispatch
surface, so the orchestrator instead authorizes the original lane to apply only
the exact confirmed fixes in its recorded disposition and verifies the returned
gate/publication evidence. The post-draft handoff remains separate and transfers
integration to the supervising orchestrator.

Render `assets/lane-brief.md` for every local end-to-end, PR-owning implementation lane
instead of hand-authoring a brief. Council proposal and synthesis implementers,
and bounded remediation implementers, use their schema-bound role briefs and
return the artifact or fix their dispatch requested; they do not receive this
draft-publication contract.

Never write an implementer brief freehand, whatever its shape. Outside a v2 run
— a dispatch with no run record — render the `implement` skill's
`assets/implementer-brief.md` against its own source catalog
(`implement/SKILL.md` § "Brief template source catalog") instead. That template
is the base contract this one extends: its § "Hard rules", § "Gate commands and
time bounds", § "Proposal-only units" and § "Delegation contract" are stated
there once, and `assets/lane-brief.md` § "Inherited base contract" names all
four and supplies their per-lane values rather than restating them. A brief
composed from memory is how the 2026-09-06 fan-out shipped three workers that
each broke a different one of those rules.

`implement` is a **required dependency** of this skill, declared in
`assets/policy-contract.json`. `assets/lane-brief.md` is the superset of that
skill's brief template and names four of its sections without restating them,
so a consumer holding `orchestrate` without `implement` renders a lane brief
whose hard rules, gate bounds, proposal-only clause and delegation contract are
absent. The lane brief therefore **blocks** when the base template is
unreadable, rather than degrading — a one-command vendoring fix, not a mode to
run in. The agent definitions under `ai/agents/` keep the discover-don't-require
degradation: a bounded role can return an honest typed result without the
contract, a lane cannot open an honest PR without it.

Neither template is a work contract for a **bounded role subagent**. Both
finish at a published draft PR, which `ai/agents/implementer.md` § "Never"
forbids non-overridably; a role agent gets its own schema-bound role brief and
returns a typed result. The delegation contract's rule 5 is the one place the
two audiences meet, and it splits there explicitly.

For a PR-owning lane, the source catalog above is the complete input contract: source every value, select the harness procedure
named by the rendered brief. Provision the lane branch/worktree, then
transactionally refresh the existing claim so its record names that exact branch.
Authenticate the refreshed claim into the handoff snapshot without transferring
its ownership.
As a render-time completeness check, scan the entire rendered file and refuse
dispatch if any unreplaced `{{name}}` token remains. This is the renderer's
check, not content validation of the opaque body; the `brief` validator checks
double-brace tokens only inside the envelope block.
For local PR-owning lanes, validate the rendered brief before dispatch and refuse dispatch on any failure:
`node dev-flow-support/assets/validate-result-schemas.mjs brief "$brief_path"`.
Place the per-attempt report under the common Git directory, or install and
verify its worktree exclusion before dispatch; an assertion that it is excluded
is not evidence. Preserve its nonce-scoped sentinels. Prompts sent after dispatch
refer to that reporting contract indirectly and never quote a sentinel value,
because old pane output must not satisfy a later attempt.

## PR-open confirmation

Before promoting a lane's PR, confirm the lane produced v2 evidence
appropriate to its topology and resolved policy for the lane's active
run ID. Each enabled confidence stage (resolved cap ≥ 1) must have its
own evidence — adjudication records from `/review`, not merely a kickoff
marker — and a disabled stage (cap 0) must have its authenticated
disabled-stage verdict; a single verdict never covers an enabled stage.
A lane dispatched under the fork topology or without a vendored
`/review` skill uses the inline fallback by design and produces no v2
evidence; the orchestrator accepts that limitation and does not require
evidence the procedure cannot produce. `retro-run-report.mjs` exit 10
(`no-run-record`) is the diagnostic for a lane that was expected to
produce evidence and did not; when the condition fails and the skill
path is available for the lane's topology, the routing failed and the
lane must be re-run before the PR is promoted.

**The implementer record is confirmed at PR open, and written here when the
lane cannot write it.** When a lane's draft PR opens, the four implementer
values (`model-family`, `model`, `model-version`, `model-effort`; harmon-devkit#1262)
must name the model that actually ran that lane — the family, model line,
version and effort this dispatch attested, never a value read back from the
lane's own output, the issue, or the branch. A lane whose harness writes labels
records them itself through `/implement` step 8; confirm it with the implement
skill's `assets/record-implementer.sh check --repo <repo> --pr <n> --registry
<default-branch registry snapshot> --harness <lane harness>`. **The orchestrator
writes on behalf of a lane whose harness cannot write labels** — an Antigravity
lane, or any lane briefed not to touch GitHub — by running the same asset's
`apply` with the lane's PR, its issue, and the dispatch-attested values; the
same applies whenever the orchestrator itself opened the lane's draft PR.
`apply` validates the values against the registry first and refuses
an unknown value rather than guessing one; a refusal is a blocker to report,
not a value to fill in. A harness whose registry entry declares no `efforts`
(an Antigravity lane) records family, model and version only and leaves
`model-effort` unset — pass no `--effort` and never invent one — while a
harness that declares efforts still owes one from its list. On an
organization the issue takes the issue fields; on a personal account,
labels; the PR takes labels on both; and on the issue the last implementer
wins, which also clears an earlier implementer's effort when this one
records none. Like `claim:*`, the record is never a routing input — nothing here or in
any dispatch reads it back to choose a model.

The maintainer-facing ready report is the last message about a promoted PR,
not the first one after promotion. **Invariant: the ready report is sent
only for a `POST-PROMOTION-CLOSED` event that names the promotion event id
the watcher armed on, with zero activity rows in that window, and only
after one re-read taken after the close shows the same head, the same
readiness fingerprint, and every check still concluded green; any other
observation (a different promotion id, any activity row, any changed
value, any indeterminate read) withdraws the report and re-arms.** The
re-read uses the same mechanisms `AGENTS.md` § Readiness gate names for the
promotion-time check (`headRefOid`/`isDraft`, required CI status, and
`readiness-gate.sh fingerprint`); promotion itself is never reported as
readiness, and a status sent during the watch instead reads "promoted at
T, post-promotion watch until T+15", never "ready". Matching the vendored
`/integrate` skill's own handling of an invalidated promotion
(`.claude/skills/integrate/SKILL.md` step 6): withdrawing runs
`gh pr ready --undo` and confirms the PR is draft on the current head
before deciding whether to re-verify or escalate. The mechanism that
satisfies this invariant — window arming, activity/close correlation by
promotion event id, retry on an indeterminate read — belongs to
`assets/lane-watch.sh`; this section states only what must be true before
the report is sent, never the ordering or per-endpoint steps the watcher
uses to get there.
This maintainer-facing report is distinct from § Persistent supervision's
internal per-lane ledger entry ("a ready PR is reported"), which is
orchestrator bookkeeping, not the maintainer-facing message this rule defines.

If the orchestrator reverses its own promotion (`gh pr ready --undo`, for any
reason, including mid-watch), the withdrawal is announced before anything
else in the next maintainer-facing message — "#n is no longer ready: `<reason>`; back to draft on `<head>`" — ahead of any other status in that same message.

## Implementer selection

Select implementers only from
the resolved `[stage.implement].pool`, registry role eligibility, and resolved
family/harness preferences; council dispatches also enforce its
`distinct_families` requirement. Enforce one
writer per feature branch. A lane can commit only its lane branch; the feature
owner alone assembles selected lanes, then records the included/discarded lanes
and canonical SHA in that assembly's `run.json` stage transition before pushing
the feature branch. Under council with `synthesis = true`, dispatch one fresh
implementer with the ordered source proposals and accept its artifact only when
`result.implementer.payload.synthesis_of` names those proposal identities in
that same order; record every proposal's selection outcome in the assembly.
Reject a lane that requests feature-branch write authority.

Immediately before every implementer invocation—initial lanes, council
proposals and synthesis, and remediation—the feature owner calls
`assets/dev-flow-monitor.sh reserve-agent-run` with a deterministic dispatch
event and the resolved `[breadth].max_agent_runs`. Confidence finders and
fallbacks spend the independent rounds envelope and never this implementer
budget. The monitor pins the total implementer ceiling on the first reservation
and durably accounts every slot under the active-run lock. A crash after
reservation spends the slot; an exact event re-arm adopts it without spending
twice. A changed or exhausted budget blocks before dispatch.

## Lane launch and waits

A headless lane has nobody to answer an editor. Start every lane with
`GIT_MERGE_AUTOEDIT=no` and `GIT_EDITOR=true` in its environment: the first
keeps `git merge` from opening one, the second makes any command that still
asks for a message (`git commit` while finishing a conflicted merge,
`git merge --continue`) accept the prepared one instead of waiting. Under
herdr, set both on the tab and on every pane that hosts a lane, and never
start a lane in the root pane `herdr worktree open` or `worktree create`
gives you (neither takes `--env`); open a tab or split a pane with the
variables inside that workspace instead:

```bash
herdr tab create --workspace <workspace> --label <lane> --no-focus --env GIT_MERGE_AUTOEDIT=no --env GIT_EDITOR=true
herdr pane split --pane <pane-id> --direction <right|down> --cwd <worktree> --no-focus --env GIT_MERGE_AUTOEDIT=no --env GIT_EDITOR=true
```

Under any other launcher, export both into the lane's environment before the
harness starts. The variables are the backstop, not the instruction: if and
where a lane is permitted to merge the default branch into its own (this
skill's lane brief does not grant it; a consumer's may), every brief and every
relay spells the command `git merge --no-edit origin/<default-branch>`. A
merge that stops on a conflict is finished by resolving the files, `git add`
on each, then `git commit --no-edit --cleanup=strip` (the cleanup drops the
`# Conflicts:` comment block `--no-edit` would otherwise keep in the pushed
message); `git merge --abort` backs it out
instead. A lane stuck in an editor anyway reports BLOCKED and is escalated to
the orchestrator and the maintainer; it is never recovered by the lane, or the
orchestrator, terminating a process — that is the maintainer's decision.

`assets/settle-wait.sh` is the required primitive for every bounded lane
settle and CI settle. Both modes take **seconds**. A lane settle is two steps:
confirm the prompt was delivered, then settle:

```bash
herdr agent prompt <lane> "<text>" --wait --until working --timeout 30000
bash <skill-dir>/assets/settle-wait.sh agent <lane> --timeout-seconds 3600
bash <skill-dir>/assets/settle-wait.sh checks --repo <owner/repo> --pr <n> --head <pushed-sha> --timeout-seconds 1800 [--interval-seconds 30]
```

The delivery check is the one sanctioned raw herdr `--timeout`, and its unit
is **milliseconds** (`30000` is 30 seconds). It proves the prompt landed:
settling straight after a prompt without it can return on the idle state the
lane was in before the prompt arrived. Every longer wait goes through the
asset, which converts seconds to herdr's milliseconds itself; never pass a
raw `--timeout` to `herdr agent wait`, and never use `agent prompt --wait`
for the long settle. Without `--until`, `agent` waits on herdr's default
settled set (`idle`, `done`, `blocked`), then reads the lane with
`herdr agent get` and settles only on `idle` (tab seen) or `done` (the same
state, unseen); `--until <state>` is for a state-specific wait. `checks`
takes the full SHA you pushed as `--head` (required): while the PR still reports another head it is not settled, and it
reports a settle only when the PR head, re-read after the run reads, is still
that SHA. A `pull_request` run is scoped to `--pr` by its `pull_requests[]`:
one naming only other PRs is ignored, and one with an empty or unprovable
association (fork PRs list none) is counted on its own, never collapsed or
used to supersede. Of this PR's runs it keeps the newest run of each workflow,
so a cancelled or failed run superseded by a re-run no longer counts. The
superseded run's own read decides: it is dropped only when that read says
completed and its latest attempt started (`run_started_at`, else
`created_at`) before the newest run's did; one whose read is not completed
stays pending, and one manually re-run after the newest run started, or whose
start time either read lacks, counts on its own conclusion. It counts every
run of any other event, reads each counted run's own `.status` and
`.conclusion`, pages as far as GitHub's 1000-run search cap at any page size,
and is indeterminate when the run list reports that cap. As in GitHub's own check
rollup, the newest `pull_request` run is the verdict even if its jobs were
skipped, so a workflow that skips its tests on an `edited` re-run can hide an
earlier failure; never settle CI with
`gh run watch --exit-status` or `gh pr checks --watch`, which report stale or
partial conclusions across re-run attempts. It covers Actions workflow runs
GitHub has already created, not external status checks; the readiness gate
still owns the full check verdict.

The exit status is the verdict, and it means different things per mode. In
`checks` mode: 0 settled green, 1 settled with a failing run, 2 usage, 3
indeterminate (the PR head was not `--head` at the last poll, or that poll
could not be read, listed no runs, or hit the 1000-run cap), 4 expired with
runs pending. In `agent` mode the status is herdr's own except for 0 and 5:
0 settled (`idle` or `done`), 5 the lane is blocked at an approval or
question, `unknown`, or unreadable, and any other status is herdr's own and
not settled — herdr's 1 (server error) and 2 (usage) are not the `checks`
codes — with 124 when the backstop stopped an overrunning herdr (137 if it
had to be killed). Never follow a wait, or the delivery check, with `; echo`,
`|| true`, or anything else that discards that status: an expired wait must
never read as settled. `lane-watch.sh` below stays the persistent monitor;
this asset is for a single bounded wait.

### Cloud lanes

Cloud lanes are used only on the operator’s explicit request.
Never choose cloud lanes unprompted or recommend them. Local Herdr agents remain
the default. Render `assets/cloud-lane-brief.md`, checked by its own render check
in the cloud reference; the `brief` validator governs local PR-owning lanes. See
[Cloud lanes](references/cloud-lanes.md) for launch, messaging, GitHub watching,
environment limits, and the orchestrator-owned review and PR handoff. This mode
replaces local worktree, agent-settle, and report-file handling for that lane;
claims, policy resolution, fences, and readiness duties still bind.
The orchestrator names the cloud lane's `claude/*` branch before launch, so the
lane is planned, fenced and claimed like any other.

## Persistent supervision

Watching is the standing mode, not a one-shot step. Use the harness's
session-lifetime persistent monitor primitive—never a background shell subject
to an ordinary command timeout—to poll fresh lane-agent and PR state and emit
only transitions (`idle`, `done`, `blocked`, `unknown`, and PR deltas). If it
exits before the overall run reaches a terminal outcome, re-arm it immediately;
never interpret monitor termination as human cancellation. If no persistent
primitive is available, block instead of silently falling back to occasional
manual polling.

Use `assets/lane-watch.sh` for that polling. Harness monitor primitives may run
their command under a non-Bash shell, so always invoke the file as
`bash <skill-dir>/assets/lane-watch.sh --state-file <run-dir>/lane-watch.state --registry
<kickoff-registry-snapshot> <deadline> <lane:branch:nonce:owner/repo>...`;
never paste its loop inline. Keep the state file across re-arms so reported
sentinels and post-promotion activity remain deduplicated. The watcher bounds
every `herdr` and `gh` read, prefers each lane's `.lane-report.md` sentinel,
tags pane-only fallback results, and watches reviews plus top-level and inline
comments for 15 minutes after a draft becomes ready. When a lane's
post-promotion window's promotion event cannot be resolved before that
window's own deadline passes, the watcher emits
`POST-PROMOTION-INDETERMINATE <lane>: #<pr>` instead of silently abandoning
the window — the event means only that the promotion epoch could not be
confirmed in time; that path also clears the lane's tracked `PR` state as it
tears the window down, so the very next observation — the watcher's own next
poll, or a fresh process restarted against the same `--state-file` — sees
the still-promoted PR as newly observed and re-arms a fresh window on its
own, which is what makes restarting with the same state file a genuine
retry rather than a no-op. Keep the registry argument
bound to the immutable kickoff snapshot across every re-arm. It only reports
events; the orchestrator remains responsible for every action. The watcher-owned
`lane-watch.state` is separate from the run's canonical `monitor.json`; never
pass that JSON monitor state to `--state-file`.

The watcher's own restart durability does not, by itself, make the
orchestrator's reporting durable: `POST-PROMOTION-ACTIVITY` and
`POST-PROMOTION-CLOSED` are lines on the watcher's stdout, consumed by a
separate orchestrator process, and the § PR-open confirmation gate depends
on the orchestrator having durably seen every activity line for the
*current* window — never merely on what its own live stdout stream has shown
since its own last restart. An orchestrator restart mid-window must not
silently default to "no activity seen"; confirm that against durable state,
either by re-deriving what happened over the window's `[since,until]`
directly from the same GitHub activity sources `lane-watch.sh` itself polls,
or by maintaining its own durable log of every `POST-PROMOTION-ACTIVITY` /
`POST-PROMOTION-CLOSED` line it has actually processed.

Every emitted transition terminates in a recorded action: idle reads and
adjudicates the lane status (including any unsupported claim that the user was
asked); done validates and assembles or records a blocker; blocked/unknown
surfaces the evidence and stops or re-briefs within authority; a ready PR is
reported with merge-queue externalities; a dirty PR returns to its owning lane;
and an external merge releases dependents, recomputes the queue, and rechecks
stacked branches. Keep a visible per-lane ledger of assignment, fresh state,
last progress, and next action. Hand off the run record before primary-session
context exhaustion so a fresh driver can re-arm the same monitor.

Resolve the shared run directory with `git rev-parse --git-common-dir`, never by
appending to a worktree's `.git` path (which is a file in linked worktrees).
`assets/dev-flow-monitor.sh state-path --run-id <run-id>` returns the canonical
`<git-common-dir>/dev-flow-v2/runs/<run-id>/monitor.json` path. Keep
the schema-valid `run.json` beside it. Resolve the branch's shared active pointer
with `active-path`, and activate a new run by compare-and-swap from the prior
generation while passing the kickoff-pinned registry revision; the resulting
active pointer is the run's immutable registry binding. Activation also binds
each run ID to exactly one branch before any branch-specific pointer can write
its canonical monitor ledger. Every `reserve` and
`reconcile` supplies that canonical active path, run ID, branch, and generation,
and derives the canonical monitor-state path from the run ID; a superseded run
blocks even when it presents the same expected head. Before assembly, push, or
comment, first reserve an event/action/expected-head in monitor state. An
assembly reservation also persists the exact integrated and discarded lane
identities, and reconciliation requires the landed observation to reproduce
that selection before the run transition is written. Never reserve or replay a
merge.
For comments, also reserve the trusted immutable actor ID, deterministic marker,
SHA-256 digest of the exact body, and kickoff-pinned registry revision; the
monitor must resolve actor trust from that immutable registry snapshot, never
from a value declared only by the run or caller. On re-arm, inspect every `reserved` action's exact external
postcondition (assembled canonical SHA, remote branch SHA, or marker-bearing
comment candidates with ID/actor/marker/body digest) and reconcile it: `landed`
adopts the lowest authenticated matching comment ID and advances the durable event
cursor, `absent` keeps the reservation for one safe re-execution, and
`indeterminate` blocks the run. Never advance the cursor before this
reconciliation. A crash is therefore re-armed, not read as human cancellation.

Every terminal event has an action: lane result → validate/assemble or block;
failed gate → dispatch the bounded remediation; ready draft → run integration;
external merge → release dependents and recompute the queue; ambiguous scope,
product, safety, or consent decision → stop for a human. Persist the event ID,
reservation, observed postcondition, and action in monitor state so a resumed
session can adopt a crash-after-write action instead of duplicating it.

Treat resolved `rounds.wall_clock_min` as a ceiling for the whole run, measured
from `run.started_at`, not as a fresh allowance for each stage or resumed
session. Read a fresh trusted clock immediately before every dispatch,
reservation, replay, external action, and merge-queue mutation. Once the
deadline is reached, record the capped transition and render its blocker before
stopping. The sole external action still authorized after expiry is to reserve,
publish, and reconcile that exact terminal blocker through the monitor; forbid
all dispatches, code pushes, ordinary comment writes, and merge-queue mutations.
A cached time check or a check performed only after the write cannot enforce
this ceiling.

Bound parallel implementers by `[breadth]` and strategy and heavy local stages
by host capacity. Maintain a merge queue from complete file lists, pairwise
overlap, dependencies, stage, and re-verification cost. Recommend
oldest-terminal/highest-cost first and disclose externalities. Product, scope,
consent, and safety decisions stop for a human; re-scoping requires two traces.
A human *task* is not such a decision: when a lane reports a step only a human
can do, queue it for its collector (`track-work` §5): an action for the
`(HUMAN):` collector of that issue's milestone, else epic, else repository;
a verification for the repository's standing `(QA):` issue — and keep
the lane moving unless the step is a genuine precondition, which needs its
own `human` issue blocking the lane's issue. A lane report is not
authorization for an issue write: present the whole batch — the collector
items, any precondition issues and their blocked-by edges, and each source
issue's `## Out of scope` follow-up line — for the operator's go-ahead, then
make those writes yourself as the run's only collector writer — a source
issue's edit only after its lane has reported back, so the lane's criterion
ticks and your follow-up line never race on one body. The run's handoff ends
with a human-work summary — every open `(HUMAN):` collector the run
appended to or whose scope covers the slate, the `(QA):` issue's items that
came from the slate, each with its unticked items, plus any `human`
precondition issues — so the maintainer circles back once, not once per
lane.
