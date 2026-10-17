---
name: mimir-research-convention
description: Standing convention for conducting research — source-tier defaults, proof requirements, and self-validation of every finding against verifiable sources.
---

# Research Convention

## Purpose

Define the standing operating standard for conducting research: which sources count as ground truth, how every finding must be proven, and how proofs are self-validated before reporting. This convention is cross-cutting — it applies to any research task regardless of subject or method.

## Source Tiers

Research sources fall into two tiers by authority:

**Authoritative sources** — where ground truth lives:
- The project's source tree and configuration (code, build artifacts, tests, dependencies)
- The system-of-record documentation for the project (architecture decisions, API specifications, operational procedures, team conventions)

**Contextual sources** — where intent and history live:
- Work-tracking systems (issue trackers, tickets, roadmaps)
- Decision logs, communication archives, and meeting notes

Findings from authoritative sources are definitive. Findings from contextual sources provide context and rationale but do not override authoritative sources.

### Parameterization

Each project or deployment maps its concrete systems onto these two tiers. The research brief may name specific systems (e.g., "consult the internal wiki and the issue tracker"). If no systems are named, the standing default applies: start with authoritative sources, then consult contextual sources for history and intent.

### Example Instantiation

For reference, a typical instantiation in an organization using Codebase, Confluence, and Jira:

| System | Tier | Role |
|---|---|---|
| Codebase (source tree rooted at session working directory) | Authoritative | Source code structure, implementation details, patterns, configuration, tests, dependencies |
| Confluence (internal wiki/docs) | Authoritative | Architecture decisions, API specifications, deployment procedures, team conventions |
| Jira (issue tracker) | Contextual | Work history, current progress, roadmap, acceptance criteria, strategic direction |

This example is illustrative, not normative. Your project may use different systems or map them differently.

## Proof Requirements

Every research finding must be accompanied by verifiable proof. This section defines valid proof formats and validation rules. Reviewers validate research Workfiles against these same standards — completeness, specificity, spot-checks, and the unverified-claim ratio — so a finding that fails them here will be blocked downstream.

### Proof Principles

1. **Every claim requires proof** — No finding can be reported without a corresponding proof reference.
2. **Proofs must be specific** — Vague citations (e.g., "the codebase", "the docs") are not acceptable.
3. **Unverifiable claims must be marked** — If a claim cannot be verified against a source, mark it as `[UNVERIFIED]` with a brief explanation of why verification was not possible. Keep unverified claims rare: reviewers flag Workfiles where more than 25% of claims are unverified.

### Counts and Enumerations

A finding that counts things — matches, lines, files, references, entries — is arithmetic over an enumeration, and the enumeration is its proof. Four rules apply to every such finding, in any Workfile or report:

1. **Enumerate first, total last.** List the counted items, or the per-file / per-category subtotals each with its own proof, before the total; compute the total from that list and state it after it. A total stated before or without its list is an unproven claim.
2. **Label the unit and the method.** Every count names what one unit is and the command or method that produced it — `104 occurrences (rg -o --count-matches '<pattern>')`, `57 lines containing …`, `15 files`. "Matches", "references", and "hits" are ambiguous between occurrences, lines, and files until the unit says which; a line count and an occurrence count of the same pattern are two findings, not one.
3. **Partition, or reconcile.** Categories that break a count down are mutually exclusive and jointly exhaustive over the counted set, and their subtotals sum to the total. Where an item legitimately belongs to two categories, or two categories were counted by different methods, add one explicit reconciliation line — `Reconciliation: <a> + <b> − <overlap> = <total>` or `<n> lines carry <m> occurrences` — instead of a total that does not add up.
4. **Say what the count is a count of.** A count of a literal pattern is not a count of the concept it stands for: state which was taken (`104 occurrences of the literal path form; prose mentions of the folder were not counted`), so a reader sizing an edit knows what remains uncounted.

### Valid Proof Formats by Source Kind

