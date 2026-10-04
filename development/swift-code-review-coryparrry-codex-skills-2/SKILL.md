---
name: swift-code-review
description: Review Swift and Apple-platform changes, including SwiftUI/AppKit behavior, concurrency, persistence, packages, Xcode project/build configuration, mixed-language boundaries, generated code, and unsafe interoperability, for reachable correctness and regression risks. Use directly for a focused Swift diff, pull request, branch, commit, Swift 6 migration, AI-authored Swift, or Apple-platform and Xcode project change, and use as the Swift/Apple specialist lane when `deep-code-review` covers a mixed-language or repository-wide change.
---

# Swift Code Review

Review invariants, not surface syntax. Produce one evidence-led review that keeps scope explicit and findings first while distinguishing compiler acceptance, data-race safety, and application correctness.

Treat review as read-only. Do not edit, stage, commit, push, post comments, or resolve threads unless the user separately asks for those actions.

When invoked as a specialist lane under `deep-code-review`, return exact-state evidence, coverage, validation gaps, and candidate findings to the umbrella reviewer. Let the umbrella review own cross-language integration, deduplication, final disposition, and merge-readiness claims.

When the same request includes fixes, complete and report the review phase before entering a separately identified write-enabled repair phase. Do not edit while evidence collection is still changing the review inventory.

## 1. Fix the review scope

User-specified scope always wins. Resolve the exact comparison before reviewing:

- **Files, paths, or pasted changes:** treat that material as the finding scope. Inspect repository context needed to validate it when available, but do not report unrelated context as findings. If context is unavailable or explicitly excluded, state the limitation and do not approve beyond the supplied material.
- **Working tree:** inventory staged, unstaged, and all untracked paths before deciding which are in scope; state exclusions.
- **Non-merge commit:** compare the resolved commit with its sole parent.
- **Merge commit:** state the selected parent-specific, merge-base, or combined comparison; do not infer it silently.
- **Branch or pull request:** use the authoritative current base and head, normally their merge-base diff.
- **Explicit endpoints:** compare the two resolved trees directly rather than substituting a merge-base diff.

Record the resolved base, head, and merge-base IDs as applicable, plus the comparison mode.

Before reviewing a repository:

- read repository-level guidance and each applicable path-specific `AGENTS.md` or equivalent for the in-scope files;
- inspect the branch, `HEAD`, and working tree;
- preserve unrelated local work;
- verify the current PR head and base when a PR is in scope;
- state when supplied excerpts make the inventory incomplete.

If the change is too large to review reliably, partition it by subsystem or risk surface when the boundaries are clear. Ask for coherent slices only when the intended boundary cannot be inferred. Name everything that remains unreviewed; never silently skim a broad diff.

First inventory every changed path and classify it by subsystem and risk. Maintain a coverage ledger of reviewed and unreviewed slices. Review coherent slices deeply, then make one integration pass across shared contracts and cross-cutting state. Opening every file is not sufficient for a complete review. Tool or context limits that prevent any slice from being completed make the review partial.

Re-snapshot the inventory before reporting. If a commit, generated file, staged change, uncommitted edit, or validation command changes any in-scope path, pause and re-resolve the base, head, working-tree status, and changed-path inventory. State whether the new snapshot is included or excluded, then re-read every affected slice and repeat the integration pass. Do not combine findings from different snapshots without identifying which snapshot each finding belongs to.

Use one reviewer for a focused change. When subagents are available and the change has independent high-risk surfaces, the primary reviewer may assign at most two non-overlapping, read-only lanes after inventorying the complete diff, identifying shared contracts, and locating cross-cutting boundaries. Recheck every proposed finding against the full change before reporting it; do not create iterative reviewer-versus-reviewer loops.

Report completeness separately from disposition. A partial review may request changes based on a surviving Confirmed or High-confidence blocker in the reviewed scope, but it must never approve the complete change. If no such blocker survives, use `Disposition: not assessed`.

If the scope remains genuinely ambiguous after inspecting local context, ask one concise question.

## 2. Establish intent and environment

Use this order as the starting evidence priority for intended behavior:

