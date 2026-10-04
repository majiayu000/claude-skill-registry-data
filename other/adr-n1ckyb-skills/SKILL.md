---
name: adr
description: Write or update an Architecture Decision Record in docs/adr/ for OpenDataSuite. Use when an issue's acceptance criteria require an ADR, or when adding a crate, plugin contract, persisted format, CLI presentation boundary, or a dependency with licensing implications.
---

# Write an ADR

1. List `docs/adr/` and pick the next number `NNNN` (4 digits, zero-padded). ADR-0000 is the template.
2. Copy `docs/adr/0000-template.md` to `docs/adr/NNNN-<kebab-title>.md`.
3. Fill every section. Requirements:
   - **Context** cites the driving issue(s) (`#N`) and relevant AGENTS.md rules.
   - **Options considered**: at least two real alternatives, each with pros/cons.
   - **Decision** is one clear statement; **Consequences** lists what becomes easier,
     harder, and what follow-up issues are needed.
   - For module/crate decisions include a dependency diagram (Mermaid `graph LR`).
   - For dependency decisions include licence, maintenance status, and an exit strategy.
4. Status starts as `Proposed`; it becomes `Accepted` when merged. Never edit the decision of
   an accepted ADR — supersede it with a new one and set the old one's status to
   `Superseded by ADR-NNNN`.
5. Add the ADR to the index table in `docs/adr/README.md`.
6. If the decision changes the roadmap or crate layout, update `docs/ROADMAP.md` and AGENTS.md in the same PR.
