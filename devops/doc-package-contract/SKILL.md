---
name: doc-package-contract
description: "Enforce the fixed 23-file, 8-directory documentation package under the resolved output root — routing each document to its required-content contract in `references/package-contract-*.md`, stamping the internal or public header, and refusing to add, drop, rename, or merge a canonical file. Use when scaffolding a package, drafting or revising any canonical document, or checking structural completeness. This skill MUST be consulted because a package whose shape changes per project cannot be diffed, audited, or compared across engagements — the structure is the contract and only the content adapts."
allowed-tools: Read, Write, Edit, Glob, Grep, Bash
context: fork
agent: general-purpose
---

# Documentation Package Contract

Owns the shape of the package: which files exist, what each must contain, and what opens every one of them.

## Iron Law

**THE PACKAGE SHAPE IS FIXED — 8 directories, 23 files, every run. Content adapts; structure never.**

A missing canonical file is indistinguishable from an incomplete run. An irrelevant topic is handled with a justified `N/A` at section level, never by deleting the file — because "we dropped that file, it did not apply" and "we ran out of time" read identically six months later.

## The 23 files

| Path | Audience | Default confidentiality | Contract |
|---|---|---|---|
| `00-control/documentation-index.md` | All | Internal | `package-contract-00-control.md` |
| `00-control/evidence-ledger.md` | Diligence, verification | Internal | `package-contract-00-control.md` |
| `00-control/assumptions-questions-and-contradictions.md` | Diligence, owners | Internal | `package-contract-00-control.md` |
| `00-control/claim-and-disclosure-register.md` | Disclosure, legal | Restricted | `package-contract-00-control.md` |
| `00-control/terminology-and-ownership.md` | All | Internal | `package-contract-00-control.md` |
| `01-project/executive-project-brief.md` | Executive, investor | Internal | `package-contract-01-project.md` |
| `01-project/product-and-domain.md` | Product, engineering | Internal | `package-contract-01-project.md` |
| `02-architecture/system-architecture.md` | Engineering, security | Internal | `package-contract-02-architecture.md` |
| `02-architecture/components-and-codebase.md` | Engineering | Internal | `package-contract-02-architecture.md` |
| `02-architecture/data-and-ai.md` | Engineering, data, privacy | Internal | `package-contract-02-architecture.md` |
| `02-architecture/interfaces-and-integrations.md` | Engineering, partners | Internal | `package-contract-02-architecture.md` |
| `02-architecture/infrastructure-and-deployment.md` | Engineering, operations | Internal | `package-contract-02-architecture.md` |
| `03-assurance/security-privacy-and-compliance.md` | Security, privacy, legal | Restricted | `package-contract-03-assurance.md` |
| `03-assurance/reliability-performance-and-observability.md` | Operations, engineering | Internal | `package-contract-03-assurance.md` |
| `03-assurance/testing-quality-and-delivery.md` | Engineering | Internal | `package-contract-03-assurance.md` |
| `04-operating/onboarding-and-local-development.md` | New teammates | Internal | `package-contract-04-operating.md` |
| `04-operating/operations-and-incident-response.md` | Operations | Internal | `package-contract-04-operating.md` |
| `04-operating/decisions-technical-debt-and-risks.md` | Leadership, engineering | Internal | `package-contract-04-operating.md` |
| `05-due-diligence/technical-due-diligence-report.md` | Decision maker | Restricted | `package-contract-05-due-diligence.md` |
| `05-due-diligence/assets-dependencies-and-licenses.md` | Diligence, legal | Internal | `package-contract-05-due-diligence.md` |
| `06-public/technical-partner-guide.md` | Partners | Per disclosure policy | `package-contract-06-public.md` |
| `06-public/customer-product-and-trust-guide.md` | Customers | Per disclosure policy | `package-contract-06-public.md` |
| `07-verification/documentation-verification-report.md` | All | Internal | `package-contract-07-verification.md` |

Load **only** the contract for the document you are drafting. Loading all eight pulls over 500 requirements and hard rules into one context for no benefit.

## Headers

Every file opens with YAML frontmatter — `internal-v1` for the 21 internal documents, `public-v1` for the two under `06-public/`. Body line 1 is the H1; body line 2 is the contract pointer comment. This is positional and mechanically checked.

