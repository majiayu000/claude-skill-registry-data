---
name: orc-tools
description: Build and use ORC tools through authored tool leaves, guarded code callers, described catalogs, typed dynamic or finite arguments, recursive specialist chains and parallel actions. Use when selecting, invoking, composing or debugging tools, including researcher-generated tool nodes.
---

# Tools as ORC behaviors

Start from the observable postcondition and the host's effect authority. Read the consuming checkout's instructions, principles and public DSL. Current guidance is source-inspected at ORC `1851212396cced2fc4533fda30b824bd4b691390`; historical experiments remain evidence of their original revision.

## Choose the execution shape

| Work | Shape |
| --- | --- |
| One authored tool, arguments are declared read keys | `tool`: fixed `:tool`, flat read-to-argument map, exactly one write |
| Deterministic computation, nested argument map or several calls | `code` using built-in `:call-tool-fn` and `:tool-contracts` |
| A reusable multistep goal with local recovery | `delegate` to a separately built child tree |
| One bounded semantic capability/argument choice | `llm-decision`, then exact route guards |
| New text/numbers/structured arguments | Ordinary typed `llm`, or computation from trusted state |
| Unknown sequence requiring generated code and execution feedback | Bounded recursive `repl-researcher`; a separate surface |

Read [catalogs and arguments](references/catalogs-and-arguments.md) for model-visible selection and enforcement, [tools as behaviors](references/tools-as-behaviors.md) for recursive/dependent/parallel actions, [current invocation](references/current-invocation.md) for executable API forms, and [researcher tools](references/researcher-tools.md) for checkpoint boundaries.

## Build and select the capability

Expose stable catalog IDs, purpose, applicability, limits, argument meanings, result meanings, effects and success evidence in the actual model input. Registry names or schemas alone do not explain useful selection. The `:tool-contracts` top-level shape has no capability-description slot; place semantic purpose in typed catalog data/instructions and field descriptions in Malli schemas. Inspect the actual provider body. Use [blackboard contracts](../orc-blackboard-contracts/SKILL.md) and describe every registered key.

Separate semantic selection, argument preparation, invocation and goal verification. Jev can choose supplied IDs/enums/booleans; it cannot write new queries, dates or prose. Use [decision models](../orc-decision-models/SKILL.md) for registered native routing, then an ordinary typed LLM for unrestricted arguments when needed. Route catalog IDs through authored branches to fixed tool leaves or delegates; never execute arbitrary model-produced tool names, FQNs or sheet IDs.

A tool leaf's arguments are `{:read-key value ...}` with nil values omitted. If `:reads [:args]` then it calls with `{:args <map>}`, not the map's entries. Choose code when the capability expects that map directly. Result contract is validated against the raw caller result before the tool leaf unwraps a map entry matching its one write key. Declare that actual boundary. Use authored tools for simple one-call leaves; code remains supported for manual argument construction and several calls.

## Use native enforcement deliberately

Both code and tool leaves preserve `:tool-caller-fn` builder FQN and `:tool-contracts`. The builder receives blackboard and context and returns a caller. Without a builder, runtime `:call-tool-fn` is used; a missing caller fails a tool leaf. Configure runtime capabilities in execution/poller context and verify delegated inheritance. An unresolved/invalid declared builder fails rather than falling back to an ungated caller.

Ordinary authored tools invoke the resolved caller with two arguments. A context-dependent host needs a builder that closes over inherited context and forwards it; prove this inside the actual host body. Preserve supplied three-argument checkpoint context when applicable. The [invocation reference](references/current-invocation.md) shows both forms and the current code-leaf requirement for an explicit output contract.

Declared Malli arguments are enforced before dispatch; declared results before return. Validation uses a schema-directed key view but passes original arguments/results unchanged. Duplicate string/keyword field spellings are rejected where a contract is declared. Missing or `:untyped` contracts are permissive, and contracts are not a tool-name allowlist, authorization policy, or domain validity check. The host must enforce those. Result rejection cannot undo an effect already performed.

