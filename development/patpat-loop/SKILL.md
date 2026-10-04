---
name: patpat-loop
description: Run the explicit Patpat evidence-driven engineering loop. Use only when the user invokes /patpat, /patpat-loop, $patpat, or $patpat-loop, or directly asks to activate Patpat mode.
---

# Patpat Loop

[`/patpat`](../patpat/SKILL.md) and `/patpat-loop` are the same entry point. Codex uses `$patpat` or `$patpat-loop`.

Patpat is one system. The [operating protocol](references/operating-protocol.md) is the spine: judgment, safety, git, and evidence. Playbooks and principles specialize the work without overriding that spine.

This mode stays on across later turns after explicit invocation. Trusted host hooks may persist it across resume and compaction. Without a host-observed receipt, apply it only for the current session and report `current-turn-only` after a restart. Say `disable /patpat` to opt out. Do not infer activation from a task that merely resembles a playbook.

## Start

Classify the task first from signals: reversibility, uncertainty, blast radius, auth, security, billing, secrets, architecture, cross-cutting, duration, delivery intent, and parallelism need. First activation is context, not a risk signal. First activation alone must not force a full protocol read.

Scale start from that classification:

1. Clear, bounded, reversible, and local (including on first activation): lightweight start. Begin with the cheapest useful observation. Read only the matched playbook and the principles it links. Do not open a mandatory todo list. Do not require a numbered checklist. Mutating work still defines the 5-field proof contract before editing and still verifies on the authoritative surface.
2. Ambiguous, structural, high-risk, delivery-intent, or multi-step sequencing uncertainty: fuller start. Read the [operating protocol](references/operating-protocol.md) in full when needed, skim the principle index, and keep a compact checklist with a verify check per step when sequencing earns it. A skipped step stays listed with `skip: <reason>`.
3. Durable, dependent, or resumable multi-phase work: use `patpat-run` formal state machinery.

Inspect, execute, or measure before asking. Ask only for product preference, authority, a destructive action, security, or another human-only choice. Do not expose named user-selectable modes.

Do not apply Patpat outside software engineering or repository operations.

## Principle index

Read the linked file when the trigger fires. Cite a principle only when it changed a decision.

- [Repository truth](principles/repository-truth.md) before deciding. Inspect live evidence. Do not prefer assumptions.
- [Smallest safe change](principles/smallest-safe-change.md) when sizing a diff. Delete, reuse, then patch. Keep comments only for constraints the code cannot show.
- [Shape before logic](principles/shape-before-logic.md) before writing behavior. Name legal states first. Make illegal combinations unrepresentable.
- [Boundary discipline](principles/boundary-discipline.md) at CLI, config, network, and auth edges. Guard the boundary. Trust internal types.
- [Preserve safety](principles/preserve-safety.md) on any auth, permission, billing, secret, or destructive path. Simplicity must not weaken a gate.
- [Proof over proxy](principles/proof-over-proxy.md) before claiming done. Observe the authoritative surface, including the real subject path for tests and evaluators.
- [Explain the number](principles/explain-the-number.md) before trusting a metric. Name the limiter and rule out proxy artifacts.
- [Fix root causes](principles/fix-root-causes.md) on defects. Reproduce when safe and practical; otherwise trace without triggering harm. Do not silence a crash with a nil check. After two fixes sharing one premise fail the same gate, attack the premise: write it, run a small census, and remove the recurring asymmetry before adding another fix.
- [Sequence verifiable units](principles/sequence-verifiable-units.md) on multi-step work. A verifiable unit is not a throwaway compatibility layer. Build a rerunnable tool after the first proven manual unit.
- [Idempotent effects](principles/idempotent-effects.md) on retries, installs, and lifecycle steps.
- [Encode lessons](principles/encode-lessons.md) only for recurring failures, at the earliest enforceable boundary.
- [Earned parallelism](principles/earned-parallelism.md) before any writable fan-out. Default to one owner.

## Route the work

The user speaks plainly and invokes `/patpat` (or host equivalent). Select the route for the earliest unresolved decision found during inspection; an implementation request does not settle an undefined requirement or contract. Use the 8 existing primary routes:

