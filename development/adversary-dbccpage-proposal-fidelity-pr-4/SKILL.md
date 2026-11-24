---
name: adversary
description: "Repository Single Point of Entry (SPOE) for swarms (save for the paper swarm). Run the mandatory 22-role Panel through one tested coordinator; every model contribution uses PFP. Use actual host tools, bounded repair and source-bound learning."
operad_source_colours: ["State", "Proof", "Paper", "Code", "Contract"]
operad_target_colour: "Receipt"
operad_arity: 5
operad_residual: "unknown"
families: [governance, cognitive-architecture, rop-monad, dialectic, adversary, mimesis, logos, dianoia, creativity, oecog, theoria, curious]
---

# Adversary: Make the Work Real (Swarm Single Point of Entry)

**Status:** `ADMITTED`\
**AuthorityEffect:** `None`.

Adversary handles software, research, cognitive work and teamwork. The paper
review entrypoint (`core-paper-review-swarm` / `rip-papers`) keeps its exception.

Use `/adversary <request>` in the current host. All 22 Panel operators contribute
with available tools. A persona selects a perspective; actual worker identity
and executed checks establish participation and gate outcomes.

Every run uses the versioned full [Panel](../../../adversary/roles/adversary_panel.yaml)
and [scenes](../../../adversary/roles/scenes.yaml).
Report missing roles honestly. Briefs and optional tools vary within this workflow.

## Recall and Learn on Every Run

Before starting work and before every worker spawn, read
[/auto-learn](../auto-learn/SKILL.md), find relevant existing lessons and include
their paths and limits in the worker brief. The actual worker reads them before
acting; shared context is enough, with no new startup framework.

After every outer run, including partial or failed work, invoke
[/auto-oe-autop](../auto-oe-autop/SKILL.md) and `auto-learn` once: deduplicate
concrete lessons, apply useful HIGH-confidence fixes, recheck the original need,
mirror selected changes and carry unresolved work into the next brief.
Inner helpers return findings to this finish; learning/recheck never recurse.

The shared v4 backend retains native checks and its procedure. Routine learning adds
no separate intake, `learning.json` or novella. Preserve historical evidence
and applicable custody. The nine-stage maintenance runner is explicit.

## Default: Drive the Shared Backend in the Host

For substantive work, `/adversary` and Python use the same coordinator in
`adversary.use_cases.teamwork`. The skill supplies the current IDE
session's tools and judgment; it does not reimplement the stage sequence.

