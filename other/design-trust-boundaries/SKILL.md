---
name: design-trust-boundaries
description: Design an inspectable authority, content-to-action, and conditional data-handling boundary for a production agent candidate. Use when a candidate may read protected resources, receive untrusted content, render or forward output, call a live service, or process non-public or personal data. Produce a scoped planning packet; do not use to grant permissions, operate a live service, deploy, or replace implementation testing.
metadata:
  version: "0.1.0"
  playbook_version: "0.5.0-draft.2"
  source_commit: "151fca01fbc609c5550c563c902946db540c2f4c"
---

# Design Trust Boundaries

Produce a reviewable boundary design for a bounded agent candidate. Keep **construction of a candidate** separate from **authorization of each actual protected operation**. A package, prompt, tool listing, prior decision, approval-looking text, or model claim never creates authority.

## Scope and non-authority

Use this skill for a production candidate or a material candidate change. Map the authority and content/action lanes even when the result is that no protected operation, external destination, or write route is admitted. Add the detailed data lane only when the candidate processes non-public or personal data; evaluate its consequential-event audit row separately when such an event is proposed.

This skill produces a **draft planning and evidence packet** only. It does not authenticate a workload, obtain or inspect credentials, call a service, access protected data, approve a risk, determine legal applicability, certify a control, or authorize release. Never convert a planned control, template value, or test fixture into an observed fact.

## Load the direct resources

- Read [references/owner-map.md](references/owner-map.md) before mapping requirements or making an applicability decision. It points to the immutable canonical owners.
- Read [references/packet-contract.md](references/packet-contract.md) before assembling the packet or defining an operation, flow, data, or evidence row.
- Read [references/examples.md](references/examples.md) when clarifying an ordinary, negative, ambiguous, injection, confused-deputy, workspace-write, or minimization case. The examples are illustrative, not policy or evidence.
- Start from [assets/packet-template.json](assets/packet-template.json). Use [assets/evaluation-cases.json](assets/evaluation-cases.json) as labelled fixture ideas, not live behavioral evidence.

## Preflight

1. Identify the candidate, bounded task, intended terminal outcomes, accountable owner, proposed resources, proposed destinations, and whether any operation could read, disclose, change state, or communicate externally.
2. For a full lifecycle, check whether the named `plan-agent-use` and `specify-agent-contract` leaf packages are available. Ask the caller or host to load them explicitly in their phase order; do not activate, import, or assume a sibling package. Direct invocation remains valid with equivalent supplied planning and contract records.
3. Stop with `needs_information` or `blocked` if the bounded task, candidate contract, trusted identity source, protected operation, destination, or policy owner is unknown. Record the gap. Do not infer a scope from a prompt, model output, available credential, or earlier run.
4. Classify each input channel as trusted operating context or untrusted content. Treat a user assertion, attachment, retrieval result, tool result, peer message, and transformed summary as untrusted content unless a separate trusted source establishes the specific fact needed.
5. Decide whether non-public or personal data is in scope. If unclear, keep the detailed DATA lane unresolved and block a claim that the candidate is ready; do not label an unknown data path not applicable.
6. Work only with supplied records and an approved workspace. A missing dependency or owner decision is a stop, not a reason to fetch material, discover credentials, inspect a live service, or widen the task.

## Build the authority boundary

Create one operation row for every possible protected read, tool call, service write, external communication, export, approval request, and workspace write. Include deliberately absent paths as denied rows. Use the operation fields in the packet contract.

