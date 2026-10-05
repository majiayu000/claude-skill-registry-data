---
name: disclosure-gating
description: "Gate every externally-visible sentence through the claim and disclosure register in `00-control/claim-and-disclosure-register.md` (`CL-####`), then derive `06-public/technical-partner-guide.md` and `06-public/customer-product-and-trust-guide.md` from approved rows only. Use when drafting or editing any public document, when someone asks whether a statement can be said externally, or when the disclosure policy changes. This skill MUST be consulted because a public document is an unretractable commitment — an unregistered claim that crosses the boundary is a legal and competitive exposure that no later revision undoes."
allowed-tools: Read, Write, Edit, Grep, Glob, Bash
context: fork
agent: general-purpose
---

# Disclosure Gating

Owns the boundary between what is true internally and what may be said externally.

## Iron Law

**NO PUBLIC SENTENCE WITHOUT AN APPROVED `CL-####` ROW. Unregistered means unpublishable, regardless of how obviously true it is.**

The exception you are about to make — the claim so trivially true it cannot need a row — is how register completeness dies, and completeness is the register's only value.

## What the register tracks

Every public-facing capability, metric, reliability, privacy, security, compliance, compatibility, roadmap, and support claim. Each `CL-####` row carries the **exact proposed wording**, its supporting evidence IDs, applicable version and scope, required limitations or conditions, the approving owner, disclosure classification, destination document, and status.

Exact wording matters because approval attaches to a sentence, not to a topic. "We encrypt data at rest" and "all customer data is encrypted at rest" are different claims with different truth conditions, and approving the first does not approve the second.

Column schema and ID grammar: `references/register-schemas.md`. Policy levels, confidentiality classes, and prohibited vocabulary: `references/disclosure-policy-levels.md`.

## The approval boundary

You may **apply** a disclosure policy. You may **never appoint yourself** the business, legal, security, privacy, or communications approver.

Where `disclosure.publicClaimApproval` is `required` and no human approval is recorded, the row's status is `pending` — never `approved`, never blank. A `pending` row blocks its sentence, and an unresolved `pending` row blocks the release gate. That is the intended behaviour, not an obstacle to route around.

| Situation | Handling |
|---|---|
| Technically verified, no approver recorded | `pending`. Draft the sentence; do not release the document |
| Already appears in existing marketing copy | Existing publication is **neither** approval **nor** proof. Re-verify and re-approve, or withdraw |
| Approver rejected it | Record in the rejected section with the reason, then check whether another sentence implies it indirectly |
| Obviously true and trivially checkable | Still needs a row |

## Only `V` and `C` go public

`R`, `I`, and `U` claims may appear internally when labelled. None may appear in a public document — not qualified, not softened, not rephrased.

A `U` may be disclosed as a **limitation** ("we do not currently support X"), which is a different speech act from a claim and is often the most valuable sentence in the document.

## Derivation procedure

Phase 5 runs exactly this order. Starting anywhere else — from the internal documents, from existing marketing copy — is how unapproved claims leak.

1. Start from the **approved** rows of the register. Only those.
2. Write each sentence at the partner or customer abstraction level.
3. Strip evidence locators, internal identifiers, confidential detail, security-sensitive implementation detail, internal ownership, and unannounced plans.
4. **Preserve every limitation and condition needed to keep the sentence true after stripping.**
5. Verify examples against supported behaviour using visibly synthetic data.
6. Compare the rendered document claim-by-claim against the register. A sentence with no matching approved row is a release-gate failure, not a warning.

Step 4 is where simplification goes wrong. Detail may be omitted; the result may not become false.

