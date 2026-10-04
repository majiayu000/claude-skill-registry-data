---
name: enterprise-ai-data-governance
description: Use when designing, implementing, or reviewing enterprise AI data governance, seven-layer memory systems, four-layer MVP rollouts, Markdown knowledge vaults, document conversion, OCR pipelines, structured data catalogs, Agent retrieval, RAG governance, or FDE-style delivery across macOS, Linux, Windows, or WSL.
---

# Enterprise AI Data Governance

## Overview

Turn enterprise structured data, unstructured documents, and paper archives into governed, AI-ready knowledge and durable Agent memory. Use the seven-layer memory model as the target architecture and the four-layer MVP as the practical first rollout.

## Core Principles

- Preserve original evidence in `raw`; never replace it with an AI summary.
- Use `work` for conversions, drafts, extraction logs, and unresolved issues.
- Put only reviewed, durable knowledge in `vault`.
- Use `memory.md` and `MEMORY.md` as retrieval maps, not full-text stores.
- Keep databases and APIs as facts of record for structured and changing data.
- Separate evidence, indexes, facts, cases, procedures, state, and governance metadata.
- Require source traceability, least privilege, human review, and rollback.
- Define scope, interfaces, validation, rollout, and handoff as part of FDE delivery.

## Seven-Layer Memory Model

| Layer | Name | Purpose | Typical artifacts |
|---|---|---|---|
| L0 | Evidence memory | Locate original proof | Files, scans, exports, logs, transcripts |
| L1 | Index memory | Route an Agent to context | `memory.md`, keywords, prompts, summaries, paths, embeddings |
| L2 | Semantic memory | State accepted facts and rules | Glossaries, policies, metrics, data dictionaries, business rules |
| L3 | Situational memory | Reuse past experience | Projects, meetings, incidents, cases, retrospectives |
| L4 | Procedural memory | Execute repeatable work | Skills, SOPs, checklists, delivery templates |
| L5 | State memory | Continue current work | Daily notes, projects, issues, actions, risks |
| L6 | Meta-memory | Decide whether memory can be trusted and used | Access, trust, version, expiry, owner, audit rules |

Treat a keyword-and-path memory as L1 and a reusable Skill as part of L4. Add L2, L3, L5, and L6 when moving from personal retrieval to enterprise Agent operations.

## Workflow

1. Define the business scope.
   - Name the domain, users, use cases, sources, permissions, and success metrics.
   - Prefer one high-value pilot before enterprise-wide migration.
2. Inventory source material.
   - Separate structured systems, Office and PDF files, paper archives, meetings, messages, images, audio, and video.
   - Record owner, steward, sensitivity, retention, update frequency, and source path.
3. Map memory layers.
   - Assign each artifact to L0-L6.
   - Do not mix facts, cases, procedures, current state, and permissions in one undifferentiated file.
4. Design the target workspace.
5. Run the cross-platform environment preflight before selecting conversion tools.
6. Start with the four-layer MVP when the full scope is too large.
7. Convert material to AI-ready forms.
   - Keep large tables in databases, warehouses, CSV, Parquet, or APIs and create Markdown data cards.
   - Bind OCR output to original image paths and require human review for high-risk records.
   - Extract decisions, actions, risks, owners, and dates from meetings and transcripts.
8. Normalize approved Markdown.
   - Add governance frontmatter and required body sections.
   - Mark status as `draft`, `reviewing`, `approved`, or `deprecated`.
9. Distill and route memory.
   - Generate L1 entries with keywords, applicable questions, priority sources, tools, risk controls, and update notes.
10. Wire Agent retrieval.
    - Check L6 permission, search L1, retrieve L0 evidence and L2 rules, review L3 cases, select L4 procedures, and inspect L5 state.
    - Output sources, versions, timestamps, assumptions, and uncertainty.
11. Validate and roll out.
    - Use golden questions, permission tests, stale-knowledge tests, source traceability, OCR sampling, grey release, and rollback drills.

