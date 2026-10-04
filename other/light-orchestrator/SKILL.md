---
name: light-orchestrator
description: Coordinate and recover multi-stage Light research projects through the canonical .light/passport.yaml state, stages 1-13, resident overlays, checkpoints, findings, parallel joins, stale propagation, handoffs and user-authorized reroutes. Use for a new/resumed/partial/dirty/failed/stale/delivered research project; when the user says continue, resume, take over, checkpoint, reroute, recover or deliver; or when work crosses two or more Light research stages. Never turn frontend-design/system-design/patent-disclosure/software-copyright or overlays into stages, never execute a suggested back-edge without explicit user authorization, and never declare delivery from file existence alone.
---

# Light orchestrator

Coordinate, route and recover the research lifecycle. Do not impersonate the
stage skills and do not turn a deterministic check into a research judgment.

Read
[`references/orchestrator-resource-map.md`](references/orchestrator-resource-map.md)
before a real lifecycle run. It defines intake, state authority, migration,
evidence states, access tiers, resident budget and handoff. Read
[`references/integration-contract.json`](references/integration-contract.json)
when changing any role, gate or route. The detailed rationale is
[`../../docs/design/orchestrator-spec.md`](../../docs/design/orchestrator-spec.md).

## Non-negotiable boundaries

1. Never choose the research direction, final idea, plan, venue, back-edge,
   revision-budget exception, known-limitation conversion or final delivery
   for the user. Present a recommendation, evidence, alternatives and
   consequences, then stop.
2. `reroute.py` is advisory. Only
   `passport.py add-back-edge --authorization-id <user-record>` may write a
   real back-edge, and only after the user authorizes that exact route.
3. A back-edge must go to an earlier stage (`to < from`). The 2⊣3 data
   feasibility result is an `admission_hold`, not a back-edge.
4. Never call a gate passed from prose. Use a producer's
   `light.findings.v1`, `run_checkpoint.py`, its exit code, a fresh timestamp
   and a content hash.
5. Never collapse evidence states. Use only `VERIFIED`, `PLANNED`, `UNKNOWN`,
   `UNAVAILABLE` or `FAILED`.
6. Never overwrite dirty/untracked user work, silently migrate a passport,
   silently rerun a stale downstream chain, or silently mark a limitation.
7. Never put an overlay or engineering skill in the scientific DAG.
   `system-design`, `frontend-design`, `patent-disclosure` and
   `software-copyright` have no stage, findings, `STAGE_GATES`, `ROUTES` or
   scientific back-edge.
8. Never claim 23-skill delivery because files exist. Verify the live
   inventory, hashes, checkpoints, limitations, handoff and user delivery
   decision.
9. Never silently install or reconfigure local runtimes. If a stage emits an
   environment advisory such as `r_advisory.requires_user_choice=true`, present
   the choices and consequences; only continue with install/config after an
   explicit user authorization. Non-interactive runs may choose the documented
   honest fallback only when the downstream contract does not require that
   runtime.

## 1. Intake every project

Start with:

```bash
python scripts/lifecycle.py intake --root <project-root>
```

Act on the primary state:

| State | Required behavior |
|---|---|
| `new` | inspect scope; propose only needed stages; ask at strategic choices |
| `resume` | trust passport/hash/handoff over chat memory; continue `next_action` |
| `partial` | preserve delivered stages; choose the next dependency-ready node |
| `dirty` | inventory user changes; do not mutate until they are protected |
| `failed` | inspect blocking evidence; run checkpoint/reroute; stop for user |
| `stale` | show the propagated reverify set; rerun only after scope is clear |
| `delivered` | verify the full delivery package; ask the user to accept/deliver |

If multiple flags coexist, treat dirty work as a mutation blocker and failed
evidence as a progression blocker. Do not hide either behind the primary label.

## 2. Keep one canonical state

`.light/passport.yaml` is the canonical pipeline state. memory-pm owns project
facts, decisions, versions and handoff history around it; a handoff is only a
hash-bound pointer.