| Internal truth | Acceptable | Unacceptable |
|---|---|---|
| Encrypted at rest in the primary store; the analytics replica is not | "Customer records are encrypted at rest. Derived analytics data is not." | "All data is encrypted at rest." |
| 99.5% measured last quarter, no contractual SLA | "Measured availability last quarter was 99.5%. No level is contractually committed." | "99.9% uptime SLA." |
| Region-pinned primary; backups replicate cross-region | "Primary storage is region-pinned. Backups replicate to a second region in the same jurisdiction." | "Your data never leaves your region." |
| No known breach | *say nothing about breach history* | "Never been compromised." |

## What never crosses

Credentials and tokens in any form, including "example" values that are real · personal data and customer identities, including in sample payloads · internal repository paths, file names, evidence IDs, register IDs, ticket references · vulnerability details and unpatched version ranges · internal hostnames, IP ranges, topology · internal ownership, team names, escalation chains · unannounced roadmap and pricing · internal reliability objectives presented as customer guarantees · any row that is `pending` or `rejected`.

Run `bin/dossier-claim-scan.sh` before considering a public document complete. The `block-unregistered-claim` hook enforces this at `PreToolUse`, so this is a check you cannot forget to run — but running it early is cheaper than being blocked late.

## Prohibited without scope and evidence

Each of these is a claim, not an adjective: `secure` · `compliant` · `encrypted` · `anonymous` · `private` · `real time` · `unlimited` · `always` · `never` · `guaranteed` · `fully automated` · `zero downtime` · `bank-grade` · `enterprise-ready`.

Prefer the specific replacement. Not "real time" but "typically under 400 ms, not guaranteed". Not "anonymous" but "pseudonymized — we retain a reversible identifier". The specific version is both truer and more useful.

## When there is no external surface

The two public files still exist. Interface sections are `N/A` with evidence, and the partner guide explains the supported partnership model instead. A missing canonical file is indistinguishable from an incomplete run.

## Output Format

```markdown
## Public Claims

| ID | Proposed wording (exact) | Evidence | State | Scope and version | Required qualification | Classification | Destination | Approver | Status |
|---|---|---|---|---|---|---|---|---|---|
| CL-0001 | {verbatim sentence} | [EV-0042] | V | {applies to} | {condition that keeps it true} | Public | 06-public/... | {role or `unassigned`} | approved / pending / rejected |

## Rejected or Withdrawn

| ID | Wording | Reason | Decided by | Date |
|---|---|---|---|---|
```

Plus the gate input:

```markdown
### Disclosure Result
UNSUPPORTED_PUBLIC_CLAIMS={n}
PENDING_APPROVALS={n}
REDACTION_HITS={n}
```

Zero unsupported public claims is a gate condition. Any non-zero value here blocks release.

## Rationalization Prevention

| Excuse | Response |
|--------|----------|
| "This is on our website already" | Existing publication is neither approval nor technical proof. Re-verify or withdraw. |
| "It is obviously true, a register row is bureaucracy" | The register's value is completeness. The obvious exception is how completeness dies. |
| "I verified it technically, so I can approve it" | Technical truth is one of three tests. Contractual and communications approval are not yours to give. |
| "Saying 'secure' is standard marketing language" | It is a claim about scope and controls. Define both or delete the word. |
| "The limitation makes the sentence weak" | The limitation makes the sentence true. Weak and true beats strong and false. |
| "Customers will not understand the qualified version" | Then find clearer words for the true claim. Do not find clearer words for a false one. |
| "It is a partner doc, partners are under NDA" | NDA governs confidentiality, not accuracy. A false statement under NDA is still false. |
| "No approver is assigned, so I will mark it approved" | Then approval means nothing. `pending` is the honest state, and it blocks the gate for a reason. |

## Integration

Invoked in Phase 5 of `/dossier:baseline`, by `/dossier:claim` for single-claim verdicts, and by `/dossier:refresh` whenever the blast radius touches a claim consumed by a public document. Loaded by `dossier-doc-drafter` for the two public files and by `dossier-pass-c-audience`, which audits leakage independently.

References: `references/disclosure-policy-levels.md`, `references/register-schemas.md`, `references/package-contract-06-public.md`.