## Target Workspace

```text
enterprise-ai-memory/
  raw/          # L0 evidence
  index/        # L1 index
    memory.md
    keyword-map.md
    prompt-map.md
    entity-map.md
  vault/        # L2 semantic knowledge
    glossary/
    policies/
    metrics/
    data-catalog/
    business-rules/
  cases/        # L3 situational memory
    projects/
    meetings/
    incidents/
    retrospectives/
  skills/       # L4 procedural memory
  state/        # L5 current state
    daily/
    current-projects/
    open-issues/
    action-items/
  governance/   # L6 meta-memory
    access-policy.md
    retention-policy.md
    source-trust.md
    deprecated.md
    audit-rules.md
```

## Cross-Platform Environment Preflight

Before choosing or installing any tool:

1. Identify macOS, Linux, Windows, or WSL.
2. Check the project for an existing implementation or dependency.
3. Prefer operating-system built-ins and the Python standard library.
4. If Python is unavailable, run the matching bootstrap script only to detect and display the next approval request.
5. If Python is available, run `scripts/preflight.py` for one dependency at a time.
6. Treat WSL as Linux. Do not cross into the Windows host without a separate request and approval.
7. Read `references/enterprise-ai-data-governance-guide.zh-CN.md` when platform-specific selection or Chinese implementation guidance is needed.

Use these entry points:

- macOS, Linux, WSL without Python: `scripts/bootstrap-posix.sh`
- Windows without Python: `scripts/bootstrap-windows.ps1`
- All supported platforms with Python: `scripts/preflight.py`

The preflight and bootstrap scripts never install software.

## Mandatory Installation Gate

Before any download or installation, disclose all of the following in the user's language:

- Current platform.
- One named software dependency.
- Purpose for the current task.
- Project, user, or system installation scope.
- Detected package manager or installation method.
- Every command that would be executed.
- Administrator, sudo, UAC, or elevated PowerShell requirements.
- Network, disk, PATH, service, registry, policy, and environment impact.
- A no-install alternative, or state that none is available.

Then output `INSTALL_APPROVAL_REQUIRED` and stop.

Proceed only when the user explicitly approves the named software after seeing the exact platform-native commands. Handle one direct dependency at a time. Earlier blanket approval does not authorize later software. Re-prompt before any newly discovered elevation, PATH, registry, service, or execution-policy change.

On rejection, non-interactive execution, installation failure, or verification failure, stop the installation chain. Do not use unreviewed remote pipe installers such as `curl | sh`, `curl | bash`, or remote PowerShell expressions.

## Four-Layer MVP

Use this structure for a practical first implementation. It is a rollout subset, not a replacement for L0-L6.

```text
pilot-domain/
  raw/
  work/
  memory.md
  vault/
    glossary/
    policies/
    metrics/
    data-catalog/
    business-rules/
    cases/
  skills/
    task-skill/SKILL.md
  governance-lite.md
  state-lite.md
```

Minimum acceptance:

- `raw` preserves evidence with owner, source, and version or hash.
- `memory.md` routes common questions to the right files and tools.
- `vault` contains reviewed facts, rules, metrics, and key cases.
- `skills` contains at least one repeatable high-value procedure.
- `governance-lite.md` records access and expiry.
- `state-lite.md` records open tasks, project state, and risks.

## Approved Markdown Template

```markdown
---
id: legal-contract-2024-0001
title: Annual Customer Purchase Agreement
source_type: pdf_scan
source_path: raw/legal/contracts/2024/0001.pdf
domain: legal
owner: Legal Department
data_steward: Contract Operations
confidentiality: restricted
pii: true
retention: 10y
status: approved
version: 1.0
hash: sha256:example
created_at: 2024-05-12
updated_at: 2026-07-16
agent_use: conditional
allowed_agents: [legal-agent, sales-agent]
---

# Summary
# Key Facts
# Business Rules
# Risks
# Related Files
# Agent Usage Guidance
```

