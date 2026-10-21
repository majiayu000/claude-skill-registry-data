---
name: verified-execution
description: "Use when the user requests verified delivery, an evidence-led execution loop, or durable goal tracking with measurable completion criteria and real usage evidence."
---

# Verified Execution

## Activation and Routing

The main agent executes goals, fixes code, tests, and drives observable QA.
This body owns the complete actor contract, including isolated/body-only use;
no sibling skill, project-doc tree, or evaluator bundle is required. Resolve
optional references from the real, symlink-resolved skill directory, not cwd.

Decide risk first: low-risk reversible work uses the proportionate one-line
ledger/CLI evidence exception below; user-facing, hard-to-reverse or multi-criterion
work uses the full loop. Keep real evidence, cleanup receipts and honest outcomes
in either mode. Measure cycle time/rework/coverage, not confidence in your own work.
For a cycle, follow the lifecycle lane and authenticated owner; otherwise skip
the cycle-only fences and use State and criteria → Per-Criterion Loop → Standalone Gate.

For repository-local symbol discovery, use CodeGraph first when `.codegraph/` exists; otherwise use local `rg` and direct reads only. Never use web search for local repository symbols. Run verification and inspection commands as separate calls; never chain them with `echo` or `printf` banner markers.

First-party hosts are exactly Codex, Claude Code, Omo native, omp, and opencode.

## IssueOps Benchmark Artifact Contract

When Verified Execution contributes to an IssueOps artifact or benchmark response, include a compact labeled evidence block. Scale the evidence weight to the risk, but keep the labels so the artifact proves the method was applied.

```text
Success criteria: <criterion ids and binary pass/fail definitions>
Evidence artifact: <path, transcript, stdout, screenshot, or parsed dump>
Cleanup receipt: <runtime/temp state removed and verified, or "none spawned">
Verification mode: <full loop or proportionate lightweight mode, with rationale>
Skipped checks: <checks skipped with explicit reason; "none" if all ran>
```

## Cycle Lane: Authority and Startup (Only When a Cycle Exists)

Render every acceptance criterion as a binary observation. Use the exact
13-field owner report below, including evidence paths, HEAD, changed files,
artifact URL, verification and the `issueops execution complete` receipt.

Before execution, verify that the plan states the current issue, exact lifecycle ID, branch, base SHA, canonical worktree, bounded scope, acceptance criteria, verification, completion, and cleanup boundary. Never link an unrelated plan as readiness evidence.

After the canonical worktree exists, the active generation holder owns plan and implementation edits there. The source checkout may observe the selected cycle but must not steer or mutate it.

Do not cite stale tools such as positional `state write <key> <content>` forms as executable commands. IssueOps v1 liveness is the persisted generation plus exact native process receipt; inspect it with `issueops execution status --id "$ISSUEOPS_ID" --json`.

For the selected execution, the source checkout is observation-only. From it, use only non-mutating reads such as `git status`, `git diff`, `git log`, `git show`, `git rev-parse`, `git ls-files`, and `rg`. Tests, builds, formatting, installation, generation, commits, and publication run only in the canonical worktree. CLI/MCP generation, actor, and cwd denials must never be bypassed. The owner uses the installed `issueops` command unless the plan shows `./bin/issueops` exists in the exact worktree.

For a report-only cycle, run only the verification commands declared in the plan. Do not invent API, provider-ref, or history probes; the bounded report is not authority to widen verification or inspect unrelated external state. If a declared command cannot run, record the exact failure instead of substituting a new probe.

The Verified Execution report path is a safe relative path from the canonical worktree. The report must exist inside that root as committed regular-file content; an absolute path, parent escape, or leaf symlink fails. The worktree must be clean before completion.

Execution shell red flags include the eval and source primitives, active command substitution, unquoted process substitution, zsh equals expansion (`=git` or `=(...)`), parameter/tilde expansion, and unquoted brace/glob pathname expansion. Use explicit canonical argv paths. Do not steer a launched native owner through raw terminal injection; lifecycle control uses the persisted execution status, replacement, reconciliation, release, and completion commands.

Before draft publication, query `git rev-parse HEAD` in the canonical worktree as a standalone observation. Use the exact active generation, explicit head/base branches, labels, assignee, native actor, and cwd for `issueops remote create-pr`. Do not use implicit branch defaults, force/delete push, merge, or close.