| Source Kind | Valid Proof Format | Example Shape |
|---|---|---|
| File-based (code, config, local docs) | Path + line numbers | `src/foo.ts:42-58` |
| Web/document system | Full, resolvable URL or stable page identifier | `https://docs.example.com/page-id` |
| Tracker/registry (issues, tickets, packages) | Unique key or full URL | `PROJ-1234` or `https://tracker.example.com/browse/PROJ-1234` |
| Data/API (databases, telemetry, endpoints) | Query/request + retrieval timestamp | `SELECT … @ 2026-07-28` |
| Ephemeral/human (meetings, chat) | Dated, attributed reference — or mark `[UNVERIFIED]` | `standup 2026-07-21, per <role>` |

### Proof Examples

**File-based Proof (Good):**
```
The Button component accepts a `disabled` prop (src/components/Button.tsx:15-20).
```

**File-based Proof (Bad):**
```
The Button component has a disabled prop (see Button.tsx).
```
*Missing line numbers; not specific enough.*

**URL-based Proof (Good):**
```
According to the API Design Guide (https://docs.example.com/api-design),
all endpoints must return a 200 status on success.
```

**URL-based Proof (Bad):**
```
The documentation says endpoints should return 200 (see the docs).
```
*Missing full URL; not resolvable.*

**Unverifiable Claim (Good):**
```
The team prefers TypeScript over JavaScript [UNVERIFIED — no explicit documentation found;
based on codebase observation that all new files are .ts/.tsx].
```

## When to Use

- On every research task, unless the brief explicitly overrides the scope (e.g., "research external libraries", "research only the issue tracker, ignore code").
- When the brief names specific systems, treat those as the tier instantiation for the task.

## Workflow

1. **Receive the research brief** from the requesting agent.
2. **Apply the stated scope** — if the brief names systems or overrides the default, follow it exactly.
3. **If no scope is stated, apply the standing convention:**
   - Start with authoritative sources (project source tree and system-of-record documentation)
   - Consult contextual sources (work-tracking systems, decision logs) for history and intent
   - Authoritative findings override contextual ones
4. **Attach proof per Proof Requirements** — Include specific file paths with line numbers, full URLs, or unique keys. Mark any unverifiable claims with `[UNVERIFIED]` and explain why verification was not possible.
5. **Self-validate proofs before reporting** — Verify that file paths exist and line numbers are accurate, URLs resolve to valid pages, keys are valid and accessible. Re-add every total from its enumerated list and confirm each count carries its unit and method. Flag any broken or stale proofs; a total that does not reproduce is a defect to fix, never to footnote.

## Quality Criteria

- Research is scoped to the brief, or to the standing definition when the brief states no scope.
- Every finding has verifiable proof per Proof Requirements — no finding without proof or an `[UNVERIFIED]` marker.
- Proofs are specific, not vague — file paths include line numbers, URLs are complete and resolvable, keys are exact and identifiable.
- Every count is unit-labeled with its method, computed last from an enumeration that appears in the Workfile, and — when broken into categories — either partitions the counted set or carries a reconciliation line.
- Authoritative sources are consulted before or alongside contextual sources.
- Ambiguous briefs are clarified with the requesting agent before proceeding.

## Anti-Patterns

- **Ignoring the convention** — Researching external sources when internal sources are the standing default.
- **Context-first research** — Using contextual sources as authoritative when authoritative sources are available.
- **Unproven findings** — Reporting a claim with no proof reference at all.
- **Vague citations** — Citing "the codebase" or "the documentation" without specific file paths, line numbers, or URLs.
- **Arithmetic by assertion** — a total whose subtotals do not sum to it, mix units (lines, occurrences, files) without saying so, or overlap without a reconciliation line; a concept counted by a literal pattern and reported as if it were the concept.
- **Stale proofs** — Citing files or pages that no longer exist without flagging them as broken or marking the claim as `[UNVERIFIED]`.
- **Scope creep** — Expanding research beyond the stated or standing scope without explicit approval.