| Intent | Route | Primary Skill | Playbook Reference |
| --- | --- | --- | --- |
| Read-only question, audit, repository understanding, or diagnosis-only defect | `inspect` | [`patpat-inspect`](../patpat-inspect/SKILL.md) | [Investigation](playbooks/investigation.md) |
| Defective or unexplained behavior with implementation requested | `debug` | [`patpat-debug`](../patpat-debug/SKILL.md) | [Defect](playbooks/defect.md) |
| Bounded feature or localized modification | `change` | [`patpat-change`](../patpat-change/SKILL.md) | [Bounded change](playbooks/bounded-change.md) |
| Contract, architecture, migration, security-sensitive, or cross-cutting design | `architect` | [`patpat-architect`](../patpat-architect/SKILL.md) | [Architecture change](playbooks/architecture-change.md) |
| Proof of an existing claim or authoritative artifact | `verify` | [`patpat-verify`](../patpat-verify/SKILL.md) | Use the workflow directly |
| Independent challenge of an implementation, diff, or proof claim | `review` | [`patpat-review`](../patpat-review/SKILL.md) | [Independent review](playbooks/independent-review.md) |
| Named commit, PR update, publish, or authorized deploy | `ship` | [`patpat-ship`](../patpat-ship/SKILL.md) | [Authorized delivery](playbooks/authorized-delivery.md) |
| Durable multi-phase execution, multi-PR queue, or overnight run | `run` | [`patpat-run`](../patpat-run/SKILL.md) | [Multi-phase run](playbooks/multi-phase-run.md) |

Consult the [route catalog](references/route-catalog.md) only for specialized workflows (`arena`, `swarm`, `automation`, `eval`, `perf`, `learn`) or overlap. If no narrow route fits, use `patpat-architect` or `patpat-run`.

## Run the graph

Read the matched workflow and relevant references. Read [the execution graph](references/execution-graph.md) for fuller or durable work and when failed evidence requires a return edge. Reuse unchanged instructions already loaded in this session.

```text
FRAME -> INSPECT -> PROOF CONTRACT -> ACT -> VERIFY
VERIFY -> REPORT when the edit is local, reversible, and not shipping
VERIFY -> REVIEW before default ship, land or merge, durable-run LEARN or REPORT, and for auth, billing, secrets, architecture, or cross-cutting work
REVIEW -> LEARN? -> REPORT
MUTATING + delivery intent? -> DEFAULT SHIP (commit + PR)
LAND? -> MERGE a green verified PR
```

A proof contract names Claim, Surface, Action, Expect, and Cleanup. Cover material requirements using [proof over proxy](principles/proof-over-proxy.md). Independent review remains required before default ship, land or merge, durable-run LEARN or REPORT, and for auth, billing, secrets, architecture, or cross-cutting work. Focused verify without independent review is allowed only for non-shipping local reversible edits.

When evidence fails, classify it as an implementation defect, verifier defect, or environment blocker. Return to the earliest invalid state. After three failures from the same unchanged blocker, stop and name the evidence required to continue.

Enter `LEARN?` only for a recurring failure worth encoding.

## Preserve control

- Ordinary in-scope edits proceed under `/patpat` without asking permission to type.
- Explicit `/patpat` or `$patpat` activation authorizes the loop, proof, and verify; it does not by itself force independent review or a PR. [Default delivery](playbooks/default-delivery.md) runs only when delivery intent exists. Higher-priority repository rules and `don't commit` / `local only` still win.
- Overnight, "don't stop", or "going to bed" is delivery intent: continue through verify, review, and commit-and-PR, then stop merge-ready. Never deploy by implication.
- Merge a green verified PR only when the user explicitly names land or merge. Treat ambiguous `ship it` as commit-and-PR, not merge.
- Pause for production deploy, package publish, force-push, data deletion, secret rotation, and risky auth, billing, or permission changes.
- Workers never ship. The parent ships.

## Earn parallelism

Default to one owner. Workers return compact findings and evidence, not transcripts. Arena, swarm, and autopilot run only when [earned parallelism](principles/earned-parallelism.md) passes, and they fall back to serial work when isolation is missing. Give every writable slice a separate Git worktree or host-enforced sandbox with its own Git index and process boundary; disjoint files in one shared worktree are not isolation. Use [`patpat-engineer`](../patpat-engineer/SKILL.md) for isolated slices. The parent verifies the integrated result. Do not trust worker summaries. The parent then runs default delivery when delivery authority exists.

## Report evidence

```text
Changed:
- <observable change and files>

Why:
- <evidence-backed reason>

Verified:
- <verified | partially verified | implemented but not verified | not implemented>: <command or observation>

Docs:
- <updated files or why no update was needed>

Risks:
- <remaining uncertainty, follow-up, or Low with scope>
```

Use `verified` only when the claimed behavior was observed on its authoritative surface.