For supervised evidence, self-verify requires binary/source contract parity. If an evidence worker is intentionally on a base checkout while the installed binary is feature HEAD, record a response-contract mismatch as a version-skew observation, do not mutate the base, and leave the final self-verify score to the coordinator running matching feature HEAD. The opt-in LLM path currently renders a read-only prompt only. No Z.AI request is sent, so `gate` is expected to remain non-passing without an ingested verdict. When the coordinator environment intentionally exports `ISSUEOPS_SELF_VERIFY_LLM_EVAL=gate`, use explicit `--llm-eval=false` for the required deterministic completion sequence, record the override, and restart from its first gate after an interrupted or prompt-only run.

Hooks are context-only: SessionStart emits the static project-doc catalog, and `post-compact` remains available for Omo and diagnostics. Hooks do not enforce tool mutations or own execution authority; CLI/MCP commands enforce their own generation, native actor, and canonical cwd fences. For focused hook coverage, use `./cmd/issueops/hookcli` and its retained `./cmd/issueops/hookcli/hookinput` tests; `./internal/core/hookinput` does not exist.

A targeted Go test is GREEN only when the intended test names actually ran. `[no tests to run]` is not GREEN; update stale regex names and rerun with `-v`, requiring the named `=== RUN` lines and PASS:

```bash
go test -v ./cmd/issueops/hookcli -run '^TestRetiredHookSubcommandsAreRejected$' -count=1
```

When a zsh verification wrapper captures an exit code, never assign to `status`: zsh reserves `status` as a read-only parameter. Use `rc` or `exit_code`, and report the test command verdict separately from wrapper bookkeeping errors.

Shell arguments containing Markdown backticks must be single-quoted or passed as direct argv; never place backticks inside a double-quoted shell command argument, where zsh executes command substitution.

Native owner startup must use the exact installed Codex or Claude command and the canonical worktree. A hook-trust, usage-limit, rate-limit, reset, or model-selection prompt is a user decision boundary; never automate it. Resume only after the native process receipt and generation claim are observable.

Before any replacement, inspect the exact native process, canonical worktree, branch, HEAD, and dirty paths. Any possible writer blocks another writer even when the diff appears stable. A stable diff is not lease evidence. Follow preview → revoke → finalize-preview → finalize with generation and inventory fingerprints; never adopt WIP while the old writer may still be active.

Startup evidence is not a convenience bundle: run cwd, git root, branch, HEAD, dirty paths, and source-checkout status as independent commands. A combined command loses which raw read or exit established authority and must be rerun before mutation. When a long suite fails, inspect and fix the first failing test/golden before another unchanged long rerun.

Preview `issueops execution prepare` first and review workspace root, branch, base SHA, and next command. Confirmation repeats the identical request with only `--confirm`. Any later ambiguity uses `issueops execution reconcile` and never another create attempt.

Installed-file readback does not prove an already running host process loaded the new code. MCP runs in-process; reconnect the host's MCP server to apply an updated binary. Inspect `issueops execution whoami --json` and `issueops execution status --id "$ISSUEOPS_ID" --json` for current native identity and lease authority rather than probing retired enforcement hooks.

When an owner is blocked, it remains mutation-free and returns the exact state error and rendered next command in the fixed report. It must not create a second decision system. The active holder publishes and verifies the draft PR/MR, then records `issueops execution complete` with the exact lifecycle ID, generation, actor, cwd, committed report, final HEAD, artifact URL, and verification results. CLI/MCP commands own this boundary; hooks only supply project-doc context.

A yielded execution cell is unfinished evidence. Poll that exact cell or its returned process session through a terminal exit and capture the final exit/output before counting, replacing, or proceeding past the gate; if an edit follows, restart the ordered verification gate from step 1. Never infer completion from partial package output or from starting a later command.

Never construct `gofmt -w` arguments with shell command substitution such as `$(git diff --name-only ...)`. Inspect and verify the changed Go paths, then invoke `gofmt` with the explicit direct argv list so whitespace, glob, and option-like filenames cannot change the formatting scope.