```markdown
---
dossier-header: internal-v1
title: System Architecture
...
---
# System Architecture
<!-- contract: references/package-contract-02-architecture.md#system-architecture -->
```

Field rules, the status ladder, and the public header's exclusions: `references/document-headers.md`.

`last-verified` is the date the document's **claims were checked against evidence** — not the date the file was edited. A formatting fix does not advance it. Advancing it without re-checking is the quietest way to make a stale package look current.

## What every document must make clear

Independent of its subject, a reader must be able to answer four questions without leaving the page:

1. What is true **now**
2. What is **planned** but not implemented
3. What is **unknown** or unverified
4. Which **limits and conditions** apply

Plus: where the canonical source of truth lives, so the reader knows what to trust when this document goes stale.

## Justified `N/A`

An `N/A` is a claim — "this is demonstrably irrelevant to this project" — and needs evidence like any other.

| Situation | Correct handling |
|---|---|
| No AI component | Section `N/A` with the evidence for the absence |
| No persistent data | **Not** `N/A`. Explain how state is handled — statelessness is a design fact |
| No external interface | Interface sections `N/A`; the partner guide explains the supported partnership model |
| Not inspected | **Never `N/A`.** This is `U` with an `AQ-####` row |

The last row is the failure mode that matters. `N/A` and `Unknown` are opposite claims, and using one for the other is a High finding.

## Supplemental documents

Permitted when the project genuinely needs them — a safety case, a per-service deep dive. They must be linked from the documentation index, must explain why they exist, and must not duplicate a canonical source of truth. The canonical 23 stay intact regardless.

One supplement is always written: a `README.md` signpost at the output root, from `templates/package-readme.md`. A reader browsing the output root otherwise lands on eight numbered directories with no entry point, and the index cannot route someone who never finds it. The signpost states no fact about the project — no counts, no dates, no verdict — so it cannot go stale and needs no evidence row. Everything that can drift stays in the index, which the signpost links to. Register it in the index's supplemental table like any other.

## Diagrams

Use Mermaid where it materially improves understanding of real structure, data flow, trust boundaries, or deployment flow. Every node and edge needs evidence; inferred connections are labelled inferred in internal documents.

Decorative diagrams, generic textbook illustrations, and exhaustive file trees have negative value — they cost review attention and carry no decision.

## Output Format

Scaffold via `bin/dossier-scaffold.sh --output-root <path>`, which leaves a frontmatter-fenced existing file untouched but repairs (overwrites) one that is empty or missing the fence. Verify via `bin/dossier-package-check.sh`.

```markdown
### Package Structure

| Document | Exists | Header valid | Status | Last verified | Contract pointer resolves |
|---|---|---|---|---|---|

### Structural findings
| Severity | File | Problem | Required correction |
|---|---|---|---|
```

The documentation index is regenerated from this table, never hand-maintained in parallel — a hand-maintained index drifts from the package it indexes, which is exactly the failure the package exists to prevent elsewhere.

## Rationalization Prevention

| Excuse | Response |
|--------|----------|
| "This project has no AI, so `data-and-ai.md` is noise" | It is one file with a justified `N/A` section and a data model that does apply. Deleting it breaks every cross-package diff. |
| "I will merge the two public documents, the audiences overlap" | Partners and customers need different abstraction levels and different disclosure boundaries. Merging optimizes for the writer. |
| "The index is out of date but the documents are fine" | The index is how every reader enters. A wrong index makes correct documents unreachable. |
| "I updated the formatting, so I will refresh `last-verified`" | That date means claims were re-checked. Advancing it for a formatting fix is a false statement about verification. |
| "This section does not apply — `N/A`" | Does not apply, or was not inspected? They are opposite claims. Only one of them is `N/A`. |
| "A diagram here would look good" | Would it change a decision? If not, it costs review attention and adds a drift surface. |
| "Adding a supplemental file is easier than fitting this in" | Then the canonical file is wrong or the content is not needed. Supplements are for genuine extra depth. |

## Integration

Loaded by `dossier-doc-drafter` for every document, by `/dossier:init` when scaffolding, and by `dossier-pass-a-evidence`, which rebuilds the file inventory **from these contracts rather than from the index** — auditing the index against itself would prove nothing.

References: `references/document-headers.md`, `references/package-contract-*.md`, `references/project-type-adaptation.md`.
