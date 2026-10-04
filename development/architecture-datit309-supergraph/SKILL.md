---
name: architecture
description: Proactive architecture review — explore codebase structure, generate a self-contained HTML report with Mermaid diagrams and candidate improvements, then grill the findings. Use when planning a large refactor, onboarding to an unfamiliar codebase, or before a major architectural change.
---

# /supergraph:architecture

Three phases: explore → HTML report → grilling loop.

Announce: "🏛️ /supergraph:architecture — mapping codebase structure..."

## Phase 1 — Explore

**1a. Read CONTEXT.md:**
```bash
cat CONTEXT.md 2>/dev/null || echo "No CONTEXT.md"
```

**1b. Codebase Memory overview (optional):**
Use `CBM_PROJECT` with `get_architecture` aspects `overview`, `layers`,
`boundaries`, `clusters`, and `hotspots`. After `get_graph_schema`, run shared
contract recipes `hubs`, `bridges`, `cross-boundary`, and `test-gaps`.
If codebase-memory-mcp is unavailable, label graph evidence `unavailable`, use
Serena/filesystem evidence, and generate Mermaid diagrams from imports.

**1c. Serena structure (optional):**
```
mcp__serena__get_symbols_overview()
```

**1d. Read 3-5 hub node files** — understand actual structure, naming, patterns.

## Phase 2 — Generate HTML Report
Write self-contained `docs/supergraph/architecture-review-<YYYY-MM-DD>.html` with Tailwind+Mermaid header, architecture `graph TD`, per-candidate card (Problem/Proposal/Before/After Mermaid/Impact/Trade-offs with badge Strong/Worth exploring/Speculative), plus tables for Test Gaps and Unexpected Coupling.

Open: `open docs/supergraph/architecture-review-<date>.html || xdg-open ... || echo "Report saved: ..."`

## Phase 3 — Grilling Loop

For each Strong candidate, ask one focused question:

> "Candidate N proposes [X]. Is this consistent with [constraint from CONTEXT.md / known business rule]?"

Incorporate answers to refine the candidate cards. Mark dismissed candidates as `Rejected — [reason]`.

After grilling, present final prioritized list:
```
Strong candidates (ready for /supergraph:plan):
  1. [Name] — [one-line rationale]

Worth exploring (needs spike first):
  2. [Name] — [open question to resolve]

Speculative (park for later):
  3. [Name] — [what would need to be true]
```

## Report

```
✅ /supergraph:architecture complete
- Report: docs/supergraph/architecture-review-<date>.html
- Communities: N | Hub nodes: N | Bridge nodes: N
- Candidates: N Strong, N Worth exploring, N Speculative
- Next: /supergraph:plan (for Strong candidates) or /supergraph:prototype (for uncertain ones)
```

## Rules

- Always open the HTML file automatically
- Mermaid diagrams must reflect actual graph data, not invented structure
- Speculative candidates must be labeled — never present guesses as strong recommendations
- Update CONTEXT.md if review revealed undocumented architectural invariants:
  ```bash
  printf '\n## <invariant>\n[description]\n' >> CONTEXT.md
  ```
- If graph was empty or unavailable, note "Diagram generated from filesystem structure" in the HTML report header