Code sees host exceptions unchanged and may catch them; uncaught errors fail its node. Researcher model-facing calls get safe structured error data, with host messages shared only through explicit `:orc.tool/message`. A successful code return containing an error/status map is data unless the host translates it. Sanitize sensitive host errors before code/tool failures can be persisted; safe researcher wrapping does not protect every consumer boundary.

## Compose and prove the goal

Use sequences for dependent observations, parallel for compatible independent work with distinct writes, and nested delegates for reusable goals. Build child trees first and supply their actual `:target-sheet-id`. A tool result can change what action is useful; sequence a fresh semantic decision or new argument preparation on that result. Do not force every task into one-call completion or a universal action template. Avoid regex/phrase classification of human/AI meaning and canned prose recovery.

Guard every selection branch, including none/clarify. A failed chosen tool must not fall through to unrelated success. Keep eligible recovery inside the selected goal and bound repair. Distinguish invocation success, valid observation and achieved parent postcondition. Use [specialist composition](../orc-compose-specialists/SKILL.md) and the [two-attempt repair](../orc-design-tree/references/bounded-repair.md).

For mutations, prepare stable host-owned operation identities and original payloads before effects, persist through authorized Grain commands, and bind receipts/projected facts to the exact request. Retrying a prior identity must preserve its payload; reject changed payloads and duplicate/reused receipts. For known batches validate the full proposal before the first effect. External replay safety and reconciliation remain the host/callee's responsibility; no contract flag creates them.

Verify live selected/none paths, malformed args/results, caller absence, denied effects, nested argument identity, dependent observations, recursive lineage, parallel overlap/output ownership, family budget and useful projection readback. Enforce the original deadline after admission waits as well as before them. Keep every invocation, receipt hit and actual effect separately; a cached result must not hide repeated work. Measure host overlap separately from serialized MCP/remote execution. Use `get-family-usage` for registered model calls across descendants. A shared outbound campaign guard still owns any physical retry cap. Capture requests and observations without credentials via [model/SIO](../orc-model-sio/SKILL.md) and [observability](../orc-observe-debug/SKILL.md).

MCP server `isError` is failure, even with otherwise schema-valid fields; translate the literal flag before accepting evidence. Missing real session is failure unless an explicitly configured dry run is intended and visibly marked. Do not count dry-run output as effect evidence. Ordinary execution leases and tool checkpoint receipts are distinct from durable judge jobs.

## Judge observed effects

Use [orc-judges](../orc-judges/SKILL.md) for quality monitoring or evidence-gathering judge tools. Supply actual effect evidence tied to tenant/run/operation identity. Confirmed missing effects differ from unavailable evidence; hashes identify content but do not prove actions. PR 43 tool/decision updates do not repair judge attachment, scheduling or score identity.

## Current proof and cancellation limits

Read [current proofs and limits](references/current-proofs-and-limits.md) for actual dynamic, finite, parallel and real-MCP outcomes at their recorded pins. At the earlier merge pin `1851212396cced2fc4533fda30b824bd4b691390`, family budget admission refused the excess provider call, but cancellation could leave missing child traces and delayed root delivery. Reproduce before transferring that defect claim to a later checkout. Do not claim complete cancellation/readiness from a timeout or an earlier green suite. Real tools also succeeded while a researcher's semantic evidence selection failed: verify relevance and final task completion separately from invocation.

For retrieval, validate that the returned source identity equals the exact identity requested from the discovery observation, on every attempt and retry, before passing it to generation or persistence. A well-formed result with a different ID is a failed selected retrieval. Comparing a generated note to that wrong result does not establish the requested provenance. For intentional identity remapping, require a described, validated mapping from the original observation.

## Tools in adaptive recursive work

Use [orc-repl-researcher](../orc-repl-researcher/SKILL.md) for a stage that must discover tool arguments, generate action trees and refine them from results. Its generated code receives guarded caller/context; the emitted palette has no dedicated tool tag. Use [researcher pattern reuse](../orc-researcher-pattern-reuse/SKILL.md) for described code catalogs and corpus guidance. Neither names in a catalog nor harvested source register an executable. Preserve real opaque references, three-argument checkpoint-safe calls, host idempotency and actual projected effects.

## Revisit tool behaviors without replaying completed effects