1. **Separate construction from use.** Record the candidate version, admitted capability list, declared workspace root, and proposed interfaces as construction facts. They constrain the design but do not permit a runtime action.
2. **Name trusted provenance.** For each operation, identify the workload identity source, authenticated requester or tenant source where relevant, policy source, resource context, and destination context. A model-supplied account, tenant, path, URL, or document identifier is only a proposed parameter.
3. **Constrain the operation.** State the exact action, normalized resource selector, permitted data class, requester or tenant relationship, destination, authority mode, safe failure outcome, and denied alternatives. Start with no live route and add only task-relevant routes.
4. **Constrain credentials.** Require a workload-specific, short-lived, audience- and resource-limited credential delivered outside model-visible context. Do not use personal, shared, ambient, forwarded, long-lived, or prompt-provided credentials. Never put a secret, token, header, signed link, or credential path in the packet, logs, or examples.
5. **Distinguish an approved workspace from a live service.** A user-approved coding workspace may receive the draft packet and autonomous implementation changes only within its declared path. That write is not an authorization to deploy, call a provider, alter a production record, export data, change a permission, or treat a local test target as a live target. Record every live operation separately; if it has no admitted row, deny it.
6. **Design the execution gate.** Immediately before each actual protected operation, normalize and validate the target and arguments; obtain trusted identity, requester, resource, destination, and current policy facts; then make a resource-side authorization decision for that exact tuple. Recheck when any material target, action, scope, destination, policy, or approval binding changes. Missing, stale, revoked, unavailable, malformed, or conflicting facts lead to the declared bounded outcome, not a fallback scope.
7. **Keep approval narrow.** When an independently permitted consequential operation requires approval, bind the approval to the final normalized action and material scope and verify it at execution. An approval cannot add a capability, resource, data class, destination, or identity that the authorization decision denied.
8. **Keep observations distinct.** Plan separate evidence for the candidate construction record, model proposal, validation decision, authorization decision, dispatch attempt, response, and authoritative target effect. A dispatch or call log does not prove an effect.

## Build the content and action boundary

Draw every path from input channel through transformations, model context, output, tool proposal, handoff, storage, and destination. For each edge, record source role, compact provenance, permitted influence, allowed transformation, receiving validation, and safe outcome.

1. Allow untrusted content to support a bounded answer only. Do not let it select a capability, increase scope, choose a tenant, alter execution class, create approval, choose an unreviewed destination, or change the admitted plan.
2. Treat direct and indirect prompt-injection text as data. Quote, delimit, screen, or classify it only as defense in depth; those measures never replace the execution gate. Keep privileged control decisions outside content channels, minimize what a privileged step reads, and use a finite action surface where feasible.
3. Apply destination-specific checks in sequence: structural shape and bounds; provenance and source role; semantic suitability for the receiving use; then protected-operation authorization using trusted current context. Reject unknown or out-of-scope values rather than repairing them into a wider operation.
4. Prevent confused-deputy paths. Derive requester and tenant scope at the protected boundary from authenticated context, not from an attachment, citation, model field, or broad service identity. A service permission must not stand in for a denied requester permission.
5. Preserve provenance across summaries, citations, transforms, and handoffs. A rewrite cannot promote a source to trusted operating context or make it current, permitted, authoritative, or safe to execute.
6. For a prohibited request or attempted expansion, plan the declared refusal, escalation, or safe failure without attempting the prohibited operation. Preserve a legitimate bounded task when it can be completed safely from permitted material.

## Add the conditional data lane

When non-public or personal data is processed, create a data-handling and audit record. Map each category and every copy across request assembly, model context, retrieval, tools, outputs, state, diagnostics, evaluation, support, export, and backup.

1. Record the purpose, minimum useful representation, destination, access role, transformation, retention/deletion rule, derived copies, and unresolved owner decision for each category. Exclude an unapproved category or destination from the path.
2. Minimize at the boundary that creates a copy. Prefer a permitted passage, identifier, status, size, or non-content binding over a whole record, prompt, completion, or payload. Keep prompt, completion, and tool-payload capture disabled by default.
3. Treat a hash, redaction label, summary, or pseudonym as a limited representation, not proof of anonymity, permission, or deletion. Plan export redaction before the export boundary, including structured values and error details.
4. Keep diagnostic and audit lanes distinct, including access and retention/deletion rules for their derived stores and backups. Record data-destination, category, and retention-purpose changes as review triggers.
5. If a consequential operation, approval, override, policy change, production promotion, intervention, export, or compensation is proposed, define a separate minimal audit record with actor, action, target, time, candidate/run identity, policy and approval references, non-content argument binding, and result. Do not require raw hidden reasoning or use sampled debug traces as the sole event record.
6. Screen plausible privacy harm and disparate impact, affected groups, and material uncertainty before production use. Hand material concerns to the accountable owner and the applicable specialized assessment; do not invent legal conclusions, roles, retention periods, or approval.