- Current schema: `light.passport.v3`.
- Schema: `references/passport.schema.json`.
- Starter: `templates/passport.v3.yaml`.
- `state_hash`: SHA-256 of canonical state excluding the hash field.
- `inputs_fingerprint`: path + file bytes, not mtime.
- `state_revision`: increments on every v3 save.

For an older passport:

```bash
python scripts/passport.py migrate --file .light/passport.yaml
# inspect the dry-run and UNKNOWN legacy authorization
python scripts/passport.py migrate --file .light/passport.yaml --write
```

Do not run `--write` until the user authorizes ledger migration. Migration may
mark a legacy back-edge authorization `UNKNOWN`; it must not invent proof.

## 3. Route only the defined roles

### Pipeline nodes

1 literature-search → 2 data-engineering and 3 idea-generation → 4
idea-critique → 5 research-plan → 6 experiment-coding → 7 result-analysis.

Stage 7 forks to 8 paper-writing and 9 figure. Stage 8 also feeds 9 figure and
10 citation. Stages 9 and 10 join at 11 typesetting → 12 venue-matching → 13
review-rebuttal.

Dependencies are forward DAG edges. Parallel branches must declare
`depends_on`; a join waits for every required branch. Do not treat list order
as dependency order.

### Resident overlays

- memory-pm: state context and on-demand ledger findings;
- project-structure: off-DAG project-tree lifecycle, no findings;
- consistency: cross-artifact findings attached to the current checkpoint;
- research-ethics: integrity findings attached to the current checkpoint;
- file-reading: off-DAG parsing/understanding, no findings.

### Off-DAG engineering and IP handoff

Invoke frontend-design or system-design only when the project needs a UI or
software architecture. Their outputs may be referenced by the project, but
they remain off-DAG and do not produce scientific findings.

Invoke patent-disclosure or software-copyright only when the user explicitly
needs IP/material handoff from a real project. They prepare review materials,
not legal advice, filings, registration guarantees or scientific findings.

## 4. Run a real checkpoint

先选择**最小充分执行模式**，不要把每个任务都升级成多 agent 编排：

```bash
python scripts/execution_mode.py --input task-profile.json
```

输出 `light.execution_mode.v1`，只做决策、不执行任务：

```json
{
  "complexity": "complex",
  "path_predictable": false,
  "subtasks_independent": true,
  "clear_evaluator": true,
  "requirements_complete": true,
  "user_decision_needed": false,
  "distinct_categories": 3,
  "budget_allows_parallel": true,
  "iterative_improvement": false,
  "human_checkpoints": ["高成本执行前", "最终交付前"]
}
```

布尔字段必须是真正的 JSON `true/false`；若启用 `iterative_improvement`，还必须给
`max_iterations >= 1`，避免无界 evaluator loop。

- `direct`：单步、低风险、无依赖；
- `fixed_workflow`：依赖顺序稳定；
- `routed`：需先分类再分流；
- `parallel`：独立分支且预算允许；
- `orchestrated`：动态依赖、需共享状态协调；
- `evaluator_loop`：有明确验收器，且预算允许修订。

缺少会改变路线的必填信息时返回 `UNRESOLVED`，并只问一个最有信息量的问题；用户已给足信息时不得为了“互动感”重复询问。

高风险、付费、远程、发布、投稿、删除或不可逆动作先生成 `light.decision.v1`，再过授权门：

```bash
python scripts/decision_checkpoint.py --input decision.json
```

`execution_mode.py` enforces this rule by data, not by caller goodwill: even
when `user_decision_needed=false`, a task profile that declares remote
execution, paid resources, external writes, publish/submit, delete/overwrite
of user work, irreversible action, high risk, private/legal/ethics-sensitive
scope, or positive cost must return `UNRESOLVED` unless it carries a passing
`light.decision_checkpoint.v1` with an authorization ID. A single boolean must
not bypass the authorization gate. Use
`templates/task-profile.example.json` as the fail-closed example.