For permission-dependent continuation, map [authority transitions](../orc-blackboard-contracts/references/context-flow.md#apply-the-authority-transition-contract) before choosing ask/wait/handoff; a selected tool or proposed consent cannot change host authority.

For a known specialist that needs another action before it can finish, use the [authored controller](../orc-compose-specialists/references/authored-controller.md). A successful tool invocation can establish a prerequisite while leaving the parent goal open. Reassess the resulting artifact/evidence, select the next eligible tool behavior, and return the new observation to the original obligation. Keep prior accepted artifacts and effect receipts; build fresh dynamic arguments from current evidence rather than replaying stale queued calls.

A finite model can select a described tool/source ID, bounded arguments, a completion verdict or the next specialist. An ordinary LLM supplies newly written queries, notes or repair feedback. In either case, validate the selected tool's actual `:arguments` and `:result` contracts, exact source/operation identity and authority. Code leaves receive execution context at the top level alongside `:inputs` and `:call-tool-fn`; their return must contain every declared write with an acceptable value. Use a complete typed outcome or separate branches for different result shapes. Node execution success and the user's achieved goal are separate checks.

## Make tool failure observations precise

Distinguish empty argument batches, duplicate targets, unauthorized paths, stale versions and execution failures in typed observations. A generic denial string can send semantic repair to the wrong cause even when guards prevent an unsafe write. Preserve the actual attempted arguments and exact failed invariant. Do not turn a successful later retry into evidence that its intermediate diagnosis was correct. Experiment fault injection must obey the same path/identity scope before it mutates anything; otherwise the harness itself can manufacture the alleged tool defect.

When argument generation can discover that no safe candidate exists, its typed output needs a valid no-action/missing-information outcome. An always-required item plus only effectful operation choices can force an invalid proposal even with strict structured output. Separate proposal from validated invocation; code must not execute a no-action result. Present current effective availability with its source/override relationship, rather than an unexplained available catalog flag beside a contradictory unavailable list.

When adapting an external tool contract, check real nonempty results as well as arguments. Preserve typed dictionaries as described maps with typed keys and values; forcing them into empty closed records can reject a valid result after the tool has acted. Reconcile actual effects before retrying. See [external tool receipt evidence](references/bounded-workspace-acceptance.md#external-tool-receipts-during-fresh-transfer).

## Verify generated workspace code with independent assertions

When a tool executes code that the agent can replace, keep acceptance assertions under a trusted owner. A zero exit status or completion marker from the same interpreter as editable code does not prove that tests ran: an import can exit or alter the test process. In the bounded workspace fixture, unchanged protected assertions ran in a trusted parent, while an isolated child exposed only the public API over a bounded value protocol. Premature exit or an invalid response became an explicit tool infrastructure failure, not passing acceptance. Keep the protocol's supported values and isolation limits explicit; this pattern alone is not a security guarantee for arbitrary code.

Child confinement does not cover later privileged work in the parent. When collecting child-created artifacts, use rooted no-follow traversal, reject links and special files explicitly, and bound hashing before reading bytes. A real canary probe exposed a parent scratch-manifest read outside the child boundary; the corrected scanner and its preserved failure evidence are in the workspace host verification (historical local experiment; private archive not bundled).

For versioned edits, a path listing or search hash identifies a revision but does not establish that the full content was observed. Bind replacement authority to the actual source read, its version and coverage/truncation. Retain a complete per-file read across unrelated workspace changes when the exact path, content hash and full-read coverage still match; do not equate an old global read revision with stale target bytes. Keep the proposed edit bound to the current workspace revision and current target hash, and validate the whole batch before the first write. Changed target bytes need a matching complete read; listing their new hash is insufficient. Fresh reads before a first proposal are valid; do not require a stale attempt to manufacture recovery evidence. Sequential filesystem writes followed by recorded receipts do not provide crash-atomic effects.

The bounded workspace discovery evidence and its limits are indexed in the experiment report (historical local experiment; private archive not bundled).

Read [bounded workspace acceptance evidence](references/bounded-workspace-acceptance.md) when applying these host and read-authority rules. It separates actual protected acceptance, native transport correspondence and qualified shutdown from claims the experiment did not test.
