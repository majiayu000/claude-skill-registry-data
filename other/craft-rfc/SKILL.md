---
name: craft-rfc
description: Proposing technical designs. How we should build X.
---

# Skill: Craft RFC

> "Design before you build. Write before you code."

## RFC vs ADR

| Artifact | Purpose | When |
|----------|---------|------|
| **RFC** | Propose a *design* | Before implementation |
| **ADR** | Record a *decision* | After choice is made |

RFC answers: "How should we build X?"
ADR answers: "Why did we choose X?"

## The Standard

1. **Location**: `.claude/memory/{branch}/rfc/RFC-{Title}.md`
2. **Status**: Draft → Accepted → Implemented → Superseded
3. **Structure**: Abstract → Problem → Solution → Open Questions
4. **Scope**: One RFC per feature/system

## The Protocol

1. **Interview** — Extract requirements via `AskUserQuestion`
2. **Visualize** — Use `/map` for structure, `/flow` for processes
3. **Draft** — Write RFC with diagrams and open questions
4. **Review** — User approves or requests changes
5. **Accept** — Status → Accepted, implementation begins
6. **Implement** — Status → Implemented when complete

## Visualization

Complex systems deserve diagrams. Use liberally:

- **`/map`** — Directory trees, data structures, component hierarchies
- **`/flow`** — Process flows, state machines, request lifecycles

## When to Write

| Write RFC | Don't Write RFC |
|-----------|-----------------|
| New package/library | Bug fixes |
| System redesign | Config changes |
| Complex feature | Simple CRUD |
| Cross-domain work | Single-file changes |

## Template

See `examples.md` for template and real-world examples.