`PROPOSED` 返回 `UNRESOLVED` 并给出唯一关键问题；只有 `AUTHORIZED` 且授权主体、scope
与风险规则一致才返回 `allowed=true`。`REJECTED/REVOKED/EXPIRED` 一律拒绝执行。
本门只核授权，不替用户执行动作。

多任务、并行分支、人工暂停或断点恢复还必须过 workflow ledger：

```bash
python scripts/workflow_ledger.py --input templates/workflow-ledger.example.json
```

`light.workflow.ledger.v1` 核对 owner/context scope、依赖闭包、join 是否提前、任务证据、
真实 `sha256:<64hex>`、独立验证包、HITL decision id/scope/question/options/expiry、`max_attempts`、terminal retry 以及
`resume_snapshot.workflow_digest/task_id/visit_count/state_hash`。它只给 runnable/waiting/failed
集合，不执行任务。快照与当前 workflow digest 不同、重试预算耗尽仍 RUNNING、依赖未完成却
启动 join、等待用户却没有具体问题与至少两个带后果说明的选项，均为 FAIL；`WAITING_USER`
只有在问题/选项完整时才保持 UNRESOLVED，不得自动代答。

`SUCCEEDED` 不能只靠 owner 自填 `completion_status=PASS`。它还必须带
`verification.status=PASS`、与 owner 不同的 `verifier_id`、方法、带时区且不在未来的
`checked_at`、验证报告路径/哈希，以及与当前 `evidence_artifacts` **完全相同**的
`subject_sha256s`。方法只允许 `machine_gate`、`independent_review` 或 `human_review`；
后者还必须绑定 `authorization_id`。这只证明“当前哈希版本被一个可定位的验证步骤检查过”，
不证明内容必然正确；机器门优先，agent 自评不得冒充独立验证。

Run the stage's producer first. Then preview:

```bash
python scripts/run_checkpoint.py \
  --file .light/passport.yaml --stage <1-13> \
  --findings <producer-findings.json> --ts <ISO-8601>
```

Inspect report, exit code, producer, target, inner gate findings and expected
stage contract. After the user authorizes the ledger write:

```bash
python scripts/run_checkpoint.py \
  --file .light/passport.yaml --stage <stage> \
  --findings <producer-findings.json> --ts <ISO-8601> --write
```

`--write` without `--ts` is invalid. A critical finding returns exit 1,
records `FAILED`, and blocks progression. PASS/WARN records `VERIFIED`; WARN
still remains visible.

`STAGE_GATES` has entries for 2–11 except 12, plus 13. Stage 1 produces search
signals for downstream consumption. Stage 12 is a user decision packet, not a
confirmation gate.
Stage 3 must aggregate idea-generation's `idea_genealogy` and
`innovation_engine` critical findings before the warn-only collision/diversity
signals; anti-collage failures cannot be bypassed by sending the candidate
straight to idea-critique.

## 5. Suggest, stop, then reroute

On a failed checkpoint:

```bash
python scripts/reroute.py \
  --findings <failed-findings.json> --stage <source-stage> \
  --passport .light/passport.yaml
```

Interpret actions:

- `rework`: a legal earlier-stage back-edge;
- `admission_hold`: stop entry to stage 3; do not write an edge;
- `known_limitation`: revision budget is exhausted; ask whether to record it;
- `manual`: the signal cannot be mapped without human judgment.

Present:

1. the exact critical finding and evidence locator;
2. the recommended route and why;
3. alternatives: repair in place, choose another legal root cause, or record a
   limitation when justified;
4. cost and effect on downstream stale stages;
5. a direct user decision request.

Only after the user's exact authorization:

```bash
python scripts/passport.py add-back-edge \
  --file .light/passport.yaml --from <source> --to <earlier-target> \
  --root-cause "<evidence-backed cause>" \
  --evidence-ptr "<producer:gate@locator>" \
  --authorization-id "<user-message-or-decision-id>"
```