## Concrete memory.md Example

```markdown
# Sales Memory

## Customer Payment Risk

Keywords: payment, overdue, credit limit, accounts receivable

Applicable questions: Can the customer continue to receive goods, and what payment risk is present?

Priority sources:
- vault/finance/metric_accounts_receivable.md
- vault/sales/entity_customer_credit.md

Related cases:
- cases/sales/customer-credit-review-2026-001.md

Applicable skill:
- skills/customer-risk-analysis/SKILL.md

Callable tool:
- receivables_lookup(customer_id)

Risk controls:
- Require sales-finance permission and redact unrelated customer records.
- Require human approval before changing a credit limit or shipment status.

State entry:
- state/sales/open-credit-reviews.md

Update record:
- 2026-07-16: Added overdue-invoice routing and approval boundary.
```

## Structured Data Cards

Create Markdown cards rather than copying entire tables:

- `table_customer.md`: purpose, fields, keys, cadence, owner, sensitive fields, and examples.
- `metric_gross_margin.md`: formula, sources, grain, exclusions, caveats, and decision uses.
- `entity_customer.md`: meaning, identifiers, lifecycle, and related systems.
- `query_overdue_payment.md`: approved query, filters, permissions, and example calls.

Call live tools or APIs for changing values such as inventory, revenue, receivables, order status, attendance, or finance data.

## Risk Controls

- Classify content as public, internal, confidential, or restricted.
- Retrieve only the snippets or rows required for the task.
- Link answers to sources, tools, versions, and timestamps.
- Audit the user, Agent, query, matched files, tool calls, and output without copying secrets.
- Mark, redact, or restrict PII before vault approval.
- Preserve source hashes and approved Markdown versions.
- Record owner, reviewer, confidence, replacement source, and stale date.
- Keep previous approved versions available for rollback.
- Require human review for legal, finance, HR, safety, compliance, and high-impact operational decisions.

## Acceptance Checklist

- [ ] Pilot scope, users, data sources, interfaces, and acceptance metrics are explicit.
- [ ] L0-L6 mapping exists for the pilot domain.
- [ ] The four-layer MVP exists as `raw / memory.md / vault / skills`.
- [ ] Approved Markdown includes governance frontmatter and body sections.
- [ ] `memory.md` routes to sources and tools instead of duplicating full text.
- [ ] Facts, cases, procedures, state, and governance metadata remain distinct.
- [ ] Structured data is accessed through governed tools or APIs.
- [ ] Golden questions cover retrieval, citation, permissions, and stale knowledge.
- [ ] Restricted documents cannot be retrieved by unauthorized users or Agents.
- [ ] Agent answers include sources, versions, and data timestamps.
- [ ] Rollout, rollback, handoff, FAQ, and emergency steps exist.
- [ ] Retrospectives update templates, scripts, checks, or memory.
- [ ] The current platform and shell are identified before dependency selection.
- [ ] Existing project and operating-system capabilities are checked before installation is proposed.
- [ ] Missing dependencies produce `INSTALL_APPROVAL_REQUIRED` with complete platform-native commands.
- [ ] Only one direct dependency is approved at a time.
- [ ] WSL does not silently modify the Windows host.
- [ ] Rejection, non-interactive execution, elevation changes, installation failures, and verification failures stop the installation chain.
- [ ] Linux, Windows, and WSL are labeled as simulated-only until real-platform smoke tests run.

## Recommended Pilot

Prefer a contract and customer-risk Agent or a customer-service knowledge Agent. These pilots expose structured data, unstructured documents, historical communications, permission boundaries, and clear business value without requiring enterprise-wide migration.

## References

Read `references/enterprise-ai-data-governance-guide.zh-CN.md` for the Chinese implementation manual, cross-platform software selection, installation examples, and rollout guidance.