1. the user's request;
2. linked issue, PR description, specification, or accepted plan;
3. repository architecture and product-direction documents;
4. commit messages and behavior-focused tests;
5. the implementation.

Do not treat the new implementation, including AI-authored or generated output, as proof of intended behavior. When explicit intent is unavailable, infer conservatively from unchanged public contracts, callers, tests, and repository conventions, and state the assumption. For pasted-only changes, report only internally provable defects and explicit context or validation gaps.

When sources conflict, determine which one represents the current accepted contract and report unresolved conflicts explicitly. Do not silently resolve disagreement solely by list order.

Record only the environment details that can change the conclusion:

- compiler and Xcode version;
- affected targets, products, modules, schemes, and build configurations;
- Swift language mode for each affected target;
- strict-concurrency level;
- default actor isolation and upcoming feature flags;
- conditional compilation flags and participating generated sources or macro expansions;
- SDK and minimum deployment targets;
- package tools version and affected dependency versions;
- relevant Debug, Release, platform, and architecture differences.

Do not equate compiler version with language mode. Use Swift Evolution proposals to understand design intent, but verify proposal status, implementation version, feature flags, and behavior in the active compiler, SDK, module interface, or dependency version. A proposal alone is not proof of shipped behavior.

## 3. Route by affected invariant

Route by affected invariant and live review hypothesis, not only by files or syntax changed:

| Trigger | Required reference |
|---|---|
| Actors, global actors, `Sendable`, `sending`, locks, tasks, cancellation, callbacks, continuations, streams, ARC teardown, queues, or event loops | [concurrency-and-lifetime.md](references/concurrency-and-lifetime.md) |
| SwiftUI state, Observation, identity, lists, navigation, tasks, layout, modifiers, animations, accessibility, scenes, windows, AppKit lifecycle, delegates, KVO, target-action, or responder-chain behavior | [swiftui-and-appkit.md](references/swiftui-and-appkit.md) |
| Core Swift ownership and value semantics, borrowing, generics, protocols/existentials, overload or witness dispatch, collections/indices, numeric or Unicode behavior, error propagation, parsers, external input, unsafe memory, C/C++/Objective-C interoperability, persistence, retry, public API, compatibility, security, or performance | [data-api-and-platform-boundaries.md](references/data-api-and-platform-boundaries.md) |
| `Package.swift`, dependency resolution, resources, build settings, linker flags, build tools/plugins, macros, or generated-code boundaries | [data-api-and-platform-boundaries.md](references/data-api-and-platform-boundaries.md), plus any reference implicated by generated behavior |
| An unfamiliar claim needs primary support, a repository case, or AI-specific calibration | [evidence-and-ai.md](references/evidence-and-ai.md) |

Load another reference when unchanged callers, consumers, generated expansion, or platform boundaries make that domain material. Do not apply every checklist to every diff.

Use these default review depths:

| Change | Minimum depth |
|---|---|
| Claimed mechanical rename or formatting | First rule out public, serialized, dynamic, generated, selector-based, persistence, and resource-name dependencies. Then confirm no semantic diff and run the narrowest relevant check. |
| Local deterministic transformation | Inspect inputs, outputs, boundaries, error semantics, complexity, and tests. |
| Tests, fixtures, previews, or snapshots | Verify the check exercises intended production behavior, distinguishes defective from corrected behavior, preserves assertion strength, and is deterministic under relevant runtime and concurrency conditions. Route by the production surface tested. |
| SwiftUI view change | Trace state ownership, identity, observed reads, layout states, parent/child size budgets, modifiers, accessibility, and visible runtime behavior. |
| Async work or callback bridge | Map ownership, isolation, cancellation, freshness, reentrancy, duplicate/late completion, and teardown. |
| Persistence or external side effect | Establish the applicable atomicity, idempotency, retry, partial-failure, migration, and recovery guarantees. |
| Public API or package change | Check source/runtime compatibility, isolation, sendability, overload dispatch, availability, and downstream adoption. |
| Unsafe, interop, or security-sensitive code | Require an explicit bounds/lifetime/threat invariant and adversarial validation. |