1. Write the brief first ([brief guide](../../../adversary/documentation/shared_teamwork.md#writing-the-brief-carried-over-from-teamwork-preview)):
   what, not how; every `--acceptance` checked; ask only on consequential ambiguity;
   say the expected outcome. Start with `python -m adversary.entrypoints.cli
   teamwork start --objective "<request>" [--deliverable/--constraint/--acceptance]
   --state <working-state.json> --checker-id <original-checker-version>
   --checker-source <checker.py> --check-command <actual independent check argv...>`.
   Check command last; new state path per task; record an unavailable optional
   tool with `teamwork tool-unavailable`. Declare task-applicable gates before work
   with `--native-gate-scope`; use the software profile in the gate reference.
   Required missing evidence still HOLDs. Run Syntax Prefilter with `teamwork check` and the
   returned `teamwork native-gates --state <working-state.json>` (no model prompt).
   Read `pfp_turn.system`, `pfp_turn.user` and its reply schema before each
   model-authored intake, build, review, repair or learning turn. PFP owns
   preparation and checking; ordinary roles need a minimal profile, not the
   mathematical campaign's stages or decoding requirements.
2. Perform the returned `next_action` (objective, instructions, candidate, artifact
   hashes, findings) with actual host tools. Read relevant skills; delegate real workers when useful; inherit the session
   model. If delegation is unavailable, apply the perspective in this session
   and label it honestly. Each worker receives the exact prepared PFP system,
   user and response schema and returns the actual bound reply bytes. Host tool
   observations travel separately. Do not invent workers or tool execution, or
   translate unbound prose into a claimed raw reply.
   For edits, keep a short checklist of the original public API and invariants
   in every worker brief. Repair from the relevant original source, not just the
   latest failing excerpt. Review the complete baseline-to-candidate diff;
   narrow green checks can miss removed methods, mutability or weakened types.
   When stages need explicit working notes, use the optional
   [prompt/scratchpad template](../adversary-digests/references/review_to_structure.md#optional-staged-prompt-and-scratchpad).
   Keep candidate content intact and carry only relevant corrections forward.
3. Save the actual model reply instance matching `pfp_turn.response_schema`,
   including its supplied task/attempt/input bindings, and submit `python -m
   adversary.entrypoints.cli teamwork submit --state <working-state.json>
   --raw-reply <reply.json>`. Build/repair answers are text; review answers contain
   `summary` and `findings`; learning adds `lessons`. Shape-valid prose remains
   UNVERIFIED. Preserve raw bytes on refusal. `--result` alone is retired and
   refused. Use `--host-result` alongside the raw reply for actual artifact
   readback; use `check`, `native-gates`, `recheck`, `digest`, `ddc-store` and `ddc-complete`
   for actual host operations. Acceptance is selected by the host before work;
   a missing binding refuses before any model contribution.
   Python cannot attest the IDE's hidden transport or observe its billing;
   the supported guarantee is this shared prepare/submit boundary.
4. Perform each returned action under a closed 22-role roster under a declared schedule; every declared seat either contributes or is reported as skipped by the schedule with its reason: intake, Jeremy's build, reviewers ending
   with Adversary, then Scar Chronicler's learning. `--schedule` (or `--preset`) may skip or blind seats
   (`panel_schedules.yaml`, `panel_presets.yaml`); the coordinator decides and reports each skip.
   Preserve dissent, the objective, permissions and prior replies. Do not
   independently restart, narrow the roster or switch executors.
5. Follow `semantic_digestion_v2`: `ddc-store` seals/readbacks actual intake;
   Scar Chronicler learns with exact `learning_reply_binding`, then original-task recheck
   and digestion precede Defect Hunter's review of that actual learning/digestion.
   Findings require new DDC and an appended correction, reviewed before another
   original recheck/digestion; preserve earlier replies. An unavailable paid review
   stays `REVIEW_PENDING`, with no further dispatch or fabricated closure.
   Follow returned actions through `ddc-complete`; scoped `/auto-oe-autop` runs
   once, including partial work. C/R/I/T storage grants no mathematical authority.
   Fresh native intergates use `pfp-intergates-source-v1`; old captures keep their
   legacy profile. Optional `teamwork persist --state <working-state.json>` adds
   a durable package; report persistence failure separately from task completion.

Separate host artifact observation (replace values with actual readback):

```json
{"action_id":"<returned id>","worker":"actual IDE host","summary":"Read the changed file","artifacts":{"path/to/file":"<actual SHA-256>"}}
```

Working state is an editable host exchange, not authentication or a checker
certificate. Do not edit it to skip an action. A bare shell's `teamwork run
--executor ide` returns `IDE_SESSION_REQUIRED` with a pending action; it cannot
acquire this IDE conversation or silently use OpenRouter.

Ordinary IDE work requires no API key or separate API calls. Use the current
host's supported agent tools and existing subscription sign-in.
Do not silently switch to API authentication or paid overflow. Roles may use
different models only when the host supports that selection and the user has
authorized it; otherwise inherit the session model and report the actual worker.
Native usage consumes host allowances; unknown dollar cost is not zero cost.
Use `teamwork run --executor openrouter|anthropic` with an explicit model,
new output/state paths and financial policy. The provider proposes text; Python
writes only the designated file. It does not execute model-supplied shell commands.
See the [shared workflow guide](../../../adversary/documentation/shared_teamwork.md)
for runnable examples. Routed runs need durable accounting and a run-wide
ceiling (OpenRouter $0.05, Anthropic $4 rated); unknown cost stops dispatch.
Estimated admission is not a vendor-enforced maximum bill. IDE billing is
unavailable; do not describe it as measured zero cost.
For arbitrary old repository files or intelligence, use
[/adversary-digests](../adversary-digests/SKILL.md): read the actual sources, apply
useful learning to existing owners and carry unresolved work into the next brief.
The same coordinator and optional typed `intake`/`learn`/`start --brief` path remain
available when explicit source-bound interchange is useful. Routine learning
requires no new packet; detector activation retains its existing admission rules.
## Original Challenge Work Through PFP

For an original demo problem, use the shared `challenge` adapter instead of
inventing an answer comparator. `challenge start --challenge C001 --ordinal 0
--state <new.json>` starts the full Panel and runs actual Syntax Prefilter. Follow each
returned PFP role via `challenge submit --state <state.json> --raw-reply <reply.json>`.
Bare Metal Anchor/repair returns a JSON string containing the original witness object;
the original independent judge runs after all fifteen reviews. `challenge run`
selects explicit OpenRouter; `challenge replay` makes zero sends. All commands
follow `python -m adversary.entrypoints.cli`.

Read the returned public input and schema as supplied. C001 exposes the original
distractor prose, while the parsed graph, spans and oracle labels stay with the
host. Build a concrete witness; review roles return their typed findings. Preserve
original scientific requirements as open until executed; finite certificate
acceptance does not establish attention steering, paired hidden-case performance
or a speed advantage. Read the [challenge runbook](../../../education/documentation/004_oepfp/docs/18_original_challenge_play.md)
for supported cases, financial bounds, commands and observed limits.

For C006 use `mechanism start/run/submit/replay` with an explicit board. An
admitted move is not a completed session: only a checked zero-defect VERIFY
finishes. Closing a fundamental cycle does not prove minimum L1 descent; require
the weighted native certificate and independent exact check. Never copy native
repair values into participant briefs. See the runbook for full-session commands.

For Pilot 035 use `pilot035 start/next/submit/replay` and the
[immune-fence runbook](../../../adversary/documentation/pilot035_immune_fence.md).
It requires scoped admission, actual IDE replies and the full Panel. The pinned
checker covers only the explicit Tao table; no paid fallback is available.
Resume with `pilot035 resume --state <parent.json> --output <child.json> --reason "<why>"`.
This retains the checker, ancestry and spend; generic `teamwork resume` cannot redirect it.

## Digest Run Intelligence and Its Descendants

For an applied-learning task, add `--source <sealed-run-or-digestion.json>`,
`--initial-task-id <original-task>` and `--checker-id <version>` to `teamwork
start`, followed last by `--check-command <actual acceptance command...>`.
Use the pending shared actions: apply real structure with current artifact
hashes, review it, then `teamwork recheck --state <state>`. The host executes
that chosen command and preserves current-byte bindings and actual output.

Read the actual resulting digestion report with `teamwork digest --state
<state> --source <new-report.json>`. Findings return to repair and the same
original-task check, including affected descendants. Preserve all ancestor
reports; do not overwrite them. An unavailable check, coverage gap or exhausted
repair allowance stays open. An unused candidate or archive move is not closure.
Follow the [report context and Python examples](../../../adversary/documentation/shared_teamwork.md).
Continue a stopped IDE task with `teamwork resume --state <stopped.json>
--output <new-state.json> --reason "<what changed>"`. Keep the exact parent file.
Resume preserves every failure, the original task/mode/checker and spent work.
V3/v4 admits at most ten original-task evaluations across resumes;
failed or interrupted checks consume an episode. The original durable
`episode_binding` ledger cannot be replaced or reset. Reviews are not rounds.
Fresh v4 reserves storage, Scar Chronicler, digestion, native gates and final readback;
partial learning retains the candidate, findings and stop reason. Complete
that finish before resuming. Historical v1/v2 bytes retain their old meaning.
It grants nothing automatically: explicitly add only the needed allowance with
`--additional-repairs 1` or `--additional-actions 4` when exhausted. An unavailable
repair also spends an attempt. Source coverage gaps require new explicit intake
with the old evidence retained. Never reset a provider gateway or financial spend.

`next` reports stop reasons and remaining work. Repeated unchanged repair stops
as `NO_PROGRESS`; do not manufacture progress. Continued `persist` uses a new
immutable snapshot with the same logical run ID. Use `--snapshot-key <new-key>`
for another explicit snapshot; preserve all prior bundles.

Cleanup is optional: `teamwork cleanup --state <completed.json> --plan
<operator-plan.json> --receipt <new-receipt.json>`. Use the guide's small explicit
plan for named untracked copies under `_ic/adversary/working/<task>/` only.
Require exact retained bytes and pinned Git recovery, current original-task and
final-digestion readback, and the existing native lifecycle/retention decision.
An open finding, live reference, lease, hold, failed readback or grace refusal
retains the copy. Declare indirect dependencies explicitly. Keep before/after
receipts, original sources, outputs, parent states and historical evidence.
DISCHARGED here concerns only the clean disposable source; teamwork remains
`OPEN_RESIDUAL`. There is no sweep, new scheduler or remote fallback.
## Mandatory Panel, Task-Specific Contributions

The frozen order is Syntax Prefilter, Scope Guard, Context Transport, Punchlist, Gauge Breaker, Bare Metal Anchor,
Defect Hunter, Boundary Fuzzer, Overconfidence Probe, Anti Hype, Quarantine, Resilience, Custody,
Covert Verifier, Integrity Auditor, Hardware Constraint, Truth Repair, Primal Dual, Backdoor Auditor,
Manuscript Truth, Adversary and Scar Chronicler. Every role contributes its governed technical
perspective to the same original need. These examples do not narrow the roster.

`panel_coverage` reports required, observed, skipped and missing roles from
validated history. Full attendance and unanimous prose remain UNVERIFIED; only the
original task's independent checker can accept a candidate.

## Work Completion and Evidence Verdict Are Separate

| Field | Meaning |
| --- | --- |
| `work_status: completed` | Required workflow actions completed; report actual validation and remaining task obligations. |
| `work_status: partial` | Useful work is delivered and some requested work remains. |
| `work_status: blocked` | A concrete missing input, authorization or external condition prevents the remaining work. |
| `OPEN_RESIDUAL` | Default evidence verdict when there is no bound accepting checker receipt. It can accompany completed work. |
| `PASS_TO_MASTER` | An existing checker receipt accepts the exact candidate; a native bout also needs its native authorization guards. |
| `REFUSE` | A recorded typed refusal or rejected candidate, with the actual reason retained. |

`work_status` is workflow completion. It is not mathematical proof,
provider evidence, checker acceptance or authority. Record actual `verification`,
`artifacts` and `open_obligations` in the existing summary. A remaining conjecture
can stay open while its requested implementation or review is complete.

New runs automatically organize the seed once and observe Syntax Prefilter, final PFP prompts
and captured replies with the Rust density observer (default 128 dimensions).
Select `--density-dimension 28..1024` and `--forge-organization off` for explicit
comparisons. Preserve seed bytes, typed requirements, permissions and immune guidance.
Geometry is diagnostic: entropy/purity never admit a candidate or establish meaning.
See the [geometry runbook](../../../adversary/documentation/prompt_geometry.md).

Checkpoints write UNS `uns.md`, UTS `uts.jsonl` and the single DDA tape `ddc.jsonl`
beside state in `<state-stem>.reports/`. Terminal bundles under `_ic/adversary/` add
`summary.json`, `receipt.json` and a `mam/` story, with no separate `dda*` file. Retain state on
`REPORTING_FAILED`; retry `teamwork persist --state <state>`. Use actual dialogue, checks and outcomes; missing roles stay missing and IDE billing stays unobserved.
Historical `novella.md`/DDA bytes/readers and DDC semantics remain; replay creates no run. AutoP/learning runs once per outer run.

### Hermetic Evidence Invariant (No Evidence Borrowing)

Recheck the current task's exact candidate bytes. Foreign task receipts or old pass markers cannot grant `PASS_TO_MASTER`; borrowed task evidence is refused as `TASK_EVIDENCE_BORROWING_LEAK`.

### Strict Input Schema Enforcement

Workflow/step parsers enforce declared types. Refuse malformed scalars as `BAD_STEP`; never coerce them into nullary operations or silently drop mismatched list items.

## Signed Native Circuit

Native `run-live` mediates every model seat through PFP while preserving seven
acts, scenes, gates, signed admission and independent checks. Actual raw replies
bind task/attempt/candidate context; shape alone is `UNVERIFIED`. Existing
accounting reserves before sending, settles cost, retains spend and stops on
uncertainty. Duplicate Python seat executors remain retired. Use the current
build and fresh signed deployment in the [native guide](../../../adversary/documentation/live_cli.md).
This specialized suboperation runs inside the full Panel; it does not prove
22 independent workers. Ordinary IDE/OpenRouter work needs native DDC storage
but no signed deployment. Fixture/schema/finite checks retain their limits.

Checker-backed `PASS_TO_MASTER` remains evidence-bound. `persist-run` requires an
`ACCEPTED` receipt for it; a supplied receipt with `REFUSE` must state `REJECTED`.
Fixture bouts remain `FIXTURE_ONLY`; ablation runs never authorize. A reference
checked against its own checker is `REFERENCE_SELF_CONSISTENT` or
`REFERENCE_SELF_INCONSISTENT`, not an independently accepted answer.

## Reference Dispatch

| Task condition | Reference |
| --- | --- |
| Persisting a substantive host result or native bout | [Run output custody](references/run_output_custody.md) |
| Selecting scenes, character operators or a recovery route | [Master and Primal Dual scenes](references/roles_swarm_scenes.md) |
| Executing native primary, empirical or transition gates | [Panel gates and intergates](references/panel_gates_and_intergates.md) |
| A concrete approach has stalled and needs reframing | [Dialectics and gauge breaks](references/dialectics_and_gauge_break.md) |
| Auditing terminology, rhetoric or presentation claims | [Semiotic sign and BS detector](references/semiotic_sign_and_bs_detector.md) |
| Reviewing routing concentration or unresolved obligations | [Routing and obligation frontier](references/routing_monopoly_and_obligation_frontier.md) |
| Working on the specific 19L57G1 derivation or proof estate | [19L57G1 epistemic foundation](references/19l57g1_epistemic_foundation.md) |
| Inspecting carrier, observer and operator architecture | [Four-layer operator architecture](references/four_layer_operator_architecture.md) |
| Connecting the existing Blackrod or Panopticon interfaces | [Blackrod and Panopticon](references/blackrod_and_panopticon_interface.md) |

Mathematical invariants in specialist references apply to their stated domain;
they are not additional completion requirements for unrelated IDE tasks.

Keep this file within 300 lines and 20 KB, UTF-8 without BOM. Detailed domain
contracts stay in the existing references and executable implementations.