Before this fence, each worker commit must use a Conventional Commit subject and a literal `Lore:` block with `Intent`, `Why`, `Changes`, `Verify`, and `Risk` as required by `.issueops/COMMIT_POLICY.md`.

A completed execution is never a new mutation lease. Review feedback that requires edits starts a new bounded execution or an explicitly authorized continuation before completion.

Pending external intent survives interruption: reconcile ambiguous workspace/publication state, or replace a failed holder with exact generation and quiescence evidence. Record before/after process, worktree, branch, HEAD, and dirty-path observations. Cleanup remains a separate human-authorized operation after verified merge evidence.

## Execution Mode and Evidence

Choose risk before execution. Full mode is for user-facing, hard-to-reverse, or
multi-criterion work: goals, append-only ledger, per-criterion artifacts, metrics,
and a binding adversarial reviewer. For trivially reversible docs, wording,
single-file validation, or config work, a one-line pass/fail ledger and command
stdout/diff are enough; goals/metrics are optional. Record the risk rationale and
review skip explicitly. Both modes require observable evidence, honest results,
and verified cleanup (or "none spawned"). Tests alone never prove completion.

For each full-mode criterion, actually run one channel: HTTP (status + headers +
body), terminal/tmux (transcript), browser (actions + screenshot), or computer use
(actions + screenshot; AppleScript on macOS, `xdotool` on Linux only). Use available
host tools. CLI stdout, DB diffs and parsed config are valid auxiliary evidence
for CLI/data criteria and the low-risk exception, never substitutes for a
user-facing channel. Dry-run, printed commands, speculation and "looks correct"
are not usage evidence. Artifacts must be nonempty, untruncated, reproducible,
make pass/fail binary, and name goal + criterion + channel. If output exceeds
32 KB, record the truncation point and retain/read the complete artifact before PASS.

### State and criteria (before implementation)

Prefer IssueOps state; otherwise use local files, never invented state elsewhere:
- IssueOps: `.issueops/verified-execution/`; fallback: `.verified-execution/`.
- Each root contains `goals.json`, append-only `ledger.jsonl`, and `evidence/<goal>-<criterion>-<channel>.<ext>`.
- Read availability with `issueops state read --key verified-execution-goals-<repo-hash>`;
  checkpoint with `issueops state write --key verified-execution-goals-<repo-hash> --input goals.json --json`.

Read the user brief, plan, or cycle intent; no usable goal means clarify before
execution, not fabricated criteria. Plan TODOs map 1:1 to criteria. Goal fields:
`id`, `title`, `objective`, `status`, `successCriteria`. Each criterion has unique
`id`, exact `scenario` (tool, steps, inputs, binary outcome), `channel`,
`expectedEvidence` path, `status`, `capturedEvidence`, `cleanupReceipt`, and
applicable `ultraqaClasses`. Initial status is pending and captured evidence/receipt
are null. Pick relevant adversarial classes: `malformed_input`, `prompt_injection`,
`cancel_resume`, `stale_state`, `dirty_worktree`, `hung_command`, `flaky_test`,
`misleading_success`, `repeated_interruption`. Do not proceed to a criterion without
a concrete expected artifact path.

The checkpoint is a JSON object with a top-level `goals` array and sibling
`metrics` object, not a bare goal or array. Initialize all five metrics to 0.0:

```json
{
  "goals": [
    {
      "id": "G1",
      "title": "Short goal title",
      "objective": "Concrete deliverable description",
      "status": "pending",
      "successCriteria": [
        {
          "id": "G1-C1",
          "scenario": "curl -i http://localhost:3000/api/x | expect 200 + body.id",
          "channel": "HTTP call",
          "expectedEvidence": ".issueops/verified-execution/evidence/G1-C1.txt",
          "status": "pending",
          "capturedEvidence": null,
          "cleanupReceipt": null,
          "ultraqaClasses": ["malformed_input", "stale_state"]
        }
      ]
    }
  ],
  "metrics": {
    "evidenceCoverage": 0.0,
    "reworkRate": 0.0,
    "cycleEfficiency": 0.0,
    "parallelizationRatio": 0.0,
    "cleanupCompliance": 0.0
  }
}
```

For web usage evidence, use the current host's available browser tool.
In this repository, `skills/issueops/references/execution.md` provides supplemental
cycle details; it is not a prerequisite for this body-only standalone contract.