The command increments the target's durable `revision_rounds`. The limit is
two. A third attempt fails; do not reset the count across sessions or replace
it with a fresh passport.

Canonical suggestions are 4→3, 7→6, 7→5, 8→7, 9→7, and
13→3/5/8. An 8→6 route is a user root-cause override, not an automatic route.

## 6. Propagate freshness and recover

```bash
python scripts/passport.py stale-check --file .light/passport.yaml --root <project>
python scripts/lifecycle.py handoff --root <project> --out <handoff.json>
python scripts/lifecycle.py verify-handoff --root <project> --handoff <handoff.json>
```

An upstream byte change stales dependent stages. It does not automatically
invalidate independent parallel siblings. A changed passport hash invalidates
the old handoff. `verify-handoff` also checks the recorded project root,
timezone-bearing `generated_at` and the live intake snapshot
(`intake_state`, `next_action`, blockers, `need_reverify`,
known limitations and evidence state). A file-only stale change or new dirty
work therefore invalidates an old handoff even when the passport hash did not
change. Resume from the reported next action only after failed/dirty/stale
blockers are visible.

## 7. Resident injection

Claude Code's SessionStart hook injects red lines plus the resume report.
Codex/OpenCode consume the same memory-pm resume implementation through their
instruction files, but their trigger is model-read rather than harness-forced.
Do not claim identical automatic behavior.

The hook budgets 4,200 characters for discipline and 5,400 for state. On
overflow it truncates to a pointer to this skill or the canonical passport. If
memory-pm cannot load, it emits `UNAVAILABLE` and the manual resume command.

## 8. Delivery

Before asking the user to accept delivery:

1. run `integration_audit.py` and confirm 23 roles/stages/gates/routes;
2. validate passport schema and state hash;
3. verify all required stage checkpoint evidence is current;
4. 对多任务运行重新执行 `workflow_ledger.py`，确认 retry budget、snapshot compatibility、
   parallel join、完成态独立验证绑定和 WAITING_USER 状态；
5. surface every `UNKNOWN`, `UNAVAILABLE`, `FAILED`, stale stage and known
   limitation;
6. verify the handoff against the current passport hash;
7. state what was not run and why;
8. present delivery/hold/rework choices and ask the user.

Do not convert `PLANNED` to `VERIFIED`, waive a failed gate, exceed the revision
budget, or finalize delivery without the user's decision.

After explicit acceptance, record it mechanically:

```bash
python scripts/passport.py authorize-delivery \
  --file .light/passport.yaml --root <project> \
  --authorization-id <user-record> \
  --known-limitation "<accepted limitation>"
```

The command refuses non-delivered/non-VERIFIED stages and stale/incomplete
artifacts. It is the only supported transition to `delivery_status=DELIVERED`.

## Completion check

- [ ] Intake classified new/resume/partial/dirty/failed/stale/delivered.
- [ ] Passport is v3, hash-valid and explicitly migrated if needed.
- [ ] Stages 1–13, five overlays and four engineering/IP skills retained their roles.
- [ ] Findings producer and consumer are named; no dead gate exists.
- [ ] Parallel fork/join and dependency closure are valid.
- [ ] Workflow ledger has bounded retries, real artifact hashes, task evidence and compatible resume snapshot.
- [ ] WAITING_USER carries decision id/scope/question/options/expiry and was not auto-resumed.
- [ ] Reroute remained advice until explicit authorization.
- [ ] Back-edge is earlier-directed, authorization-bound and budgeted.
- [ ] Handoff hash and next action verify.
- [ ] Handoff root, timestamp and live intake snapshot still match.
- [ ] Evidence uses only the five states.
- [ ] Known limitations and unavailable resources are visible.
- [ ] High-impact task profiles cannot select an execution mode until a passing decision checkpoint with authorization ID is attached.
- [ ] User, not orchestrator, decided reroute and delivery.