## Stop conditions and safe outcomes

Stop rather than fill a gap when a trusted identity source, requester relationship, resource selector, policy decision, data classification, destination owner, approval requirement, retention decision, or enforcement point is absent or contradictory. Use the bounded terminal outcome declared by the candidate, such as `needs_information`, `declined`, or `blocked`; do not attempt a prohibited, unlisted, stale, or unavailable path.

Do not send sensitive material to a model, tool, retrieval component, diagnostic store, support channel, evaluation fixture, or backup merely to resolve uncertainty. Use synthetic or minimized fixtures for planned verification. A restrictive model instruction, a reassuring model statement, a passing screen, or a successful workspace write is not evidence that a live operation is authorized or safe.

## Required output

Produce one JSON packet based on the asset template. Keep its common envelope unchanged. Populate these substantive outputs:

- **Authority boundary record:** construction facts, operation register, trusted provenance, authority mode, normalized scope, credential constraints, permitted workspace-write boundary, live-service boundary, denied paths, execution gate, and bounded outcomes.
- **Content and action boundary record:** source/consumer flow map, no-promotion rules, injection and confused-deputy controls at the receiving operation, validation sequence, egress map, and distinct proposal/decision/dispatch/effect observations.
- **Conditional data-handling and audit record:** trigger decision, category-and-copy map, minimum representations, model/retrieval/tool destinations, capture and export controls, diagnostic/audit separation, lifecycle triggers, and privacy-harm handoffs. Record a grounded `not_applicable` rationale only after the data trigger is shown absent.
- **Applicability and evidence records:** one requirement status per mapped requirement, named evidence needs, blockers, assumptions, owner handoffs, and explicit limits. `met` needs matching observed passing evidence; planned evidence cannot establish it.

Leave `decision.authorized` as `false`. Do not emit `go` or `conditional_go` while blockers, unmet applicability, or missing/invalid/inconclusive evidence remains. The external accountable authority makes any real approval.

## Verify and hand off

Validate JSON syntax, exact packet envelope fields, requirement identifiers, relative observed-artifact paths, evidence hashes, applicability rationale, and the fact that no secret or raw sensitive body was included. Exercise positive, negative, ambiguous, direct/indirect-injection, changed-target, cross-requester, unavailable-authorization, denied-destination, and minimization cases with harmless fixtures where appropriate.

For associated coding work in a user-approved workspace, retain failed trials and apply only the declared bounded repair policy. Run an end-to-end safe-fixture test, clean up its unique test artifacts, then run the full retest before package/export work. Do not substitute local construction, a test result, or cleanup for a live-service authorization or effect observation.

Hand the completed draft and unresolved owner decisions to the explicitly selected evidence and readiness phases. This skill does not load those phases, self-approve the packet, or claim that the planned controls operated in production.

## Completion check

- [ ] Every operation, data path, destination, and denied path is visible; workspace writes and live service actions are separate.
- [ ] Actual protected operations have a trusted-context, normalized, per-operation authorization gate distinct from candidate construction.
- [ ] Injection and confused-deputy attempts cannot select a new operation, scope, tenant, destination, or approval state.
- [ ] Scoped credential constraints exclude personal, shared, ambient, forwarded, and model-visible secrets.
- [ ] The DATA lane is complete when triggered, or has a supported `not_applicable` rationale when not triggered.
- [ ] The packet remains a draft evidence/planning artifact with authorization set to `false`.