### Delegation boundary

The main agent implements, fixes, tests and drives QA. Delegate only these
net-positive patterns: high-volume exploration, devil's advocate, parallel
independent research, cross-verification, isolated-worktree edits, model
specialization, tool-gated read-only exploration, background long-running work,
plan/execute separation, forked-context exploration, independent task fan-out,
and triage to a specialist. No nested sub-agents. Small/single-file tasks, work
requiring full conversation context, cross-cutting architecture, and safety/
reversibility/alignment decisions stay with the main agent; overhead must pay off.

Every dispatch includes goal, exact files, baseline characterization test when
changing existing behavior, constraints/project rules, verification commands,
one QA channel and exact artifact path. Workers lack interview context. Use only
current host tools; if dispatch is unavailable/disallowed, record the limitation
and work directly. A required independent review remains unfulfilled, not an
invented approval. Verify every worker diff, tests, diagnostics and evidence yourself.

## Per-Criterion Loop

Cap one goal at 5 cycles and identical criterion failures at 3; checkpoint the
diagnosis at either limit. After 2+ failures use systematic root-cause diagnosis
(with the debugging skill if available), not another unchanged attempt.

1. **Plan:** read scenario, expected evidence and ledger; identify independent
   wave tasks. Register atomic todos: path, action, criterion, verification.
   Serialize only on a named dependency.
2. **Execute:** for existing code behavior, first pin current behavior with a
   passing characterization test. RED must fail for the intended requirement,
   not syntax/import errors. Capture it, then make the smallest GREEN change
   (roughly under 20 lines); a larger step calls for a finer test. Pure prose
   changes use validation/diff evidence, not prose-pinning tests.
3. **Integrate:** inspect your diff, run relevant tests and changed-file LSP
   diagnostics. Fix scope drift, hollow tests, or missing evidence. Re-verify
   isolated worker output; fix it directly or return specific failure context.
4. **Run scenario:** personally execute the named QA surface; a heavy browser/
   computer channel may use a dedicated QA-only specialist. On failure, fix the
   cause and rerun the same criterion. Capture transcript/stdout/screenshot/
   assertion/status+body/diff/dump at the expected path; missing artifact is BLOCKED.
5. **Clean before recording:** remove every spawned runtime resource and verify
   removal: PIDs (kill, failed kill -0), terminal sessions (kill and inventory),
   browser contexts (close), containers (remove), ports (empty lsof), temporary
   mktemp paths (remove), QA-only environment variables (unset). Retain evidence.
   Record resource → action → verification, or "none spawned"; leftovers are BLOCKED.
6. **Record once:** PASS needs artifact + receipt; FAIL needs captured output +
   diagnosis; BLOCKED needs evidence + blocker. Ledger fields are `ts` (ISO8601),
   `goal`, `criterion`, `status`, `evidence` (path and cleanup receipt), `rework`.
   Full evidence also records exact channel command, summary, attempts, rework,
   cycle (of 5), and timestamp. Update criterion state and checkpoint.
7. **Measure in full mode:** recompute `evidenceCoverage = passed_with_evidence / total_criteria`,
   `reworkRate = self_corrections / total_criteria`,
   `cycleEfficiency = completed_criteria / total_attempts`,
   `parallelizationRatio = total_tasks / waves_used`,
   `cleanupCompliance = cleanup_receipts / completed_scenarios`.
   Start metrics at zero. Targets: ≥95% coverage, ≤15% rework, ≥80% efficiency,
   ≥4x parallelization where independent work permits, 100% cleanup and durable
   cross-session survival. Comparative target is ≥20% improvement over the
   inherited ulw-loop baseline, not a claim of measured improvement. These
   targets never justify unnecessary delegation.
8. **Complete goal:** every criterion must pass with evidence; append `ts`,
   `goal`, `event: goal_complete` and current `metrics`. Only after all goals pass,
   enter the appropriate final gate below.

## Final Gate: Standalone Lane

Inside a cycle use its clean → docs → verify stages once, not this extra sequence.
The prepared-worktree confirmation sets the authorized endpoint; finishing this
skill creates no additional approval stop. Standalone order:

