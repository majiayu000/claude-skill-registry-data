---
name: verification-protocol
description: "Run one independent verification pass over a documentation package by attempting to falsify it — a coverage inventory rebuilt from the contracts rather than the index, a two-stratum claim sample, end-to-end traces executed against the sources, audience task simulation, and mechanics validation — emitting findings in the `references/finding-schema.md` shape before any repair. Use when executing verification pass A, B, or C, or when auditing a package produced by another session or model. This skill MUST be consulted because describing a document is not verifying it — a pass that reads the package and agrees with it has produced no evidence, and passes that share context reproduce each other's blind spots."
allowed-tools: Read, Grep, Glob, Bash
context: fork
agent: Explore
---

# Verification Protocol

One independent pass. Owns falsification, sampling, tracing, and finding emission — and deliberately owns none of the merge, the repair, or the round loop.

## Iron Law

**VERIFY BY ATTEMPTING TO FALSIFY. Start from the sources, not from the document — and never read another pass's findings.**

A pass that opens the package, reads a claim, and finds it plausible has produced nothing. The only output that counts is a check that could have failed.

## The independence contract

You do **not** receive, and must not seek out: the drafting transcript · the authored project-model narrative as authority · another pass's findings · prior-round findings · the reconciliation logic · the author's self-score.

You receive: the package root · the resolved scope · the source roots · your lens · the round number.

This is not etiquette. Passes that share context converge on each other's blind spots, which defeats the entire reason there are three of them. If you find yourself reasoning about "what the other passes probably caught", stop — that reasoning is the failure mode.

Full contract, enforcement mechanisms, and the two independence tiers: `references/independent-audit-protocol.md`.

## Your lens

| Pass | Lens | Emphasis |
|---|---|---|
| **A** | Evidence and coverage | Rebuild the inventory from the contracts. Audit the census categories at 100%. Verify sampled claims against cited rows **and the original source** |
| **B** | Model falsification | Execute end-to-end traces from the sources. Report every point where the package and reality diverge |
| **C** | Audience, consistency, disclosure | Simulate each reader completing their task using only the package. Then headers, dates, links, terminology, leakage |

Run your lens. Do not compensate for what you imagine another pass is missing.

## Step order

1. **Independent coverage.** Inventory the project evidence yourself. Compare against the index, ledger, terminology, registers. **Rebuild the required-file list from `references/package-contract-*.md`, never from the documentation index** — auditing the index against itself proves nothing.
2. **Claim sample.** Stratum 1 is a census of the categories in `verification.claimSample.auditAllCategories` — security, compliance, licensing, financial, performance, customer-reference — audited at 100%. Stratum 2 is a risk-based sample of the rest. **State the method and size**; an unstated sample is not evidence.
3. **Falsify the model.** Execute the traces. See below.
4. **Audience usability.** Simulate the readers for your lens.
5. **Mechanics.** Links, diagram syntax versus inventories, examples against schemas, referenced versions, accidental secrets, duplicated facts across documents.
6. **Findings before repair.** Emit the table. Do not edit anything first.

## Per-claim audit

For each sampled claim determine: exact wording and destination · materiality · evidence locator · authority, date, version, environment · **whether the evidence actually entails the claim** · whether an important condition was lost · the correct state · whether public disclosure is approved · verdict.

The entailment check is the one that finds real defects. Evidence frequently supports a *neighbouring* claim: the row proves the configuration file specifies three replicas; the document says three replicas are running. Both sentences are reasonable. Only one is supported.

## Executing traces

Trace from the sources, not from the architecture document. Use the traces recorded in the project model so your findings are comparable, then look for what they omit.

Hunt specifically for: missing components or edges · inconsistent names, roles, permissions, ownership · undocumented coupling and manual steps · wrong state ownership or consistency assumptions · retries without idempotency · timeouts, queues, caches, and failure modes absent from happy-path diagrams · unsafe or untested recovery · false isolation or tenancy assumptions · weak observability · cost and scaling cliffs · stale or unsupported dependencies · licensing or provenance ambiguity · secrets or sensitive disclosure · AI autonomy, injection, leakage, evaluation, drift, and fallback gaps · customer and partner promises broader than the implementation.

Happy-path bias is the default failure of every documentation package. The error paths are where the package and the system diverge.

## Audit constraints

- Read-only outside the documentation root unless explicitly authorized.
- Never reproduce a secret, credential, personal datum, or exploitable detail — not even as evidence for a finding. Name the file and the pattern class.
- Do not infer implementation from intentions, tickets, roadmaps, or prose.
- Passing tests prove what they assert, not undocumented behaviour beyond their scope.
- Missing incidents, vulnerabilities, or failures are not proof of safety.
- A policy is not an implemented control. A target is not a measured outcome.
- An existing public statement is neither disclosure approval nor technical proof.
- Do not treat the package as correct because it is polished, internally consistent, or confident.

## Do not inherit the draft's confidence

A well-written package is *more* dangerous than a rough one, because its polish substitutes for verification in the reader's mind — and in yours. Confidence in the prose is not evidence, and a document that reads as authoritative deserves more scrutiny, not less.

## Output Format

Findings only. No edits, no merge, no score justification borrowed from another pass. Emit the marker, then the table in the canonical two-column form from `references/finding-schema.md`.

```markdown
<!-- DOSSIER_AUDIT round={n} pass={A|B|C} model={id} started={ISO} findings={n} critical={n} high={n} -->

## Pass {X} Findings

| Finding | Required correction |
|---|---|
| **{id}** · {severity} · dim {n} · `{location}`<br>{problem}<br>_Verifier evidence:_ {source path or executed check} | {exact change}<br>_Evidence still needed:_ {artifact, or `none`} |

## Coverage
| Evidence class | Inventoried independently | Present in the package | Gap |
|---|---|---|---|

## Claim sample
STRATUM_1_CENSUS={n} audited={n}
STRATUM_2_POPULATION={n} sampled={n} method={description}

## Checks
| Check | Result | Reason if not executed |
|---|---|---|
```

Then score independently per `scoring-and-release-gate`. Variance across passes is signal, not noise — do not calibrate toward an expected number.

## Rationalization Prevention

| Excuse | Response |
|--------|----------|
| "The document is well-sourced, spot-checking is enough" | Then spot-check by opening the source, not by reading the citation. A citation that exists is not a citation that entails. |
| "Another pass probably caught this" | You cannot know that, and reasoning about it is the correlated-error failure this design exists to prevent. Report it. |
| "This is the third round, most of it was verified before" | Prior rounds are not your input. A regression is exactly what a fresh pass exists to catch. |
| "I could not run the check, but the code looks right" | `not executed` with the reason. Reading is not running. |
| "This finding is minor, I will fold it into a bigger one" | Merge is reconciliation's job, not yours. Emit both. |
| "The package says this section is N/A" | Verify the `N/A`. "Does not apply" and "was not inspected" are opposite claims and look identical on the page. |
| "The architecture doc explains the flow clearly" | Then trace it from the source and see whether the source agrees. |
| "My score is lower than seems fair" | Then it is lower. Calibrating toward an expected number destroys the signal three passes exist to produce. |

## Integration

Loaded by `dossier-pass-a-evidence`, `dossier-pass-b-falsification`, and `dossier-pass-c-audience` — each with a different second skill, so their analytical priors differ by construction. Dispatched by `/dossier:audit` in a single message. **Never loaded together with `finding-reconciliation`**; a test enforces that.

References: `references/independent-audit-protocol.md`, `references/finding-schema.md`, `references/scorecard-rubric.md`.
