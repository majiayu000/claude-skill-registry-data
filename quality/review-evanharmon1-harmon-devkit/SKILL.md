---
name: review
description: >-
  Drive one confidence stage at a time: dispatch challenger passes for
  challenge and reviewer passes for review, validate evidence, adjudicate,
  render durable records, compute the exit, and dispatch fresh implementers
  for confirmed fixes. Never bypass provenance, the round-push broker, or exit.
  Use when the Dev Loop enters either confidence stage. Invoke as /review.
---

# Review

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

`/review` owns both confidence stages, not the security or integration stages.
Its input names `challenge` or `review`, the base and head, policy, registry,
run directory, and the active run identity. The policy is a
`schema_version = 2` `.devflow.toml` resolved through
`dev-flow-support/assets/devflow-policy.mjs`; this skill carries no interpreter for the legacy
or v1 shape, and a reader refusal is a blocker carrying the reader's own
migration message, never grounds to hand-decode the file or guess a cap
(harmon-devkit#604). Create the record directory before
the first dispatch and retain `run.json`, `policy.json`, `passes/`,
`adjudications/`, and `verdict.json` there; `/integrate` consumes that exact
directory. Capture and refresh base and canonical head before every logical
round. A changed head invalidates an unadjudicated pass rather than letting it
describe a new tree.

When the run has a lane assembly, the first confidence pass after that
assembly must review the latest implement transition's exact
`assembly.canonical_head`. Compare it before dispatch and again on receipt; a
different head blocks until the feature owner records the actual assembly
rather than certifying an unauthenticated tree.

## Which path produces the record

**Both paths produce it, and it is the same record.** In an orchestrated run
this skill writes it from the role agents' passes (or an envelope-mode
runner's). An ordinary interactive session with no validated brief envelope
runs the inline `task challenge` / `task review` procedure instead, and writes
the record itself as `/implement` § 6a describes: `run-record.mjs solo-init`
reserves a single-lane run, `receipt` and `adjudicate` publish each round's
pass and adjudication, `ledger` materializes the per-stage
`history.<stage>.json` and the shared `heads.json` the verification call reads, `transition` advances the
stage, and this skill's
`assets/post-evidence.sh` posts and registers the round's evidence marker.
Either way it is one `run.json` with `passes/`, `adjudications/` and trusted
evidence markers, validated by the same validator; nothing downstream branches
on which path wrote it. A session that never ran a confidence stage — or could
not record one (the fork topology above, or a `solo-init` refusal) — has no
record, and neither stage treats that as an error.

## Stage invariants

Every confidence stage carries the mandatory round-two scaffolding checkpoint
as an invariant, independent of its current control-flow wording. Before any
round-two adjudication can cause another pass or remediation dispatch, classify
each finding whose subject exists only because an earlier round of that same
stage added it, and record exactly one disposition: delete the scaffolding,
restructure it to an invariant, split the mechanism out, or keep it as
genuinely in scope with the reason.
A rewrite of `continue`, remediation, or exit handling must preserve
this checkpoint; no path may harden round-one scaffolding first and classify it
later.

**Splitting the mechanism out** is the disposition for scaffolding that is
still wanted — deletion drops work that is genuinely needed, and restructuring
to an invariant is unavailable because the subject is code rather than accreted
procedure-prose. It applies when successive rounds' gating findings concentrate
in one mechanism, most sharply one an earlier round of this same stage added;
`verdict.split_candidate` from `dev-flow-support/assets/dev-flow-exit.sh` is the computed
evidence for that judgement and names the mechanism, the rounds that introduced
it, and the findings living in it. It describes a **completed**
round — it needs adjudicated priorities, so a candidate exists only once its
round has been adjudicated — and it is evidence for your judgement, not a
prescription about where the decision goes. Below the cap that is a
disposition on the round in hand; at the cap there is no further round to
spend and the split is part of the escalation.
Recording it is four things, all of them or it is not a split: the mechanism
leaves the change; it is filed as its own issue **on the current milestone**,
carrying the design constraints the rounds established, by this session at the
moment it splits — never left to memory; the finding the mechanism was
addressing is restored as a filed follow-up so the defect it existed for is not
silently dropped; and one deletion round confirms the removal, after which the
stage exits through its ordinary conditions.

**Where the deletion round comes from depends on when the split is decided.**
With cap headroom left it is an ordinary next round. Decided on the **final
permitted round** there is none to spend: the exit computation rejects every
round above the resolved cap, and no intervention makes one legal. There the
stage ends `capped`, and confirming the removal is part of what the operator's
escalation decides — never something the stage grants itself. That is what "a
split changes no cap" means: it buys no round, it only changes what the
escalation is about. Write it as
`disposition: split` with a `reference` naming the filed issue — the
adjudication schema rejects a split that names none — and append the run-level
half to `run.json.splits`. Then validate the pair here, before the stage
stops: `dev-flow-support/assets/validate-result-schemas.mjs run <run.json> --adjudication
<each round document>`, treating a failure as a blocker. A split decided on
the final permitted round ends the stage `capped`, which never reaches
integration, so this stage is the only place that check will run. Those records prove the split was decided and the
issue filed, which is what they can decide; that the mechanism actually left
the tree is the deletion round's own review, not a claim the record checks. A
split buys no exception to the exit condition.

## Entry gate

The input must also name the canonical `owner/repo` that will receive the PR.
Before creating the record directory, dispatching a role, or writing external
state, resolve `origin` and require it to identify that same repository:

```sh
origin_url="$(git remote get-url origin)" || exit 2
origin_repo="$(gh repo view "$origin_url" --json nameWithOwner -q .nameWithOwner)" || exit 2
[ "$origin_repo" = "$target_repo" ] || exit 2
```

Treat an absent remote, a failed identity lookup, or a mismatch as this skill
being unavailable, not as permission to guess. Return control without creating
review state so `/implement` can use its inline confidence-stage procedure for
the conventional fork topology where `origin` is the writable fork and the PR
targets upstream.

## Dispatch and receipt

When the resolved cap is `0` for the requested stage, dispatch no finder,
create no pass, round, or adjudication, and do not invoke a model. Run the exit
computation immediately and advance only when its disabled-stage verdict says
`action: advance`; any other result is a blocker. A zero cap disables the
stage—it is not permission to manufacture a clean round.

Runtime isolation is optional; its absence alone is not a dispatch blocker.
The challenger or reviewer still stays within its declared role scope and gets
the captured base/head plus access to the source and diff it must review. For a
committed round, require every source and diff read to resolve from those
captured Git revisions, never mutable worktree bytes. For an orchestrated
`codex-cli` pass, give `scripts/codex-review.sh` the resolved values as leading
`--model <model> --reasoning <level>` arguments; in envelope mode (below),
give every other local-CLI finder (`scripts/finder-review.sh`) its resolved
model as `--model <model>`, which the runner pins into the vendor invocation
and records in the envelope.
Pass each dispatch the
remaining whole-run wall-clock budget and bound the caller's supervision and
wait by that deadline. On expiry, stop waiting, follow the orchestrator's
capped-run handling, and reject any late result; this grants no authority to
terminate a process. Give every pass the run identity, policy, and finder slot.
Include the complete
validated finding records from every earlier round of this same stage, not
merely their IDs, so the role can compare evidence before asserting
`repeat-of` or `supersedes`; an empty list is explicit in round 1. A runner in
envelope mode (below) takes no such input yet — carrying them across rounds is
harmon-devkit#955 — so its findings assert `original`/`new` and the
verification pass below is what corrects provenance and fingerprints.

For `challenge`, dispatch every primary finder in `[stage.challenge].finders`
to the `challenger` role. For `review`, do the same for
`[stage.review].finders` using the `reviewer` role. Retry an unavailable primary
once as that same primary; only after that retry fails may the ordered
`finder_fallbacks` chain be consumed. Do not silently reduce coverage.

**Every configured finder runs in the same logical round, and the round is
what the cap counts.** Each finder fills one slot and returns one pass, and
each accepted pass is persisted as its own receipt in `passes/` — a round with
three finders writes three receipts and spends **one** unit of the stage's
rounds cap, never three. The round is complete only when every configured slot
has produced exactly one pass at the same `reviewed_head`; an incomplete one is
`capped`/`finder_unavailable` and has no adjudication target. Which product
produced a pass is carried only in its `finder`/`slot` fields and in its
finding ids (`<stage>-r<round>-<finder>-<n>`); adjudication, the exit
computation and the renderer read `findings[]` and never branch on it, so a
finder's own output shape and severity vocabulary are decoded once, against
that finder's `agent-registry.json` `raw_shape` and `severity_map`, before it
reaches any of them. **Where that decoding happens is what `raw_shape`
selects.** A `github-review-json` finder — the PR-side cloud reviews — has a
machine-readable payload, so `assets/normalize-finder-findings.mjs` decodes it
mechanically and fails closed on anything it cannot decode. A `labelled-text`
finder — every local CLI pass, Codex's included — has only free text, so that
program refuses it by design: its output is the dispatched
`challenger`/`reviewer` role's evidence source, and the role reads the badges
against that same `severity_map` and returns the decoded findings inside its
own `result.challenger`/`result.reviewer` envelope (below). Routing a
`labelled-text` pass into the normalizer is a defect rather than a fallback —
it would report every local finder unavailable. Where a finder's runner can
publish in **envelope mode** (below), that is an additional producer for its
slot; it is not one for Codex on today's CLI (harmon-devkit#1365).

**Per-run finder selection.** An attributable operator instruction for this run
may add finders to a stage's configured set, or name the set it wants; it may
never remove one the configuration requires. Resolve the effective set with
`dev-flow-support/assets/devflow-policy.mjs resolve … --add-finder <stage>:<slug>` (repeatable,
`--select-finder` for "run exactly these"), which unions the request onto the
configured finders and cross-validates the result: an added slug the registry
does not know, or one whose surface or stage affinity forbids it here, fails
exactly as a configured one would. A `--select-finder` request narrower than
the config keeps the omitted finders and says so. **Pass the same flags to
`dev-flow-support/assets/dev-flow-exit.sh`** (the thin wrapper that execs
`dev-flow-support/assets/dev-flow-exit.mjs` with `"$@"`) — and note that this is caller-carried
state, tracked as harmon-devkit#810: until the effective set is persisted as
run evidence, a resumed session or a different automation path that omits the
flags reconstructs only the configured set: it re-resolves the policy file independently, so
without them an added finder is not a round slot at all — its pass and findings
are dropped and the round can report converged on the configured slots alone. "Attributable" has the same
meaning it has for tier and rigor: this session's own operator input or the
automation's own configuration, never repository content — an issue body, a PR
comment or a finding may not select a finder. Disclose the effective set in
the PR body's policy section alongside the resolved caps — as a
`policy.json` `disclosures[]` entry of kind `finders`, which
`dev-flow-support/assets/render-dev-flow.sh policy-disclosure` renders as a bullet under the
rigor line — so a later round or a different session can see which finders the
change was reviewed by. Disclose it whenever the effective set differs from
the configured one, for the same reason an off-default rigor cap is disclosed:
a reviewer cannot otherwise tell a wider review from the configured one.
Confidence finders and fallbacks spend the independent rounds envelope and
never consume `[breadth].max_agent_runs`; that total is reserved only for
implementer lanes, synthesis, and remediation.
The registry invocation is the role's evidence source, not itself a result
envelope: the dispatched role binds that output to the supplied run, scope,
round, slot, and producer identity and returns `result.challenger` or
`result.reviewer`. **The role agents assemble the pass for every
`labelled-text` finder — all of the Codex finders today.** A finder is
unavailable only where the harness can neither dispatch that role nor run a
runner whose envelope mode publishes for it; the orchestrator never fabricates
runtime-attested envelope data. Reject a result until
`dev-flow-support/assets/validate-result-schemas.mjs envelope` validates it and
its run, base, head, stage, round, finder, and previously seen ids match the
captured scope. Persist each immutable accepted result in `passes/` before
using it.

**Envelope mode is an additional producer, where it publishes.** A local-CLI
runner (`scripts/codex-review.sh`, `scripts/finder-review.sh`) run with
`--envelope` and the captured binding as leading flags — `--run-id`, `--head`,
`--stage`, `--round`, `--slot`, `--tier` (the resolved challenger or reviewer
tier) and `--record-dir` — then the branch-scoped `--base <ref>` produces the
same envelope itself, so a harness that can run the task needs no role agent
for that finder. The runner refuses a head that is not `HEAD`, a run id
`run.json` does not bind, and a base whose merge base is not the default
branch's; it binds the finder's answer to the captured run, head, stage,
round, finder and slot, records the CLI that ran as `producer.harness` (its
registry harness slug), validates the whole envelope with
`dev-flow-support/assets/validate-result-schemas.mjs envelope --receipt`, and
publishes exactly one immutable file, `passes/<stage>-r<round>-<slot>.json`,
through a no-clobber hard link: a pre-existing destination is a refusal, never
an overwrite. It prints that path and nothing else on stdout, and it **never
writes `run.json`**. **Codex envelope mode currently fails closed**:
`codex exec review` answers in prose and ignores the in-prompt schema, so it
publishes no pass, and Codex slots stay with the role agents until
harmon-devkit#1365 delivers a schema-enforcing, approval-never path.

**Append the pass receipt, then verify.** Receipt authority stays with the
caller that owns the run record — in an orchestrated run, the supervising
orchestrator, never the lane that ran the finder. Whichever producer
filled the slot — a role agent's result persisted in `passes/`, or a runner's
published file — re-validate it with the same `envelope --receipt` call
against the captured run, then append
`{"kind": "pass", "file": "<stage>-r<round>-<slot>"}` (the filename without
`.json`) to `run.json`'s `receipts` under the shared mutex and validated-write
path below, and only then enter verification below. A pass you have not receipted is an **orphan**: it is never evidence, the exit
computation rejects it, and its finding ids reserve nothing. A runner in
envelope mode that exited non-zero published nothing under a `.json` name. A
retry refused because its destination already exists means an earlier attempt — typically
one you stopped waiting on — published after all; never delete or overwrite
that file to make room. Validate it and receipt it as this slot's pass if it
binds the captured scope, or record the slot as failed; either way the decision
and the receipt are yours, not the runner's. A finder failure is retried by
its configured fallback and the substitution is recorded; exhausted coverage
is a blocker, never a smaller round disguised as complete.

## Verify, adjudicate, publish, exit

Before adjudication, run `dev-flow-support/assets/dev-flow-exit.sh --run <record> --stage
<stage> --policy <policy> --current-head <head> --repo-root <trusted-repo>
--history <record>/history.<stage>.json --heads <record>/heads.json --verification-only
--json`, capturing both its status and JSON projection. Materialize the trusted history and head map from the feature-owner's
verified branch state before dispatch; never let a finder supply them. The
change ledger is per stage — `<record>/history.<stage>.json` for the stage
being verified, never a shared `history.json`, because its entries carry only
round and path — and the head map `<record>/heads.json` is shared by both
stages (`run-record.mjs ledger --stage <stage>` writes both). Its
provenance and fingerprint corrections are preconditions, not an advisory
reviewer assertion. A recognized terminal nonzero status with a valid blocker
projection is handled as that blocker. Any other command failure, missing or
malformed projection, or indeterminate verification result authorizes no
adjudication and no round-evidence publication: persist the diagnostic, render
and reserve-first publish a terminal blocker instead, then stop. If a valid
projection reports `action: dispatch` because no
complete round for the refreshed canonical head survived, invalidate the stale
pass and dispatch the returned `next_round`; never adjudicate it. Any
`action: escalate` projection is terminal: persist it as `verdict.json`, render
the blocker, and stop. For an incomplete logical round (`finder_unavailable`
or `breadth_exhausted`), that blocker carries the accepted partial finding IDs;
the round has no adjudication target and must never reach the second exit call.
Only an `action: adjudicate` projection authorizes the orchestrator
to correct the finding facts and write one schema-valid
`adjudications/<stage>-r<N>.json`, containing the schema-supported priority,
disposition, classification, reason, and evidence for every finding, validated
against every accepted pass. Cite any verified provenance/fingerprint
correction in `evidence`; keep the machine values in the verification/exit
projection rather than adding fields the adjudication schema rejects. Only
after that write, run the exit command again with the same trusted repository
history and head map, persist its returned JSON as `verdict.json`, and act on
that second outcome.

Every `run.json` replacement, including pass receipts, evidence registrations
and stage transitions, must perform its read-modify-write inside
`run-record.mjs`'s `withMutex(runPath, ...)` (`run.json.wlock`) and publish
through `writeValidated('run', runPath, document)`. Read and validate the
existing record with `validateFile` while holding that mutex. Never replace
it from an unlocked read or a separate hand-written rename recipe.
The shared validated writer owns candidate validation, atomic rename and
canonical readback with the record's receipts and current local adjudications.
The following validation obligations are implemented by that shared writer:
Before replacing `run.json`, write the complete candidate beside it through
`writeValidated`, whose internal validation invokes
`dev-flow-support/assets/validate-result-schemas.mjs run <candidate> --receipts <candidate>`
with the current local adjudication documents.
Rename the candidate over `run.json` only through the shared writer,
after that validation passes. Its canonical readback invokes
`dev-flow-support/assets/validate-result-schemas.mjs run <run.json> --receipts <run.json>`
with the current adjudication documents before the locked operation returns.
`--receipts <same-record>` binds the stage named by every supplied
adjudication document to a transition receipt already present in that
record, enforcing the binding here at write time rather than only later
by the exit engine. Either validation failure fails the round and is a
terminal blocker; never publish an invalid candidate or defer validation
until publication or promotion.
Operational `run.json` records validate under the schema with their trusted
`receipts` sequence intact.

After each adjudication, keep the immutable source envelopes locally, but build
the fenced JSON public comment only from a verification-bound projection. Join
the validated source facts to `verdict.json.verified_findings` by finding ID and
publish only the verified or corrected provenance and fingerprint values,
never the producer's superseded assertions. A missing, unverified, duplicate,
or mismatched projection is a blocker, not permission to fall back to raw
envelopes. Combine the verified projection, the round's adjudication JSON and
its exit projection in ONE fenced JSON object, never separate JSON fences.
As a caller contract, its `passes` array contains envelopes with
verified/corrected `payload.findings`. Then append the human table from
`dev-flow-support/assets/render-dev-flow.sh round-table --record <record> --stage <stage>
--round <N>`.

Scan and redact the complete verification-bound projection first. If the comment
would exceed the 60,000-byte single-comment budget, split the sanitized projection
deterministically into an ordered sequence, reserving room in every segment for
its canonical run/stage/round/sequence marker. Splitting is a projection-layer
operation and must finish before reserving any comment. Append each unique
sequence marker, scan the exact segment again, compute its digest, then reserve,
post, and reconcile segments strictly in sequence; each reservation binds the
active run generation, head, role, finder, actor ID, registry revision, marker,
and exact segment digest. Never reserve an oversized unsplit body: split any
body that would exceed the 60,000-byte single-comment budget. On re-arm,
fetch the complete bounded candidate set for that segment and pass it to
`reconcile`; the monitor validates the candidates' run, head, role, finder,
actor, marker, and digest bindings, hashes their bodies, and adopts the lowest
authenticated match. Post once only after `reconcile` proves the candidate set
has no authenticated match and returns `retry`; `block` is terminal.

For a round that fits one comment (sequence 1, within the 60,000-byte budget), start its first line with the JSON marker `<!-- dev-flow-v2-evidence: {"run_id":"<run_id>","stage":"<stage>","round":<n>,"sequence":1,"destination":"issue"} -->`; publish it through `assets/post-evidence.sh`.
For a round exceeding the 60,000-byte single-comment budget, follow the split
procedure above by hand; the helper posts single comments only.
The helper requires a canonical `run-<issue>-<name>` identity and refuses
`--issue` unless it matches that run's issue number.
The marker has exactly five fields: the run ID, a run-stage enum value, a
positive round, sequence 1, and destination `issue`. The helper handles one
round comment within a 60,000-byte budget; oversized or split projections are
refused, never posted partially. The general marker grammar (including PR
rollups with `round:null`) remains in `ai/schemas/README.md`.

Write the marker object alone to `marker.json`, and the sanitized Markdown
summary plus exactly one fenced JSON verification-bound projection to
`round.md`, both in your own scratch directory. That projection must name
`run_id`, `stage`, `round`, and `reviewed_head` matching the captured scope,
a `passes` array with `payload.findings` arrays (the caller's projection
contract).
The helper scans the exact final comment, including its canonical marker line, with `gitleaks stdin --no-banner --redact` and the repository's `.gitleaks.toml` when present, refusing detections, scanner failures or a missing scanner before any reservation or POST; projection adjudication remains caller-owned.

```sh
assets/post-evidence.sh --repo <owner/repo> --repo-root <checkout> \
  --run <record>/run.json --branch <branch> --generation <generation> \
  --active-state <active-state> --head <reviewed-head> --actor-id <actor-id> \
  --role <challenger|reviewer> --finder <finder> --issue <issue-number> \
  --marker-file <scratch>/marker.json --body-file <scratch>/round.md \
  --scratch-dir <scratch>
```

This is an orchestrator-owned publication helper, never a role-agent write.
It requires Python 3's POSIX `fcntl` standard library and holds an exclusive
per-run `post-evidence.lock` (Linux/macOS, no separate lock utility)
across reserve, reconcile, POST and registration. A second caller waits at
most 30 seconds or refuses; it cannot post concurrently. Monitor re-arm is
restricted to the holder of that inherited lock descriptor; ordinary callers
retain the duplicate-event refusal.
It validates the marker and run record before reserving, reads a complete
bounded candidate set (at most ten 100-comment pages; a full final page
blocks), and posts only on monitor `retry`. It adopts the monitor's lowest
authenticated match and revalidates the readback on every re-arm. A failed
or ambiguous post is resumed with the same destination and scope, never by a
direct comment write. The helper binds the destination repository to origin
and the issue to the run identity.
After a successful reservation, the exact comment bytes persist atomically
beside it as `<event>.body.md`. That copy is authoritative only while the
event reservation exists; an orphan copy is replaced. On re-arm omit `--body-file` to reuse that copy, or supply the identical body. A changed
caller body or destination refuses. Its stdout is the adopted comment ID. For registration it
hashes the exact posted whole-comment body, matching the harvester's current
marker authentication, and appends `evidence_registrations` with its canonical chain digest.
Registration takes `run-record.mjs`'s shared `run.json.wlock` mutex and uses
its `writeValidated` candidate/validation/rename/readback path. This
registration is serialized with other writers using that same mutex.
Validation binds receipts and all local adjudications. Exact
existing ID/marker/actor/payload matches are adopted without appending;
conflicts block and a login rename never changes the immutable chain.

After adoption, append the canonical comment ID, immutable actor ID, display
login, `sha256:` body digest, and marker fields to
`run.json.evidence_comments` only when it is absent, reading and comparing
under that shared mutex and publishing through its validated writer. On
re-arm, first search by
both comment ID and canonical marker: when ID, immutable actor ID, digest, and
every marker field match exactly, adopt the existing entry without appending;
display login is non-authoritative metadata and never participates in evidence
identity or tamper comparison. When an ID or marker matches with conflicting
authenticated content, block. Validate the run record,
then reserve and apply an update to its issue comment through the same monitor.
A crash between evidence creation and run-record publication therefore resumes
from the adopted monitor postcondition and cannot orphan an unindexed comment or
duplicate its index entry. Before a draft exists, the issue comment is the
durable projection; terminal blockers are rendered with `blocker-comment` and
use the same reserve-first path. At draft creation, use
`dev-flow-support/assets/render-dev-flow.sh publish` for the PR-body projection without deleting
the local record.

Act only on the second returned outcome. `continue` dispatches the next pass
when no confirmed remediation exists (including an empty or entirely
declined/deferred round); otherwise it dispatches a fresh bounded implementer,
commits the one fix round, and pushes only through `assets/round-push.sh` by
path. Immediately before that remediation dispatch, the feature owner must
reserve its deterministic dispatch event through `reserve-agent-run` against
the same run-pinned `[breadth].max_agent_runs`; an exact re-arm adopts the
reservation, while exhaustion records `breadth_exhausted`, renders the blocker,
and stops before invoking the implementer. The stage-invariant round-two
checkpoint above applies before this dispatch and before a no-remediation next
pass alike.
`diverging` permits only deletion, restructuring, or splitting out of
round-created scaffolding; `capped` with P0/P1 records an intervention and
blocker, then stops before a PR. What a blocked stage's report offers a maintainer,
and how the split option's evidence is corroborated before it is published, is
[#813](https://github.com/evanharmon1/harmon-devkit/issues/813). Do not
restate `verdict.split_candidate` into a report by hand in the meantime: it is
branch-controlled, and corroborating it against the record is exactly the work
that issue exists to do. A `converged` result advances by default, but an attributable
operator may override it upward to exactly one additional pass while the
resolved stage cap still has headroom. Before dispatch, append that operator's
reason and attribution to `run.json.interventions` as `kind: other`; refuse the
override when no round remains. Never override an exit downward or reinterpret
the script's outcome.

### Stage exit rules and sequencing

Stage exit is governed by `AGENTS.md` § "Loop cap and exit". A stage whose
resolved cap is **0 never opens**: zero rounds run, there is nothing of its
own to adjudicate, and none of the three exits below is what closed it — it was
never open, and every deterministic gate and adjudication obligation elsewhere
is unaffected. For a stage whose cap is 1 or more, the stage ends on an
adjudicated outcome, never on "findings fixed" alone. The three valid exit rules
are:

1. **Two consecutive clean rounds**: two CONSECUTIVE rounds each adjudicating to
   zero P0 and zero P1 findings (a round with a confirmed P0/P1 is not clean
   regardless of fixes; an all-P2 round counts as clean for this exit but is
   NOT an empty-round exit). The second consecutive clean round is itself the
   confirmation, so no further run is owed.
2. **An empty round**: a round with NO findings at all (any severity), once the
   stage has run at least the effective floor of `min(min_rounds, cap)` rounds
   (resolved from the review policy in `.devflow.toml`; default fallback 1).
3. **A capped final round**: a capped final round (including a cap of 1) that
   adjudicates to zero P0/P1 findings ends the stage by itself, because the
   confirmation run is forbidden by the cap. If P0/P1 findings persist at the cap,
   stop and escalate to the maintainer.

At stage exit, record the exit reason and qualifying round in the `run.json`
stage transition string, the stage ledger, and stage reports; round history is
preserved in the pass and adjudication receipts.

**Stage sequencing:**
Per `AGENTS.md` § "Who decides, and what is delegated", stage sequencing is
strict: **challenge then review**, counted and capped separately (`.devflow.toml`
sets distinct caps for each). Concurrent rounds are invalid for exit purposes
(findings are still adjudicated, but concurrent rounds cannot satisfy an exit
condition); review begins only after challenge has legitimately exited (or
where challenge's resolved cap is 0 and the stage never opened).

**Hand-off to integration and the CI readiness condition:**
When a terminal `review` exits and hands off to integration (via `security`
and draft PR publication), the draft-first invariant is unchanged: publish the
draft PR first, and the CI readiness condition from `AGENTS.md` § Readiness gate
is evaluated by the integration stage once the draft exists: every required check
CONCLUDED successfully (pending or an empty check list is indeterminate, never a pass).
A terminal and clean current-head Codex result is required (or where the
resolved integration cap is 0 — a cap of 0 leaves no cloud-review cycle to
trigger a fresh `@codex review` from, so this one condition drops out; every
other readiness condition still applies unchanged).

### Stage advance write

Without that recorded upward override, an `action: advance` result is the sole
authority to advance the run record. Take the shared `run.json.wlock` mutex
and read/validate `run.json` inside it. First recognize and
validate an exact already-applied current-to-next transition; adopt it and
complete the remaining readback, publication, and next-stage steps without
appending a second transition. Otherwise require the last transition to name
the current stage and have no `exit`; any other state blocks.
Close the current transition by setting its `exit` to
`"<rule>: <detail>"`, where the rule is the verdict outcome and therefore starts
with one of `continue`, `converged`, `diverging`, or `capped`; the detail names
the verdict's exit reason and qualifying round. Capture one UTC timestamp. In
the same complete candidate, append exactly
`{"stage":"<next>","entered_at":"<timestamp>"}` to `stage_transitions` and its
matching `{"kind":"transition","stage":"<next>","entered_at":"<same timestamp>"}`
receipt to `receipts`. Never
append `{from,to,at,reason}`: those are verdict concepts, not the run schema's
transition shape. Publish the close and append together through
`run-record.mjs`'s `writeValidated('run', runPath, document)` while still
holding the shared mutex. Its validated canonical readback must succeed
before publishing evidence or entering the next stage.

This advance recipe covers stages whose resolved cap is at least `1`. The next
stage is `review` after a terminal `challenge`; a terminal `review` enters
`security`. A cap-zero advance is outside this recipe and tracked in #957.
Deferred P2s remain recorded for integration.