1. Targeted verification of changed behavior.
2. If cleanup is in scope, remove lazy/duplicated/unused diff residue without
   changing behavior (use the cleanup skill when available). Harness health
   `issueops self-verify` is not a generic cleanup substitute.
3. Re-verify after cleanup.
4. Full mode/user-facing/hard-to-reverse work requires a fresh adversarial reviewer
   given goal, criteria, artifacts and full diff. Its gate is binding: verify
   every concern, fix valid ones, return disconfirming evidence for invalid ones,
   rerun full scenario QA after fixes, and resubmit to the same reviewer until
   unconditional approval. "Looks good but" or LGTM without evidence review fails.
   Proportionate low-risk work may skip with its specific recorded rationale.
5. Record `aiSlopCleaner` (status/evidence), `verification` (status/commands/evidence),
   `codeReview` (status/recommendation/evidence), `criteriaCoverage` (totalCriteria/passCount),
   and `metrics` (all five fields above). Reviewer pass is `APPROVE`; a risk-based
   skip is `status: skipped, recommendation: null` with rationale, never fake approval.
   Record other inapplicable steps honestly rather than claiming they ran.

A failed step in an ordered verification sequence restarts from step 1; do not
reuse partial passes as a completed sequence. Cycle stages own valid evidence
reuse/resealing and their bounded review loop, not this standalone review loop.

## Cycle Recording and Ordered Completion

Use `issueops next --id "$ISSUEOPS_ID" --json` for lifecycle routing; implement
owns this execution loop, then clean → docs → verify → pr → completion. Never
jump directly from criterion PASS to pr. The owning stage records START/scenario,
PASS/evidence/cleanup and progress feedback with source `verified-execution`.
`issueops feedback add` and `issueops status` are supported aliases, not authority.
For authenticated recording, obtain `record_actor_flags` and `claim_actor_flags`
from `issueops execution whoami --json`, for records and lease operations
respectively; retain exact lifecycle ID, generation, native actor, canonical cwd.
Use the owning stage's rendered commands, not invented flags or direct phase jumps.
If it is absent, leave recording pending; standalone execution still works.

Preserve this order and the existing user-confirmed endpoint:
1. Record cleanup category and rerun verification; finish the report/implementation
   diff before entering ai-slop-clean with the sealed command.
2. Review project docs. If updates are needed, edit first, verify/reseal, then
   record `updated` with changed paths; otherwise record evidenced `no-change`.
   Never relabel old evidence as execution against a new fingerprint.
3. For migration/entity/SQL schema changes only, observe real DB indexes and target
   row counts (catalog/estimates, not large scans); record sources or justified waiver.
4. After acceptance and authorized verification pass, read current `next.review`
   model/effort/tier/lenses immediately before fresh independent review. Missing
   routing is blocked, not a fallback to prepare-time defaults. Record actual
   reviewer model/effort/verdict/findings; follow the stage's bounded escalation
   and override rules. Revise means fix/reverify/review; stop blocks publication;
   only pass proceeds. An owner-model choice is not a reviewer override.
5. Commit/push the sealed diff only within existing authorization. Changed diff
   requires renewed cleanup/verification/review. Verify clean/synced branch, enter
   pr, observe final HEAD separately, and preview the governed draft request with
   explicit branches, labels, assignee, actor/cwd/generation. Confirmation repeats
   the identical request with only `--confirm`; never infer remote-write approval.
6. Read back URL, target, labels, assignee and Korean body. Only then complete from
   pr with committed relative report, final HEAD, exact artifact URL and repeatable
   verification results. Verify completion receipt and lease release with status,
   then stop: no automatic merge, close, or worktree/branch cleanup.

On lease/session/generation denial: one status read, at most one exact rendered
next command, then release a claimed lease and return blocked if still denied.
Digest drift is mutation-free. Preserve safe WIP; reconcile ambiguous external
intent rather than retrying creation. A completed execution grants no new lease.

### Fixed IssueOps v1 Owner Report

Return these 13 fields exactly once, in this order (bounded evidence, no secrets,
claim-token text, private reasoning, or raw transcript):