## 4. Trace invariants beyond the diff

For a complete review, read the complete diff before deciding that a pattern is a finding. For a declared partial review, read every in-scope slice and inventory the exclusions. On the first pass, establish the change's purpose, major design choices, and affected system boundaries. Surface a fundamental design or contract problem before spending time on local details.

Then inspect only the surrounding graph needed to verify each risk:

```text
entry or event
→ validation
→ state transition
→ work ownership
→ suspension or callback
→ isolation or transfer
→ external side effect
→ completion
→ freshness check
→ state/UI/persistence commit
→ cancellation and teardown
```

For each meaningful mutable value or resource, be able to state:

> All reads, writes, transfers, and lifetime transitions of X occur under Y invariant, except Z, which is safe because W.

Inspect these paths when affected by the change or necessary to prove a suspected risk:

- callers and downstream consumers;
- alternate, convenience, generic, and deprecated entry points;
- tests, fakes, previews, and generated interfaces;
- applicable cancellation, retry, failure, teardown, and migration paths;
- cache-hit, synchronous-callback, and oldest-supported-platform behavior when applicable.

Reason through, or exercise where existing tooling permits, competing events such as duplicate input, out-of-order completion, cancellation, reentrancy, deletion, identity replacement, view/window closure, shutdown, malformed input, and partial success.

For stateful UI that combines cached or retained content with refresh, filtering, selection, or incomplete metadata, build a small state matrix before approving. Cross content availability (none, retained, fresh) with metadata/list availability (unavailable, partial, exact), freshness (idle, in flight, failed), and selection/destination (none, current, removed or replaced). Check every reachable combination, especially retained content with an empty or partial list. Do not use an empty collection, zero count, or hidden branch as a proxy for absent content or known-zero state unless the contract explicitly makes that meaning safe.

For fixed or bounded SwiftUI/AppKit containers, calculate the parent/child layout budget in each visible state: headers, content minimums, footers, padding, safe-area or reserved controls, overlays, and scroll regions must fit within the offered height and width. A child `minHeight` can exceed the parent's total content height even when each view looks locally reasonable; verify footer reachability, clipping, overflow, and flexible versus fixed sizing rather than checking only the final fresh-content frame.

## 5. Verify findings

Treat every suspected issue as a hypothesis. Try to disprove it using current code, contracts, and tests before reporting it.

A review finding must be introduced or worsened by the change, or the change must newly expose or depend on the defective behavior. Record unrelated pre-existing issues separately and do not use them to determine disposition.

A finding must contain:

1. a reachable trigger or violated contract;
2. the exact invariant that fails;
3. a concrete impact;
4. current-code or primary-source evidence;
5. the smallest practical repair direction;
6. a concrete test, reproduction, static proof, or inspection method that distinguishes the current defect from corrected behavior.

Do not report:

- a diagnostic annotation merely because it is present;
- speculative performance concerns without a demonstrated hot path, scale factor, or measurement plan;
- style handled by automated tooling;
- generic requests for actors, weak captures, protocols, tests, or abstraction;
- missing test coverage as a defect unless an explicit test contract is violated or a demonstrated regression lacks its required regression test;
- low-confidence possibilities as confirmed defects;
- AI authorship as severity evidence.

## 6. Validate proportionately

Run the smallest relevant repository-approved checks. Escalate only when the changed surface warrants it:

- compile affected targets under their actual settings;
- run focused unit, integration, UI, migration, or package tests;
- compare relevant build configurations and architectures without altering the declared support contract;
- when OS-version runtime behavior matters, run on representative oldest-supported and current runtimes when available; do not equate deployment-target compilation with runtime validation;
- use sanitizers, Instruments, API/ABI checks, or stress tests only for exercised risks;
- for user-visible SwiftUI/AppKit changes, validate the exact fresh build and relevant intermediate states when runtime access is available.

Follow repository-specific Apple/Xcode tooling instructions. A passing build, test, sanitizer, or screenshot is evidence only for the paths it exercised.

