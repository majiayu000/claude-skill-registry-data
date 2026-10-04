---
name: appstore-readiness-audit
description: Audit Apple apps before App Store upload or review. Use when checking a release candidate for build, runtime, privacy, SDK, account, payment, metadata, compliance, or reviewer-access rejection risks. Return read-only, evidence-backed upload and submission verdicts.
---

# App Store readiness audit

Audit the exact release candidate that App Review would receive. Treat readiness as an evidence state, not as a successful compile or a generic policy checklist.

Operate read-only. Do not edit the app or metadata, change signing, upload a build, submit for review, or alter external services. Use isolated temporary build output only after checking build phases for side effects. Ask before a check needs credentials, signing changes, device resets, paid resources, or external mutation.

Do not promise approval.

## 1. Set the evidence boundary

Read applicable repository instructions, then record:

- repository path, branch, commit, and dirty state;
- new app or update, platforms, device families, OS targets, and storefronts;
- project or workspace, scheme, target, and Release configuration;
- bundle ID, marketing version, and build number;
- supplied archive, app bundle, export, or TestFlight build and its SHA-256;
- available App Store Connect and runtime evidence;
- user exclusions.

Mark absent artifact or runtime checks `NOT_TESTED`. Mark App Store Connect values `UNKNOWN` unless current read-only data or a dated export proves them. Never imply that source, artifact, runtime, or store state was inspected when it was not. Re-snapshot if the source changes during the audit.

## 2. Refresh applicable Apple rules

Read [apple-sources.md](references/apple-sources.md). Fetch the current core pages needed for the requested verdict, then only the conditional pages activated by the app's features. Record retrieval dates, visible update or effective dates, platform scope, and direct URLs.

Use Apple as the authority for policy. Community material may suggest tests but cannot establish a requirement.

If Apple sources disagree, preserve both statements and emit `SOURCE_CONFLICT`. Set the affected check to `UNKNOWN` and hold the verdict when the conflict can change eligibility. Do not transfer a requirement between platforms or hard-code today's toolchain, storefront, age-rating, SDK-list, or metadata rules.

After one reasonable retry, record an unavailable page as an evidence gap and continue.

## 3. Classify the product

Inspect project settings, source, generated configuration, entitlements, privacy manifests, dependencies, StoreKit files, release automation, and supplied metadata. Build a feature map with `YES`, `NO`, or `UNKNOWN`, evidence, and confidence.

Include accounts and deletion, login providers, UGC and social features, children, tracking, analytics, advertising, permissions, IAP and subscriptions, physical commerce, external purchase links, AI processing, regulated features, background modes, downloaded code, encryption, and external hardware.

Search matches and missing files are leads. Confirm material features through reachable code, configuration, artifact contents, dependency documentation, runtime evidence, or supplied product facts.

## 4. Run separate gates

Read [audit-catalog.md](references/audit-catalog.md) and activate only the relevant sections:

1. Project and Release configuration: identity, toolchain, signing, entitlements, capabilities, production settings, build, archive, and Xcode validation.
2. App completeness: clean launch, core journeys, production services, working URLs, visible failure recovery, lifecycle, devices, and accessibility.
3. Privacy and dependencies: data flows, SDK behavior, manifests, Required Reason APIs, permissions, ATT, policy, retention, and App Privacy answers.
4. Conditional policy: accounts, login, UGC, children, commerce, AI data transfer, regulated features, territories, agreements, and export compliance.
5. Metadata and App Store Connect: claims, screenshots, age rating, URLs, privacy, IAP, availability, review information, and operational status.
6. Reviewer simulation: clean install, no developer knowledge, working access, reviewable features, purchases, resources, recovery, and expected results.

Keep source inspection, Release compilation, tests, archive creation, Validate App, upload processing, runtime behavior, and App Store Connect reconciliation as distinct results. Static evidence cannot become a runtime pass. Local metadata is intended metadata until reconciled with the store record.

## 5. Record findings

Use these statuses: `PASS`, `FAIL`, `NOT_TESTED`, `UNKNOWN`, and `NOT_APPLICABLE`.

Classify the basis separately as `APPLE_POLICY`, `APPLE_TOOLCHAIN`, `DETERMINISTIC`, `RUNTIME`, `APP_STORE_CONNECT`, `MANUAL_HEURISTIC`, or `UNKNOWN`.

Use `BLOCKER`, `HIGH`, `MEDIUM`, or `INFO` severity. Do not calculate a readiness score.

For each finding, record a stable ID, status, severity, confidence, and basis. Record the applicable platform and feature. Record exact app evidence and reviewer impact. Record the smallest resolution direction and a verification step. If the finding depends on Apple policy or tooling, record a direct Apple source. Otherwise, record `N/A` for the Apple source. Do not call an absent file a blocker until the rule applies and the relevant scope is complete.

## 6. Decide readiness

| Verdict | Rule |
|---|---|
| `NO_GO` | A confirmed blocker exists. |
| `HOLD_UNVERIFIED` | A high-risk finding, required unknown or untested check, material source conflict, or missing evidence prevents the requested claim. |
| `READY_FOR_UPLOAD` | Required local project, Release, artifact, and current toolchain checks pass. Store and reviewer evidence may remain incomplete. |
| `READY_FOR_SUBMISSION` | Required project, artifact, policy, runtime, privacy, metadata, commerce, compliance, and reviewer checks have current passing evidence. |

If the user asks about submission and store or runtime evidence is missing, return `HOLD_UNVERIFIED`. Do not substitute `READY_FOR_UPLOAD`.

## 7. Report

Use [report-format.md](references/report-format.md). Lead with blockers and high-risk findings, then give the verdict, evidence boundary, gate ledger, incomplete checks, feature map, reviewer handoff, and lower-severity observations.

Do not print credentials or private reviewer data. During each source refresh, record the current Review Notes byte limit. Resolve `scripts/check_review_notes.py` relative to this loaded `SKILL.md`, not the audited app repository. Replace `<skill-root>` and `<review-notes-byte-limit>` before you present or run the command.

End by stating that the audit identifies known readiness risks and does not guarantee App Review approval. If no material finding survives verification, say so without inventing one.