~~~text
Status: <completed | blocked>
Lifecycle: <exact lifecycle ID>
Host/model: <host / model (effort)>
Worktree/branch/final HEAD: <exact values>
Lease generation/completion: <generation + receipt or blocker>
Commits: <ordered SHA + subject>
Changed files: <exact paths>
Acceptance evidence: <AC-ID → test/command/result and artifact paths>
Verification: <every command + PASS/FAIL, explicit skips>
AI-slop clean: <removed duplication/legacy/noise or none>
Draft PR/MR: <URL or none>
Deviations: <issue/code or intent/issue mismatch + file:line or none>
Blockers: <exact state/error/next command or none>
~~~

Completed requires draft readback, all required verification PASS and completion
receipt; blocked preserves safe state without further unauthorized mutation.

## Portable Cycle Evidence

- Before domain changes record invariant, exact mechanism, equivalent behavior,
  and current source/command evidence. Report missing documented mechanism
  separately from whether another path enforces the invariant.
- API changes require plan/draft evidence of changed endpoints (or none), public
  errors reachable through business logic, available static checks, agent review
  for visible errors, and targeted commands. Prefer repo commands; if absent,
  record that and use the nearest check, without blaming unrelated pre-existing debt.
- Runtime/environment differences need a matrix: Environment | Repo/config
  evidence | Runtime evidence | Failure path | Remediation order. Separate source
  from live DB/config/env/pod/log observations and similar-looking failure paths;
  distinguish local-only probes from same-network/workload proof.
- For feedback record classification (contract_change, defect, question, noise,
  valid_review, stale_review, rollout_evidence_missing, environment_debt), validity
  evidence, original-thread reply status, and resolution (unresolved, fixed,
  resolved, obsolete, follow-up). Apply only verified feedback. Scope/criteria/
  non-goals/verification/labels/link changes require owning-stage issue-body update
  before continuing, within remote-write authorization.
- Before ready/done record actual-worktree diff, source/target branches, issue/PR
  body freshness, copied or explicitly replaced labels, single-commit policy or
  reason for multiple commits, divergence/cleanliness, cleanup status or numbered
  choices. Prepare an inspectable draft completion record before remote writing
  and final reporting: diff, verification, labels, linked children, PR/MR URL,
  review-thread status, cleanup and unresolved follow-ups. Tests alone do not
  satisfy requested remote updates, replies, merge readiness, or cleanup.

## Structured Steering and Collaboration

Reject free-form steering in place of structured, evidence-backed state changes.
Record every steering event in the ledger:

| Kind | Required fields |
|---|---|
| add_subgoal (real blocker) | --title, --objective, --evidence, --rationale |
| split_subgoal (too large) | --goal-id, --children, --evidence, --rationale |
| reorder_pending (dependency) | --order (IDs), --evidence |
| revise_criterion (no observable PASS) | --goal-id, --criterion-id, --scenario, --evidence |
| mark_blocked_superseded (replacement) | --goal-id, --replacements, --evidence |

These are record fields, not invented executable CLI flags. Optional collaborators:
planning supplies criteria; debugging diagnoses; algorithm work supplies redesign
and benchmarks; DB work supplies before/after EXPLAIN ANALYZE; research supplies
reviewed reports; code-quality metrics add SNR/entropy/redundancy; self-verify
health scores feed evidence coverage; repeated failures yield recorded lessons
(with self-augment if available). Authorized code/evidence commits stay atomic.
Use current file/patch/search/shell/async tools with explicit cwd on Codex, Claude
Code, Omo, omp, and opencode; never name unavailable host tools as executable.

## Stop Rules

- All goals and criteria pass with artifacts/receipts and the applicable final gate
  is clean: DONE at the authorized endpoint.
- Three identical criterion failures or five goal cycles: checkpoint failed and
  surface diagnosis, not endless retries.
- Destructive commands, secret exfiltration or production writes: block at the
  safety boundary and offer a safe substitute; no hidden expansion of authority.
- Leftover QA state: clean, verify and append receipt before proceeding; never PASS.
- User /cancel: release in-progress state cleanly; do not auto-resume.

## Optional Reference

[Evidence examples](references/evidence-contract.md) and
[historical comparisons](references/comparison-context.md) add no runtime requirement.
No evaluator reference is needed to execute this skill. `quality inspect` is not
semantic skill evaluation; `issueops skill-bench` is unsupported.
