---
name: adr
description: Draft a new Architecture Decision Record for Pieceful and walk the owner through the decision. Use for /adr or whenever a significant design decision comes up.
argument-hint: "<decision topic>"
---

# /adr: record a decision

1. Read `docs/decisions/README.md` (index, when to write one, review checklist) and any ADRs or docs related to the topic.
2. Research the options (facts, constraints, verified API behavior). Mark anything unverified as **To verify**.
3. **Ask the owner** (AskUserQuestion): 2–4 options with trade-offs and a recommendation. The owner decides.
4. Write `docs/decisions/NNNN-<slug>.md` from `0000-template.md` (next free number). Consequences must cover third-party load and privacy.
5. Mark it `Proposed`, or `Accepted` if the owner already decided. Update the index. If accepted, update the docs it affects.
6. Summarize and stop. Don't commit.