Do not assume builds or tests are read-only. Before running them, inspect applicable build phases, package plugins, test setup, and documented commands for side effects. Run only local, non-destructive checks in isolated derived-data, cache, and temporary-output locations. Skip or sandbox commands that may mutate user state, simulators or devices, databases, Keychain, external services, signing or deployment state, dependencies, tracked artifacts, or files outside isolated build directories. Report skipped checks as validation gaps.

Compare repository status before and after validation and report any tool-created changes. Never claim a check passed unless it ran successfully. Classify a failure as pre-existing only when reproduced on the resolved base or supported by reliable prior evidence; otherwise call it an unclassified validation failure and do not attribute it to the change.

## 7. Rank and report

Rank only surviving findings:

- **P0:** catastrophic, widespread, irreversible, or immediately exploitable critical harm.
- **P1:** realistic merge-blocking correctness, safety, lifecycle, persistence, or major regression risk.
- **P2:** concrete but limited-scope edge-case, compatibility, accessibility, resource, or performance failure.
- **P3:** a concrete change-introduced maintainability hazard with a clear mechanism and local future cost.

Calibrate priority using blast radius, frequency, recoverability, user harm, data integrity, and supported-platform reach.

Assign confidence separately:

- **Confirmed:** reproduced or directly proven by code or contract.
- **High:** mechanism and reachability are clear.
- **Moderate:** plausible and material, but one environmental fact remains unverified; report it as an unresolved question or validation gap rather than a finding.
- **Low:** omit it or ask a concise question when the answer would materially change the review.

Begin with a compact scope block:

```md
Scope: <working tree or resolved base/head and comparison mode>
Reviewed: <paths or slices>
Not reviewed: <none or exclusions>
Completeness: <complete or partial>
Inventory complete: <yes, no, or unknown>
```

`Inventory complete: yes` means every changed path in the resolved comparison is known, not merely that every supplied excerpt was read.

Then lead with findings ordered by priority. For each finding include:

```md
### [P1] Specific failure

- Confidence:
- Location(s):
- Change relation: <introduced, worsened, or newly exposed/depended on>
- Trigger:
- Broken invariant:
- Impact:
- Evidence:
- Smallest correction:
- Validation or proof:
```

Keep line ranges tight. Do not bury findings under a long review summary.

Group multiple manifestations of one mechanism into a single root-cause finding unless they require materially different corrections or carry different impact.

After findings, include only:

- pre-existing observations, unprioritised and explicitly excluded from disposition;
- unresolved questions that materially affect correctness;
- validation performed and validation gaps;
- an approval/request-changes disposition when the user or review surface calls for one.

Only Confirmed and High-confidence findings determine disposition. For a complete review, request changes for P0/P1 findings and for P2 findings that are explicitly merge-blocking under a stated contract. Approve with comments when only non-blocking P2/P3 findings remain. For a partial review, use `request changes based on reviewed scope` when such a blocker survives; otherwise use `not assessed`. A decision-blocking validation gap always produces `not assessed — validation required`, not a speculative request-changes decision.

If no material finding survives verification, say so directly and state what was not validated. Do not manufacture comments to demonstrate effort.

## 8. Stop at sufficient evidence

Stop when:

- every in-scope change has been inspected at proportionate depth and every in-scope high-risk boundary has been traced;
- each reported finding is reachable and evidence-backed;
- relevant validation has run or its absence is explicit;
- remaining uncertainty is recorded;
- further checklist expansion would be generic rather than change-specific.

When reviewing a follow-up patch or a checkout that contains a prior fix, re-prove the original invariant and inspect its adjacent retained, incomplete, empty, failure, cancellation, and replacement states. Treat a fix that restores one path as new behavior that can regress a neighboring path; do not close the earlier finding solely because the original line or interaction now appears corrected.

If a Confirmed design or contract blocker makes the remainder not meaningfully reviewable, inspect enough to identify independent risks, list the affected remainder as unreviewed, and return a partial request-changes result.

Prefer approving a completely reviewed change that improves code health once no blocking finding or decision-blocking validation gap remains. Do not block on personal preference or unattainable perfection.
